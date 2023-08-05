import jax
import jax.numpy as jnp
from findiff.coefs import coefficients

from jfd.operator import Composition, Operator


def _general_1d_conv(f, ax, coefs, offsets):
    result = None
    size = f.shape[ax]
    padding_left = -offsets[0]
    padding_right = offsets[-1]
    assert padding_left >= 0 and padding_right >= 0
    for coef, offset in zip(coefs, offsets):
        slc = [
            slice(None, None),
        ] * (ax + 1)
        slc[ax] = slice(offset + padding_left, size + offset - padding_right)
        if result is None:
            result = coef * f[tuple(slc)]
        else:
            result = result + coef * f[tuple(slc)]
    return result


class Diff1D(Operator):
    def __init__(self, ax, h, order=1, accuracy=2):
        self.ax = ax
        self.coefficients = coefficients(order, accuracy)
        self.h = h
        self.order = order
        assert (
            self.coefficients["center"]["offsets"][-1]
            == -self.coefficients["center"]["offsets"][0]
        )
        self.left_padding = -self.coefficients["center"]["offsets"][0]
        self.right_padding = self.coefficients["center"]["offsets"][-1]

    def apply(self, f):
        central_result = _general_1d_conv(
            f,
            self.ax,
            self.coefficients["center"]["coefficients"],
            self.coefficients["center"]["offsets"],
        ) / (self.h**self.order)

        forward_result = _general_1d_conv(
            f,
            self.ax,
            self.coefficients["forward"]["coefficients"],
            self.coefficients["forward"]["offsets"],
        ) / (self.h**self.order)
        slc = [
            slice(None, None),
        ] * (self.ax + 1)
        slc[self.ax] = slice(0, self.left_padding)
        forward_result = forward_result[tuple(slc)]

        backward_result = _general_1d_conv(
            f,
            self.ax,
            self.coefficients["backward"]["coefficients"],
            self.coefficients["backward"]["offsets"],
        ) / (self.h**self.order)
        slc = [
            slice(None, None),
        ] * (self.ax + 1)
        slc[self.ax] = slice(
            backward_result.shape[self.ax] - self.right_padding,
            backward_result.shape[self.ax],
        )
        backward_result = backward_result[tuple(slc)]
        return jnp.concatenate(
            [forward_result, central_result, backward_result], axis=self.ax
        )


class FinDiff(Operator):
    def __init__(self, multiindex, h, accuracy=2):
        self.operator = Composition(self._parse_multiindex(multiindex, h, accuracy))

    def apply(self, f):
        return self.operator(f)

    @classmethod
    def _parse_multiindex(cls, multiindex, h, accuracy=2):
        operators = []
        for deriv in multiindex:
            ax, order = deriv[0], deriv[1]
            if order == 0:
                continue
            if isinstance(h, tuple):
                ax_h = h[ax]
            else:
                ax_h = h

            if len(deriv) == 3:
                ax_accuracy = deriv[2]
            else:
                ax_accuracy = accuracy
            operators.append(Diff1D(ax=ax, order=order, h=ax_h, accuracy=ax_accuracy))
        return operators


class Grad(Operator):
    def __init__(self, dims, h, accuracy=2):
        self._dims = dims
        if not isinstance(h, tuple):
            self._hs = (h,) * len(dims)
        else:
            self._hs = h
        self._operators = [
            Diff1D(ax, h=ax_h, order=1, accuracy=accuracy)
            for (ax, ax_h) in zip(dims, self._hs)
        ]

    def apply(self, f):
        return jnp.stack([op(f) for op in self._operators], axis=0)


class Laplace(Operator):
    def __init__(self, dims, h, accuracy=2):
        self._dims = dims
        if not isinstance(h, tuple):
            self._hs = (h,) * len(dims)
        else:
            self._hs = h
        self._operators = [
            Diff1D(ax, h=ax_h, order=2, accuracy=accuracy)
            for (ax, ax_h) in zip(dims, self._hs)
        ]

    def apply(self, f):
        return sum(op(f) for op in self._operators)


class Div(Operator):
    def __init__(self, dims, h, accuracy=2):
        self._dims = dims
        if not isinstance(h, tuple):
            self._hs = (h,) * len(dims)
        else:
            self._hs = h
        self._operators = [
            Diff1D(ax, ax_h, order=1, accuracy=accuracy)
            for (ax, ax_h) in zip(dims, self._hs)
        ]

    def apply(self, f):
        assert f.shape[0] == len(self._dims)
        return sum(
            op(f[i]) for i, (ax, op) in enumerate(zip(self._dims, self._operators))
        )


if __name__ == "__main__":
    import matplotlib.pyplot as plt

    def _solve(op, x):
        return op(x)

    N = 100
    x, h = jnp.linspace(0, 2 * jnp.pi, N, retstep=True)
    A = Diff1D(0, h, order=1)
    # print(A.coefficients, A.left_padding, A.right_padding)
    # f = jnp.sin(x)
    f = x**3
    plt.plot(x, f)
    solve = jax.jit(_solve, static_argnums=(0,))
    plt.plot(x, solve(A, f))
    plt.show()
