from typing import List

from pydantic.main import BaseModel

from gorgon.utils.typing import Integer


class Block(BaseModel):
    index: Integer
    timestamp: Integer
    logical_time: Integer
    transactions: List
