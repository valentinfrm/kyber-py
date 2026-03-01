import params

"""
reformulated compress formula to avoid floating arithmetic
"""
def compress(x, d):
    q = params.q
    return ((x * (1 << d + 1) + q) // (2 * q)) % (1 << d)

def decompress(y, d):
    q = params.q
    return ((2 * q * y) + (1 << d)) // (1 << (d + 1))