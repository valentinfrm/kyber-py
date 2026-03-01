import params

def add(a, b):
    return (a + b) % params.q

def sub(a, b):
    return (a - b) % params.q

def mul(a, b):
    return (a * b) % params.q

def reduce(a):
    return a % params.q