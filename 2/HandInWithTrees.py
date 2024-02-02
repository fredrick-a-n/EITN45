from collections import Counter
from bitarray import bitarray
import numpy as np
from totree import printBTree
from treevisualization import visualize_binary_tree
from node import Node

INPUT_PATH = 'Alice29.txt'
COMPRESSED_PATH = 'compressed'
DECOMPRESSED_PATH = 'decompressed.txt'


def read_data(path):
    # Output:
    #   data: file as array of raw bytes
    if isinstance(path, str):
        data = []
        with open(path, 'rb') as f:
            for byte in f.read():
                data.append(byte.to_bytes(1, byteorder='big'))
        return data
    else:
        raise TypeError('Input must be a string')


def print_to_file(data, path):
    # Input:
    #   data: bytes to print
    #   path: string with the path to the file
    # print(type(data))
    # print(type(path))
    if isinstance(data, bytes) and isinstance(path, str):
        with open(path, 'wb') as f:
            f.write(data)
    else:
        raise TypeError('Input must be bytes and a string')


def huffman_tree(occurrences):
    # Input:
    #  occurrences: dictionary with the number of occurrences of each symbol
    # Output:
    #   root: the root of the Huffman tree
    if isinstance(occurrences, dict):
        probabilities = sorted([(key, value)
                                for (key, value) in occurrences.items()], key=lambda x: x[1])
        while len(probabilities) > 1:
            left = probabilities.pop(0)
            right = probabilities.pop(0)
            node = Node(left[0], right[0])
            probabilities.append((node, left[1]+right[1]))
            probabilities = sorted(probabilities, key=lambda x: x[1])
        return probabilities.pop(0)[0]
    else:
        raise TypeError('Input must be a dictionary')


def codebook(node, code=''):
    # Input:
    #   root: the root of the Huffman tree
    #   code: the code for the current node
    # Output:
    #   codebook: a dictionary with the Huffman code for each symbol
    if isinstance(node, Node):
        book = {}
        (left, right) = node.children()
        book.update(codebook(left, code+'0'))
        book.update(codebook(right, code+'1'))
        return book
    elif isinstance(node, bytes):
        return {node: code}
    elif node is None:
        return {}
    else:
        print(type(node))
        raise TypeError('Input must be a Node')


def compress(data, codebook):
    # Input:
    #   data: list of bytes with the data to compress
    #   codebook: a dictionary with the Huffman code for each byte
    # Output:
    #   compressed_data: bytes with the compressed data
    if isinstance(data, list) and isinstance(codebook, dict):
        s = ''
        for symbol in data:
            s += (codebook[symbol])

        # If the compressed data is not a multiple of 8, it will add dummy bits to make it a multiple of 8
        # Select dummy bits so that they match no code in the codebook
        # If it doesn't find any unused bit combination in 2^l attempts, it will simply fill it with zeroes which might add additional characters on decompression  
        if len(s) % 8 != 0:
            l = (8-len(s) % 8)
            inv_codebook = {value: key for key, value in codebook.items()}
            for _ in range(pow(2, l)):
                dummy_bits = ''.join(str(element) for element in [np.random.choice([0, 1]) for i in range(l) ])
                if any([inv_codebook.get(dummy_bits[0:i]) is not None for i in range(0, len(dummy_bits))]):
                    continue
                else:
                    s += dummy_bits
                    break
        compressed_data = bitarray(s).tobytes()
        return compressed_data
    else:
        raise TypeError('Input must be a list and a dictionary')


def decompress(compressed_data, codebook):
    # Input:
    #   compressed_data: list of bytes with the data to decompress
    #   codebook: a dictionary with the Huffman code for each byte
    # Output:
    #   data: bytes with the decompressed data
    if isinstance(compressed_data, list) and isinstance(codebook, dict):
        data = bytes()
        codebook = {value: key for key, value in codebook.items()}
        compressed_data = b''.join(compressed_data)
        s = bitarray()
        s.frombytes(compressed_data)
        s = s.to01()
        i = 0
        while i < len(s):
            j = i+1
            while s[i:j] not in codebook.keys() and j < len(s):
                j += 1
            if j < len(s)-1:
                data += (codebook[s[i:j]])
            elif j == len(s) and s[i:j] in codebook.keys():
                data += (codebook[s[i:j]])
            i = j
        return data
    else:
        raise TypeError('Input must be a list and a dictionary')


if __name__ == '__main__':

    # COMPRESS
    data = read_data(INPUT_PATH)
    occurrences = Counter(data)
    root = huffman_tree(occurrences)
    codebook = codebook(root)
    compressed_data = compress(data, codebook)

    # DECOMPRESS    
    compressed = read_data(COMPRESSED_PATH)
    decompressed = decompress(compressed, codebook)
    print_to_file(decompressed, DECOMPRESSED_PATH)

    # tree = printBTree(root, lambda node: (node.zero, node.one), False, True)
    # visualize_binary_tree(root, codebook)
    # with open('tree.txt', 'w') as f:
    #     f.write(tree)
