

import attr
from typing import TypeVar, Generic, cast, Union, Callable

LeftT = TypeVar('LeftT')
RightT = TypeVar('RightT')


class Either(Generic[LeftT, RightT], object):
    def map_left(self, callable_):
        # type: (Callable) -> Union[Left, Right]
        if isinstance(self, Left):
            return Left(callable_(self.val))
        else:
            return cast(Right, self)

    def into_inner(self):
        # type: () -> Union[LeftT, RightT]
        if isinstance(self, Left):
            return self.val
        else:
            return cast(Right, self).val


@attr.s
class Left(Either):
    val = attr.ib()


@attr.s
class Right(Either):
    val = attr.ib()


EitherT = TypeVar('EitherT', bound=Either)
