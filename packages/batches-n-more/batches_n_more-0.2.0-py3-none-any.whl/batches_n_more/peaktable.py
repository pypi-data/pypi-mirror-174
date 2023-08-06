# written by Lukas Gessl


# PyPI
import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import pandas as pd
import plotnine as p9
from typing import List, Union, Tuple
import os

# this package
from linear_regression import LinearRegression


class Peaktable:
    """Peak table representation for efficient calculations and analysis
    
    ...

    Attributes:
    -----------
    pt: 2-dim float numpy array
        actual peak table with samples as rows
    mz: 1-dim numpy float array
        mz values
    rt: 1-dim numpy float array
        retention times
    sample_names: list of str
        sample names, i.e. column names, for pt
    qc_samples: 1-dim int numpy array
        column indices of quality control samples
    shape: tuple with 2 entries
        shape of pt
    batches: 1-dim int numpy array
        for every sample, i.e. column, in pt, its batch
    _na_bool: None | 2-dim bool numpy array
        corresponging to pt, True where values are missing

    Methods:
    --------
    sort()
        sort rows of peak table by, first, mz values and, second, retention times
    write_excel(filepath)
        store a Peaktable object as an excel file
    pqn()
        apply probabilistic quantile normalization on peak table
    qc_correct()
        correct batch effects according to fold changes between batch-wise row means in peak table
    plot_pca_2d()
        scatter plot of first vs. second principal component of peak table
    rt_hist()
        histogram of retention times in peak table
    mz_hist()
        histogram of mz values in peak table
    correct_batch()
        correct batch effects inspired by exploBATCH
    """

    def __init__(
        self, 
        pt: np.ndarray, 
        mz: np.ndarray, 
        rt: np.ndarray, 
        sample_names: List[str], 
        qc_samples: np.ndarray,
        batches: np.ndarray = None,
        _na_bool: Union[None, np.ndarray] = None
        ) -> None:
        """
        Arguments:
        ----------
        pt: 2-dim float numpy array
            peak table holding abundancies (features in rows, samples in columns)
        mz: 1-dim float numpy array
            mz values for rows in pt
        rt: 1-dim float numpy array
            retention times for rows in pt
        sample_names: list of strings
            the sample names, i.e. column names, for pt
        qc_samples: 1-dim int numpy array
            column indices of quality control samples in pt
        batches: 1-dim int numpy array
            for every sample, i.e. column, in pt, its batch. Defaults to None, in which
            case all samples are considered to form batch 0
        _na_bool: None | 2-dim bool numpy array
            corresponding to pt, True where values are missing. Default is None, which
            indicates no missig values
        """

        self.pt = pt
        self.rt = rt
        self.mz = mz
        self.sample_names = sample_names
        self.qc_samples = qc_samples
        self.shape = pt.shape
        self._na_bool = _na_bool

        if batches is None:
            batches = np.tile(0, reps = pt.shape[1])
        self.batches = batches


    def sort(self) -> None:
        """Sort rows of peak table by, first, mz values and, second, retention times
        """
        rt_mz = np.concatenate([self.rt[np.newaxis, :], self.mz[np.newaxis, :]], axis = 0)
        ind = np.lexsort(rt_mz)
        self.pt = self.pt.take(ind, axis = 0)


    def write_excel(
        self, 
        filepath: str, 
        n_mz_round = 5, 
        n_rt_round = 6, 
        na_sheet: bool = True
        ) -> None:
        """Write into excel file

        Arguments:
        ----------
        filepath: str
        n_mz_round: int
            round mz values off to n_mz_round decimal places in excel file. Default is 5
        n_rt_round: int
            round retention times off to n_rt_round decimal places in excel file. Default is 6
        na_sheet: bool
            store an additional sheet with NAs encoding missing values in excel file. Default is True
        """
        
        index = []
        for mz, rt in zip(self.mz.round(n_mz_round), self.rt.round(n_rt_round)):
            index.append("mz:" + str(mz) + "_rt:" + str(rt))

        # ordinary data
        pt_num = self.pt.copy()
        pt_num[self._na_bool] = pt_num.min() / 10.
        pt_df = pd.DataFrame(
            data = pt_num,
            columns = self.sample_names,
            index = index
        )
        # NaN data
        pt_na_df = pt_df.copy()
        pt_na_df[self._na_bool] = None

        with pd.ExcelWriter(filepath) as writer:
            pt_df.to_excel(writer, sheet_name = "numeric")
            if na_sheet:
                pt_na_df.to_excel(writer, sheet_name = "NA", na_rep = "NA")


    def pqn(self) -> None:
        """Apply Probabilistic Quantile Normalization on the peak table"""

        reference = np.median(self.pt, axis = 1)
        quotient = np.diag(1/reference) @ self.pt
        self.pt = self.pt @ np.diag(1/np.median(quotient, axis = 0))


    def qc_fold_correct(
        self
        ) -> None:
        """Correct (merged) peak table according to fold changes between the medians of QC samples
        """

        qc_correct_(self)



    def plot_pca_2d(self, filepath: str = None) -> p9.ggplot:
        """Plot a PCA of the peak tables colored by batches

        Parameters:
        -----------
        batch_assign: 1-dim int numpy array
            for every sample column in self.pt, its corresponding batch
        filepath: str
            store the plot as this file. Default is None, in which case
            no plot is stored

        Returns:
        --------
        plotnine ggplot object
            the plot
        """

        # scale data to standard units
        pt = np.zeros(shape = self.pt.shape)
        pt[:, :] = self.pt
        means = np.tile(pt.mean(axis = 1)[:, np.newaxis], (1, pt.shape[1]))
        pt = np.diag(1/pt.std(axis = 1)) @ (pt - means)

        pca = PCA(n_components = 2)
        pca_pt = pca.fit_transform(pt.T)
        labels = []
        for i in range(2):
            col = "PC" + str(i + 1) + " (" + str(np.round(pca.explained_variance_ratio_[i], 3)) + ")"
            labels.append(col)
        pca_df = pd.DataFrame(
            data = pca_pt,
            columns = ["PC1", "PC2"]
        )
        pca_df["Batch"] = self.batches

        plt = p9.ggplot(pca_df, p9.aes("PC1", "PC2", color = "factor(Batch)")) +\
            p9.geom_point() + p9.labs(x = labels[0], y = labels[1], color = "Batch") +\
            p9.theme_538()
        if filepath is not None:
            plt.save(filepath, verbose = False)

        return plt

    
    def rt_hist(self, filepath: str = None, n_bins = 80) -> p9.ggplot:
        """Plot a histogram of the retention times of the features of the peak table

        Arguments:
        ----------
        filepath: str
            store the plot as this file. Default is None, in which no plot is stored
        n_bins: int
            number of bins in histogram. Defaults to 80

        Returns:
        --------
        plotnine ggplot object
            the plot
        """

        df = pd.DataFrame(data = self.rt, columns = ["retention time"])
        plt = p9.ggplot(df, p9.aes(x = "retention time")) + p9.geom_histogram(bins = n_bins) + p9.theme_538()
        if filepath is not None:
            plt.save(filepath, verbose = False)
        return plt


    def mz_hist(self, filepath: str = None, n_bins = 80) -> p9.ggplot:
        """Plot a histogram of the mz values of the features of the peak table

        Arguments:
        ----------
        filepath: str
            store the plot as this file. Default is None, in which no plot is stored
        n_bins: int
            number of bins in histogram. Defaults to 80

        Returns:
        --------
        plotnine ggplot object
            the plot
        """

        df = pd.DataFrame(data = self.mz, columns = ["mz value"])
        plt = p9.ggplot(df, p9.aes(x = "mz value")) + p9.geom_histogram(bins = n_bins) + p9.theme_538()
        if filepath is not None:
            plt.save(filepath, verbose = False)
        return plt


    def correlation_heatmap(self, filepath: str = None) -> p9.ggplot:
        """Plot the matrix of correlations between all possible pairs of qc samples as a heatmap
        
        Arguments:
        ----------
        filepath: str
            store the plot as this file. Default is None, in which no plot is stored

        Returns:
        --------
        plotnine ggplot object
            the plot
        """

        qc_pt = self.pt.take(self.qc_samples, axis = 1)
        sample_names = [self.sample_names[i] for i in self.qc_samples]
        sample_names = np.array(sample_names)
        df = pd.DataFrame(qc_pt, columns = sample_names)

        # bring this data frame into tidy format as desired by plotnine
        rho = df.corr().to_numpy().flatten()
        s1 = np.repeat(sample_names, sample_names.size)
        s2 = np.tile(sample_names, sample_names.size)
        data = {"s1": s1, "s2": s2, "rho": rho}
        df = pd.DataFrame(data = data)

        plt = p9.ggplot(
            mapping = p9.aes("s1", "s2", fill = "rho"), 
            data = df
            ) +\
            p9.geom_tile() +\
            p9.scale_fill_distiller() +\
            p9.theme_538() +\
            p9.labs(
                title = "Pearson correlation between QCs",
                x = "",
                y = ""
                ) +\
            p9.theme(
                axis_text_x = p9.element_text(rotation=45, hjust = 1)
            )

        if filepath is not None:
            plt.save(filepath, verbose = False)

        return plt


    def batch_correct(
        self,
        n_pcs: int = 3,
        significance_threshold: float = 0.05,
        n_jobs: int = 1,
        verbose: bool = True
        ) -> None:
        """Correct batch effects in an aligned peak table largely inspired by exploBATCH 
        (https://doi.org/10.1038/s41598-017-11110-6)
        
        Parameters:
        -----------
        n_pcs: int
            analyze batch effects after projecting the data down to n_pcs. Default is 3
        significance_threshold: float
            consider batch effect in regression as present if p value of regression coefficient
            is below signficance_threshold. Default is 0.05
        n_jobs: int
            number of jobs used to compute linear models. Default is 1
        verbose: bool
        """

        # standardize
        scaler = StandardScaler().fit(self.pt.T)
        self.pt = scaler.transform(self.pt.T).T
        # calculate first n_pcs PCs
        pca = PCA(n_components = n_pcs)
        Y = pca.fit_transform(self.pt.T) # shape (n_samples, n_pcs)
        n_batches = self.batches.max() + 1
        beta = np.zeros(shape = (n_batches, n_pcs))
        X = np.zeros(shape = (self.shape[1], n_batches))
        # fill X with covariates (batch affiliation)
        for i, batch in enumerate(self.batches):
            X[i, batch] = 1
        X[:, -1] = 1
        # do ordinary linear regression for every PC on batch affiliation
        p_values = beta.copy().T # keep track of coefficient p-values to possibly report them
        for j in range(n_pcs):
            lr = LinearRegression(fit_intercept = False, n_jobs = n_jobs)
            lr = lr.fit(X, Y[:, j])
            beta[:, j] = np.where(lr.p < significance_threshold, lr.coef_, 0)
            p_values[j, :] = lr.p
        beta[-1, :] = 0 # 

        # calcualte batch effects in linear subspace
        Y = X @ beta
        # map batch effects back to whole space and subtract them 
        self.pt -= pca.inverse_transform(Y).T
        # undo standard scaling
        self.pt = scaler.inverse_transform(self.pt.T).T

        if verbose:
            index = ["PC" + str(i + 1) for i in range(n_pcs)]
            columns = ["batch " + str(self.batches[-1]) + " vs. " + str(j) for j in range(n_batches)]
            df = pd.DataFrame(p_values, index = index, columns = columns)
            print("p values for regression coeffcients in batch correction")
            print("(under null hypothesis that there is no link between batch and PC):")
            print(df)


    def batch_correct_wrapper(
        self,
        n_pcs: int = 3,
        significance_threshold: float = 0.05,
        n_jobs = 1,
        verbose: bool = True,
        generate_plots: bool = True,
        plot_dir: str = None
        ):
        """A wrapper for a typical procedure to correct batch effects in an aligned feature table:
        first apply qc_fold_correct(), then batch_correct() looks for batch effect on the resulting
        feature table and, if it finds batch effects, corrects it
        
        Parameters:
        -----------
        n_pcs: int
            see batch_correct() method. Default is 3
        significance_threshold: float
            see batch_correct() method. Default is 0.05
        n_jobs: int
            see batch_correct() method. Default is 1
        verbose: bool
            Default is True
        generate_plots: bool
            plot 2-dim PCA and heatmap of pairwise correlations between samples after qc_fold_correct()
            and after batch_correct(). Default is True
        plot_dir: str
            store the plots in this directory. Default is None, in which case no plots are stored
        """

        self.qc_fold_correct()
        self.batch_correct(
            n_pcs = n_pcs,
            significance_threshold = significance_threshold,
            n_jobs = n_jobs,
            verbose = verbose
            )

        if generate_plots:
            # automatically generate file paths
            pca_path = os.path.join(plot_dir, "pca_after_batch_correction.pdf")
            corr_path = os.path.join(plot_dir, "corr_after_batch_correction.pdf")

            self.plot_pca_2d(filepath = pca_path)
            self.correlation_heatmap(filepath = corr_path)


def qc_correct_(
    Pt_merge: Peaktable
    ) -> None:
    """Correct (merged) peak table according to fold changes between quality control samples
    in-place

    Parameters:
    -----------
    Pt_merge: Peaktable object
        merged peak table
    """

    sample_index_split = np.zeros(Pt_merge.batches[-1] + 2, dtype = int)
    for i in range(Pt_merge.batches[-1] + 1):
        sample_index_split[i + 1] = np.argwhere(Pt_merge.batches == i)[-1][0] + 1

    mean_pt = np.zeros(shape = (Pt_merge.shape[0], Pt_merge.batches[-1] + 1))
    for j in range(Pt_merge.batches[-1] + 1):
        start = sample_index_split[j]
        stop = sample_index_split[j + 1]
        qc_samples = Pt_merge.qc_samples
        bool = np.logical_and(qc_samples >= start, qc_samples < stop)
        col_ind = qc_samples[bool]
        cols = Pt_merge.pt.take(col_ind, axis = 1)
        mean_pt[:, j] = cols.mean(axis = 1)

    # taking the mean column of the first batch as a reference, calculate fold changes
    folds = np.diag(1/mean_pt[:, 0]) @ mean_pt
    for j in range(folds.shape[1]):
        start = sample_index_split[j]
        stop = sample_index_split[j + 1]
        Pt_merge.pt[:, start:stop] = np.diag(1/folds[:, j]) @ Pt_merge.pt[:, start:stop]