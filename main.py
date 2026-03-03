import sampling

def main():
    result = sampling.sample_poly_shake(bytes(32) + bytes([0]) + bytes([0]))
    print(result.coeff)


if __name__ == "__main__":
    main()
