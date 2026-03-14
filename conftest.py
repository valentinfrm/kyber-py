# pytest configuration: adds root directory to Python path for module discovery
import params
import pytest

@pytest.fixture(autouse=True)
def reset_params_768():
    params.k = 3
    params.eta1 = 2
    params.du = 10
    params.dv = 4
    params.n = 256
    params.q = 3329
