from multiprocessing.shared_memory import SharedMemory
from pickle import loads, dumps

from modulepy import log


class SharedDict(object):
    _data: dict = {}

    def set(self, key: str, value):
        self._data[key] = value

    def get(self, key: str, default=None):
        if key in self._data.keys():
            return self._data[key]
        return default


class SharedMemoryDict(SharedMemory, SharedDict):
    host: bool = False

    def __init__(self, name: str, size: int = 4096, create: bool = False):
        self.host = create
        SharedMemory.__init__(self, name=name, size=size, create=create)

        if create:
            log.debug(f"Created shared memory {self.name}")
        else:
            log.debug(f"Attached to shared memory {self.name}")

    def __del__(self):
        self.close()
        if self.host:
            self.unlink()

    def update(self):
        prv = self._data
        self._data = loads(self.buf[0:self.size].tobytes())
        if prv != self._data:
            log.debug(f"Data for {self.name} changed:")
            log.debug(f"\t{prv}")
            log.debug(f"\t{self._data}")


class LocalSharedDict(SharedMemoryDict):
    def __init__(self, name: str, size: int = 4096):
        SharedMemoryDict.__init__(self, name, size, True)

    def set(self, key: str, value):
        SharedMemoryDict.set(self, key, value)
        data = dumps(self._data)
        self.buf[0:len(data)] = data


class RemoteSharedDict(SharedMemoryDict):
    def __init__(self, name: str):
        SharedMemoryDict.__init__(self, name)
