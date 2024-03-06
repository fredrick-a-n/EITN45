import numpy as np
import matplotlib.pyplot as plt

def bit_flip_decode(r: np.ndarray, H: np.ndarray, imax = 100, should_print=False) -> np.ndarray:
    v_hat = np.copy(r)
    for i in range(imax):
        if should_print:
            print(f"v_hat at iteration {i}: {v_hat}")
        # Calculate syndrome
        syndrome = H.dot(v_hat) % 2
        if should_print:
            print(f"Syndrome at iteration {i}: {syndrome}")

        # If syndrome is 0, then the code is correct so we break the loop
        if all(x == 0 for x in syndrome):
            if should_print:
                print(f"No errors detected at iteration {i}. Decoding complete.")
            return v_hat

        # Compute number of invalid syndromes per codebit
        sigma = syndrome.dot(H)
        if should_print:
            print(f"Sigma at iteration {i}: {sigma}")

        # Flipping the bits with the highest number of invalid syndromes
        max = np.max(sigma)
        for i in range(len(sigma)):
            if sigma[i] == max:
                v_hat[i] = v_hat[i] ^ 1
    if should_print:
        print(f"Maximum iterations reached. Decoding may not be complete.")
    return v_hat


def array_from_file(filename: str) -> np.ndarray:
    data = []
    with open(filename, 'r') as file:
        for line in file:
            numbers = [int(num) for num in line.split()]
            data.append(numbers)
    
    ndarray = np.array(data)
    
    return ndarray

def bitarray_to_string(bitarray: np.ndarray) -> str:
    reshaped_array = np.reshape(bitarray, (len(bitarray) // 8, 8))

    bytes_array = np.packbits(reshaped_array, axis=-1)

    return ''.join([chr(byte) for byte in bytes_array.flatten()])


if __name__ == '__main__':

    # Part 1
    parity_matrix = np.array([[1, 1, 0, 0, 0, 0, 0],
                              [0, 1, 1, 0, 0, 0, 0],
                              [0, 1, 1, 1, 1, 0, 0],
                              [0, 0, 0, 1, 1, 0, 0],
                              [0, 0, 0, 0, 1, 1, 0],
                              [0, 0, 0, 0, 1, 0, 1]])
    bitvec = np.array([0, 1, 0, 0, 1, 0, 0])
    print("Part 1:")
    print(bit_flip_decode(bitvec, parity_matrix, should_print=True))

    # Part 2
    parity_matrix = array_from_file("H_1024_3_6.txt")
    bitvec = array_from_file("ChannelOutputBinary.txt")
    bitarray = bit_flip_decode(bitvec[0], parity_matrix)
    bitarray = bitarray[:512]
    with open("DecodedMessage.txt", 'w') as file:
        file.write(bitarray_to_string(bitarray))
    print("Part 2:")
    print(bitarray_to_string(bitarray))