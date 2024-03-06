import numpy as np
import matplotlib.pyplot as plt
from handin12 import bit_flip_decode, array_from_file, bitarray_to_string
from progress.bar import Bar
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

# Parameters
n = 1024  # Length of the codeword
k = 512   # Length of the message
R = k / n  # Code rate
numBlocks = 10000  # Number of blocks to transmit

# Channel error probabilities
pvec = np.array([0.01, 0.02, 0.03, 0.04, 0.06, 0.08, 0.1])
print (len(pvec))
# Initialize error counters
biterrors = np.zeros(len(pvec))
numbits = np.zeros(len(pvec))
blockerrors = np.zeros(len(pvec))

imax = 25
H = array_from_file("H_1024_3_6.txt")

lock = threading.Lock()

with Bar('Processing', max=len(pvec) * numBlocks) as bar:
    def simulate_epsilon(indp, p):
        for _ in range(numBlocks):
            # Simulate channel errors
            errors = np.random.rand(n) < p
            r = errors.astype(int)  # Received vector, all-zero codeword + errors
            print(r)
            vhat = bit_flip_decode(r, H, imax=imax, should_print=False)

            # Count errors
            errorpositions = (vhat != 0)  # Since v is all-zero
            biterrors[indp] += np.sum(errorpositions)
            blockerrors[indp] += np.any(errorpositions)
            numbits[indp] += n
            with lock:
                bar.next()

    with ThreadPoolExecutor(max_workers=np.max([len(pvec), 8])) as executor:
        for indp, p in enumerate(pvec):
            executor.submit(simulate_epsilon, indp, p)

# Calculate error probabilities
Pb = biterrors / numbits
Pblock = blockerrors / numBlocks

# Plot results
plt.figure()
plt.semilogy(pvec, Pblock, '-o', label='P_B')
plt.semilogy(pvec, Pb, '-x', label='P_b')
plt.semilogy(pvec, pvec, '--', label='uncoded')
plt.xlabel('$\epsilon$')
plt.ylabel('$P_b / P_B$')
plt.grid(True)
plt.legend()
plt.show()