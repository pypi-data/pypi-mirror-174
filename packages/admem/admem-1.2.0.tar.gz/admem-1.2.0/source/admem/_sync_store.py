# Copyright (c) 2022 Mario S. Könz; License: MIT
import contextlib
import typing as tp

from ._protocols import BackendStoreProtocol
from ._protocols import T
from ._store_setup import ACTIVE_STORES

__all__ = ["store", "switch_store", "switched_store"]


class SyncStore:
    @classmethod
    def get_last_active(cls) -> BackendStoreProtocol:
        return next(reversed(ACTIVE_STORES.values()))

    @classmethod
    def get_last_active_key(cls) -> str:
        return next(reversed(ACTIVE_STORES))

    @property
    def impl(self) -> BackendStoreProtocol:
        return self.get_last_active()

    def dump(self, obj: tp.Any) -> bool:
        _, created = self.impl.dump(obj)
        return created  # type: ignore

    def load(self, dataclass: type[T], **filter_kwgs: tp.Any) -> T:
        return self.impl.load(dataclass, **filter_kwgs)


store = SyncStore()


def switch_store(identifier: str) -> None:
    ACTIVE_STORES.move_to_end(identifier)


@contextlib.contextmanager
def switched_store(identifier: str) -> tp.Iterator[None]:
    last_key = store.get_last_active_key()
    switch_store(identifier)
    yield
    ACTIVE_STORES.move_to_end(last_key)
    switch_store(last_key)
