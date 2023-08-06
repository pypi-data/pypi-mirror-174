from sklearn.metrics import f1_score, precision_score, recall_score, roc_auc_score


def eval_metrics(actual, pred):
    precision = precision_score(actual, pred)
    recall = recall_score(actual, pred)
    f1 = f1_score(actual, pred)
    auc = roc_auc_score(actual, pred)
    return precision, recall, f1, auc
