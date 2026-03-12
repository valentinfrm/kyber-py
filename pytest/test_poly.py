from ntt import NTT, iNTT, mul_NTT

def test_poly_mul_kyber():
    from kyber_py.polynomials.polynomials_generic import GenericPolynomialRing
    R = GenericPolynomialRing(3329, 256)
    coeffs1 = list(range(256))
    coeffs2 = list(range(256, 512))
    
    # Regular multiplication in kyber_py
    f = R(coeffs1)
    g = R(coeffs2)
    regular_product = f * g
    
    # NTT
    ntt_f = NTT(coeffs1)
    ntt_g = NTT(coeffs2)
    ntt_product = mul_NTT(ntt_f, ntt_g)
    your_result = iNTT(ntt_product)
    
    assert list(your_result) == list(regular_product.coeffs)
