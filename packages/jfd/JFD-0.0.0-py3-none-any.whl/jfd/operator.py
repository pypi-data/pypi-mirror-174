class Operator:
    def __add__(self, other):
        return Sum([self, other])

    def __sub__(self, other):
        pass

    def __mul__(self, other):
        return Product([self, other])

    def __matmul__(self, other):
        return Composition([self, other])

    def __getitem__(self, slc):
        return Composition([SliceOperator(slc), self])

    def apply(self, f):
        raise NotImplementedError

    def __call__(self, f):
        if isinstance(f, list):
            return [self.__call__(item) for item in f]
        return self.apply(f)


class Sum(Operator):
    def __init__(self, operators):
        self._operators = operators

    def apply(self, f):
        return sum(op(f) for op in self._operators)


class Composition(Operator):
    def __init__(self, operators):
        self.operators = operators

    def apply(self, f):
        for op in self.operators[::-1]:
            f = op(f)
        return f


class SliceOperator(Operator):
    def __init__(self, slc):
        self._slc = slc

    def apply(self, f):
        return f[self._slc]


class Id(Operator):
    def apply(self, f):
        return f


class Coef(Operator):
    def __init__(self, value):
        self._value = value

    def apply(self, f, **kwargs):
        if isinstance(self._value, str):
            return kwargs[self._value]
        else:
            return self._value


class Product(Operator):
    def __init__(self, operators):
        self._operators = operators

    def apply(self, f):
        result = self._operators[0](f)
        for op in self._operators[1:]:
            result = op(f)
        return result
