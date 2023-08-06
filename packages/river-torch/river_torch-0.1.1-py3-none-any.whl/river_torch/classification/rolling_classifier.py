import math
import warnings
from typing import Callable, Dict, List, Type, Union

import pandas as pd
import torch
from ordered_set import OrderedSet
from river import base
from river.base.typing import ClfTarget
from torch import nn

from river_torch.base import RollingDeepEstimator
from river_torch.utils.hooks import ForwardOrderTracker, apply_hooks
from river_torch.utils.tensor_conversion import (df2rolling_tensor,
                                                 dict2rolling_tensor,
                                                 labels2onehot, output2proba)


class _TestLSTM(torch.nn.Module):
    def __init__(self, n_features, hidden_size=2):
        super().__init__()
        self.n_features = n_features
        self.hidden_size = hidden_size
        self.lstm = torch.nn.LSTM(
            input_size=n_features, hidden_size=hidden_size, num_layers=1
        )
        self.softmax = torch.nn.Softmax(dim=-1)

    def forward(self, X, **kwargs):
        # lstm with input, hidden, and internal state
        output, (hn, cn) = self.lstm(X)
        hn = hn.view(-1, self.hidden_size)
        return self.softmax(hn)


class RollingClassifier(RollingDeepEstimator, base.Classifier):
    """
    Wrapper that feeds a sliding window of the most recent examples to the wrapped PyTorch classification model. The class also automatically handles increases in the number of classes by adding output neurons in case the number of observed classes exceeds the current number of output neurons.

    Parameters
    ----------
    module
        Torch Module that builds the autoencoder to be wrapped. The Module should accept parameter `n_features` so that the returned model's input shape can be determined based on the number of features in the initial training example.
    loss_fn
        Loss function to be used for training the wrapped model. Can be a loss function provided by `torch.nn.functional` or one of the following: 'mse', 'l1', 'cross_entropy', 'binary_crossentropy', 'smooth_l1', 'kl_div'.
    optimizer_fn
        Optimizer to be used for training the wrapped model. Can be an optimizer class provided by `torch.optim` or one of the following: "adam", "adam_w", "sgd", "rmsprop", "lbfgs".
    lr
        Learning rate of the optimizer.
    output_is_logit
            Whether the module produces logits as output. If true, either softmax or sigmoid is applied to the outputs when predicting.
    is_class_incremental
        Whether the classifier should adapt to the appearance of previously unobserved classes by adding an unit to the output layer of the network. This works only if the last trainable layer is an nn.Linear layer. Note also, that output activation functions can not be adapted, meaning that a binary classifier with a sigmoid output can not be altered to perform multi-class predictions.
    device
        Device to run the wrapped model on. Can be "cpu" or "cuda".
    seed
        Random seed to be used for training the wrapped model.
    window_size
        Number of recent examples to be fed to the wrapped model at each step.
    append_predict
        Whether to append inputs passed for prediction to the rolling window.
    **kwargs
        Parameters to be passed to the `build_fn` function aside from `n_features`.

    Examples
    --------
    >>> from river_torch.classification import RollingClassifier
    >>> from river import metrics, datasets, compose, preprocessing
    >>> import torch

    >>> class MyModule(torch.nn.Module):
    ...
    ...    def __init__(self, n_features, hidden_size=1):
    ...        super().__init__()
    ...        self.n_features=n_features
    ...        self.hidden_size = hidden_size
    ...        self.lstm = torch.nn.LSTM(input_size=n_features, hidden_size=hidden_size, batch_first=False, num_layers=1, bias=False)
    ...        self.softmax = torch.nn.Softmax(dim=-1)
    ...
    ...    def forward(self, X, **kwargs):
    ...        output, (hn, cn) = self.lstm(X)  # lstm with input, hidden, and internal state
    ...        hn = hn.view(-1, self.lstm.hidden_size)
    ...        return self.softmax(hn)

    >>> dataset = datasets.Keystroke()
    >>> metric = metrics.Accuracy()
    >>> optimizer_fn = torch.optim.SGD

    >>> model_pipeline = preprocessing.StandardScaler()
    >>> model_pipeline |= RollingClassifier(
    ...     module=MyModule,
    ...     loss_fn="binary_cross_entropy",
    ...     optimizer_fn=torch.optim.SGD,
    ...     window_size=20,
    ...     lr=1e-2,
    ...     append_predict=True,
    ...     is_class_incremental=True
    ... )

    >>> for x, y in dataset.take(5000):
    ...     y_pred = model_pipeline.predict_one(x)  # make a prediction
    ...     metric = metric.update(y, y_pred)  # update the metric
    ...     model = model_pipeline.learn_one(x, y)  # make the model learn
    >>> print(f'Accuracy: {metric.get()}')
    Accuracy: 0.4468
    """

    def __init__(
        self,
        module: Union[torch.nn.Module, Type[torch.nn.Module]],
        loss_fn: Union[str, Callable] = "binary_cross_entropy",
        optimizer_fn: Union[str, Callable] = "sgd",
        lr: float = 1e-3,
        output_is_logit: bool = True,
        is_class_incremental: bool = False,
        device: str = "cpu",
        seed: int = 42,
        window_size: int = 10,
        append_predict: bool = False,
        **kwargs,
    ):
        self.observed_classes = OrderedSet()
        self.output_layer = None
        self.output_is_logit = output_is_logit
        self.is_class_incremental = is_class_incremental
        super().__init__(
            module=module,
            loss_fn=loss_fn,
            optimizer_fn=optimizer_fn,
            window_size=window_size,
            append_predict=append_predict,
            device=device,
            lr=lr,
            seed=seed,
            **kwargs,
        )

    @classmethod
    def _unit_test_params(cls) -> dict:
        """
        Returns a dictionary of parameters to be used for unit testing the respective class.

        Yields
        -------
        dict
            Dictionary of parameters to be used for unit testing the respective class.
        """

        yield {
            "module": _TestLSTM,
            "optimizer_fn": "sgd",
            "lr": 1e-3,
        }

    @classmethod
    def _unit_test_skips(self) -> set:
        """
        Indicates which checks to skip during unit testing.
        Most estimators pass the full test suite. However, in some cases, some estimators might not
        be able to pass certain checks.
        Returns
        -------
        set
            Set of checks to skip during unit testing.
        """
        return {
            "check_shuffle_features_no_impact",
            "check_emerging_features",
            "check_disappearing_features",
            "check_predict_proba_one",
            "check_predict_proba_one_binary",
        }

    def learn_one(self, x: dict, y: ClfTarget, **kwargs) -> "RollingClassifier":
        """
        Performs one step of training with the most recent training examples stored in the sliding window.

        Parameters
        ----------
        x
            Input example.
        y
            Target value.

        Returns
        -------
        Classifier
            The classifier itself.
        """

        if not self.module_initialized:
            self.kwargs["n_features"] = len(x)
            self.initialize_module(**self.kwargs)

        self._x_window.append(list(x.values()))

        # check last layer
        self.observed_classes.add(y)
        if self.is_class_incremental:
            self._adapt_output_dim()

        # training process
        x = dict2rolling_tensor(x, self._x_window, device=self.device)
        if x is not None:
            return self._learn(x=x, y=y)
        return self

    def _learn(self, x: torch.Tensor, y: Union[ClfTarget, List[ClfTarget]]):
        self.module.train()
        self.optimizer.zero_grad()
        y_pred = self.module(x)
        n_classes = y_pred.shape[-1]
        y = labels2onehot(
            y=y, classes=self.observed_classes, n_classes=n_classes, device=self.device
        )
        loss = self.loss_fn(y_pred, y)
        loss.backward()
        self.optimizer.step()
        return self

    def predict_proba_one(self, x: dict) -> Dict[ClfTarget, float]:
        """
        Predict the probability of each label given the most recent examples stored in the sliding window.

        Parameters
        ----------
        x
            Input example.

        Returns
        -------
        Dict[ClfTarget, float]
            Dictionary of probabilities for each label.
        """
        if not self.module_initialized:
            self.kwargs["n_features"] = len(x)
            self.initialize_module(**self.kwargs)

        x = dict2rolling_tensor(x, self._x_window, device=self.device)
        if x is not None:
            self.module.eval()
            y_pred = self.module(x)
            proba = output2proba(y_pred, self.observed_classes)
        else:
            proba = self._get_default_proba()
        return proba

    def learn_many(self, X: pd.DataFrame, y: list) -> "RollingClassifier":
        """
        Performs one step of training with the most recent training examples stored in the sliding window.

        Parameters
        ----------
        x
            Input examples.
        y
            Target values.

        Returns
        -------
        Classifier
            The classifier itself.
        """
        # check if model is initialized
        if not self.module_initialized:
            self.kwargs["n_features"] = len(X.columns)
            self.initialize_module(**self.kwargs)
        X = df2rolling_tensor(X, self._x_window, device=self.device)

        self.observed_classes.update(y)
        if self.is_class_incremental:
            self._adapt_output_dim()

        y = labels2onehot(
            y,
            self.observed_classes,
            self.output_layer.out_features,
            device=self.device,
        )
        if X is not None:
            self._learn(x=X, y=y)
        return self

    def predict_proba_many(self, X: pd.DataFrame) -> List:
        if not self.module_initialized:
            self.kwargs["n_features"] = len(X.columns)
            self.initialize_module(**self.kwargs)

        batch = df2rolling_tensor(
            X, self._x_window, device=self.device, update_window=self.append_predict
        )

        if batch is not None:
            self.module.eval()
            y_preds = self.module(batch)
            probas = output2proba(y_preds, self.observed_classes)
            if len(probas) < len(X):
                default_proba = self._get_default_proba()
                probas = [default_proba] * (len(X) - len(probas)) + probas
        else:
            default_proba = self._get_default_proba()
            probas = [default_proba] * len(X)
        return probas

    def _get_default_proba(self):
        if len(self.observed_classes) > 0:
            mean_proba = (
                1 / len(self.observed_classes)
                if len(self.observed_classes) != 0
                else 0.0
            )
            proba = {c: mean_proba for c in self.observed_classes}
        else:
            proba = {c: 1.0 for c in self.observed_classes}
        return proba

    def _adapt_output_dim(self):
        out_features_target = (
            len(self.observed_classes) if len(self.observed_classes) > 2 else 1
        )
        if isinstance(self.output_layer, nn.Linear):
            n_classes_to_add = out_features_target - self.output_layer.out_features
            if n_classes_to_add > 0:
                mean_input_weights = torch.empty(
                    n_classes_to_add, self.output_layer.in_features
                )
                nn.init.kaiming_uniform_(mean_input_weights, a=math.sqrt(5))
                self.output_layer.weight = nn.parameter.Parameter(
                    torch.cat([self.output_layer.weight, mean_input_weights], axis=0)
                )

                if self.output_layer.bias is not None:
                    new_bias = torch.empty(n_classes_to_add)
                    fan_in, _ = nn.init._calculate_fan_in_and_fan_out(
                        self.output_layer.weight
                    )
                    bound = 1 / math.sqrt(fan_in) if fan_in > 0 else 0
                    nn.init.uniform_(new_bias, -bound, bound)
                    self.output_layer.bias = nn.parameter.Parameter(
                        torch.cat([self.output_layer.bias, new_bias], axis=0)
                    )
                self.output_layer.out_features += n_classes_to_add
        elif isinstance(self.output_layer, nn.LSTM):
            n_classes_to_add = out_features_target - self.output_layer.hidden_size
            if n_classes_to_add > 0:
                assert (
                    not self.output_layer.bidirectional
                ), "Bidirectional LSTM not supported"
                assert (
                    self.output_layer.num_layers >= 1
                ), "Multi-layer LSTM not supported"
                w_ii, w_if, w_ig, w_io = torch.chunk(
                    self.output_layer.weight_ih_l0, chunks=4, dim=0
                )
                w_hi, w_hf, w_hg, w_ho = torch.chunk(
                    self.output_layer.weight_hh_l0, chunks=4, dim=0
                )
                input_weights = [w_ii, w_if, w_ig, w_io]
                hidden_weights = [w_hi, w_hf, w_hg, w_ho]
                mean_input_weights = [
                    torch.mean(w, dim=0).unsqueeze(1).T for w in input_weights
                ]
                mean_hidden_weights_dim_0 = [
                    torch.mean(w, dim=0).unsqueeze(0) for w in hidden_weights
                ]
                mean_hidden_weights_dim_1 = [
                    torch.mean(w, dim=1).unsqueeze(1) for w in hidden_weights
                ]

                if n_classes_to_add > 1:
                    mean_input_weights = [
                        w.repeat(n_classes_to_add, 1) for w in mean_input_weights
                    ]
                    mean_hidden_weights_dim_0 = [
                        w.repeat(n_classes_to_add, 1) for w in mean_hidden_weights_dim_0
                    ]
                    mean_hidden_weights_dim_1 = [
                        w.repeat(1, n_classes_to_add) for w in mean_hidden_weights_dim_1
                    ]

                self.output_layer.weight_ih_l0 = nn.parameter.Parameter(
                    torch.cat(
                        [
                            input_weights[0],
                            mean_input_weights[0],
                            input_weights[1],
                            mean_input_weights[1],
                            input_weights[2],
                            mean_input_weights[2],
                            input_weights[3],
                            mean_input_weights[3],
                        ],
                        axis=0,
                    )
                )
                self.output_layer.weight_hh_l0 = nn.parameter.Parameter(
                    torch.cat(
                        [
                            torch.cat(
                                [
                                    hidden_weights[0],
                                    mean_hidden_weights_dim_0[0],
                                    hidden_weights[1],
                                    mean_hidden_weights_dim_0[1],
                                    hidden_weights[2],
                                    mean_hidden_weights_dim_0[2],
                                    hidden_weights[3],
                                    mean_hidden_weights_dim_0[3],
                                ],
                                axis=0,
                            ),
                            torch.cat(
                                [
                                    mean_hidden_weights_dim_1[0],
                                    torch.normal(
                                        0,
                                        0.5,
                                        size=(n_classes_to_add, n_classes_to_add),
                                    ),
                                    mean_hidden_weights_dim_1[1],
                                    torch.normal(
                                        0,
                                        0.5,
                                        size=(n_classes_to_add, n_classes_to_add),
                                    ),
                                    mean_hidden_weights_dim_1[2],
                                    torch.normal(
                                        0,
                                        0.5,
                                        size=(n_classes_to_add, n_classes_to_add),
                                    ),
                                    mean_hidden_weights_dim_1[3],
                                    torch.normal(
                                        0,
                                        0.5,
                                        size=(n_classes_to_add, n_classes_to_add),
                                    ),
                                ],
                                axis=0,
                            ),
                        ],
                        axis=1,
                    )
                )

                if self.output_layer.bias:
                    new_bias_hh_l0 = torch.empty(n_classes_to_add * 4)
                    new_bias_ih_l0 = torch.empty(n_classes_to_add * 4)
                    self.output_layer.bias_hh_l0 = nn.parameter.Parameter(
                        torch.cat(
                            [self.output_layer.bias_hh_l0, new_bias_hh_l0], axis=0
                        )
                    )
                    self.output_layer.bias_ih_l0 = nn.parameter.Parameter(
                        torch.cat(
                            [self.output_layer.bias_ih_l0, new_bias_ih_l0], axis=0
                        )
                    )
                self.output_layer.hidden_size += n_classes_to_add

        self.optimizer = self.optimizer_fn(self.module.parameters(), lr=self.lr)

    def find_output_layer(self, n_features):

        handles = []
        tracker = ForwardOrderTracker()
        apply_hooks(module=self.module, hook=tracker, handles=handles)

        x_dummy = torch.empty((1, n_features), device=self.device)
        self.module(x_dummy)

        for h in handles:
            h.remove()

        if tracker.ordered_modules and isinstance(
            tracker.ordered_modules[-1], (nn.Linear, nn.LSTM)
        ):
            self.output_layer = tracker.ordered_modules[-1]
        else:
            warnings.warn(
                "The model will not be able to adapt its output to new classes since no linear layer output layer was found."
            )
            self.is_class_incremental = False

    def initialize_module(self, **kwargs):
        super().initialize_module(**kwargs)
        self.find_output_layer(n_features=kwargs["n_features"])
