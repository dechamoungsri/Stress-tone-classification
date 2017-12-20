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

import GPy
import traceback

from sklearn.metrics import accuracy_score

class DBSCAN_executioner(object):

    @staticmethod
    def run(X, labels_true, path, dominant, inverselengthscale, stress_only=False, stress_list=None):

        ##############################################################################
        X = np.array(X)
        labels_true = np.array(labels_true)
        if stress_only:
            print 'stress_only'

            stress_index = np.where(stress_list==1)

            print stress_index

            X = np.copy(X[stress_index])
            labels_true = np.copy(labels_true[stress_index])

        # Compute DBSCAN
        print 'Stress : {}, Unstress: {}'.format(len(np.where(labels_true==1)[0]), len(np.where(labels_true==0)[0]))
        lengthscale=1/np.array(inverselengthscale, dtype=float)
        kernel = GPy.kern.RBF(len(X[0]), lengthscale=lengthscale, ARD=True)

        print lengthscale

        XX = -1*np.log(kernel.K(X, X))

        # incre = 0.00005
        incre = 0.00001

        jncre = 1
        done = False

        measure_list = []
        outfile = []
        # print labels_true
        # Best :  (0.0025000000000000005, 35.0, 0.69180773481515445)
        print XX.shape, len(labels_true)
        print 'Mean, min, max'
        print np.mean(XX), np.amin(XX), np.amax(XX)

        # sys.exit()
        outfile.append('Incre : {}'.format(incre))
        outfile.append('Mean, min, max')
        outfile.append('{}, {}, {}'.format(np.mean(XX), np.amin(XX), np.amax(XX)))

        for i in np.flipud(np.arange(0.00, 0.01, incre)):
        # for i in np.flipud(np.arange(0.001, 0.004, incre)):
            if done : break
            for j in np.flipud(np.arange(jncre, 40.0, jncre)):
                try:
                    db = DBSCAN(eps=i, min_samples=j, metric='precomputed').fit(XX)
                    labels = db.labels_
                    
                    n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
                    # if n_clusters_ == en(set(labels_true)):
                    # print n_clusters_, i, j
                    measure_list.append((i, j, metrics.v_measure_score(labels_true, labels)))
                except:
                    # print 'Error at : eps={}, min_samples={}'.format(i ,j)
                    # traceback.print_exc()
                    # sys.exit()
                    pass
                    
        Utility.sort_by_index(measure_list, 2)

        if len(measure_list) == 0:
            print 'Error: Cannot find best at : {}'.format(path)

        print 'Best : {}'.format(measure_list[len(measure_list)-1])
        v_best = measure_list[len(measure_list)-1][2]

        outfile.append('Best : '.format(measure_list[len(measure_list)-1]))

        for m in measure_list:
            if m[2] == v_best:
                print m
                outfile.append('{}'.format(m))

        db = DBSCAN(
            eps=measure_list[len(measure_list)-1][0], 
            min_samples=int(measure_list[len(measure_list)-1][1]),
            metric='precomputed').fit(XX)

        core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
        core_samples_mask[db.core_sample_indices_] = True
        labels = db.labels_

        acc = accuracy_score(labels_true, labels)
        swap = np.copy(labels_true)
        stress_index = np.where(swap==1)
        unstress_index = np.where(swap==0)
        swap[stress_index] = 0
        swap[unstress_index] = 1
        acc_swap = accuracy_score(swap, labels) 
        if acc_swap > acc:
            acc = acc_swap

        print 'Accuracy score : {} / swap: {}'.format(acc, acc_swap)

        # for idx, t in enumerate(labels):
        #     print labels[idx], labels_true[idx]

        # print db.core_sample_indices_
        # print labels
        Utility.save_obj([len(measure_list)-1][0], '{}/best_measure_params.npy'.format(path))
        Utility.save_obj(labels, '{}/clustered_label.npy'.format(path))

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

        Utility.write_to_file_line_by_line('{}/clustering_result.txt'.format(path), outfile)

        # print("Silhouette Coefficient: %0.3f"
        #       % metrics.silhouette_score(X, labels))

        ##############################################################################
        # Plot result
        import matplotlib.pyplot as plt
        plt.clf()
        # Black removed and is used for noise instead.
        unique_labels = set(labels)
        colors = plt.cm.Spectral(np.linspace(0, 1, len(unique_labels)))
        for k, col in zip(unique_labels, colors):
            if k == -1:
                # Black used for noise.
                col = 'k'

            class_member_mask = (labels == k)

            xy = X[class_member_mask & core_samples_mask]
            plt.plot(xy[:, dominant[0]], xy[:, dominant[1]], 'o', markerfacecolor=col,
                     markeredgecolor='k', markersize=14)

            xy = X[class_member_mask & ~core_samples_mask]
            plt.plot(xy[:, dominant[0]], xy[:, dominant[1]], 'o', markerfacecolor=col,
                     markeredgecolor='k', markersize=6)

        plt.title('Estimated number of clusters: %d' % n_clusters_)
        # plt.show()
        print '{}/stress_unstress_clustering_lengthscale.eps'.format(path)
        plt.savefig('{}/stress_unstress_clustering_lengthscale.eps'.format(path))
        return labels_true, labels
