from sklearn.metrics import average_precision_score, auc, precision_recall_curve
import numpy as np



def get_aupr(Y, P, threshold=7.0):
    Y = np.where(Y >= threshold, 1, 0)
    P = np.where(P >= threshold, 1, 0)
    aupr = average_precision_score(Y, P)
    precision, recall, thresholds = precision_recall_curve(Y, P)
    auc_precision_recall = auc(recall, precision)

    return auc_precision_recall


def r_squared_error(y_obs, y_pred):
    y_obs = np.array(y_obs)
    y_pred = np.array(y_pred)
    y_obs_mean = [np.mean(y_obs) for y in y_obs]
    y_pred_mean = [np.mean(y_pred) for y in y_pred]

    mult = sum((y_pred - y_pred_mean) * (y_obs - y_obs_mean))
    mult = mult * mult

    y_obs_sq = sum((y_obs - y_obs_mean) * (y_obs - y_obs_mean))
    y_pred_sq = sum((y_pred - y_pred_mean) * (y_pred - y_pred_mean))

    return mult / float(y_obs_sq * y_pred_sq)


def get_k(y_obs, y_pred):
    y_obs = np.array(y_obs)
    y_pred = np.array(y_pred)

    return sum(y_obs * y_pred) / float(sum(y_pred * y_pred))


def squared_error_zero(y_obs, y_pred):
    k = get_k(y_obs, y_pred)

    y_obs = np.array(y_obs)
    y_pred = np.array(y_pred)
    y_obs_mean = [np.mean(y_obs) for y in y_obs]
    upp = sum((y_obs - (k * y_pred)) * (y_obs - (k * y_pred)))
    down = sum((y_obs - y_obs_mean) * (y_obs - y_obs_mean))

    return 1 - (upp / float(down))


def get_rm2(ys_orig, ys_line):
    r2 = r_squared_error(ys_orig, ys_line)
    r02 = squared_error_zero(ys_orig, ys_line)

    return r2 * (1 - np.sqrt(np.absolute((r2 * r2) - (r02 * r02))))


def get_mse(y, f):
    mse = ((y - f) ** 2).mean(axis=0)
    return mse


def get_pearson(y, f):
    rp = np.corrcoef(y, f)[0, 1]
    return rp


def get_cindex(Y, P):
    summ = 0
    pair = 0

    for i in range(1, len(Y)):
        for j in range(0, i):
            if i is not j:
                if (Y[i] > Y[j]):
                    pair += 1
                    summ += 1 * (P[i] > P[j]) + 0.5 * (P[i] == P[j])

    if pair != 0:
        return summ / pair
    else:
        return 0