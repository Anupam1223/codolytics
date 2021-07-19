import pandas as pd
import pytest

from ....services.metrics import Metrics


@pytest.fixture
def test_metrics_class():
    """
    Checks metrics class
    """
    test_df = pd.DataFrame([(1, 2), (3, 4)], columns=["A", "B"])
    print(type(test_df))
    with pytest.raises(FileNotFoundError) as exec:
        Metrics()
    assert str(exec.value) == "No such file or directory found"
    metrics = Metrics(test_df)
    return metrics
