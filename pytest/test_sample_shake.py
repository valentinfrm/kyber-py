import sampling
import params

def test_sample_poly_shake():
    result = sampling.sample_poly_shake(bytes(32) + bytes([0]) + bytes([0]))
    assert len(result.coeff) == 256
    assert all(0 <= c < params.q for c in result.coeff)