import typing as t

from typing import Any, Protocol


from gorgon.crypto.block import Block


class RepositoryProtocol(Protocol):
    source: Any

    def new_block(self) -> Block:
        return t.cast(Block, self.source.create())

    def get_block(self) -> Block:
        return t.cast(Block, self.source.get())
