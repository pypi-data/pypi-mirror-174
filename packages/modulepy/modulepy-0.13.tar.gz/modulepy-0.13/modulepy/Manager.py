from pathlib import Path

from modulepy import log
from modulepy.Loader import Loader
from modulepy.Version import Version
from modulepy.Information import Information
from modulepy.Base import Base


class Manager(Base):
    information = Information("Manager", Version(1, 0, 0))

    modules: dict[str, Base] = {}
    errors: dict[str, Exception] = {}

    def __init__(self, module_directory: Path):
        Base.__init__(self)
        log.debug("Initializing")
        self.data.set("module_directory", module_directory)

    def on_start(self):
        self.load_modules()
        self.start_modules()

    def on_stop(self):
        self.unload_modules()

    def load_modules(self):
        directory = self.data.get("module_directory")
        log.debug(f"Loading modules from {directory}")
        for module in Loader.load_modules_in_directory(directory):
            if not module.information.is_available(list(self.modules.keys())):
                self.modules[module.information.name] = module()
                log.debug(f"Loaded {module.information}")
            else:
                log.warning(f"Module {module.information} already loaded.")

    def start_modules(self):
        """
        Starts all modules and creates a client for each one
        :return:
        """

        # first sort by dependencies
        deps = {}
        for module in self.modules.keys():
            deps[module] = 0

        for module in self.modules.values():
            for dependency in module.dependencies:
                if dependency.name == self.information.name:
                    continue
                deps[dependency.name] += 1

        # then start by most to the least count
        for module in sorted(deps, key=lambda x: x[1]):
            log.debug(f"Starting module {module}")
            self.modules[module].start()

    def unload_modules(self):
        log.info("Unloading modules")
        for module in self.modules.values():
            if module.is_alive():
                log.debug(f"Stopping {module.information}")
                module.stop()
                module.join()
            else:
                log.debug(f"{module.information} is already stopped")
