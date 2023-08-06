# written by Lukas Gessl

# function that are accessed by several scripts

# PyPI
from typing import List
import numpy as np
import networkx as nx
import pandas as pd

# this package
from peaktable import Peaktable


def extract_rt_mz(Pt_list: List[Peaktable]):
    """Extract retention times and mz values from multiple peak tables intended for alignment and concatenate them
    
    Parameters:
    -----------
    Pt_list: List[Peaktable]

    Returns:
    --------
    tuple of two
        (1) a 2-dim float numpy array with retention times (0-th column) and mz values (1st column) from all peak tables (beginning with 0-th
        peak table in Pt_list, then 1st peak table and so on, order is preserved)
        (2) a 1-dim int numpy array of length len(Pt_list) + 1. The indices belonging to the i-th peak table of Pt_list span the row indices
        index_split[i] to index_split[i + 1] (excluded) in (1)
    """
    
    rt_mz_list = []
    for Pt in Pt_list:
        rt_mz_list.append(np.concatenate([Pt.rt[:, np.newaxis], Pt.mz[:, np.newaxis]], axis = 1))

    rt_mz_all = np.concatenate(rt_mz_list, axis = 0) # abundances don't matter for the alignment (for now)
    index_split = np.zeros(len(rt_mz_list) + 1, dtype = int) # keep track of single peak tables in the aggregated array
    for i, Pt in enumerate(Pt_list):
        index_split[i + 1] = index_split[i] + Pt.shape[0]

    return rt_mz_all, index_split


def find_cliques_max_k(
    network,
    k
    ) -> List[np.ndarray]:
    """Find all (maximal) cliques of size k in a given undirected network where every node has at most k neighbors
    
    Parameters:
    -----------
    network: 2-dim integer numpy array
        network in matrix representation (1 indicates an edge between two nodes, 0 no edge)
    k: int
        every node in network is connected to at most k other nodes

    Returns:
    --------
    list of 1-d numpy arrays
        every array holds the nodes of one maximal clique of size k
    """

    start_nodes = network.nonzero()
    max_cliques = []
    for i in range(len(start_nodes[0])):
        if start_nodes[0][i] == -1: # link is already part of a maximal clique of size len(pt_list)
            continue
        i_node = start_nodes[0][i] # first node
        j_node = start_nodes[1][i] # second node
        if i_node >= j_node: # bbhs matrix is symmetric
            continue
        j_index = network[i_node, :].nonzero()[0]
        j_index.sort()
        i_index = network[:, j_node].nonzero()[0]
        i_index.sort()
        # some pre-filtering
        if len(i_index) + len(j_index) < 2*k or network[i_node, :] @ network[:, j_node].T < k:
            continue
        # check if all nodes are connected to each other
        n_ones = 0
        for l in i_index:
            for m in j_index:
                n_ones += network[l, m]
        if n_ones == k**2:
            max_cliques.append(i_index)
            # a node can come up in at most one maximal clique of size len(pt_list)
            # therefore, it is not worth investigating any BBH with any of the nodes
            # that are part of the clique we just found involved
            for j in range(i, len(start_nodes[0])):
                if (start_nodes[0][j] in i_index) or (start_nodes[1][j] in i_index):
                    start_nodes[0][j] = -1

    return max_cliques


def find_max_cliques(
    network: np.ndarray,
    k_min: int
    ) -> List[np.ndarray]:
    """Find all maximal cliques comprising at least k_min nodes
    
    Arguments:
    ----------
    network: 2-dim int numpy array
        network in matrix representation
    k_min: int
        only report maximal cliques with at least k_min member nodes
        
    Returns:
    List[np.ndarray]
        each 1-dim int numpy array holds a maximal clique
    """

    network = nx.from_numpy_matrix(network)
    max_cliques = nx.find_cliques(network)
    cliques = []
    for clique in max_cliques:
        size = len(clique)
        if size >= k_min:
            cliques.append(np.array(clique, dtype = int))

    return cliques


def clique_overview(
    cliques: List[np.ndarray]
    ) -> None:
    """Print an overview on clique sizes
    
    Arguments:
    cliques: list of 1-dim int numpy arrays
    """

    max_clique_size = len(max(cliques, key = lambda x: x.size))
    min_clique_size = len(min(cliques, key = lambda x: x.size))

    counts = np.zeros(max_clique_size - min_clique_size + 2, dtype = int)
    for clique in cliques:
        counts[clique.size - min_clique_size] += 1
    counts[-1] = counts.sum()
    columns = ["size " + str(i) for i in range(min_clique_size, max_clique_size + 1)]
    columns.append("total")
    df = pd.DataFrame(counts[np.newaxis, :], columns = columns, index = ["#"])
    print(df)


def get_max_node(cliques: List[np.ndarray]) -> int:
    """Get the maximum node index of all the nodes held by the cliques

    Arguments:
    ----------
    cliques: list of 1-dim int numpy arrays

    Returns:
    --------
    int
        maximum node index
    """

    return max(max(cliques, key = max))


def counts_per_node(cliques: List[np.ndarray]) -> np.ndarray:
    """Report how often every node comes up in cliques
    
    Arguments:
    ----------
    cliques: list of 1-d int numpy arrays

    Returns:
    1-dim int numpy array
        i-th entry encodes in how many cliques node i comes up
    """


    max_node = get_max_node(cliques)

    counts = np.zeros(max_node + 1)
    for clique in cliques:
        counts[clique] += 1

    return counts