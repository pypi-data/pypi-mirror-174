# written by Lukas Gessl

# similarity (between features) functions for Peaktable_align.align()

def std_similarity(p, q, rt_tol, mz_tol):
    """Calculate similarity between two features. The higher the returned value, the more
    similar

    Parameters
    ----------
    p, q: 1-d float numpy arrays of length 2
        first entry is retention time of a feature, second entry is its mz value
    rt_tol, mz_tol: float
        see combine_pt()

    Returns
    -------
    float
        similarity between feature p and q
    """

    import numpy as np

    if np.abs(p[0] - q[0]) > rt_tol or np.abs(p[1] - q[1]) > mz_tol:
        return 0
    
    return (rt_tol - np.abs(p[0] - q[0]))/rt_tol * np.exp(-(p[1] - q[1])**2 / (2 * mz_tol**2))