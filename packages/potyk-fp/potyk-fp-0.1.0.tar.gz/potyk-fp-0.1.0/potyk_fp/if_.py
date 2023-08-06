class _IfPart:
    def __init__(self, val):
        self.val = val() if callable(val) else val

    def then(self, other): ...

    def el(self, other): ...

    def get(self): ...

    @classmethod
    def wrap(cls, other):
        other = other() if callable(other) else other
        return other if isinstance(other, _IfPart) else cls(other)


class If(_IfPart):
    """
    >>> If(True).then('then').el('else').get()
    'then'
    >>> If(False).then('then').el('else').get()
    'else'
    """

    def then(self, other): return Then.wrap(other) if self.val else self

    def el(self, other): return Then.wrap(other)


class Then(_IfPart):
    def get(self): return self.val

    def then(self, other): return self

    def el(self, other): return self
