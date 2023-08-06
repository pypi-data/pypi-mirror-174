from typing import TypeVar, Type, Generic


SelectorInstance = TypeVar("SelectorInstance")


class Selector(Generic[SelectorInstance]):
    model: Type[SelectorInstance]
