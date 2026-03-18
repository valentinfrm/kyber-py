import params

def bytes_to_bits(byte_array):
    #LSB first
    result = []
    for b in byte_array:
        for _ in range(8):
            result.append(b & 1) # LSB
            b = b >> 1
    return result

def bits_to_bytes(bit_array):
    #LSB first
    result = []
    for i in range(len(bit_array) // 8): # cuts off remaining bits if len(bit_array) % 8 != 0
        x = 0
        for j in range(8):
            x += bit_array[i * 8 + j] * 2**j
        result.append(x)
    return result

def byte_encode(int_input, d):
    """
    encodes a list of integers into a list of bytes

    Args:
        d (int): bits per coeff
        int_input (list): integers to encode
    
    Returns:
        bytes: len(int_input) * d / 8 bytes
    """
    bits = []
    for value in int_input:
        for _ in range(d):
            bits.append(value % 2) # always LSB
            value = value >> 1

    return bytes(bits_to_bytes(bits))

def byte_decode(byte_input, d):
    """
    decodes a list of bytes into a list of integers

    Args:
        d (int): bits per coeff
        byte_input (list): 32 * d bytes
    
    Returns:
        list: integers
    """
    n = len(byte_input) * 8 // d # amount of ints to produce
    int_input = int.from_bytes(byte_input, "little") # one long int
    
    mask = (1 << d) - 1
    integers = [0] * n
    
    for i in range(n):
        value = int_input & mask # int & bit = int
        integers[i] = value
        int_input >>= d
        
    return integers

def transpose_matrix(A):
    k = len(A)
    A_t = [[None] * k for _ in range(k)]
    for row in range(k):
        for col in range(k):
            A_t[col][row] = A[row][col]
    return A_t

def compress(x, d):
    """
    calculates x ⟼ ⌈(2^d / q) ⋅ x⌋ mod 2^d

    Args:
        x (int): coeff to compress
        d (int): bit size after compression
    Returns:
        int: compressed value of bit size d in Z_2^d 
    Note:
        Reformulated to avoid floating point arithmetic
        ⌈x⌋ = ⌊x + 0.5⌋ = ⌊(2x + 1) / 2⌋
    """
    q = params.q
    return ((x * (1 << (d + 1)) + q) // (2 * q)) % (1 << d)

def compress_poly(x, d):
    """
    calculates x ⟼ ⌈(2^d / q) ⋅ x⌋ mod 2^d for all elements of the list

    Args:
        x (list): coeffs to compress
        d (int): bit size after compression
    Returns:
        list: compressed values of bit size d in Z_2^d 
    Note:
        Reformulated to avoid floating point arithmetic
        ⌈x⌋ = ⌊x + 0.5⌋ = ⌊(2x + 1) / 2⌋
    """
    x_cpy = list(x)
    for i in range(len(x)):
        x_cpy[i] = compress(x[i], d)
    return x_cpy

def decompress(y, d):
    """
    calculates y ⟼ ⌈(q / 2^d) ⋅ y⌋ 

    Args:
        y (int): coeff to decompress
        d (int): bit size after compression
    Returns:
        int: decompressed coefficient in Z_q
    Note:
        Reformulated to avoid floating point arithmetic
    """
    q = params.q
    return ((2 * q * y) + (1 << d)) // (1 << (d + 1))

def decompress_poly(y, d):
    """
    calculates y ⟼ ⌈(q / 2^d) ⋅ y⌋  for each element of the list

    Args:
        y (list): coeffs to decompress
        d (int): bit size after compression
    Returns:
        list: decompressed coeffs in Z_q
    Note:
        Reformulated to avoid floating point arithmetic
    """
    y_cpy = list(y)
    for i in range(len(y)):
        y_cpy[i] = decompress(y[i], d)
    return y_cpy
