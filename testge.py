import numpy as np

def GEPP(A, b, doPricing = True):
    '''
    Gaussian elimination with partial pivoting.
    
    input: A is an n x n numpy matrix
           b is an n x 1 numpy array
    output: x is the solution of Ax=b 
            with the entries permuted in 
            accordance with the pivoting 
            done by the algorithm
    post-condition: A and b have been modified.
    '''
    n = len(A)
    if b.size != n:
        raise ValueError("Invalid argument: incompatible sizes between"+
                         "A & b.", b.size, n)
    # k represents the current pivot row. Since GE traverses the matrix in the 
    # upper right triangle, we also use k for indicating the k-th diagonal 
    # column index.
    
    # Elimination
    for k in range(n-1):
        if doPricing:
            # Pivot
            maxindex = abs(A[k:,k]).argmax() + k
            if A[maxindex, k] == 0:
                raise ValueError("Matrix is singular.")
            # Swap
            if maxindex != k:
                A[[k,maxindex]] = A[[maxindex, k]]
                b[[k,maxindex]] = b[[maxindex, k]]
        else:
            if A[k, k] == 0:
                raise ValueError("Pivot element is zero. Try setting doPricing to True.")
        #Eliminate
        for row in range(k+1, n):
            multiplier = A[row,k]/A[k,k]
            A[row, k:] = A[row, k:] - multiplier*A[k, k:]
            b[row] = b[row] - multiplier*b[k]
    # Back Substitution
    x = np.zeros(n)
    for k in range(n-1, -1, -1):
        x[k] = (b[k] - np.dot(A[k,k+1:],x[k+1:]))/A[k,k]
    return x

def g_elim(a, b):
    n = b.shape[0]
    for k in range(0,n-1):
        for i in range(k+1,n):
            if a[i,k] != 0.0:
                lam = a [i,k]/a[k,k]
                a[i,k+1:n] = a[i,k+1:n] - lam*a[k,k+1:n]
                b[i] = b[i] - lam*b[k]
    for k in range(n-1,-1,-1):
        b[k] = (b[k] - np.dot(a[k,k+1:n],b[k+1:n]))/a[k,k]
    
    return b

def wtf(A):
    m = len(A)
    n = m + 1
    
    for k in range(m):
        pivots = [abs(A[i][k]) for i in range(k, m)]
        i_max = pivots.index(max(pivots)) + k
        
        # assert A[i_max][k] != 0, "Matrix is singular!"
        
        A[k], A[i_max] = A[i_max], A[k]
        
        for i in range(k + 1, m):
            f = A[i][k] / A[k][k]
            for j in range(k + 1, n):
                j = j - 1
                print(f)
                A[i][j] -= A[k][j] * f
            A[i][k] = 0
    
    x = []
    for i in range(m - 1, -1, -1):
        m = m - 1
        x.insert(0, A[i][m] / A[i][i])
        for k in range(i - 1, -1, -1):
            A[k][m] -= A[k][i] * x[0]
    return x

if __name__ == "__main__":
    A = np.array([[1.,-1.,1.,-1.],[1.,0.,0.,0.],[1.,1.,1.,1.],[1.,2.,4.,8.]])
    b =  np.array([[14.],[4.],[2.],[2.]])
    # print('A', A)
    # print('b', b)
    # print('---------------')
    # print(GEPP(np.copy(A), np.copy(b), doPricing = False))
    # print('---------------')
    # print(GEPP(A,b))
    # print('---------------')
    # print(g_elim(A,b))
    # print('---------------')
    print('a shape', A.shape)
    print('elim a', wtf(A))

    print('-------')
    t = np.array(
        [[-1,  1,  1,  0,  0, 11],
         [ 1,  1,  0,  1,  0, 27],
         [ 2,  5,  0,  0,  1, 90],
         [-4, -6,  0,  0,  0,  0]]
    )
    print('t shape', t.shape)
    print('elim t', wtf(t))
