print(__doc__)

import numpy as np

from sklearn import metrics
from sklearn.cluster import DBSCAN
from sklearn.datasets.samples_generator import make_blobs
from sklearn.preprocessing import StandardScaler

import sys
sys.path.append('/home/h1/decha/Dropbox/python_workspace/Utility/')
from tool_box.util.utility import Utility
sys.path.append('/home/h1/decha/Dropbox/python_workspace/Inter_speech_2016/')
from sklearn.cluster import KMeans
import GPy
import traceback

class Kmeans_executioner(object):

    @staticmethod
    def run(X, labels_true, path, dominant, inverselengthscale):

        data = np.copy(X)

        for l in range(len(data[0])):
            data[:,l] = data[:,l] * inverselengthscale[l]

        y = KMeans(n_clusters=2).fit_predict(data)

        print y

        labels = y

        outfile = []

        Utility.save_obj(labels, '{}/kmeans_label.npy'.format(path))

        # Number of clusters in labels, ignoring noise if present.
        n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)

        print('Estimated number of clusters: %d' % n_clusters_)
        print("Homogeneity: %0.3f" % metrics.homogeneity_score(labels_true, labels))
        print("Completeness: %0.3f" % metrics.completeness_score(labels_true, labels))
        print("V-measure: %0.3f" % metrics.v_measure_score(labels_true, labels))
        print("Adjusted Rand Index: %0.3f"
              % metrics.adjusted_rand_score(labels_true, labels))
        print("Adjusted Mutual Information: %0.3f"
              % metrics.adjusted_mutual_info_score(labels_true, labels))

        outfile.append('Estimated number of clusters: %d' % n_clusters_)
        outfile.append("Homogeneity: %0.3f" % metrics.homogeneity_score(labels_true, labels))
        outfile.append("Completeness: %0.3f" % metrics.completeness_score(labels_true, labels))
        outfile.append("V-measure: %0.3f" % metrics.v_measure_score(labels_true, labels))
        outfile.append("Adjusted Rand Index: %0.3f"
              % metrics.adjusted_rand_score(labels_true, labels))
        outfile.append("Adjusted Mutual Information: %0.3f"
              % metrics.adjusted_mutual_info_score(labels_true, labels))

        Utility.write_to_file_line_by_line('{}/k_means_result.txt'.format(path), outfile)

        # # print("Silhouette Coefficient: %0.3f"
        # #       % metrics.silhouette_score(X, labels))

        ##############################################################################
        # Plot result
        import matplotlib.pyplot as plt

        # Black removed and is used for noise instead.
        unique_labels = set(labels)
        colors = plt.cm.Spectral(np.linspace(0, 1, len(unique_labels)))
        for k, col in zip(unique_labels, colors):
            if k == -1:
                # Black used for noise.
                col = 'k'

            class_member_mask = (labels == k)

            # xy = X[class_member_mask]
            # plt.plot(xy[:, dominant[0]], xy[:, dominant[1]], 'o', markerfacecolor=col,
            #          markeredgecolor='k', markersize=14)

            xy = X[class_member_mask]
            plt.plot(xy[:, dominant[0]], xy[:, dominant[1]], 'o', markerfacecolor=col,
                     markeredgecolor='k', markersize=6)

        plt.title('Estimated number of clusters: %d' % n_clusters_)
        # plt.show()
        print '{}/stress_unstress_clustering_kmeans.eps'.format(path)
        plt.savefig('{}/stress_unstress_clustering_kmeans.eps'.format(path))
