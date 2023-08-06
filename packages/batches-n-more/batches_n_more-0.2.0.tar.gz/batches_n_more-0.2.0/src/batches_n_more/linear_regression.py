# corrected by Lukas Gessl
# after taking it from https://gist.github.com/brentp/5355925


# PyPI
from sklearn import linear_model
from scipy import stats
import numpy as np


class LinearRegression(linear_model.LinearRegression):
    """Inherit from sklearn.linear_model.LinearRegression

    ...

    Attributes:
    -----------
    t: 1-dim float numpy array
        t-test statistic for regression coefficients (does not include intercept if fit_intercept
        = True). Available as soon as .fit() method is called
    p: 1-dim float numpy array
        analogon for p-test statistic

    Methods:
    --------
    fit:
        like inherited .fit() method, but additionally calculate t- and p-test statistic
    """

    def __init__(self, *args, **kwargs):
        if not "fit_intercept" in kwargs:
            kwargs["fit_intercept"] = False
        super(LinearRegression, self).__init__(*args, **kwargs)
        self.fit_intercept_ = kwargs["fit_intercept"]

    def fit(self, X, y):
        """Fit linear model and calculate p- and t-test statistic
        
        Parameters:
        -----------
        X: {array-like, sparse matrix} of shape (n_samples, n_features)
            Training data
        y: array-like of shape (n_samples,)
            Target values. Will be cast to X's dtype if necessary
        sample_weight: array-like of shape (n_samples,), default=None
            Individual weights for each sample

        Returns:
        --------
        self: object
            Fitted estimator
        """
        self = super(LinearRegression, self).fit(X, y)

        n = X.shape[0]
        X_inter = X.copy()
        if self.fit_intercept_ is True:
            X_inter = np.column_stack((np.ones(n), X_inter))
        df = n - X_inter.shape[1]
        sigma_hat = np.sqrt(np.sum((self.predict(X) - y) ** 2) / float(df))
        beta_cov = np.linalg.inv(X_inter.T @ X_inter)
        se = sigma_hat * np.sqrt(np.diagonal(beta_cov))

        if self.fit_intercept_ is True:
            se = se[:-1]
        self.t = self.coef_/se
        self.p = 2 * (1 - stats.t.cdf(np.abs(self.t), df))
        return self