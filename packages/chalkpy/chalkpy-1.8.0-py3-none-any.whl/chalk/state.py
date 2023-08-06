from typing import Generic, Type, TypeVar

T = TypeVar("T", bound=Type)


class StateWrapper(Generic[T]):
    typ: T

    def __init__(self, typ: T):
        self.typ = typ


class StateMeta:
    def __getitem__(self, item: T) -> T:
        return StateWrapper(item)  # noqa


# We're using this mechanism very intentionally
# instead of using __getitem__ on a metaclass
# to allow the editor to auto-complete the
# members of T. IntelliJ doesn't auto-complete
# on the return types of metaclass methods.
# Please check that editors are happy before
# changing this pattern.
State = StateMeta()
