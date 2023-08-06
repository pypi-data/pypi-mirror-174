# written by Lukas Gessl

# PyPI
import numpy as np
import pandas as pd
from typing import List, Tuple
import plotnine as p9
import os

# this package
from align_pt import align_pt
from peaktable import Peaktable
from pt_helper import find_cliques_max_k, extract_rt_mz
from similarity_func import std_similarity
from scipy.interpolate import CubicSpline, PPoly


class Peaktable_align:
    """Starting from a list of Peaktable objects, find anchors and empower them to correct
    for between-batch retention-time and mz-value shift
    
    ...

    Attributes:
    -----------
    Pt_list: List[Peaktable]
        peak tables to be aligned, usually multiply batches of the same experiment
    _rt_anchors: 2-dim float numpy array
        anchors in rows. Therefore, every column represents one peak table in Pt_list
    _mz_anchors: 2-dim float numpy array
        analogon for mz values
    _rt_inter: List[PPoly]
        result of interpolate() method
    _mz_inter: List[PPoly]
        analogon for mz values

    Methods:
    --------

    interpolate()
        for every peak table in Pt_list, interpolate retention times of anchor features against
        those of the first feature table. Do the same for mz values. This yields _rt_inter,
        _mz_inter
    correct_rt()
        correct retention times with the help of _rt_inter
    correct_mz()
        correct mz values with the help of _mz_inter
    """

    def __init__(
        self, 
        Pt_list: List[Peaktable],
        mz_tol: float,
        rt_tol: float
        ) -> None:
        """
        Arguments:
        ---------
        Pt_list: List[Peaktable]
            peak tables to be aligned, usually multiply batches of the same experiment
        """

        self.Pt_list = Pt_list
        self.mz_tol = mz_tol
        self.rt_tol = rt_tol
        self.rt_anchors = None
        self.mz_anchors = None
        self._rt_inter = None # List[PPoly]
        self._mz_inter = None # List[PPoly]


    def find_anchors(self, verbose: bool = True) -> None:
        """For the peak tables in the Pt_list attribute, find features that can uniqely be 
        associated with each other, so-called anchors. Write them into rt_anchors, mz_anchors
        attributes

        Anchors enable retention-time correction

        Arguments:
        ----------
        Pt_list: List[Peaktable]
            contains the peaktables intended to be merged
        verbose: bool
            defaults to True
        """

        self.rt_anchors, self.mz_anchors = find_anchors_(
            self.Pt_list, 
            self.rt_tol, 
            self.mz_tol,
            verbose = verbose
            )


    def plot_shift(self, rt_or_mz: str, filepath: str = None) -> p9.ggplot:
        """For either retention times or mz values, plot each anchor value against its counterpart
        in the first peak table
        
        Arguments:
        ----------
        rt_or_mz: str
            in ["rt", "mz"]. Plot for either retention times or mz values
        filepath: str
            store the plot as this file. Default is None, in which case no plot is stored

        Returns:
        --------
        plotnine ggplot object
            the plot
        """

        if rt_or_mz not in ["rt", "mz"]:
            raise ValueError("rt_or_mz parameter must be either 'rt' or 'mz'")
        if rt_or_mz == "rt":
            anchors = self.rt_anchors
        else:
            anchors = self.mz_anchors

        # build data frame
        step = anchors.shape[0]
        anchors_4_df = np.zeros(shape = ((len(self.Pt_list) - 1) * step, 2))
        batch_lab = []
        for i in range(len(self.Pt_list) - 1):
            anchors_4_df[i * step : (i + 1) * step, 0] = anchors[:, i + 1]
            anchors_4_df[i * step : (i + 1) * step, 1] = anchors[:, i + 1] - anchors[:, 0]
            batch_lab += step * [str(i + 1)]
        df = pd.DataFrame(data = anchors_4_df, columns = ["batch_i", "batch_i - batch_0"])
        df["i"] = batch_lab

        plt = p9.ggplot(df, p9.aes(x = "batch_i", y = "batch_i - batch_0", color = "i")) +\
            p9.geom_line(alpha = 0.6) + p9.ggtitle(rt_or_mz + " shift") +\
            p9.xlab(r'$\mathrm{batch}_0$') + p9.ylab(r'$\mathrm{batch}_i - \mathrm{batch}_0$') +\
            p9.theme_538()
        if filepath is not None:
            plt.save(filepath, verbose = False)
        return plt
        

    def interpolate(self) -> None:
        """Determine cubic splines that interpolate the retention times and mz values of anchor features
        between feature tables Pt_list[i] and Pt_list[0]. This is the basis to later correct them
        via the correct_rt and correct_mz methods. Store results in Peaktable_align object
        """

        if self.rt_anchors is None or self.mz_anchors is None:
            raise ValueError("There are no anchor features available, yet. Run the find_anchors() method\
                to obtain them.")

        _mz_rt_inter = []
        for mz_rt_anchors in [self.mz_anchors, self.rt_anchors]:
            mz_rt_diff = mz_rt_anchors - np.tile(mz_rt_anchors[:, 0][:, np.newaxis], (1, mz_rt_anchors.shape[1]))
            splines = []
            for j in range(1, mz_rt_anchors.shape[1]):
                x = mz_rt_anchors[:, j]
                y = mz_rt_diff[:, j]
                y = y[x.argsort()]
                x = np.sort(x)
                spline = CubicSpline(
                    x, 
                    y, 
                    bc_type = "not-a-knot", # ?
                    extrapolate = True
                    )
                splines.append(spline)
            _mz_rt_inter.append(splines)
        self._mz_inter = _mz_rt_inter[0]
        self._rt_inter = _mz_rt_inter[1]


    def correct_mz_rt(self) -> None:
        """Correct mz values and retention times based on a two-times differentiable cubic spline
        that interpolates the differences between batch 0 and all other batches. Hence, batch 0 
        becomes the reference for mz values
        """

        if self._mz_inter is None or self._rt_inter is None:
            raise ValueError("There are no cubic splines for interpolation available, yet. Run the interpolate()\
                method to obtain them.")

        for i, Pt in enumerate(self.Pt_list[1:]):
            Pt.mz -= self._mz_inter[i](Pt.mz)
            Pt.rt -= self._rt_inter[i](Pt.rt)


    def align(
        self,
        k_min,
        mediator: str = "caesar",
        similarity_func: callable = std_similarity,
        verbose: bool = True
        ) -> Peaktable:
        """Align peak tables into one peaktable in a way inspired by BiPACE (Hoffmann et al., 2012,
        https://doi.org/10.1186/1471-2105-13-214).
        
        Arguments:
        ----------
        k_min: int
            minimum number of batches that will comprise an aligned feature in the aligned peak table
        mediator: str
            in ['ceasar', 'solon']. Apply this method to mediate conflicts when it comes to aligning
            features according to cliques. While 'ceasar' pursues top-down approach where higher-ranking
            features elimante lower-ranking features, 'solon' seeks to find an as-large-as-possible subset
            of all cliques without conflicts. For details, see clique_mediator.caesar and clique_mediator.
            solon, respectively
        similarity_func: callable
            a function of the kind as similarity_func.std_similarity which indicates similarity between two features. 
            Defaults to standard_similarity
        verbose: bool

        Returns:
        --------
        Peaktable object
            merged peak table, corrected for batch effects if fold_correct == True. For alignments not involving
            all peaks, impute these values with 1/10 of the minimum value in the orginial data. An additional
            version of the peak table with NAs will be stored in the _na_pt attribute
        """

        return align_pt(
            Pt_list = self.Pt_list,
            k_min = k_min,
            mediator = mediator,
            similarity_func = similarity_func,
            rt_tol = self.rt_tol,
            mz_tol = self.mz_tol,
            verbose = verbose
        )


    def align_wrapper(
        self,
        k_min: int,
        mediator: str,
        similarity_func: callable = std_similarity,
        verbose: bool = True,
        generate_plots: bool = True,
        plot_dir: str = None
        ) -> Peaktable:
        """Wrapper around the alignment procedure including: find anchors, interpolate shifts in retention time
        and mass-to-charge ratios, correct them, do the actual alignment
        
        Parameters:
        -----------
        k_min: integer
            2 <= k_min <= n_batches. Minimum number of batches that will comprise an aligned feature 
            in the aligned peak table
        mediator: string
            in ['ceasar', 'solon']. Apply this method to mediate conflicts when it comes to aligning
            features according to cliques. While 'ceasar' pursues top-down approach where higher-ranking
            features elimante lower-ranking features, 'solon' seeks to find an as-large-as-possible subset
            of all cliques without conflicts. For details, see clique_mediator.caesar and clique_mediator.
            solon, respectively
        similarity_func: callable
            a function of the kind as similarity_func.std_similarity which indicates similarity between two features.
            Defaults to standard_similarity
        verbose: bool
            Default is True
        generate_plots: bool
            if True, generate some plots: a histogram for mz, rt values for every batch, a line plot of mz, rt
            shifts, a 2-dim PCA of the aligned feature table, a heatmap of pairwise correlations between samples 
            in the aligned feature table. Default is True
        plot_dir: str
            store the plots in this directory. Default is None, in which case no plots are stored

        Returns:
        --------
        Peaktable
            the aligned feature table
        """

        # plot histograms of rt, mz values ...
        if generate_plots:
            if plot_dir is None:
                for i, Pt in enumerate(self.Pt_list):
                    print("mass-to-charge ratios for batch", i)
                    Pt.mz_hist()
                    print("retention times for batch", i)
                    Pt.rt_hist()
            else:
            # ... in own directory
                path = os.path.join(plot_dir, "mz_rt_histograms")
                try:
                    os.mkdir(path)
                except OSError:
                    pass
                for i, Pt in enumerate(self.Pt_list):
                    mz_file = os.path.join(path, "mz_batch" + str(i) + ".pdf")
                    Pt.mz_hist(mz_file)
                    rt_file = os.path.join(path, "rt_batch" + str(i) + ".pdf")
                    Pt.rt_hist(rt_file)

        self.find_anchors(verbose = verbose)
        if generate_plots:
            for mz_or_rt in ["mz", "rt"]:
                if plot_dir is not None:
                    shift_path = os.path.join(plot_dir, mz_or_rt + "_shift.pdf")
                else:
                    shift_path = None
                self.plot_shift(mz_or_rt, filepath = shift_path)

        self.interpolate()
        self.correct_mz_rt()
        Pt_aligned = self.align(k_min = k_min, mediator = mediator, similarity_func = similarity_func)

        if generate_plots:
            if plot_dir is None:
                pca_path = corr_path = None
            else:
                pca_path = os.path.join(plot_dir, "pca_after_align.pdf")
                corr_path = os.path.join(plot_dir, "corr_after_align.pdf")
            Pt_aligned.plot_pca_2d(filepath = pca_path)
            Pt_aligned.correlation_heatmap(filepath = corr_path)

        return Pt_aligned

        

def find_anchors_(
    Pt_list: List[Peaktable],
    rt_tol: float, 
    mz_tol: float,
    verbose: bool
    ) -> List[np.ndarray]:
    """For several peak tables, find features that can uniqely be associated with each other, 
    so-called anchors

    Anchors enable retention-time correction

    Arguments:
    ----------
    Pt_list: List[Peaktable]
        contains the peaktables intended to be merged
    rt_tol: float
        maximum retention-time shift for the same feature between different batches that is tolerated
    mz_tol: float
        analogon for mz values
    verbose: bool

    Returns:
    --------
    List[np.ndarray]
        retention-time anchors, mz anchors. Every 2-dim numpy array holds anchors in rows
    """

    rt_mz_all, index_split = extract_rt_mz(Pt_list)

    # build network of acceptance, i.e., connect two features p, q (out of different batches) iff.
    # p is acceptable for q and vice-versa. Acceptable means to lie within both rt_tol and mz_tol
    network_acc = np.zeros(shape = (index_split[-1], index_split[-1]), dtype = int)
    for Pt_i in range(len(Pt_list)):
        for i in range(index_split[Pt_i], index_split[Pt_i + 1]):
            rt_i = rt_mz_all[i, 0]
            mz_i = rt_mz_all[i, 1]
            for j in range(index_split[Pt_i]):
                rt_j = rt_mz_all[j, 0]
                mz_j = rt_mz_all[j, 1]
                if np.abs(rt_i - rt_j) < rt_tol and np.abs(mz_i - mz_j) < mz_tol:
                    network_acc[i, j] = 1
    network_acc += network_acc.T + np.identity(network_acc.shape[0], dtype = int)

    # find all isolated cliques of size len(Pt_list), the anchors

    #start_nodes = np.ones(network_acc.shape[0], dtype = int) # each node is a possible start node for such a clique
    # matrix -- or agent -- that will report us neigbors per batch if multiplied with network_acc
    nb_per_batch_agent = np.zeros(shape = (network_acc.shape[0], len(Pt_list)), dtype = int)
    for Pt_i in range(len(Pt_list)):
        nb_per_batch_agent[index_split[Pt_i]:index_split[Pt_i + 1], Pt_i] = 1

    # pre-filter nodes with exactly one neighbor per batch ...
    nb_per_batch = network_acc @ nb_per_batch_agent
    start_nodes = np.where(np.all(nb_per_batch == 1, axis = 1), 1, 0).astype(int)
    start_indices = start_nodes.nonzero()[0]
    # ... to subset our orginal network
    network_sub = network_acc.take(start_indices, axis = 0).take(start_indices, axis = 1)
    # find (maximal) cliques of size len(Pt_list) in network_sub, where every node has at most len(Pt_list) neighbors
    cliques_sub = find_cliques_max_k(network_sub, len(Pt_list))
    # map the node names (i.e. indices) back to the original network_acc
    rt_anchors = np.zeros(shape = (len(cliques_sub), len(Pt_list)))
    mz_anchors = np.zeros(shape = rt_anchors.shape)
    for i, clique in enumerate(cliques_sub):
        rt_anchors[i, :] = rt_mz_all[start_indices[clique], 0]
        mz_anchors[i, :] = rt_mz_all[start_indices[clique], 1]

    # for both rt and mz values, it's possible to have EXACTLY the same value in two or more anchor
    # features, which makes interpolation impossible
    # therefore, scan each column in mz/rt_anchors for duplicates and remove all but one of these rows
    anchors = []
    for x_anchors in [rt_anchors, mz_anchors]:
        keep_row_idx = np.arange(x_anchors.shape[0])
        for j in range(1, x_anchors.shape[1]):
            _, unique_idx = np.unique(x_anchors[:, j], return_index = True)
            keep_row_idx = np.intersect1d(keep_row_idx, unique_idx)
        x_anchors = x_anchors.take(keep_row_idx, axis = 0)
        anchors.append(x_anchors)

    if verbose:
        print("Found", anchors[1].shape[0], "mz anchors and", anchors[0].shape[0], "rt anchors")

    return anchors