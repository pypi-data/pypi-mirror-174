from __future__ import annotations

import dataclasses
import functools as ft
from typing import Callable

import jax
import jax.numpy as jnp
import jax.random as jr
import pytreeclass as pytc

from serket.nn import Linear
from serket.nn.convolution import ConvND, SeparableConvND
from serket.nn.fft_convolution import FFTConvND, SeparableFFTConvND
from serket.nn.utils import (
    _act_func_map,
    _check_and_return_positive_int,
    _lazy_bwd_rnn,
    _lazy_fwd_rnn,
    _lazy_rnn_cell,
)

# --------------------------------------------------- RNN ------------------------------------------------------------ #


@pytc.treeclass
class RNNState:
    hidden_state: jnp.ndarray


@pytc.treeclass
class RNNCell:
    pass


@pytc.treeclass
class SpatialRNNCell:
    pass


@pytc.treeclass
class SimpleRNNState(RNNState):
    pass


@pytc.treeclass
class SimpleRNNCell(RNNCell):
    in_to_hidden: Linear
    hidden_to_hidden: Linear

    def __init__(
        self,
        in_features: int,
        hidden_features: int,
        *,
        weight_init_func: str | Callable = "glorot_uniform",
        bias_init_func: str | Callable | None = "zeros",
        recurrent_weight_init_func: str | Callable = "orthogonal",
        act_func: str | None = "tanh",
        key: jr.PRNGKey = jr.PRNGKey(0),
    ):
        """Vanilla RNN cell that defines the update rule for the hidden state
        See:
            https://www.tensorflow.org/api_docs/python/tf/keras/layers/SimpleRNNCell

        Args:
            in_features: the number of input features
            hidden_features: the number of hidden features
            weight_init_func: the function to use to initialize the weights
            bias_init_func: the function to use to initialize the bias
            recurrent_weight_init_func: the function to use to initialize the recurrent weights
            act_func: the activation function to use for the hidden state update
            key: the key to use to initialize the weights
        """
        if in_features is None:
            for field_item in dataclasses.fields(self):
                # set all fields to None to mark the class as uninitialized
                # to the user and to avoid errors
                setattr(self, field_item.name, None)

            self._partial_init = ft.partial(
                SimpleRNNCell.__init__,
                self=self,
                hidden_features=hidden_features,
                weight_init_func=weight_init_func,
                bias_init_func=bias_init_func,
                recurrent_weight_init_func=recurrent_weight_init_func,
                act_func=act_func,
                key=key,
            )
            return

        if hasattr(self, "_partial_init"):
            delattr(self, "_partial_init")

        k1, k2 = jr.split(key, 2)

        self.in_features = _check_and_return_positive_int(in_features, "in_features")
        self.hidden_features = _check_and_return_positive_int(
            hidden_features, "hidden_features"
        )
        self.act_func = _act_func_map[act_func]

        self.in_to_hidden = Linear(
            in_features,
            hidden_features,
            weight_init_func=weight_init_func,
            bias_init_func=bias_init_func,
            key=k1,
        )

        self.hidden_to_hidden = Linear(
            hidden_features,
            hidden_features,
            weight_init_func=recurrent_weight_init_func,
            bias_init_func=None,
            key=k2,
        )

    @_lazy_rnn_cell
    def __call__(
        self, x: jnp.ndarray, state: SimpleRNNState, **kwargs
    ) -> SimpleRNNState:
        msg = f"Expected state to be an instance of SimpleRNNState, got {type(state)}"
        assert isinstance(state, SimpleRNNState), msg
        h = state.hidden_state
        h = self.act_func(self.in_to_hidden(x) + self.hidden_to_hidden(h))
        return SimpleRNNState(h)

    def init_state(self) -> SimpleRNNState:
        shape = (self.hidden_features,)
        return SimpleRNNState(jnp.zeros(shape))


@pytc.treeclass
class LSTMState(RNNState):
    cell_state: jnp.ndarray


@pytc.treeclass
class LSTMCell(RNNCell):
    in_to_hidden: Linear
    hidden_to_hidden: Linear

    def __init__(
        self,
        in_features: int,
        hidden_features: int,
        *,
        weight_init_func: str | Callable = "glorot_uniform",
        bias_init_func: str | Callable | None = "zeros",
        recurrent_weight_init_func: str | Callable = "orthogonal",
        act_func: str | None = "tanh",
        recurrent_act_func: str | None = "sigmoid",
        key: jr.PRNGKey = jr.PRNGKey(0),
    ):
        """LSTM cell that defines the update rule for the hidden state and cell state
        Args:
            in_features: the number of input features
            hidden_features: the number of hidden features
            weight_init_func: the function to use to initialize the weights
            bias_init_func: the function to use to initialize the bias
            recurrent_weight_init_func: the function to use to initialize the recurrent weights
            act_func: the activation function to use for the hidden state update
            recurrent_act_func: the activation function to use for the cell state update
            key: the key to use to initialize the weights

        See:
            https://www.tensorflow.org/api_docs/python/tf/keras/layers/LSTMCell
            https://github.com/deepmind/dm-haiku/blob/main/haiku/_src/recurrent.py
        """
        if in_features is None:
            for field_item in dataclasses.fields(self):
                # set all fields to None to mark the class as uninitialized
                # to the user and to avoid errors
                setattr(self, field_item.name, None)

            self._partial_init = ft.partial(
                LSTMCell.__init__,
                self=self,
                hidden_features=hidden_features,
                weight_init_func=weight_init_func,
                bias_init_func=bias_init_func,
                recurrent_weight_init_func=recurrent_weight_init_func,
                act_func=act_func,
                key=key,
            )
            return

        if hasattr(self, "_partial_init"):
            delattr(self, "_partial_init")

        k1, k2 = jr.split(key, 2)

        self.in_features = _check_and_return_positive_int(in_features, "in_features")
        self.hidden_features = _check_and_return_positive_int(
            hidden_features, "hidden_features"
        )
        self.act_func = _act_func_map[act_func]
        self.recurrent_act_func = _act_func_map[recurrent_act_func]

        self.in_to_hidden = Linear(
            in_features,
            hidden_features * 4,
            weight_init_func=weight_init_func,
            bias_init_func=bias_init_func,
            key=k1,
        )

        self.hidden_to_hidden = Linear(
            hidden_features,
            hidden_features * 4,
            weight_init_func=recurrent_weight_init_func,
            bias_init_func=None,
            key=k2,
        )

    @_lazy_rnn_cell
    def __call__(self, x: jnp.ndarray, state: LSTMState, **kwargs) -> LSTMState:
        msg = f"Expected state to be an instance of LSTMState, got {type(state)}"
        assert isinstance(state, LSTMState), msg
        h, c = state.hidden_state, state.cell_state

        h = self.in_to_hidden(x) + self.hidden_to_hidden(h)
        i, f, g, o = jnp.split(h, 4, axis=-1)
        i = self.recurrent_act_func(i)
        f = self.recurrent_act_func(f)
        g = self.act_func(g)
        o = self.recurrent_act_func(o)
        c = f * c + i * g
        h = o * self.act_func(c)
        return LSTMState(h, c)

    def init_state(self) -> LSTMState:
        shape = (self.hidden_features,)
        return LSTMState(jnp.zeros(shape), jnp.zeros(shape))


@pytc.treeclass
class GRUState(RNNState):
    pass


@pytc.treeclass
class GRUCell(RNNCell):
    in_to_hidden: Linear
    hidden_to_hidden: Linear

    def __init__(
        self,
        in_features: int,
        hidden_features: int,
        *,
        weight_init_func: str | Callable = "glorot_uniform",
        bias_init_func: str | Callable | None = "zeros",
        recurrent_weight_init_func: str | Callable = "orthogonal",
        act_func: str | None = "tanh",
        recurrent_act_func: str | None = "sigmoid",
        key: jr.PRNGKey = jr.PRNGKey(0),
    ):
        """GRU cell that defines the update rule for the hidden state and cell state
        Args:
            in_features: the number of input features
            hidden_features: the number of hidden features
            weight_init_func: the function to use to initialize the weights
            bias_init_func: the function to use to initialize the bias
            recurrent_weight_init_func: the function to use to initialize the recurrent weights
            act_func: the activation function to use for the hidden state update
            recurrent_act_func: the activation function to use for the cell state update
            key: the key to use to initialize the weights

        See:
            https://keras.io/api/layers/recurrent_layers/gru/
        """
        if in_features is None:
            for field_item in dataclasses.fields(self):
                # set all fields to None to mark the class as uninitialized
                # to the user and to avoid errors
                setattr(self, field_item.name, None)

            self._partial_init = ft.partial(
                GRUCell.__init__,
                self=self,
                hidden_features=hidden_features,
                weight_init_func=weight_init_func,
                bias_init_func=bias_init_func,
                recurrent_weight_init_func=recurrent_weight_init_func,
                act_func=act_func,
                key=key,
            )
            return

        if hasattr(self, "_partial_init"):
            delattr(self, "_partial_init")

        k1, k2 = jr.split(key, 2)

        self.in_features = _check_and_return_positive_int(in_features, "in_features")
        self.hidden_features = _check_and_return_positive_int(
            hidden_features, "hidden_features"
        )
        self.act_func = _act_func_map[act_func]
        self.recurrent_act_func = _act_func_map[recurrent_act_func]

        self.in_to_hidden = Linear(
            in_features,
            hidden_features * 3,
            weight_init_func=weight_init_func,
            bias_init_func=bias_init_func,
            key=k1,
        )

        self.hidden_to_hidden = Linear(
            hidden_features,
            hidden_features * 3,
            weight_init_func=recurrent_weight_init_func,
            bias_init_func=None,
            key=k2,
        )

    @_lazy_rnn_cell
    def __call__(self, x: jnp.ndarray, state: GRUState, **kwargs) -> GRUState:
        msg = f"Expected state to be an instance of GRUState, got {type(state)}"
        assert isinstance(state, GRUState), msg
        h = state.hidden_state
        xe, xu, xo = jnp.split(self.in_to_hidden(x), 3, axis=-1)
        he, hu, ho = jnp.split(self.hidden_to_hidden(h), 3, axis=-1)
        e = self.recurrent_act_func(xe + he)
        u = self.recurrent_act_func(xu + hu)
        o = self.act_func(xo + (e * ho))
        h = (1 - u) * o + u * h
        return GRUState(hidden_state=h)

    def init_state(self) -> GRUState:
        shape = (self.hidden_features,)
        return GRUState(jnp.zeros(shape, dtype=jnp.float32))


# ------------------------------------------------- Spatial RNN ------------------------------------------------------ #
@pytc.treeclass
class ConvLSTMNDState(RNNState):
    cell_state: jnp.ndarray


@pytc.treeclass
class ConvLSTMNDCell(SpatialRNNCell):
    in_to_hidden: ConvND
    hidden_to_hidden: ConvND

    def __init__(
        self,
        in_features: int,
        out_features: int,
        kernel_size: int | tuple[int, ...],
        *,
        strides: int | tuple[int, ...] = 1,
        padding: str | tuple[int, ...] | tuple[tuple[int, int], ...] = "SAME",
        input_dilation: int | tuple[int, ...] = 1,
        kernel_dilation: int | tuple[int, ...] = 1,
        weight_init_func: str | Callable = "glorot_uniform",
        bias_init_func: str | Callable | None = "zeros",
        recurrent_weight_init_func: str | Callable = "orthogonal",
        act_func: str | None = "tanh",
        recurrent_act_func: str | None = "hard_sigmoid",
        key: jr.PRNGKey = jr.PRNGKey(0),
        conv_layer: ConvND | SeparableConvND = ConvND,
        ndim: int = 2,
    ):
        """Convolution LSTM cell that defines the update rule for the hidden state and cell state
        Args:
            in_features: Number of input features
            out_features: Number of output features
            kernel_size: Size of the convolutional kernel
            strides: Stride of the convolution
            padding: Padding of the convolution
            input_dilation: Dilation of the input
            kernel_dilation: Dilation of the convolutional kernel
            weight_init_func: Weight initialization function
            bias_init_func: Bias initialization function
            recurrent_weight_init_func: Recurrent weight initialization function
            act_func: Activation function
            recurrent_act_func: Recurrent activation function
            key: PRNG key
            ndim: Number of spatial dimensions

        See: https://www.tensorflow.org/api_docs/python/tf/keras/layers/ConvLSTM1D
        """
        if in_features is None:
            for field_item in dataclasses.fields(self):
                # set all fields to None to mark the class as uninitialized
                # to the user and to avoid errors
                setattr(self, field_item.name, None)

            self._partial_init = ft.partial(
                ConvLSTMNDCell.__init__,
                self=self,
                out_features=out_features,
                kernel_size=kernel_size,
                strides=strides,
                padding=padding,
                input_dilation=input_dilation,
                kernel_dilation=kernel_dilation,
                weight_init_func=weight_init_func,
                bias_init_func=bias_init_func,
                recurrent_weight_init_func=recurrent_weight_init_func,
                act_func=act_func,
                recurrent_act_func=recurrent_act_func,
                ndim=ndim,
                key=key,
            )
            return

        if hasattr(self, "_partial_init"):
            delattr(self, "_partial_init")

        k1, k2 = jr.split(key, 2)

        self.act_func = _act_func_map[act_func]
        self.recurrent_act_func = _act_func_map[recurrent_act_func]
        self.in_features = _check_and_return_positive_int(in_features, "in_features")
        self.out_features = _check_and_return_positive_int(out_features, "out_features")
        self.hidden_features = out_features
        self.ndim = ndim

        self.in_to_hidden = conv_layer(
            in_features,
            out_features * 4,
            kernel_size,
            strides=strides,
            padding=padding,
            input_dilation=input_dilation,
            kernel_dilation=kernel_dilation,
            weight_init_func=weight_init_func,
            bias_init_func=bias_init_func,
            key=k1,
            ndim=ndim,
        )

        self.hidden_to_hidden = conv_layer(
            out_features,
            out_features * 4,
            kernel_size,
            strides=strides,
            padding=padding,
            input_dilation=input_dilation,
            kernel_dilation=kernel_dilation,
            weight_init_func=recurrent_weight_init_func,
            bias_init_func=None,
            key=k2,
            ndim=ndim,
        )

    @_lazy_rnn_cell
    def __call__(
        self, x: jnp.ndarray, state: ConvLSTMNDState, **kwargs
    ) -> ConvLSTMNDState:
        msg = f"Expected state to be an instance of ConvLSTMNDState, got {type(state)}"
        assert isinstance(state, ConvLSTMNDState), msg
        h, c = state.hidden_state, state.cell_state

        h = self.in_to_hidden(x) + self.hidden_to_hidden(h)
        i, f, g, o = jnp.split(h, 4, axis=0)
        i = self.recurrent_act_func(i)
        f = self.recurrent_act_func(f)
        g = self.act_func(g)
        o = self.recurrent_act_func(o)
        c = f * c + i * g
        h = o * self.act_func(c)
        return ConvLSTMNDState(h, c)

    def init_state(self, spatial_dim: tuple[int, ...]) -> ConvLSTMNDState:
        msg = f"Expected spatial_dim to be a tuple of length {self.ndim}, got {spatial_dim}"
        assert len(spatial_dim) == self.ndim, msg
        shape = (self.hidden_features, *spatial_dim)
        return ConvLSTMNDState(jnp.zeros(shape), jnp.zeros(shape))


@pytc.treeclass
class ConvLSTM1DCell(ConvLSTMNDCell):
    def __init__(self, *a, **k):
        super().__init__(*a, **k, ndim=1, conv_layer=ConvND)


@pytc.treeclass
class ConvLSTM2DCell(ConvLSTMNDCell):
    def __init__(self, *a, **k):
        super().__init__(*a, **k, ndim=2, conv_layer=ConvND)


@pytc.treeclass
class ConvLSTM3DCell(ConvLSTMNDCell):
    def __init__(self, *a, **k):
        super().__init__(*a, **k, ndim=3, conv_layer=ConvND)


@pytc.treeclass
class SeparableConvLSTM1DCell(ConvLSTMNDCell):
    def __init__(self, *a, **k):
        super().__init__(*a, **k, ndim=1, conv_layer=SeparableConvND)


@pytc.treeclass
class SeparableConvLSTM2DCell(ConvLSTMNDCell):
    def __init__(self, *a, **k):
        super().__init__(*a, **k, ndim=2, conv_layer=SeparableConvND)


@pytc.treeclass
class SeparableConvLSTM3DCell(ConvLSTMNDCell):
    def __init__(self, *a, **k):
        super().__init__(*a, **k, ndim=3, conv_layer=SeparableConvND)


@pytc.treeclass
class FFTConvLSTM1DCell(ConvLSTMNDCell):
    def __init__(self, *a, **k):
        super().__init__(*a, **k, ndim=1, conv_layer=FFTConvND)


@pytc.treeclass
class FFTConvLSTM2DCell(ConvLSTMNDCell):
    def __init__(self, *a, **k):
        super().__init__(*a, **k, ndim=2, conv_layer=FFTConvND)


@pytc.treeclass
class FFTConvLSTM3DCell(ConvLSTMNDCell):
    def __init__(self, *a, **k):
        super().__init__(*a, **k, ndim=3, conv_layer=FFTConvND)


@pytc.treeclass
class SeparableFFTConvLSTM1DCell(ConvLSTMNDCell):
    def __init__(self, *a, **k):
        super().__init__(*a, **k, ndim=1, conv_layer=SeparableFFTConvND)


@pytc.treeclass
class SeparableFFTConvLSTM2DCell(ConvLSTMNDCell):
    def __init__(self, *a, **k):
        super().__init__(*a, **k, ndim=2, conv_layer=SeparableFFTConvND)


@pytc.treeclass
class SeparableFFTConvLSTM3DCell(ConvLSTMNDCell):
    def __init__(self, *a, **k):
        super().__init__(*a, **k, ndim=3, conv_layer=SeparableFFTConvND)


@pytc.treeclass
class ConvGRUNDState(RNNState):
    pass


@pytc.treeclass
class ConvGRUNDCell(SpatialRNNCell):
    in_to_hidden: ConvND
    hidden_to_hidden: ConvND

    def __init__(
        self,
        in_features: int,
        out_features: int,
        kernel_size: int | tuple[int, ...],
        *,
        strides: int | tuple[int, ...] = 1,
        padding: str | tuple[int, ...] | tuple[tuple[int, int], ...] = "SAME",
        input_dilation: int | tuple[int, ...] = 1,
        kernel_dilation: int | tuple[int, ...] = 1,
        weight_init_func: str | Callable = "glorot_uniform",
        bias_init_func: str | Callable | None = "zeros",
        recurrent_weight_init_func: str | Callable = "orthogonal",
        act_func: str | None = "tanh",
        recurrent_act_func: str | None = "sigmoid",
        key: jr.PRNGKey = jr.PRNGKey(0),
        conv_layer: ConvND | SeparableConvND = ConvND,
        ndim: int = 2,
    ):
        """Convolution GRU cell that defines the update rule for the hidden state and cell state
        Args:
            in_features: Number of input features
            out_features: Number of output features
            kernel_size: Size of the convolutional kernel
            strides: Stride of the convolution
            padding: Padding of the convolution
            input_dilation: Dilation of the input
            kernel_dilation: Dilation of the convolutional kernel
            weight_init_func: Weight initialization function
            bias_init_func: Bias initialization function
            recurrent_weight_init_func: Recurrent weight initialization function
            act_func: Activation function
            recurrent_act_func: Recurrent activation function
            key: PRNG key
            ndim: Number of spatial dimensions

        """
        if in_features is None:
            for field_item in dataclasses.fields(self):
                # set all fields to None to mark the class as uninitialized
                # to the user and to avoid errors
                setattr(self, field_item.name, None)

            self._partial_init = ft.partial(
                ConvGRUNDCell.__init__,
                self=self,
                out_features=out_features,
                kernel_size=kernel_size,
                strides=strides,
                padding=padding,
                input_dilation=input_dilation,
                kernel_dilation=kernel_dilation,
                weight_init_func=weight_init_func,
                bias_init_func=bias_init_func,
                recurrent_weight_init_func=recurrent_weight_init_func,
                act_func=act_func,
                recurrent_act_func=recurrent_act_func,
                ndim=ndim,
                key=key,
            )
            return

        if hasattr(self, "_partial_init"):
            delattr(self, "_partial_init")

        k1, k2 = jr.split(key, 2)

        self.act_func = _act_func_map[act_func]
        self.recurrent_act_func = _act_func_map[recurrent_act_func]
        self.in_features = _check_and_return_positive_int(in_features, "in_features")
        self.out_features = _check_and_return_positive_int(out_features, "out_features")
        self.hidden_features = out_features
        self.ndim = ndim

        self.in_to_hidden = conv_layer(
            in_features,
            out_features * 3,
            kernel_size,
            strides=strides,
            padding=padding,
            input_dilation=input_dilation,
            kernel_dilation=kernel_dilation,
            weight_init_func=weight_init_func,
            bias_init_func=bias_init_func,
            key=k1,
            ndim=ndim,
        )

        self.hidden_to_hidden = conv_layer(
            out_features,
            out_features * 3,
            kernel_size,
            strides=strides,
            padding=padding,
            input_dilation=input_dilation,
            kernel_dilation=kernel_dilation,
            weight_init_func=recurrent_weight_init_func,
            bias_init_func=None,
            key=k2,
            ndim=ndim,
        )

    @_lazy_rnn_cell
    def __call__(
        self, x: jnp.ndarray, state: ConvGRUNDState, **kwargs
    ) -> ConvGRUNDState:
        msg = f"Expected state to be an instance of GRUState, got {type(state)}"
        assert isinstance(state, ConvGRUNDState), msg
        h = state.hidden_state
        xe, xu, xo = jnp.split(self.in_to_hidden(x), 3, axis=0)
        he, hu, ho = jnp.split(self.hidden_to_hidden(h), 3, axis=0)
        e = self.recurrent_act_func(xe + he)
        u = self.recurrent_act_func(xu + hu)
        o = self.act_func(xo + (e * ho))
        h = (1 - u) * o + u * h
        return ConvGRUNDState(hidden_state=h)

    def init_state(self, spatial_dim: tuple[int, ...]) -> ConvGRUNDState:
        msg = f"Expected spatial_dim to be a tuple of length {self.ndim}, got {spatial_dim}"
        assert len(spatial_dim) == self.ndim, msg
        shape = (self.hidden_features, *spatial_dim)
        return ConvGRUNDState(hidden_state=jnp.zeros(shape))


@pytc.treeclass
class ConvGRU1DCell(ConvGRUNDCell):
    def __init__(self, *a, **k):
        super().__init__(*a, **k, ndim=1, conv_layer=ConvND)


@pytc.treeclass
class ConvGRU2DCell(ConvGRUNDCell):
    def __init__(self, *a, **k):
        super().__init__(*a, **k, ndim=2, conv_layer=ConvND)


@pytc.treeclass
class ConvGRU3DCell(ConvGRUNDCell):
    def __init__(self, *a, **k):
        super().__init__(*a, **k, ndim=3, conv_layer=ConvND)


@pytc.treeclass
class SeparableConvGRU1DCell(ConvGRUNDCell):
    def __init__(self, *a, **k):
        super().__init__(*a, **k, ndim=1, conv_layer=SeparableConvND)


@pytc.treeclass
class SeparableConvGRU2DCell(ConvGRUNDCell):
    def __init__(self, *a, **k):
        super().__init__(*a, **k, ndim=2, conv_layer=SeparableConvND)


@pytc.treeclass
class SeparableConvGRU3DCell(ConvGRUNDCell):
    def __init__(self, *a, **k):
        super().__init__(*a, **k, ndim=3, conv_layer=SeparableConvND)


@pytc.treeclass
class FFTConvGRU1DCell(ConvGRUNDCell):
    def __init__(self, *a, **k):
        super().__init__(*a, **k, ndim=1, conv_layer=FFTConvND)


@pytc.treeclass
class FFTConvGRU2DCell(ConvGRUNDCell):
    def __init__(self, *a, **k):
        super().__init__(*a, **k, ndim=2, conv_layer=FFTConvND)


@pytc.treeclass
class FFTConvGRU3DCell(ConvGRUNDCell):
    def __init__(self, *a, **k):
        super().__init__(*a, **k, ndim=3, conv_layer=FFTConvND)


@pytc.treeclass
class SeparableFFTConvGRU1DCell(ConvGRUNDCell):
    def __init__(self, *a, **k):
        super().__init__(*a, **k, ndim=1, conv_layer=SeparableFFTConvND)


@pytc.treeclass
class SeparableFFTConvGRU2DCell(ConvGRUNDCell):
    def __init__(self, *a, **k):
        super().__init__(*a, **k, ndim=2, conv_layer=SeparableFFTConvND)


@pytc.treeclass
class SeparableFFTConvGRU3DCell(ConvGRUNDCell):
    def __init__(self, *a, **k):
        super().__init__(*a, **k, ndim=3, conv_layer=SeparableFFTConvND)


# ------------------------------------------------- Scan layer ------------------------------------------------------ #


@pytc.treeclass
class ScanRNN:
    cell: RNNCell | SpatialRNNCell
    backward_cell: RNNCell | SpatialRNNCell | None

    def __init__(
        self,
        cell: RNNCell | SpatialRNNCell,
        backward_cell: RNNCell | SpatialRNNCell | None = None,
        *,
        return_sequences: bool = False,
    ):
        """Scans RNN cell over a sequence.

        Args:
            cell: the RNN cell to use
            backward_cell: the RNN cell to use for bidirectional scanning.
            return_sequences: whether to return the hidden state for each timestep

        Example:
            >>> cell = SimpleRNNCell(10, 20) # 10-dimensional input, 20-dimensional hidden state
            >>> rnn = ScanRNN(cell)
            >>> x = jnp.ones((5, 10)) # 5 timesteps, 10 features
            >>> result = rnn(x)  # 20 features

            # bidirectional convolution lstm
            >>> cell = ConvLSTM1DCell(10, 20, kernel_size=3) # 10-features input, 20-features hidden state
            >>> reverse_cell = ConvLSTM1DCell(10, 20, kernel_size=3) # 10-features input, 20-features hidden state
            >>> rnn = ScanRNN(cell, reverse_cell, return_sequences=True)
            >>> x = jnp.ones((5, 10,12)) # 5 timesteps, 10 features, width 12
            >>> result = rnn(x)  # 5 timestep, 20*2 features, width 12
        """
        if not isinstance(cell, (RNNCell, SpatialRNNCell)):
            msg = f"Expected cell to be an instance of RNNCell or SpatialRNNCell, got {type(cell)}"
            raise ValueError(msg)

        if not isinstance(backward_cell, (RNNCell, SpatialRNNCell, type(None))):
            msg = "Expected backward_cell to be an instance of RNNCell, SpatialRNNCell or None"
            msg += f", got {type(backward_cell)}"
            raise ValueError(msg)

        self.cell = cell
        self.backward_cell = backward_cell
        self.return_sequences = return_sequences

    @_lazy_fwd_rnn
    @_lazy_bwd_rnn
    def __call__(
        self,
        x: jnp.ndarray,
        state: RNNState | None = None,
        backward_state: RNNState | None = None,
        **kwargs,
    ) -> jnp.ndarray:
        if not isinstance(state, (type(None), RNNState)):
            msg = f"Expected state to be an instance of RNNState, got {type(state)}"
            raise ValueError(msg)

        # backward cell
        if not isinstance(backward_state, (type(None), RNNState)):
            msg = f"Expected backward_state to be an instance of RNNState, got {type(backward_state)}"
            raise ValueError(msg)

        if isinstance(self.cell, SpatialRNNCell):
            # (time steps, in_features, *spatial_dims)
            msg = f"Expected x to have {self.cell.ndim + 2}"  # account for time and in_features
            msg += f" dimensions corresponds to (timesteps, in_features, *spatial_dims), got {x.ndim}"
            assert x.ndim == (self.cell.ndim + 2), msg
            msg = f"Expected x to have shape (timesteps, {self.cell.in_features}, *spatial_dims)"
            msg += f", got {x.shape}"
            assert self.cell.in_features == x.shape[1], msg
            state = state or self.cell.init_state(spatial_dim=x.shape[2:])

            if self.backward_cell is not None:
                msg = f"Expected backward cell to be an instance of SpatialRNNCell, got {type(self.backward_cell)}"
                assert isinstance(self.backward_cell, SpatialRNNCell), msg
                backward_state = backward_state or self.backward_cell.init_state(
                    spatial_dim=x.shape[2:]
                )

        else:
            # (time steps, in_features)
            msg = f"Expected x to have 2 dimensions corresponds to (timesteps, in_features), got {x.ndim}"
            assert x.ndim == 2, msg
            msg = f"Expected x to have shape (timesteps, {self.cell.in_features})"
            msg += f", got {x.shape}"
            assert self.cell.in_features == x.shape[1], msg
            state = state or self.cell.init_state()

            if self.backward_cell is not None:
                msg = f"Expected backward cell to be an instance of RNNCell, got {type(self.backward_cell)}"
                assert isinstance(self.backward_cell, RNNCell), msg
                backward_state = backward_state or self.backward_cell.init_state()

        if self.return_sequences:
            # accumulate the hidden state for each timestep
            def general_scan_func(cell, carry, x):
                state = cell(x, state=carry)
                return state, state

            scan_func = ft.partial(general_scan_func, self.cell)
            result = jax.lax.scan(scan_func, state, x)[1].hidden_state

            # backward cell
            if self.backward_cell is not None:
                scan_func = ft.partial(general_scan_func, self.backward_cell)
                x = jnp.flip(x, axis=0)  # reverse the time axis
                back_result = jax.lax.scan(scan_func, backward_state, x)[1].hidden_state
                # reverse once again over the accumulated time axis
                back_result = jnp.flip(back_result, axis=-1)
                result = jnp.concatenate([result, back_result], axis=1)

            return result

        # only return the hidden state for the last timestep
        def general_scan_func(cell, carry, x):
            state = cell(x, state=carry)
            return state, None

        scan_func = ft.partial(general_scan_func, self.cell)
        result = jax.lax.scan(scan_func, state, x)[0].hidden_state

        # backward cell
        if self.backward_cell is not None:
            scan_func = ft.partial(general_scan_func, self.backward_cell)
            x = jnp.flip(x, axis=0)
            back_result = jax.lax.scan(scan_func, backward_state, x)[0].hidden_state
            result = jnp.concatenate([result, back_result], axis=0)

        return result
