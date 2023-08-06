# written by Lukas Gessl

# an example how to use batches-n-more in detail

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
        Pt[0].rt_hist("results/mz_rt_histograms/rt_batch" + str(i) + ".pdf")
        Pt[0].mz_hist("results/mz_rt_histograms/mz_batch" + str(i) + ".pdf")
        Pt_list += Pt

    Pt_align = Peaktable_align(
        Pt_list,
        mz_tol = 0.003,
        rt_tol = 0.25
    )

    Pt_align.find_anchors()
    for mz_or_rt in ["mz", "rt"]:
        Pt_align.plot_shift(mz_or_rt, filepath = "results/" + mz_or_rt + "_shift.pdf")
    Pt_align.interpolate()
    Pt_align.correct_mz_rt()
    Pt_aligned = Pt_align.align(k_min = 2, mediator = "caesar")
    Pt_aligned.plot_pca_2d(filepath = "results/pca_after_align.pdf")
    Pt_aligned.correlation_heatmap(filepath = "results/corr_after_align.pdf")

    Pt_aligned.qc_fold_correct()
    Pt_aligned.batch_correct()
    # Pt_aligned.pqn()
    Pt_aligned.plot_pca_2d(filepath = "results/pca_after_batch_correction.pdf")
    Pt_aligned.correlation_heatmap(filepath = "results/corr_after_batch_correction.pdf")

    Pt_aligned.write_excel("results/aligned.xlsx")