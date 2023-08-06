from multiprocessing import Process
from time import sleep

from modulepy.Version import Version
from modulepy.Information import Information
from modulepy.SharedDict import LocalSharedDict, RemoteSharedDict


class Base(Process):
    information: Information = Information("Base", Version(0, 1, 0))
    dependencies: list[Information] = []
    clients: dict[str, RemoteSharedDict] = {}
    error: Exception = None
    interval: int = 0.2

    data: LocalSharedDict = None

    def __init__(self):
        Process.__init__(self, name=self.information.__str__())

        if not self.information.get_directory().is_dir():
            self.information.get_directory().mkdir(exist_ok=True)
        self.information.get_address().unlink(True)

        self.data = LocalSharedDict(self.information.name)
        self.data.set("do_run", True)

    def init(self):
        for dependency in self.dependencies:
            self.clients[dependency.name] = RemoteSharedDict(dependency.name)

    def update_clients(self):
        for client in self.clients.values():
            client.update()

    def on_start(self):
        pass

    def on_stop(self):
        pass

    def loop(self):
        sleep(0.2)

    def run(self) -> None:
        """
        1. initialize
        2. call on_start function (user's pre-run callback)
        3. loop
          3.1 update own data
          3.2 if own do_run is False then break
          3.3 update all client data
          3.4 call loop function (user's loop callback)
        4. call on_stop function (user's post-run callback)
        """
        self.init()
        self.on_start()

        try:
            while True:
                self.data.update()
                if not self.data.get("do_run"):
                    break

                self.update_clients()
                self.loop()
        except KeyboardInterrupt:
            pass

        self.on_stop()

    def stop(self):
        self.data.set("do_run", False)
