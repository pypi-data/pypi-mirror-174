# written by Lukas Gessl

# a collection of routines dedicated to mediate conflicts when it comes to aligning peak tables
# based on a list of maximal cliques (cf. align_pt.py)


# PyPI
import numpy as np
from typing import List

# this package
from pt_helper import get_max_node, counts_per_node


def rm_duplicate_nodes(
    cliques: List[np.ndarray],
    similarity: np.ndarray,
    mediator: str,
    ) -> List[np.ndarray]:
    """From a list of sets of nodes, remove sets of nodes with nodes that come up in more than one set

    A helper function for merge_Pt()

    Parameters:
    -----------
    cliques: list of 1-dim int numpy arrays
        each element represents a set of nodes
    similarity: 2-dim float numpy array
        similarities between features in concatenated mz/rt values (rt_mz_all)
    mediator: str
        in ['caesar', 'solon']. Apply this method to avoid conflicts between
        cliques that include nodes that come up in more than one cliques

    Returns:
    --------
    List[np.ndarray]
        cliques where sets of nodes with nodes that come in more than one set have been removed
    """

    counts = counts_per_node(cliques)

    cliques_clear = []
    cliques_ambiguous = []
    for clique in cliques:
        if np.all(counts[clique] <= 1):
            cliques_clear.append(clique)
        else:
            cliques_ambiguous.append(clique)

    def sim_score(clique):
        sc = 0
        for node_i in clique:
            for node_j in clique:
                if node_i < node_j:
                    sc += similarity[node_i, node_j]
        return sc
    
    cliques_ambiguous.sort(key = sim_score, reverse = True)
    sim_scores = np.zeros(len(cliques_ambiguous))
    for i, clique in enumerate(cliques_ambiguous):
        sim_scores[i] = sim_score(clique)

    if mediator == "solon":
        mediator_func = solon
    elif mediator == "caesar":
        mediator_func = caesar
    else:
        raise ValueError("conflict_solver must be in ['caesar', 'maximizing_set']")
    cliques_clear += mediator_func(cliques_ambiguous, sim_scores)

    # check if every node comes up at most once
    if not np.all(counts_per_node(cliques_clear) <= 1):
        print("There is a problem with mediation! Maday, mayday, mayday!")

    return cliques_clear


def caesar(
    cliques_ambiguous: List[np.ndarray],
    sim_scores: np.ndarray
    ) -> List[np.ndarray]:
    """Solve conflicts by hierachically liquidating cliques in conflict with higher-ranking cliques
    
    Arguments:
    ----------
    cliques_ambiguous: list of 1-dim int numpy arrays
        each array holds the nodes (i.e. indices) of a clique. Cliques are ordered descending by clique
        score
    sim_scores: 1-dim float numpy array
        clique similarity scores corresponding to cliques in cliques_ambiguous
        
    Returns:
    --------
    list of 1-dim integer numpy arrays
        an optimized set of cliques free of conflicts"""
    
    max_node = get_max_node(cliques_ambiguous)

    # dict: for every node, cliques (indices) that host this node
    nodes_n_cliques = {i : [] for i in range(max_node + 1)}
    for i, clique in enumerate(cliques_ambiguous):
        for node in clique:
            nodes_n_cliques[node].append(i)

    survivors = []
    alive = np.ones(len(cliques_ambiguous), dtype = int)
    for i, clique in enumerate(cliques_ambiguous):
        if alive[i] == 0:
            continue
        survivors.append(clique)
        for node in clique:
            for hosting_clique in nodes_n_cliques[node]:
                alive[hosting_clique] = 0

    return survivors


def solon(
    cliques_ambiguous: List[np.ndarray],
    sim_scores: np.ndarray
    ) -> List[np.ndarray]:
    """Solve conflicts by heuristcally finding an as-large-as-possible subset free of conflicts
    
    Arguments:
    ----------
    cliques_ambiguous: list of 1-dim int numpy arrays
        each array holds the nodes (i.e. indices) of a clique. Cliques are ordered descending by clique
        score
    sim_scores: 1-dim float numpy array
        clique similarity scores corresponding to cliques in cliques_ambiguous
    max_node: int
        an upper bound for the node with the highest number in the cliques of cliques_ambiguous
        
    Returns:
    --------
    list of 1-dim integer numpy arrays
        an optimized set of cliques free of conflicts
    """

    max_node = get_max_node(cliques_ambiguous)

    maximizing_set = []
    high_score = 0

    # heuristic to find a subset of cliques_ambiguous without conflicts
    for i, base_clique in enumerate(cliques_ambiguous):
        counts = np.zeros(max_node + 1)
        counts[base_clique] += 1
        cur_score = sim_scores[i]
        cur_set = [base_clique]
        for j, cand_clique in enumerate(cliques_ambiguous):
            if np.all(counts[cand_clique] == 0):
                counts[cand_clique] += 1
                cur_score += sim_scores[j]
                cur_set.append(cand_clique)
        if cur_score > high_score:
            high_score = cur_score
            maximizing_set = cur_set

    return maximizing_set