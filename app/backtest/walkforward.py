import numpy as np
from typing import List, Tuple, Iterator
from sklearn.model_selection import BaseCrossValidator


class WalkForwardSplit(BaseCrossValidator):
    """
    Walk-forward cross-validation splits for time series data.
    """

    def __init__(self, n_splits: int = 5, train_size: int = 10, test_size: int = 5):
        self.n_splits = n_splits
        self.train_size = train_size
        self.test_size = test_size

    def split(self, n_samples: int) -> Iterator[Tuple[int, int, int, int]]:
        """
        Generate indices for walk-forward splits.
        """
        if self.train_size + self.test_size > n_samples:
            return

        step_size = self.test_size
        for i in range(self.n_splits):
            train_start = i * step_size
            train_end = train_start + self.train_size
            test_start = train_end
            test_end = test_start + self.test_size

            if test_end > n_samples:
                break

            yield (train_start, train_end, test_start, test_end)

    def get_n_splits(self, n_samples: int = None) -> int:
        return self.n_splits


def generate_walkforward_splits(data_length: int, n_splits: int, train_size: int, test_size: int) -> List[Tuple[int, int, int, int]]:
    """
    Generate walk-forward splits for given data length and parameters.
    """
    wf = WalkForwardSplit(n_splits=n_splits, train_size=train_size, test_size=test_size)
    return list(wf.split(data_length))


def evaluate_walkforward_splits(splits: List[Tuple[int, int, int, int]], data_length: int) -> dict:
    """
    Evaluate summary statistics for walk-forward splits.
    """
    if not splits:
        return {
            "n_splits": 0,
            "total_train": 0,
            "total_test": 0,
            "train_percentage": 0.0,
            "test_percentage": 0.0
        }

    total_train = sum(end - start for _, end, start, _ in splits)
    total_test = sum(end - start for _, _, start, end in splits)

    train_percentage = (total_train / data_length) * 100
    test_percentage = (total_test / data_length) * 100

    return {
        "n_splits": len(splits),
        "total_train": total_train,
        "total_test": total_test,
        "train_percentage": train_percentage,
        "test_percentage": test_percentage
    }