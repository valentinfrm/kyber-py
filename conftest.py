# pytest configuration: adds root directory to Python path for module discovery
import params
import pytest
import os

@pytest.fixture(autouse=True)
def set_kem_params(request):
    filename = os.path.basename(request.fspath)
    
    params.n = 256
    params.q = 3329
    
    if "768" in filename:
        params.k = 3
        params.eta1 = 2
        params.du = 10
        params.dv = 4
    elif "512" in filename:
        params.k = 2
        params.eta1 = 3
        params.du = 10
        params.dv = 4
    elif "1024" in filename:
        params.k = 4
        params.eta1 = 2
        params.du = 11
        params.dv = 5
    else:
        # default: ML-KEM-768
        params.k = 3
        params.eta1 = 2
        params.du = 10
        params.dv = 4