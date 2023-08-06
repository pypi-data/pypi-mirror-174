import numpy as np
from codecarbon import OfflineEmissionsTracker
from sklearn.metrics import *
import time 
import pandas as pd
from sklearn.metrics import roc_auc_score, r2_score, accuracy_score, f1_score, balanced_accuracy_score, matthews_corrcoef, mean_absolute_error, mean_squared_error

def predict_model(model, x, project_type, threshold=0.5):
    """
    the model class is only assumed to have a predict_proba method for classification problems.
    
    :project_type: can be either classification_b classification_m or regression
    """
    probas, x_test = 0,0
    if project_type == "classification_b":
        preds = (model.predict_proba(x) >= threshold)[:,1].astype(int)
    elif project_type == "classification_m":
        preds = np.asarray([np.argmax(probas[i,:]) for i in range(len(x_test))])
    return preds

def check_and_transform(Y):
    if isinstance(Y, np.ndarray):
        pass
    elif isinstance(Y, pd.DataFrame):
        Y = Y.to_numpy()
    elif isinstance(Y, list):
        Y = np.asarray(Y)
    return Y


#Set of admissible parameters for custom metric definition

#y_pred: Predicted target classes for x_test.
#probs: Predicted probabilities for each class for x_test. 
#y_test: Ground truth target classes for x_test.
#threshold: The model's threshold.
#model: The model on which to evaluate the metric.
#x_test: the testing set.
#x_train: the training set.
#y_train: Ground truth target for x_train.
#protected_attribute: protected attribute (dict): {
#        'column_name': 'column_name',
#        'type': 'cat/float',
#        'value': 0 if 'cat', [min, max] if 'float',
#        'name_prot_attr': 'understandable name'}

#################METRICS CLASSIFICATION#################

def roc_curve(y_pred, y_test):
    fp = np.sum((y_pred == 1) & (y_test == 0))
    tp = np.sum((y_pred == 1) & (y_test == 1))
    fn = np.sum((y_pred == 0) & (y_test == 1))
    tn = np.sum((y_pred == 0) & (y_test == 0))
    fpr = fp / (fp + tn)
    tpr = tp / (tp + fn)
    tnr = tn / (tn + fp)
    fnr = fn / (tp + fn)
    return fpr, tpr, fnr, tnr

def fpr(y_pred, y_test):
    """
    The False Positive Rate corresponds to the proportions of wrong predictions among the samples that are true negative. 
    For a credit scoring application, it means according a loan to an individual which would have not pay back.
    The lower, the better.

    """
    fp = np.sum((y_pred == 1) & (y_test == 0))
    tp = np.sum((y_pred == 1) & (y_test == 1))
    fn = np.sum((y_pred == 0) & (y_test == 1))
    tn = np.sum((y_pred == 0) & (y_test == 0))
    fpr = fp / (fp + tn)
    tpr = tp / (tp + fn)
    tnr = tn / (tn + fp)
    fnr = fn / (tp + fn)
    return fpr

def tpr(y_pred, y_test):
    """
    The True Positive Rate corresponds to the proportions of right predictions among the samples that are true positive.
    For a credit scoring application, it means according a loan to an individual which would have pay back. 
    It is also called the recall or the sensitivity of the model.
    The higher, the better.

    """
    fp = np.sum((y_pred == 1) & (y_test == 0))
    tp = np.sum((y_pred == 1) & (y_test == 1))
    fn = np.sum((y_pred == 0) & (y_test == 1))
    tn = np.sum((y_pred == 0) & (y_test == 0))
    fpr = fp / (fp + tn)
    tpr = tp / (tp + fn)
    tnr = tn / (tn + fp)
    fnr = fn / (tp + fn)
    return tpr

def fnr(y_pred, y_test):
    """
    The False Negative Rate corresponds to the proportions of wrong predictions among the samples that are true positive. 
    For a credit scoring application, it means denying a loan to an individual which would have pay back.
    The lower, the better.

    """
    fp = np.sum((y_pred == 1) & (y_test == 0))
    tp = np.sum((y_pred == 1) & (y_test == 1))
    fn = np.sum((y_pred == 0) & (y_test == 1))
    tn = np.sum((y_pred == 0) & (y_test == 0))
    fpr = fp / (fp + tn)
    tpr = tp / (tp + fn)
    tnr = tn / (tn + fp)
    fnr = fn / (tp + fn)
    return fnr

def tnr(y_pred, y_test):
    """
    The True Negative Rate corresponds to the proportions of wrong predictions among the samples that are true positive. 
    For a credit scoring application, it means denying a loan to an individual which would have not pay back.
    The higher, the better.

    """
    fp = np.sum((y_pred == 1) & (y_test == 0))
    tp = np.sum((y_pred == 1) & (y_test == 1))
    fn = np.sum((y_pred == 0) & (y_test == 1))
    tn = np.sum((y_pred == 0) & (y_test == 0))
    fpr = fp / (fp + tn)
    tpr = tp / (tp + fn)
    tnr = tn / (tn + fp)
    fnr = fn / (tp + fn)
    return tnr

def compute_Matthews_corr_coef_b(y_pred, y_test):
    """
    The function computes the MMC score (between -1 and 1) that summarize how good the classification is. 
    The Matthews correlation coefficient (MCC) is a more reliable statistical rate which produces a high score only if the prediction obtained good results in all of the four confusion matrix categories (true positives, false negatives, true negatives, and false positives), proportionally both to the size of positive elements and the size of negative elements in the dataset. Reference: https://bmcgenomics.biomedcentral.com/articles/10.1186/s12864-019-6413-7. In other words, MCC is the only binary classification rate that generates a high score only if the binary predictor was able to correctly predict the majority of positive data instances and the majority of negative data instances. If a confusion matrix threshold is at disposal, the litterature recommends the usage of the Matthews correlation coefficient over F1 score, and accuracy.
    
    Drawbacks: 
    
    :y_pred: Predicted target classes.
    :y_test: Ground truth target classes.
    """
    return matthews_corrcoef(y_test, y_pred)


#def compute_Matthews_corr_coef_m(y_pred, y_test):
#    """
#    The function computes the MMC score (between -1 and 1) that summarize how good the classification is. 
#    
#    Advantages: Statistical measures like accuracy or F1 score can dangerously show overoptimistic inflated results, especially on imbalanced datasets. The Matthews correlation coefficient (MCC), instead, is a more reliable statistical rate which produces a high score only if the prediction obtained good results in all of the four confusion matrix categories (true positives, false negatives, true negatives, and false positives), proportionally both to the size of positive elements and the size of negative elements in the dataset. Reference: https://bmcgenomics.biomedcentral.com/articles/10.1186/s12864-019-6413-7. In other words, MCC is the only binary classification rate that generates a high score only if the binary predictor was able to correctly predict the majority of positive data instances and the majority of negative data instances. If a confusion matrix threshold is at disposal, the litterature recommends the usage of the Matthews correlation coefficient over F1 score, and accuracy.
    
#    Drawbacks: 
    
#    :y_pred: Predicted target classes.
#    :y_test: Ground truth target classes.
#    """
#    return matthews_corrcoef(y_test, y_pred)


def compute_expected_calibration_error_b(model, y_test, x_test,probs):
    """
    The Expected Calibration Error (ECE) measures how well a model's probabilistic predictions reflect the risk they involve.

    :probs: Predicted probabilities for each class.
    :y_test: Ground truth target classes.
    """
    labels = np.unique(y_test)
    if len(labels) > 2:
        raise ValueError(
            "Only binary classification is supported. Provided labels %s." % labels
        )
    y_prob = probs[:,1]
    n_bins = np.sqrt(len(y_prob)).astype(int)
    quantiles = np.linspace(0, 1, n_bins + 1)
    bins = np.percentile(y_prob, quantiles * 100)
    bins[-1] = bins[-1] + 1e-8
    binids = np.digitize(y_prob, bins) - 1
    bin_sums = np.bincount(binids, weights=y_prob, minlength=len(bins))
    bin_true = np.bincount(binids, weights=y_test, minlength=len(bins))
    bin_total = np.bincount(binids, minlength=len(bins))
    nonzero = bin_total != 0
    prob_true = bin_true[nonzero] / bin_total[nonzero]
    prob_pred = bin_sums[nonzero] / bin_total[nonzero]
    exp_calib_error = (bin_total[nonzero] * np.abs(prob_true - prob_pred)).sum()/len(y_test)
    return exp_calib_error

def compute_roc_auc_score(y_pred, y_test):
    """
    The AUC (Area Under the Curve) measures to which extent a model has learn to discriminate between positive and negative samples, 
    at the level of the predicted scores. 
    Taking a pair of random positive sample P and random negative sample N, it is equal to the probability that the score of P is higher
    than the score of N. 
    Notice that this metric is independent of the choice of the threshold.
    The higher, the better. 

    """
    return roc_auc_score(y_test, y_pred)


def compute_accuracy(y_pred, y_test):
    """
    The accuracy corresponds to the proportion of good predictions. 

    """
    return accuracy_score(y_test, y_pred)


def compute_balanced_accuracy_adjusted(y_pred, y_test):
    """
    The function computes the balanced accuracy. It is defined as the average of recall obtained on each class. Random performance  scores 0. Perfect performance has a score of 1.
    
    Reference: https://scikit-learn.org/stable/modules/generated/sklearn.metrics.balanced_accuracy_score.html
    
    :y_pred: Predicted target classes.
    :y_test: Ground truth target classes.
    """
    return balanced_accuracy_score(y_test, y_pred, adjusted = True)


def compute_f1_score_b(y_pred, y_test):
    """
    The F1 score is a measure that aggregates the precision (the proportion of good predictions among the samples that are predicted positive) 
    and the recall (which is the True Positive Rate) of a model. 
    A F1 score of X means that for one model error, there are 2(1-X)/X true positive. In the particular case where X=1/2, it means that to one misclassified
    sample corresponds two true positive samples.
    The higher, the better.

    """
    return f1_score(y_test, y_pred)


#def compute_f1_score_m(y_pred, y_test):
#    """
#    The function computes the f1 score for binary classifiers. It Calculate metrics globally by counting the total true positives, false negatives and false positives.
    
#    Drawbacks: F1 score, although popular, can generate misleading results on imbalanced datasets, because it fails to consider the ratio between positive and negative elements.
    
#    Reference: https://scikit-learn.org/stable/modules/generated/sklearn.metrics.f1_score.html
    
#    :y_pred: Predicted target classes.
#    :y_test: Ground truth target classes.
#    """
#    return f1_score(y_test, y_pred, average='micro')



    
def compute_emissionCO2_classification(model, x_test, y_test):
    """
    The function computes the CO2 emissions that are produced by model training. It uses 
    the tracker from the codecarbon project. Reference: https://mlco2.github.io/codecarbon/

    :model: the model on which to evaluate the metric.
    :x_test: the testing set.
    :y_test: Ground truth target classes.
    """
    tracker = OfflineEmissionsTracker(country_iso_code="FRA", log_level='critical', save_to_file = False)
    emissions_ = 0
    tracker.start()  
    try:
        model.predict_proba(x_test)                           
    finally:
        emissions_  = tracker.stop()
    return emissions_*1e9

    
def compute_inferenceTime_classification(model, x_test):
    """
    The function computes the inference time which is averaged on the test set. Note that depending on the design of the network architecture, the architecture complexity does not necessarily reflect the computational requirements for performing network inference (e.g., MobileNet has more parameters than SqueezeNet but has lower computational requirements for network inference). Reference: https://arxiv.org/pdf/1806.05512.pdf

    :model: the model on which to evaluate the metric.
    :x_test: the testing set.

    """
    t1 = time.time()
    preds = model.predict_proba(x_test)
    t2 = time.time()
    time_predict_ = float((t2-t1))/len(x_test)
    return time_predict_*1e6



def compute_NetTrustScore_b(probs, y_pred, y_test):
    """
    The function computes the NetTrustScore, a global scalar metric summarizing overall trustworthiness of a model. A model that has higher confidence when predicting correctly will receive a higher marginal trust score for that prediction. A model that has higher confidence when predicting incorrectly will receive a lower marginal trust for that prediction. Scores are then agregated across all predictions. Reference: https://arxiv.org/pdf/2009.05835.pdf
    
    :probs: Predicted probabilities for each class.
    :y_pred: Predicted target classes.
    :y_test: Ground truth target classes.
    """
    n = len(y_test)
    alpha=1
    beta=1
    if len(y_test.shape)>1:
        y_test = y_test.flatten()
    scores = []
    for num_class in set(y_test):
        indices = np.where(y_test == num_class)[0]
        len_class = len(indices)  
        correct_preds_indices = [i for (i, elt) in enumerate(y_pred) if elt == num_class and y_test[i]==num_class]
        false_preds_indices = [i for (i, elt) in enumerate(y_pred) if elt != num_class and y_test[i]==num_class]
        correct_preds = probs[correct_preds_indices, num_class]**alpha
        false_preds = (1- probs[false_preds_indices, 1-num_class])**beta   
        QA_trust = np.concatenate([correct_preds, false_preds], axis=0).reshape([-1,1])    
        trust_score = (1/len(QA_trust))*sum(QA_trust)
        proba_to_get_class = (1/n)*len_class
        scores.append(proba_to_get_class*trust_score)
    return float(sum(scores))


def fairness_DI_demographic_parity_b(y_pred, x_test, y_test, protected_attribute):
    """
    The disparate impact computed for the fairness demographic parity metric.
    
    :y_pred: Predicted target classes.
    :x_test: the testing set.
    :y_test: Ground truth target classes.
    :protected_attribute: {
        'column_name': 'column_name',
        'type': 'cat/float',
        'value': 0 if 'cat', [min, max] if 'float',
        'name_prot_attr': 'understandable name'
    }
    """
    # subgroup slices
    c_name = protected_attribute['column_name']
    if protected_attribute['type'] == 'cat':
        protected_mask = x_test[c_name] == protected_attribute['value']
    if protected_attribute['type'] == 'float':
        c_min, c_max = protected_attribute['value']
        protected_mask = ( x_test[c_name] >= c_min ) & ( x_test[c_name] <= c_max )
    # accuracy for each subgroup
    protected_accuracy = (y_pred[protected_mask] == y_test[protected_mask]).mean()
    favored_accuracy = (y_pred[~protected_mask] == y_test[~protected_mask]).mean()
    # sanity checks
    if protected_accuracy == 0:
        if favored_accuracy == 0:
            res = 1.
        else:
            res = np.Infinity # should print warning
    else: 
        res = favored_accuracy / protected_accuracy 
    return res



#################METRICS REGRESSION#################

def compute_inferenceTime_regression(model, x_test):
    """
    The function computes the inference time which is averaged on the test set. Note that depending on the design of the network architecture, the architecture complexity does not necessarily reflect the computational requirements for performing network inference (e.g., MobileNet has more parameters than SqueezeNet but has lower computational requirements for network inference). Reference: https://arxiv.org/pdf/1806.05512.pdf

    :model: the model on which to evaluate the metric.
    :x_test: the testing set.

    """
    t1 = time.time()
    preds = model.predict(x_test)
    t2 = time.time()
    time_predict_ = float((t2-t1))/len(x_test)
    return time_predict_

def compute_emissionCO2_regression(model, x_test, y_test):
    """
    The function computes the CO2 emissions that are produced by model training. It uses 
    the tracker from the codecarbon project. Reference: https://mlco2.github.io/codecarbon/

    :model: the model on which to evaluate the metric.
    :x_test: the testing set.
    :y_test: Ground truth target classes.
    """
    tracker = OfflineEmissionsTracker(country_iso_code="FRA", log_level='warning', save_to_file = False)
    emissions_ = 0
    tracker.start()  
    try:
        model.predict(x_test)                           
    finally:
        emissions_  = tracker.stop()
    return emissions_


def compute_r2(y_pred, y_test):
    """
    The function computes the R-squared for regression models. R-squared explains to what extent the variance of independant input variable explains the variance of the predicted output variable.
    
    Reference: https://scikit-learn.org/stable/modules/generated/sklearn.metrics.r2_score.html
    
    :y_pred: Predicted target classes.
    :y_test: Ground truth target classes.
    """
    return r2_score(y_test, y_pred)

def compute_mean_absolute_error(y_pred, y_test):
    """
    The function computes the mean absolute error (MAE), also called the L1 loss for regression models. 
    Advantage: less affected by outliers than the L2 error i.e. more robust. Note that if the use case does require to pay attention to the outliers, it might be an drawback rather than an advantage and MSE might be a better choice.
    Drawbacks: as a loss function, it is not differentiable (i.e. it might present difficulties in the gradient computations during backpropagation). It can be unstable (the solution i.e. the decision boundary is NOT changing smoothly with small data changes).
    
    Reference: https://scikit-learn.org/stable/modules/generated/sklearn.metrics.mean_absolute_error.html
    
    :y_pred: Predicted target classes.
    :y_test: Ground truth target classes.
    """
    return mean_absolute_error(y_test, y_pred)

def compute_mean_squared_error(y_pred, y_test):
    """
    The function computes the mean squared error (MSE), also called the L2 loss for regression models. 
    Advantages: the MSE is stable (the solution i.e. the decision boundary is changing smoothly with small data changes) and differentiable.
    Drawbacks: the MSE is more affected by outliers than the L1 error i.e. less robust. Note that if the use case does require to pay attention to the outliers, it might be an advantage rather than a drawback and MSE might be a better choice.
    Reference: https://scikit-learn.org/stable/modules/generated/sklearn.metrics.mean_squared_error.html
    
    :y_pred: Predicted target classes.
    :y_test: Ground truth target classes.
    """
    return mean_squared_error(y_test, y_pred)


metrics = [
    {'metric_name' : 'Accuracy', 'metric_function' : compute_accuracy, 'metric_type' : 'classif', 'h_is_b' : True },
    {'metric_name' : 'True positives', 'metric_function' : tpr, 'metric_type' : 'classif', 'h_is_b' : True },
    {'metric_name' : 'False positives', 'metric_function' : fpr, 'metric_type' : 'classif', 'h_is_b' : False },
    {'metric_name' : 'False negatives', 'metric_function' : fnr, 'metric_type' : 'classif', 'h_is_b' : False },
    {'metric_name' : 'True negatives', 'metric_function' : tnr, 'metric_type' : 'classif', 'h_is_b' : True },
    {'metric_name' : 'ROC AUC', 'metric_function' : compute_roc_auc_score, 'metric_type' : 'classif', 'h_is_b' : True },
    {'metric_name' : 'F1 score', 'metric_function' : compute_f1_score_b, 'metric_type' : 'classif', 'h_is_b' : True },
    {'metric_name' : 'CO2 Emission (reg)', 'metric_function' : compute_emissionCO2_regression, 'metric_type' : 'reg', 'h_is_b' : False },
    {'metric_name' : 'Inference time (reg)', 'metric_function' : compute_inferenceTime_regression, 'metric_type' : 'reg', 'h_is_b' : False },
    {'metric_name' : 'R2 score', 'metric_function' : compute_r2, 'metric_type' : 'reg', 'h_is_b' : True },
    {'metric_name' : 'Mean squared error', 'metric_function' : compute_mean_squared_error, 'metric_type' : 'reg', 'h_is_b' : False },
    {'metric_name' : 'Mean absolute error', 'metric_function' : compute_mean_absolute_error, 'metric_type' : 'reg', 'h_is_b' : False },
#    {'metric_name' : 'F1 score micro', 'metric_function' : compute_f1_score_m, 'metric_type' : 'classif', 'h_is_b' : True },
    {'metric_name' : 'CO2 Emissions', 'metric_function' : compute_emissionCO2_classification, 'metric_type' : 'classif', 'h_is_b' : False },
    {'metric_name' : 'Inference time', 'metric_function' : compute_inferenceTime_classification, 'metric_type' : 'classif', 'h_is_b' : False },
    {'metric_name' : 'Balanced accuracy adjusted', 'metric_function' : compute_balanced_accuracy_adjusted, 'metric_type' : 'classif', 'h_is_b' : True },
    {'metric_name' : 'Trust Score', 'metric_function' : compute_NetTrustScore_b, 'metric_type' : 'classif', 'h_is_b' : True },
    {'metric_name' : 'Expected calibration error', 'metric_function' : compute_expected_calibration_error_b, 'metric_type' : 'classif', 'h_is_b' : True },
    {'metric_name' : 'Matthews correlation', 'metric_function' : compute_Matthews_corr_coef_b, 'metric_type' : 'classif', 'h_is_b' : True },
#    {'metric_name' : 'Matthews correlation coeffficient m', 'metric_function' : compute_Matthews_corr_coef_m, 'metric_type' : 'classif', 'h_is_b' : True },
    {'metric_name' : 'Fairness DI demographic parity b', 'metric_function' : fairness_DI_demographic_parity_b, 'metric_type' : 'classif', 'h_is_b' : True },
#    {'metric_name' : 'Inference Time', 'metric_function' : compute_inferenceTime_classification, 'metric_type' : 'classif', 'h_is_b' : False }
]

def add_doc(m) :
    m['description'] = m['metric_function'].__doc__ 
    return m
d_metrics = [add_doc(m) for m in metrics]
