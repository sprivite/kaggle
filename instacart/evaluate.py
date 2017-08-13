import numpy as np
import pandas as pd

# 
# F1 score for evaluating model predictions
#
# From the Kaggle site: 
#  "Submissions will be evaluated based on their mean F1 score."
# I think this means the average F1 score for each prediction on a single test set?
# Not an average (over e.g. test sets) of some global F1 score?
#
def f1score(pred, obs):
    '''
    Expected inputs are equal-length lists of sets: pred are the sets of 
    products reordered by a given customer as predicted by some model, and
    obs are the actual items observed to be ordered by the same customer.
    '''
    assert len(pred) == len(obs)
    scores = []
    for pr, ob in zip(pred, obs):

        if not pr:
            pr = set([None])

        if not ob:
            ob = set([None])

        precision = len(pr & ob) / float(len(pr))
        recall = len(pr & ob) / float(len(ob))

        if precision == recall == 0:
            scores.append(0) # this removes the discontinuity at (0,0)
        else:
            scores.append( 2 * precision * recall / (precision + recall) )

    return np.mean(scores)


def f1score_global(pred, obs):
    '''
    Expected inputs are equal-length lists of sets: pred are the sets of 
    products reordered by a given customer as predicted by some model, and
    obs are the actual items observed to be ordered by the same customer.
    '''

    assert len(pred) == len(obs)
    scores = []
    TP = FP = FN = 0
    for pr, ob in zip(pred, obs):

        tp = len(pr & ob)
        fp = len(pr) - tp
        fn = len(ob) - tp

        TP += tp
        FP += fp
        FN += fn

    precision = float(TP) / (TP + FP)
    recall = float(TP) / (TP + FN)

    return 2 * precision * recall / (precision + recall)
