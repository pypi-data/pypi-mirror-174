#
# reference implementation of breathing k-means
# (C) 2020 Bernd Fritzke
#
# common parameters
# X: dataset
# C: centroids
# m: breathing depth (number of centroids added/removed during breathing)

import numpy as np
from sklearn.cluster import KMeans
from scipy.spatial.distance import cdist
import math

class BKMeans(KMeans):
    def __init__(self, m=5, theta=1.1, **kwargs):
        """ m: breathing depth
            theta: neighborhood freeze radius
            kwargs: arguments for scikit-learn KMeans
        """
        self.m = m
        self.theta = theta
        super().__init__(**kwargs)
        assert m <= self.n_clusters, f"m({m}) exceeds n_clusters({self.n_clusters})!"

    @staticmethod
    def get_error_and_utility(X, C):
        """compute error and utility per centroid"""
        n = len(X)
        k = len(C)
        dist = cdist(X, C, metric="sqeuclidean")
        dist_srt_idx = np.argsort(dist)
        # distances to nearest centroid
        d1 = dist[np.arange(n), dist_srt_idx[:, 0]]
        # distances to 2nd-nearest centroid
        d2 = dist[np.arange(n), dist_srt_idx[:, 1]]
        # utility
        util = d2-d1
        # aggregate error and utility for each centroid
        errs = {i: 0 for i in range(k)}
        utils = {i: 0 for i in range(k)}
        for center, e, u in zip(dist_srt_idx[:, 0], d1, util):
            errs[center] += e  # aggregate error for each centroid
            utils[center] += u  # aggregate utility for each centroid
        return np.array([*errs.values()]), np.array([*utils.values()])

    def fit(self, X):
        """ compute k-means clustering via breathing k-means (if m > 0) """
        # run k-means++ to get careful seeding ;-)
        super().fit(X)
        # handle trivial case k=1
        if self.n_clusters == 1:
            return self
        m = self.m
        # store best error and codebook so far
        E_best = self.inertia_
        C_best = self.cluster_centers_ + 0
        # no multiple trials from here on
        self.n_init = 1
        tmp = self.init
        # stuff to fill
        print("not yet the real thing ....")
        self.init = tmp  # restore for compatibility with sklearn
        self.inertia_ = E_best
        self.cluster_centers_ = C_best
        return self

    def _breathe_out(self, X, C, m):
        """ remove m centroids while avoiding large error increase"""
        _, U = self.get_error_and_utility(X, C)  # get utility
        useless_sorted_idx = U.argsort()
        k = len(C)
        # mutual distances among centroids
        c_dist = cdist(C, C, metric="euclidean")
        c_dist_srt_idx = np.argsort(c_dist)
        mean_dist_to_nearest = np.sort(c_dist)[:, 1].mean()
        is_close = c_dist < mean_dist_to_nearest*self.theta
        Dminus = set()   # index set of centroids to remove
        Frozen = set()   # index set of frozen centroids
        for useless_idx in useless_sorted_idx:
            if useless_idx in Frozen:
                continue
            else:
                Dminus.add(useless_idx)
                n_neighbors = is_close[useless_idx].sum()-1
                for neighbor in c_dist_srt_idx[useless_idx][1:n_neighbors+1]:
                    if len(Frozen) + m < k:
                        # still enough unfrozen to find m centroids for removal
                        Frozen.add(neighbor)
                if len(Dminus) == m:
                    break
        return C[list(set(range(k))-Dminus)]

    def _breathe_in(self, X, C, m):
        """ add m centroids near centroids with large error"""
        E, _ = self.get_error_and_utility(X, C)  # get error
        eps = math.sqrt(np.sum(E)/len(X))*0.01   # offset factor
        # indices of max error centroids
        max_e_i = (-E).argsort()[:m]
        Dplus = C[max_e_i]+(np.random.rand(C.shape[1])-0.5)*eps
        return np.concatenate([C, Dplus])


if __name__ == "__main__":
    km = KMeans(n_clusters=20)
    X = np.random.rand(1000, 2)
    km.fit(X)
    print(f"k-means++:          SSE={km.inertia_:.5f}")

    bkm = BKMeans(n_clusters=20)
    bkm.fit(X)
    imp = 1-bkm.inertia_/km.inertia_
    print(f"breathing k-means:  SSE={bkm.inertia_:.5f}" +
          f" ({imp:.2%} lower) {'ooops!' if imp<0 else ''}")
