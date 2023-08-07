# written by Lukas Gessl

# an example how to deploy batches-n-more and use wrappers for compact coding

# PyPI
import numpy as np

# this package
from peaktable_align import Peaktable_align
from pt_io import read_pt_excel


if __name__=="__main__":

    dir = "data/example/"
    files = ["First_batch.xlsx", "Second_batch.xlsx", "Third_batch.xlsx"]
    Pt_list = []
    for i, filename in enumerate(files):
        filepath = dir + filename
        Pt = read_pt_excel(
            filepath,
            sheet_name = ["inputR"],
            rt_ident = "rt:",
            mz_ident = "mz:",
            qc_ident = None
        )
        Pt_list += Pt

    Pt_align = Peaktable_align(
        Pt_list,
        mz_tol = 0.003,
        rt_tol = 0.25
    )

    # short version with wrappers
    Pt_aligned = Pt_align.align_wrapper(
        k_min = 2,
        mediator = "caesar",
        plot_dir = "results"
        )
    Pt_aligned.batch_correct_wrapper(
        n_pcs = 3,
        significance_threshold = 0.05,
        plot_dir = "results"
        )

    Pt_aligned.write_excel("results/aligned.xlsx")