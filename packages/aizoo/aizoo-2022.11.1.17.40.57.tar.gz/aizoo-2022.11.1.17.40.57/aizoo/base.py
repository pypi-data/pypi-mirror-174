#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : aizoo.
# @File         : oof
# @Time         : 2021/9/14 下午3:42
# @Author       : yuanjie
# @WeChat       : 313303303
# @Software     : PyCharm
# @Description  : todo: 增加nn模型


# ME
from meutils.pipe import *
from aizoo.model_utils import get_imp
from sklearn.model_selection import ShuffleSplit, StratifiedKFold, train_test_split


class AdversarialValidation(object):
    """Adversarial Validation
    通过对抗验证确定最优拆分折数
    """

    def __init__(self, params=None, importance_type='split', fit_params=None):
        self.params = params if params is not None else {}

        self.params['metric'] = 'auc'

        self._importance_type = importance_type
        self.feature_importances_ = None

        self.fit_params = fit_params if fit_params is not None else {}

    def fit(self, X, y, cv=5, split_seed=777):
        self.feature_importances_ = np.zeros((cv, X.shape[1]))

        _ = enumerate(StratifiedKFold(cv, shuffle=True, random_state=split_seed).split(X, y))

        metrics = []
        for n_fold, (train_index, valid_index) in tqdm(_, desc='Train🔥'):
            print(f"\033[94mFold {n_fold + 1} started at {time.ctime()}\033[0m")
            # X_train, y_train = X[train_index], y[train_index]
            # X_valid, y_valid = X[valid_index], y[valid_index]
            X_train, X_valid = X[train_index], X[valid_index]

            y_ = np.zeros(len(X_train) + len(X_valid))
            y_[:len(X_train)] = 0
            y_[len(X_train):] = 1

            X_train, X_valid, y_train, y_valid = train_test_split(np.r_[X_train, X_valid], y_, stratify=y_)
            eval_set = [(X_train, y_train), (X_valid, y_valid)]

            import lightgbm as lgb

            estimator = lgb.LGBMClassifier()
            estimator.set_params(**self.params)

            fit_params = dict(
                eval_set=eval_set,
                eval_metric=None,
                eval_names=('Train🔥', 'Valid'),
                verbose=100,
                early_stopping_rounds=100,
            )

            estimator.fit(
                X_train, y_train,
                **{**fit_params, **self.fit_params}  # fit_params
            )
            metrics.append(estimator.best_score_['Valid']['auc'])

            # 记录特征重要性
            self.feature_importances_[n_fold] = get_imp(estimator, X_train, self._importance_type)

        _ = np.array(metrics)
        print(f"\n\033[94mValid: {_.mean():.6f} +/- {_.std():.6f} \033[0m\n")

        self.metrics = _  # auc、std 越小说明拆分的数据分布越接近

        return _.mean(), _.std()


class OOF(object):

    def __init__(self, params=None, fit_params=None, task='Classifier', importance_type='split'):
        """

        @param params:
        @param fit_params:
        @param weight_func:
        @param task: Classifier or Regressor
        """
        self.task = task
        self.params = params if params is not None else {}
        self.fit_params = fit_params if fit_params is not None else {}

        self._estimators = []  # 每一折的模型
        self._importance_type = importance_type
        self.feature_importances_ = None

    @abstractmethod
    def _fit(self, X_train, y_train, w_train, X_valid, y_valid, w_valid, X_test, **kwargs):
        """
            返回estimator fit_params, 返回estimator需要有fit，predict方法
        """
        raise NotImplementedError

    def predict(self, X):

        func = lambda e: e.predict(X)

        return np.array(list(map(func, self._estimators))).mean(0)

    def fit(self, X, y, sample_weight=None, X_test=None, feval=None, cv=5, split_seed=777, target_index=None):
        """

        @param X:
        @param y:
        @param sample_weight:
        @param X_test:
        @param feval:
        @param cv:
        @param split_seed:
        @param target_index:
            固定目标域索引用于 valid
        @return:
        """
        X_test = X_test if X_test is not None else X[:66]

        self.feature_importances_ = np.zeros((cv, X.shape[1]))

        if self.task == 'Regressor':
            self.oof_train_proba = np.zeros(len(X))
            self.oof_test_proba = np.zeros(len(X_test))
            _ = enumerate(ShuffleSplit(cv, random_state=split_seed).split(X, y))  # todo: 兼容时间序列

        elif self.task == 'Classifier':
            num_classes = len(set(y))
            assert num_classes < 128, "是否是分类问题"
            self.oof_train_proba = np.zeros([len(X), num_classes])
            self.oof_test_proba = np.zeros([len(X_test), num_classes])
            _ = enumerate(StratifiedKFold(cv, shuffle=True, random_state=split_seed).split(X, y))
        else:
            raise ValueError("TaskTypeError⚠️")

        valid_metrics = []
        for n_fold, (train_index, valid_index) in tqdm(_, desc='Train 🐢'):
            print(f"\033[94mFold {n_fold + 1} started at {time.ctime()}\033[0m")

            valid_index_ = self._target_index(target_index, valid_index)  # 固定验证集, 用于早停 valid_index包含valid_index_

            X_train, y_train = X[train_index], y[train_index]
            X_valid, y_valid = X[valid_index_], y[valid_index_]

            if sample_weight is None:
                w_train, w_valid = None, None
            else:
                w_train, w_valid = sample_weight[train_index], sample_weight[valid_index_]

            ##############################################################
            estimator, fit_params = self._fit(X_train, y_train, w_train, X_valid, y_valid, w_valid, X_test)
            estimator.fit(
                X_train, y_train,
                **{**fit_params, **self.fit_params}  # fit_params
            )

            self.set_estimator_predict(estimator)  # 设定predic方法
            self._estimators.append(estimator)

            valid_predict, test_predict = map(estimator.predict, (X[valid_index], X_test))
            ##############################################################

            self.oof_train_proba[valid_index] = valid_predict
            self.oof_test_proba += test_predict / cv

            # 记录特征重要性
            self.feature_importances_[n_fold] = get_imp(self._estimators[-1], X_train, self._importance_type)

            if feval is not None:
                if self.oof_test_proba.shape[-1] == 2:  # 二分类
                    s = feval(y_valid, self.oof_train_proba[valid_index_, 1])  # 计算固定索引的cv值
                    valid_metrics.append(s)

                elif self.oof_test_proba.ndim == 1:  # 回归
                    s = feval(y_valid, self.oof_train_proba[valid_index_])
                    valid_metrics.append(s)  # 回归

        if self.oof_test_proba.shape[1] == 2:
            self.oof_train_proba = self.oof_train_proba[:, 1]
            self.oof_test_proba = self.oof_test_proba[:, 1]

        self.oof_train_test = np.r_[self.oof_train_proba, self.oof_test_proba]  # 方便后续stacking

        del X, X_test  # 释放内存

        if feval is not None:
            if target_index is None:
                self.oof_score = feval(y, self.oof_train_proba)
            else:
                _idx = list(target_index)
                self.oof_score = feval(y[_idx], self.oof_train_proba[_idx])  # 计算固定索引的cv值

            print("\n\033[94mScore Info:\033[0m")
            print(f"\033[94m     {cv:>2} CV: {self.oof_score:.6f}\033[0m")

            _ = np.array(valid_metrics)
            print(f"\033[94m     Valid: {_.mean():.6f} +/- {_.std():.6f} \033[0m\n")

            return self.oof_score

    @staticmethod
    def set_estimator_predict(estimator):
        if hasattr(estimator, 'predict_proba'):
            estimator.predict = estimator.predict_proba

        if 'TabNetRegressor' in str(estimator):
            estimator.predict = lambda X: estimator.predict(X).reshape(-1)  # NN回归会有尺寸不匹配问题

        if not hasattr(estimator, 'predict'):
            raise AttributeError("Don't exist predict⚠")

    def _target_index(self, target_index, valid_index):
        if target_index is not None:
            valid_index = list(set(target_index) & set(valid_index))
        return valid_index

    def oof_result_save(self, oof_file='submit.csv'):
        if self.oof_score:
            file_type = oof_file.split('.')[-1]
            oof_file = oof_file.replace(file_type, f"_{self.oof_score * 100:.4f}.file_type")
        pd.DataFrame({'oof': self.oof_train_test}).to_csv(oof_file, index=False)

    def opt_cv(self, X, y, feval, cv_choices=range(3, 16), **kwargs):
        scores = []
        for cv in cv_choices | xtqdm('opt cv🐢'):
            kwargs['cv'] = cv
            kwargs['feval'] = feval

            score = self.fit(X, y, **kwargs)

            scores.append((score, cv))

        return scores | xsort(True)

    def plot_feature_importances(self, feature_names=None, topk=20, figsize=None, pic_name=None):
        import seaborn as sns
        import matplotlib.pyplot as plt

        columns = ['Importances', 'Features']
        importances = self.feature_importances_.mean(0)

        if feature_names is None:
            feature_names = list(map(lambda x: f'F_{x}', range(len(importances))))

        _ = sorted(zip(importances, feature_names), reverse=True)
        self.df_feature_importances = pd.DataFrame(_, columns=columns)

        plt.figure(figsize=(14, topk // 5) if figsize is None else figsize)
        # sns.barplot(x=columns[0], y=columns[1], data=self.df_feature_importances[:topk])
        sns.barplot(x=self.df_feature_importances[:topk][columns[0]], y=self.df_feature_importances[:topk][columns[1]])

        plt.title(f'Features {self._importance_type.title()} Importances')
        plt.tight_layout()

        if pic_name is not None:
            plt.savefig(f'importances_{self.oof_score}.png')
