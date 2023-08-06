from __future__ import annotations

import dataclasses
import functools as ft

import jax
import jax.numpy as jnp

# import kernex as kex
import pytreeclass as pytc

from serket.nn.convolution import DepthwiseConv2D
from serket.nn.utils import (
    _check_and_return_positive_int,
    _check_in_features,
    _check_spatial_in_shape,
    _lazy_blur,
)


@pytc.treeclass
class AvgBlur2D:
    in_features: int = pytc.nondiff_field()
    kernel_size: int | tuple[int, int] = pytc.nondiff_field()

    conv1: DepthwiseConv2D = pytc.nondiff_field(repr=False)
    conv2: DepthwiseConv2D = pytc.nondiff_field(repr=False)

    def __init__(self, in_features: int, kernel_size: int | tuple[int, int]):
        """Average blur 2D layer
        Args:
            in_features: number of input channels
            kernel_size: size of the convolving kernel
        """
        if in_features is None:
            for field_item in dataclasses.fields(self):
                setattr(self, field_item.name, None)

            self._partial_init = ft.partial(
                AvgBlur2D.__init__,
                self,
                kernel_size=kernel_size,
            )
            return

        if hasattr(self, "_partial_init"):
            delattr(self, "_partial_init")

        self.in_features = _check_and_return_positive_int(in_features, "in_features")
        self.kernel_size = _check_and_return_positive_int(kernel_size, "kernel_size")

        w = jnp.ones(kernel_size)
        w = w / jnp.sum(w)
        w = w[:, None]
        w = jnp.repeat(w[None, None], in_features, axis=0)

        self.ndim = 2
        self.in_features = in_features
        self.conv1 = DepthwiseConv2D(
            in_features=in_features,
            kernel_size=(kernel_size, 1),
            padding="same",
            bias_init_func=None,
        )

        self.conv2 = DepthwiseConv2D(
            in_features=in_features,
            kernel_size=(1, kernel_size),
            padding="same",
            bias_init_func=None,
        )

        self.conv1 = self.conv1.at["weight"].set(w)
        self.conv2 = self.conv2.at["weight"].set(jnp.moveaxis(w, 2, 3))  # transpose

    @_lazy_blur
    @_check_spatial_in_shape
    @_check_in_features
    def __call__(self, x, **kwargs) -> jnp.ndarray:
        return self.conv2(self.conv1(x))


@pytc.treeclass
class GaussianBlur2D:
    in_features: int = pytc.nondiff_field()
    kernel_size: int = pytc.nondiff_field()
    sigma: float = pytc.nondiff_field()

    conv1: DepthwiseConv2D = pytc.nondiff_field(repr=False)
    conv2: DepthwiseConv2D = pytc.nondiff_field(repr=False)

    def __init__(
        self,
        in_features,
        kernel_size,
        *,
        sigma=1.0,
        # implementation="jax",
    ):
        """Apply Gaussian blur to a channel-first image.

        Args:
            in_features: number of input features
            kernel_size: kernel size
            sigma: sigma. Defaults to 1.
        """
        if in_features is None:
            for field_item in dataclasses.fields(self):
                setattr(self, field_item.name, None)

            self._partial_init = ft.partial(
                GaussianBlur2D.__init__,
                self=self,
                kernel_size=kernel_size,
                sigma=sigma,
            )
            return

        if hasattr(self, "_partial_init"):
            delattr(self, "_partial_init")

        self.in_features = _check_and_return_positive_int(in_features, "in_features")
        self.kernel_size = _check_and_return_positive_int(kernel_size, "kernel_size")

        self.in_features = in_features
        self.kernel_size = kernel_size
        self.sigma = sigma

        x = jnp.linspace(-(kernel_size - 1) / 2.0, (kernel_size - 1) / 2.0, kernel_size)
        w = jnp.exp(-0.5 * jnp.square(x) * jax.lax.rsqrt(self.sigma))

        w = w / jnp.sum(w)
        w = w[:, None]

        # if implementation == "jax":
        w = jnp.repeat(w[None, None], in_features, axis=0)
        self.conv1 = DepthwiseConv2D(
            in_features=in_features,
            kernel_size=(kernel_size, 1),
            padding="same",
            bias_init_func=None,
        )

        self.conv2 = DepthwiseConv2D(
            in_features=in_features,
            kernel_size=(1, kernel_size),
            padding="same",
            bias_init_func=None,
        )

        self.in_features = in_features
        self.ndim = 2

        self.conv1 = self.conv1.at["weight"].set(w)
        self.conv2 = self.conv2.at["weight"].set(jnp.moveaxis(w, 2, 3))

        # elif implementation == "kernex":
        #     # usually faster than jax for small kernel sizes
        #     # but slower for large kernel sizes

        #     @jax.vmap  # channel
        #     @kex.kmap(kernel_size=(kernel_size, 1), padding="same")
        #     def conv1(x):
        #         return jnp.sum(x * w)

        #     @jax.vmap
        #     @kex.kmap(kernel_size=(1, kernel_size), padding="same")
        #     def conv2(x):
        #         return jnp.sum(x * w.T)

        #     self._func = lambda x: conv2(conv1(x))

        # else:
        #     raise ValueError(f"Unknown implementation {implementation}")

    @_lazy_blur
    @_check_spatial_in_shape
    @_check_in_features
    def __call__(self, x, **kwargs) -> jnp.ndarray:
        return self.conv1(self.conv2(x))


@pytc.treeclass
class Filter2D:
    in_features: int = pytc.nondiff_field()
    conv: DepthwiseConv2D = pytc.nondiff_field(repr=False)
    kernel: jnp.ndarray = pytc.nondiff_field()

    def __init__(self, in_features: int, kernel: jnp.ndarray):
        """Apply 2D filter for each channel
        Args:
            in_features: number of input channels
            kernel: kernel array
        """
        if in_features is None:
            for field_item in dataclasses.fields(self):
                setattr(self, field_item.name, None)

            self._partial_init = ft.partial(Filter2D.__init__, self=self, kernel=kernel)
            return

        if hasattr(self, "_partial_init"):
            delattr(self, "_partial_init")

        if not isinstance(kernel, jnp.ndarray) or kernel.ndim != 2:
            raise ValueError("Expected `kernel` to be a 2D `ndarray` with shape (H, W)")

        self.in_features = _check_and_return_positive_int(in_features, "in_features")
        self.ndim = 2
        self.kernel = jnp.stack([kernel] * in_features, axis=0)
        self.kernel = self.kernel[:, None]

        self.conv = DepthwiseConv2D(
            in_features=in_features,
            kernel_size=kernel.shape,
            padding="same",
            bias_init_func=None,
        )
        self.conv = self.conv.at["weight"].set(self.kernel)

    @_lazy_blur
    @_check_spatial_in_shape
    @_check_in_features
    def __call__(self, x, **kwargs) -> jnp.ndarray:
        return self.conv(x)
