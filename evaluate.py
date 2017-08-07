# From the Kaggle site: "Submissions will be evaluated based on their
# mean F1 score."  I think this means the average F1 score for each
# prediction on a single test set?  Not an average (over e.g. test
# sets) of some global F score?
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
            precision = 1.
        else:
            precision = len(pr & ob) / float(len(pr))

        if not ob:
            recall = 1.
        else:
            recall = len(pr & ob) / float(len(ob))

        if precision == recall == 0:
            scores.append(0) # this removes the discontinuity at (0,0)
        else:
            scores.append( 2 * precision * recall / (precision + recall) )

    return np.mean(scores)
