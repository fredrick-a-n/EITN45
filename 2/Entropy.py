import numpy as np
class InfoTheory:
    def Entropy(self,P):
        # Input P:
        #   Matrix (2-dim array): Each row is a probability
        #       distribution, calculate its entropy,
        #   Row vector (1Xm matrix): The row is a probability
        #       distribution, calculate its entropy,
        #   Column vector (nX1 matrix): Derive the binary entropy
        #       function for each entry,
        #   Single value (1X1 matrix): Derive the binary entropy
        #       function
        # Output:
        #   array with entropies
        if isinstance(P, np.ndarray):
            if P.shape == (1,) or P.shape == (1, 1):
                # If solo value in array, send solo value to get into float option
                return self.Entropy(P[0])
            elif len(P.shape) == 1:
                # If single row vector with several elements, calculate entropy
                return -np.sum(P * np.log2(P, where=P != 0))
            else:
                # If several rows, calculate entropy for each row
                return np.array([self.Entropy(row) for row in P])
        elif isinstance(P, float):
            # If solo value, derive the binary entropy
            return -(P * np.log2(P, where=P != 0) + (1 - P) * np.log2(1 - P, where=(1 - P) != 0))
        else:
            raise ValueError("Invalid value for P")

    def MutualInformation(self,P):
        # Derive the mutual information I(X;Y)
        # Input P: P(X,Y)
        # Output: I(X;Y)
        if isinstance(P, np.ndarray):
            # H(X) + H(Y) - H(X,Y)
            # Calculate P(x) and P(y)
            px = np.transpose(np.sum(P, axis=1, keepdims=True))
            py = np.sum(P, axis=0, keepdims=True)
            # Calculate H(X), H(Y) and H(X,Y)
            hx = self.Entropy(px)
            hy = self.Entropy(py)
            hxy = np.sum(self.Entropy(P))
            return hx + hy - hxy
        else:
            raise ValueError("Invalid value for P")

if __name__=='__main__':
    ### init
    IT = InfoTheory()
    ### 1st test
    P1 = np.transpose(np.array([np.arange(0.0,1.1,0.25)]))# column vector
    H1 = IT.Entropy(P1)
    print('H1 =',H1)
    ### 2nd test
    P2 = np.array([[0.3, 0.1, 0.3, 0.3],
    [0.4, 0.3, 0.2, 0.1],
    [0.8, 0.0, 0.2, 0.0]])
    H2 = IT.Entropy(P2)
    print('H2 =',H2)
    ### 3rd test
    P3 = np.array([[0, 3/4],[1/8, 1/8]])
    I3 = IT.MutualInformation(P3)
    print('I3 =',I3)
    ### 4th test
    P4 = np.array([[1/12, 1/6, 1/3],
    [1/4, 0, 1/6]])
    I4 = IT.MutualInformation(P4)
    print('I4 =',I4)

# Supposed Output:
# H1 = [-0. 0.81127812 1. 0.81127812 -0. ]
# H2 = [1.89546184 1.84643934 0.72192809]
# I3 = [0.29356444]
# I4 = [0.2502948]
