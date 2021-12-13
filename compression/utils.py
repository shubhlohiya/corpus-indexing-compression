import numpy as np
np.random.seed(123)

def unary_encoding(n):
    """Returns unary encoding of input n."""
    return '1'*n + '0'

def binary_encoding(n, l):
    """Returns binary encoding of input n padded to length l."""
    return '' if l==0 else format(n, f'0{l}b')

def gamma_encoding(n):
    """Returns gamma encoding of input n."""
    if n == 0: return '0'
    x = int(np.log2(n))
    return unary_encoding(x) + binary_encoding(n - 2**x, x)

def fixed_prefix_code(r, m):
    """Returns fixed_prefix_code for r with choice m for golomb encoding."""
    l = int(np.log2(m))
    assert r < m, "r must be less than m"
    if l==0 : return ''
    temp = 2**(l+1) - m
    if 0 <= r < temp:
        return format(r, f'0{l}b')
    else:
        return format(r + temp, f'0{l+1}b')
    
def golomb_encoding(n, m):
    """Returns golomb encoding of input n with hyperparameter choice m."""
    q = n // m
    r = n % m
    return unary_encoding(q) + fixed_prefix_code(r, m)

def get_dgap_cumulative_dist(dgap_counts):
    """Returns a cumulative distribution over digits that occur in dgaps of the corpus."""
    pmf = np.zeros(10)
    for gap, count in dgap_counts.items():
        for sym in str(gap):
            pmf[int(sym)] += count
    pmf = pmf / np.sum(pmf)
    cdf = np.cumsum(pmf)
    return cdf

def shrink_interval(cdf, low, high, sym):
    """Shrinks interval to incorporate current sym's contribution to the arithmetic code."""
    sym = int(sym)
    lower_bound = 0 if sym == 0 else cdf[sym-1]
    higher_bound = cdf[sym]
    rng = high - low
    new_low = low + rng * lower_bound
    new_high = low + rng * higher_bound
    return new_low, new_high

def arithmetic_encoding(n, cdf):
    """Returns arithmetic encoding of input n given the cdf."""
    low, high = 0., 1.
    for sym in str(n):
        low, high = shrink_interval(cdf, low, high, sym)
    return np.random.uniform(low, high) # Not converting to binary for this assignment