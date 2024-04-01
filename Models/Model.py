from typing import Protocol, runtime_checkable


@runtime_checkable
class Model(Protocol):

    def fit(self, X, y, *args, **kwargs):
        pass

    def predict(self, X):
        pass
