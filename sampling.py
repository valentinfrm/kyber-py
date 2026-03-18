import params
import polynomial
from Crypto.Hash import SHAKE128
from auxiliary import *

def sample_poly_cbd(byte_input, eta):
    """
    samples poly coeff from PRF output with CBD

    Args:
        b (bytes): 64 * eta byte array
        eta (int): {2,3}
    Returns:
        list: 256 coefficients in Zq
    """

    int_input = int.from_bytes(byte_input, "little")
    coeffs = [0] * 256

    m1 = (1 << eta) - 1 # for eta = 2: 11b -> two bits
    m2 = (1 << 2 * eta) - 1 # total amount needed
    for i in range(256):
        tmp = int_input & m2
        x = (tmp & m1).bit_count() # bitcount == manual sum with loop
        y = ((tmp >> eta) & m1).bit_count()
        coeffs[i] = (x - y) % params.q

        int_input >>= 2 * eta # cuts used ones off

    return polynomial.poly(coeffs)

def expand(rho):
    """
    in NTT realm
    """
    k = params.k
    A = [[None] * k for _ in range(k)]
    for i in range(k):
        for j in range(k):
            A[i][j] = sample_NTT(rho + bytes([j]) + bytes([i]))
    return A


def sample_NTT(byte_input):
    shake = SHAKE128.new(byte_input)
    
    di = 0
    i = 0
    coeff = []

    while i < 256:
        C = shake.read(3) # 3 bytes -> 24 bits -> 2 * 12 (12 bits needed for max 3329)
        d1 = C[0] + 256 * (C[1] % 16)
        d2 = (C[1] >> 4) + 16 * C[2]

        # rejection sampling (if too high -> resample)
        if d1 < params.q and i < 256:
            coeff.append(d1)
            i += 1

        if d2 < params.q and i < 256:
            coeff.append(d2)
            i += 1
        
        di += 3

    return polynomial.poly(coeff)
