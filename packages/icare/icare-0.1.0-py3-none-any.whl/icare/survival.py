from icare.base import IcareBase, BaggedIcareBase
from icare.metrics import uno_cindex, tAUC, harrell_cindex, abs_cindex


class IcareSurvival(IcareBase):
    """
        Icare estimator adapted to censored targets.
        This survival model assign weights of -1 or +1 to features to reduce
        overfitting risk. It evaluates features in univariate to reduce this risk
        even more.
        Predicts a continuous value that rank the samples (not calibrated).
        Parameters
        ----------
        rho : None or float in [0, 1[, default=None
            The threshold for the correlation removal. Is None, no feature
            removal is done. If defined, it will randomly drop a feature of
            each pair that has an absolute correlation > rho.
        correlation_method: 'pearson' or 'spearman', default='pearson'
            How to compute the correlation between feature
        sign_method: a string, default='tAUC,harrell,uno'
            Which method to use to determine the signs of the feature.
            It should be string containing at least one of :
            - 'harrell': Harrell's concordance index (C-index)
            - 'uno': 'Uno's concordance index (attempt to make Harrell's C-index
            more robust)
            - 'tAUC': time-dependant ROC-AUC
            If multiple method are selected, they should be separated by a comma. In such cases,
            only the features that have the same sign for all methods will be used by the model
        cmin: None or a float in [0.5, 1[, default=None
            The threshold for feature selection based on their scores with the
            signs method. For each score of each method abs_score is computed
            (defined by max(score, 1-score)). Then mean_abs_score is computed
            by averaging all abs_score. If mean_abs_score < cmin, the feature
            is dropped
        max_features: float in ]0,1], default=1
            Proportion of feature to randomly select at the beginning of the
            fitting. It happens before any feature selection.
        features_groups_to_use: None or list, default=None
            In a context where features are grouped (e.g. radiomic features)
            from the same mask, this is used to specify which groups should be
            used by the model. The random feature selection of max_features
            happens before this step. If None, all the features are kept.
            If this is defined, the argument feature_groups of the fit()
            function should be defined.
        mandatory_features: None or list, default=None
            List of feature to always include in the model.
        random_state : int, RandomState instance or None, default=None
            Control all the random steps of the model
    """

    def __init__(self,
                 rho=None,
                 correlation_method='pearson',
                 sign_method='tAUC,harrell,uno',
                 cmin=None,
                 max_features=1.,
                 features_groups_to_use=None,
                 mandatory_features=None,
                 random_state=None):

        sign_eval_method, sign_eval_criteria, abs_fnc = {}, {}, {}
        if 'uno' in sign_method:
            sign_eval_method['uno'] = uno_cindex
            sign_eval_criteria['uno'] = 0.5
            abs_fnc['uno'] = abs_cindex
        if 'tAUC' in sign_method:
            sign_eval_method['tAUC'] = tAUC
            sign_eval_criteria['tAUC'] = 0.5
            abs_fnc['tAUC'] = abs_cindex
        if 'harrell' in sign_method:
            sign_eval_method['harrell'] = harrell_cindex
            sign_eval_criteria['harrell'] = 0.5
            abs_fnc['harrell'] = abs_cindex

        super().__init__(
            rho=rho,
            correlation_method=correlation_method,
            sign_method=sign_method,
            cmin=cmin,
            max_features=max_features,
            features_groups_to_use=features_groups_to_use,
            mandatory_features=mandatory_features,
            random_state=random_state,
            sign_eval_method=sign_eval_method,
            sign_eval_criteria=sign_eval_criteria,
            abs_fnc=abs_fnc,
        )


class BaggedIcareSurvival(BaggedIcareBase):
    """
        Bagged IcareSurvival estimator.
        This survival model ensemble a set of IcareSurvival models with bootstrap
        resampling of their respective train sets. Once fitted, each model
        make a prediction and all their prediction are aggregated.
        Predicts a continuous value that rank the samples (not calibrated).
        Parameters
        ----------
        n_estimators : int >= 1, default=10
            How many IcareSurvival estimators should be used by the model
        parameters_sets : list of dictionaries or None, default=None
            A list a dictionaries. Each dictionary is a set of hyperparameters
            for the IcareSurvival estimator. If the length of this list is > 1, then
            each estimator will randomly pick one of the hyperparameters sets of
            the list. If None, the default parameters of IcareSurvival is used for
            all estimator.
        aggregation_method='mean' or 'median, default='mean'
            How to aggregate the predictions of the estimator.
        n_jobs=int, default=None
        The number of jobs to run in parallel. :meth:`fit` and :meth:`predict`
        are all parallelized over the estimators.
        None means 1. -1 means using all processors.
        random_state : int, RandomState instance or None, default=None
            Control all the random steps of the model
    """

    def __init__(self,
                 n_estimators=10,
                 parameters_sets=None,
                 aggregation_method='mean',
                 n_jobs=1,
                 random_state=None):
        super().__init__(
            estimator=IcareSurvival,
            n_estimators=n_estimators,
            parameters_sets=parameters_sets,
            aggregation_method=aggregation_method,
            n_jobs=n_jobs,
            random_state=random_state
        )
