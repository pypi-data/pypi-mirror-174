# written by Lukas Gessl

# bunch of routines to handle file in- and output for csv or excel files containing
# peak tables. This especially means transforming csv files via pandas DataFrame into
# numpy arrays and vice-versa

# PyPI
from typing import List, Union
import pandas as pd
import numpy as np
import re

# this package
from .peaktable import Peaktable
from .peaktable import Peaktable

def read_pt_excel(
    filepath: str,
    sheet_name: Union[List[str], List[int]],
    rt_ident: str,
    mz_ident: str,
    qc_ident: str = None,
    verbose: bool = True
    ) -> List[Peaktable]:
    """Read in an excel file with feature tables in it and get a list of Peaktable objects.
    Each feature table in the excel file has to hold features in the rows, samples in the
    columns. The first row must hold sample names; sample names may encode whether a sample is
    quality control or not (see qc_ident parameter). The first column must hold feature names; 
    each feature name must encode retention time and mass-to-charge ratio (see rt_ident, 
    mz_ident parameters below).

    Parameters:
    -----------
    filepath: str
    sheet_name: List[str] | List[int]
        read these sheets from the excel file
    rt_ident: str
        retention time is the number that immediately comes after rt_ident in feature name
    rt_ident: str
        mass-to-charge ratio is the number that immediately comes after mz_ident in feature name
    qc_ident: str
        a sample in the feature table is quality control if and only if its sample names
        matches qc_ident pattern. Default is None, in which case samples are assumed to be
        quality control
    verbose: bool
        Defaults to True

    Returns:
    --------
    List[Peaktable]
    """

    pt_dict = pd.read_excel(
        filepath,
        sheet_name = sheet_name,
        header = 0,
        index_col = 0
    )

    Pt_list = []
    for pt in pt_dict.values():
        sample_names = list(pt.columns)

        # infer retention times and mz values
        rts = np.zeros(shape = pt.shape[0])
        mzs = np.zeros(shape = pt.shape[0])
        for i, rt_mz in enumerate(pt.index):
            rt = re.search(rt_ident + "[\\d\\.]+", rt_mz).group()
            mz = re.search(mz_ident + "[\\d\\.]+", rt_mz).group()
            rts[i] = float(rt[len(rt_ident): ])
            mzs[i] = float(mz[len(mz_ident): ])

        # infer samples, i.e. columns, that are qc
        if qc_ident is None:
            qc_samples = np.arange(pt.shape[1])
        else:
            qc_index = []
            for j, col_name in enumerate(pt.columns):
                if re.search(qc_ident, col_name) is not None:
                    qc_index.append(j)
            qc_samples = np.array(qc_index)

        # extract abundancies into numpy array
        pt = pt.to_numpy()
        Pt_list.append(Peaktable(pt, mzs, rts, sample_names, qc_samples))

        if verbose:
            print(filepath, "| shape:", pt.shape)
        
    return Pt_list