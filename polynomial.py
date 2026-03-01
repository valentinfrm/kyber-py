import params
from field import *

class poly:
    """Polynomial in Rq = Zq[x]/(x^n + 1)"""
    def __init__(self, coeff):
        self.coeff = coeff
        self.k = len(self.coeff)


    def poly_add(self, poly_b):
        for i in range(self.k):
            self.coeff[i] = add(self.coeff[i], poly_b.coeff[i])


    def poly_sub(self, poly_b):
        for i in range(self.k):
            self.coeff[i] = sub(self.coeff[i], poly_b.coeff[i])

    
    def poly_mul(self, poly_b):
        """multiply using negacyclic convolution -> NTT later"""
        tmp = list(self.coeff) # copy coeffs to avoid overwriting while reading
        for row in range(self.k):
            c = 0
            for col in range(self.k): 
                og_index = (row - col) % params.n # index in original poly (wraps around negacyclically)
                v = mul(tmp[og_index], poly_b.coeff[col])
                if col > row:
                    v = -v # negate when index wrapped around (x^n = -1)
                c += v
            self.coeff[row] = reduce(c)
        
        
    def poly_reduce(self):
        for i in range(len(self.coeff)):
            self.coeff[i] = reduce(self.coeff[i])