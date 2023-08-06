import torch
from aquatic.observer import MovingAverageMinMaxObserver


def test_avg_computation():
    observer = MovingAverageMinMaxObserver(averaging_constant=0.9)

    data = torch.ones((2, 62))
    data[0] = -128
    data[1] = 127

    for _ in range(20):
        # Update data
        observer(data)

    assert observer.min_val == -128
    assert observer.max_val == 127
