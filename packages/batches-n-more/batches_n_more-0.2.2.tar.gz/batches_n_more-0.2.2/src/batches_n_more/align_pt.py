# written by Lukas Gessl

# outsourced code for Peaktable_align.align() method


# PyPI
from typing import List
import numpy as np

# this package
from .peaktable import Peaktable
from .pt_helper import find_max_cliques, extract_rt_mz, clique_overview
from .clique_mediator import rm_duplicate_nodes


def align_pt(
    Pt_list: List[Peaktable],
    similarity_func: callable,
    k_min: int,
    mediator: str,
    rt_tol: float = 0.25,
    mz_tol: float = 0.003,
    verbose: bool = True
    ) -> Peaktable:
    """Align multiple peak tables (usually from different batches) into one peak table
    
    Parameters:
    -----------
    Pt_list: list of Peaktable objects
    similarity_func: function
        argument list and return type as in similarity_functions.py
    k_min: int
        minimum number of batches from which every feature in resulting aligned peak table is constructed
    mediator: str
        in ['caesar', 'solon']. Method to apply if multiple cliques include the same node
    rt_tol: float
        maximum tolerance of retention time so that two features from different peak tables (i.e. samples) can
        be aligned into one feature. Note that need to use the same unit as in the peak tables.
        Defaults to 0.25 (minutes). 
    mz_tol: float
        analogon of rt_tol for mz values. Defaults to 0.003.
    verbose: bool

    Returns:
    --------
    Peaktable object
        merged peak table
    """

    rt_mz_all, index_split = extract_rt_mz(Pt_list)

    # calculate similarities
    similarity = np.zeros(shape = (len(rt_mz_all), len(rt_mz_all)))
    for pt_index in range(len(Pt_list)):
        start_i = index_split[pt_index]
        stop_i = index_split[pt_index + 1] # use symmetry of similarity
        for i in range(start_i, stop_i):
            for j in range(0, start_i): # we need not calculate within-batch similarity
                similarity[i, j] = similarity_func(rt_mz_all[i, :], rt_mz_all[j, :], rt_tol, mz_tol)
    similarity += similarity.T

    # for every peak and peak table, find best corresponding counterpart in the peak table
    best_hits = np.zeros(shape = similarity.shape, dtype = int)
    for j in range(len(Pt_list)):
        arg_max = np.argmax(similarity[:, index_split[j]:index_split[j + 1]], axis = 1)
        for i in range(best_hits.shape[0]):
            best_hits[i, index_split[j] + arg_max[i]] = 1
    # we now have also written into the squares along the diagonal belonging to intra-batch best hits
    # annulate that
    for j in range(len(Pt_list)):
        start = index_split[j]
        stop = index_split[j + 1]
        best_hits[start:stop, start:stop] = 0
    
    # bidirectional best hits
    bbhs = best_hits * best_hits.T
    bbhs += np.diag(np.ones(bbhs.shape[0], dtype = int))

    max_cliques = find_max_cliques(bbhs, k_min)

    if verbose:
        print("Overview on clique sizes BEFORE removing duplicates")
        clique_overview(max_cliques)

    max_cliques = rm_duplicate_nodes(max_cliques, similarity, mediator = mediator)

    if verbose:
        print("Overview on clique sizes AFTER removing duplicates")
        clique_overview(max_cliques)

    # merge peak tables
    Pt_merge = merge_Pt(max_cliques, Pt_list, index_split, verbose = verbose)

    Pt_merge.sort()

    return Pt_merge


# functions outsourced from combine_pt()

def merge_Pt(
    max_cliques: List[np.ndarray],
    Pt_list: List[Peaktable],
    index_split: np.ndarray,
    verbose
    ) -> Peaktable:
    """Based on a list of maximal cliques FREE OF CONFLICTS, merge multiple 
    peak tables into one peak table
    
    Parameters:
    -----------
    max_cliques: list of 1-d numpy arrays
        as returned by find_cliques()
    pt_list: list of Peaktable objects
    index_split: 1-d numpy array
        link between features in max_cliques and pt_list. Entry i is the lowest, entry i+1 is the 
        highest index of the features from the i-th peak table in pt_list
    verbose: bool

    Returns:
    --------
    Peaktable object
        merged peak tables
    """

    sample_names_merge = [sample_name for Pt in Pt_list for sample_name in Pt.sample_names]

    # mapping for columns between single feature tables and merged feature table
    sample_index_split = np.zeros(len(Pt_list) + 1, dtype = int)
    for i, Pt in enumerate(Pt_list):
        sample_index_split[i + 1] = sample_index_split[i] + Pt.shape[1]

    # qc columns for merged peak table
    new_qc_cols = [Pt.qc_samples + sample_index_split[i] for i, Pt in enumerate(Pt_list)]
    new_qc_cols = np.concatenate(new_qc_cols, axis = 0)

    # a modfied version of index_split for reverse mapping
    index_split_rev = np.zeros(len(Pt_list), dtype = int)
    index_split_rev[:] = index_split[:-1]
    index_split_rev[0] = index_split[-1]

    # merge actual peak tables
    pt_merge = np.zeros(shape = (len(max_cliques), sample_index_split[-1]))
    mz_merge = np.zeros(len(max_cliques))
    rt_merge = np.zeros(len(max_cliques))
    for i, clique in enumerate(max_cliques):
        original_index = -np.ones(len(Pt_list), dtype = int) # will hold indices for features in orginal peak tables (or batches)
        for node in clique:
            for j in range(len(Pt_list)):
                if index_split[j] <= node and node < index_split[j + 1]:
                    original_index[j] = node % index_split_rev[j]
                    break

        rts = np.zeros(len(Pt_list))
        mzs = np.zeros(len(Pt_list))
        for j, oi in enumerate(original_index):
            start = sample_index_split[j]
            stop = sample_index_split[j + 1]
            rts[j] = np.nan if oi < 0 else Pt_list[j].rt[oi]
            mzs[j] = np.nan if oi < 0 else Pt_list[j].mz[oi]
            pt_merge[i, start:stop] = np.nan if oi < 0 else Pt_list[j].pt[oi, :]
        rt_merge[i] = np.nanmean(rts)
        mz_merge[i] = np.nanmean(mzs)

    # replace NaNs with quasi-zero
    _na_bool = np.isnan(pt_merge)
    pt_merge[_na_bool] = np.nanmin(pt_merge)/10.

    # infer batches
    samples_per_ft = np.zeros(len(Pt_list), dtype = int)
    for i in range(len(samples_per_ft)):
        samples_per_ft[i] = Pt_list[i].shape[1]
    batches = np.repeat(np.arange(len(Pt_list)), repeats = samples_per_ft)

    Pt_merge = Peaktable(
        pt = pt_merge, 
        mz = mz_merge, 
        rt = rt_merge, 
        sample_names = sample_names_merge, 
        qc_samples = new_qc_cols,
        batches = batches,
        _na_bool = _na_bool
        )

    if verbose:
        print("Aligned peak table has shape", Pt_merge.shape)

    return Pt_merge