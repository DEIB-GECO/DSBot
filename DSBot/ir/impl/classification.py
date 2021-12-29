from abc import abstractmethod

from ir.ir_exceptions import LabelsNotAvailable
from ir.ir_operations import IROp, IROpOptions
from ir.ir_parameters import IRNumPar, IRCatPar
from tpot import TPOTClassifier
from sklearn.experimental import enable_halving_search_cv
from sklearn.model_selection import HalvingGridSearchCV
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import KFold
from collections import Counter
import numpy as np
from tpot import decorators
from utils import *

class IRClassification(IROp):
    def __init__(self, name, parameters, model = None):
        super(IRClassification, self).__init__(name,parameters)
        self._model = model(**{v.name: v.value for v in parameters})
        self.labels = None

    @abstractmethod
    def parameter_tune(self, result, dataset, labels):
        pass

    def set_model(self, result):
        if 'transformed_ds' in result:
            dataset = result['transformed_ds']
        elif 'new_dataset' in result:
            dataset = result['new_dataset']
        else:
            dataset = result['original_dataset'].ds
        labels = result['labels']

        result_tuning = self.parameter_tune(result, dataset, labels)
        for p,v in self.parameters.items():
            self._model.__setattr__(p,self.parameters[p].value)
        self._param_setted = True
        return result_tuning

    def get_labels(self):
        if self.labels is None:
            raise LabelsNotAvailable
        return self.labels

    def run(self, result, session_id):

        if not self._param_setted:
            self.set_model(result)

        result['predicted_labels'] = []
        result['y_score'] = []
        result['feat_imp'] = []

        for x_train, x_test, y_train,y_test in zip(result['x_train'],result['x_test'],result['y_train'],result['y_test']):
            result['predicted_labels'] += list(self._model.fit(x_train, y_train).predict(x_test))
            result['y_score'] += list(self._model.predict_proba(x_test))
        result['classifier'] = self._model
        self._param_setted = False
        return result

class IRAutoClassification(IRClassification):
    def __init__(self):
        super(IRAutoClassification, self).__init__("autoClassification",
                                             [IRNumPar("generations", 3, "int", 2, 10, 1),
                                              # TODO: what is the maximum? Which first value give?
                                              IRNumPar("population_size", 50, "int", 10, 100, 10),
                                              IRNumPar('verbosity', 2, "int", 2, 2, 1),
                                              IRNumPar('n_jobs', -1, "int", -1, -1, 1),
                                              IRCatPar('scoring', 'accuracy', ['accuracy']),
                                              IRCatPar('config_dict', 'TPOT light', ['Default TPOT','TPOT light', 'TPOT MDR'])],
                                             # TODO: if I want to pass a list of values?,

                                             TPOTClassifier)
        self._param_setted = False

    def get_labels(self):
        if self.labels is None:
            raise LabelsNotAvailable
        return self.labels

    def parameter_tune(self, result, dataset, labels):
        pass

    def run(self, result, session_id):
        if not self._param_setted:
            self.set_model(result)

        dataset = get_last_dataset(result)
        labels = result['labels'].values
        scores = {}
        count = 0
        for i in IRGenericClassification().all_models:
            if i.name!='autoClassification':
                print('MODEL', i.name)
                model = i
                if count==len(result['x_train']):
                    count = 0
                result_tuning = model.parameter_tune(result,result['x_train'][count],result['y_train'][count])
                count += 1
                scores[model.name]= {'model': model, 'parameters':result_tuning.best_params_, 'score':result_tuning.best_score_}
        #print(scores)
        max_v = 0
        for k,v in scores.items():
            if max_v<v['score']:
                max_v = v
                exctracted_best_model = v['model']
                for p in exctracted_best_model.parameters:
                    p.value = v['parameters'][p]
                    exctracted_best_model.__setattr__(p, self.parameters[p].value)

        #decorators.MAX_EVAL_SECS = 100
        result['predicted_labels'] = []
        result['y_score'] = []
        result['feat_imp'] = []
        #model = self._model
        #model.fit(dataset, np.array(labels).ravel())
        #model.export('tpot_exported_pipeline.py')
        #exctracted_best_model = model.fitted_pipeline_.steps[-1][1]
        print(exctracted_best_model)
        result['classifier'] = exctracted_best_model#.fit(dataset, labels)
        for x_train, x_test, y_train,y_test in zip(result['x_train'],result['x_test'],result['y_train'],result['y_test']):
            #model.fit(x_train, np.array(y_train).ravel())
            exctracted_best_model.fit(x_train, np.array(y_train).ravel())
            if result['predicted_labels']!=[]:
                result['predicted_labels'] = np.concatenate((result['predicted_labels'],exctracted_best_model.predict(x_test)))
                #result['y_score'] = np.concatenate((result['y_score'], model.predict_proba(x_test)))
            else:
                result['predicted_labels'] = exctracted_best_model.predict(x_test)

                #result['y_score'] = model.predict_proba(x_test)
            #exctracted_best_model = model.fitted_pipeline_.steps[-1][1]

            if result['y_score']!=[]:
                try:
                    result['y_score'] = np.vstack((result['y_score'],exctracted_best_model.predict_proba(x_test)))
                except AttributeError:
                    result['y_score'] = np.vstack((result['y_score'],exctracted_best_model.decision_function(x_test)))

            else:
                try:
                    result['y_score'] = exctracted_best_model.predict_proba(x_test)
                except AttributeError:
                    result['y_score'] = exctracted_best_model.decision_function(x_test)
            #print(result['y_score'])


        #print(result['y_score'])
        #result['y_score'] = result['predicted_labels']

        self._param_setted = False
        return result

    def write(self,session_id):
        pass

class IRRandomForest(IRClassification):
    def __init__(self):
        super(IRRandomForest, self).__init__("randomForest",
                                             [IRCatPar('criterion', 'gini',  ["gini", "entropy"]),
                                              IRCatPar('bootstrap', True,  [True, False]),
                                              IRNumPar("n_estimators", 100, "int", 100, 110, 10),
                                              #IRNumPar("max_features", 0.05, "float", 0.05, 1.01, 0.05),
                                              IRNumPar("min_samples_split", 2, "int", 2, 21, 1),
                                              IRNumPar("min_samples_leaf", 1, "int", 1, 21, 1)],
                                             RandomForestClassifier)
        self._param_setted = False

    def parameter_tune(self, result, dataset, labels):
        random_grid = {p:(np.arange(d.min_v, d.max_v, d.step) if type(d).__name__=='IRNumPar' else d.possible_val) for p,d in self.parameters.items()}
        rf_random = HalvingGridSearchCV(estimator=self._model, param_grid=random_grid, verbose=2, n_jobs=-1, cv=KFold(3))
        rf_random.fit(dataset, np.array(labels).ravel())
        for k,v in rf_random.best_params_.items():
            self.parameters[k].value = v
        return rf_random


class IRLogisticRegression(IRClassification):
    def __init__(self):
        super(IRLogisticRegression, self).__init__("logisticRegression",
                                                   [IRNumPar('C', 1e-4, 'float', arr = [1e-4, 1e-3, 1e-2, 1e-1, 0.5, 1., 5., 10., 15., 20., 25.]),
                                                    IRCatPar("penalty", "l2", ["l1","l2"])],  # TODO: if I want to pass a list of values?
                                                   LogisticRegression)
        self._param_setted = False

    def parameter_tune(self, result, dataset, labels):
        random_grid = {p:np.arange(d.min_v, d.max_v, d.step) for p,d in self.parameters.items() if d.v_type!='categorical'}
        # Random search of parameters, using 5 fold cross validation, search across 100 different combinations, and use all available cores
        lr_random = HalvingGridSearchCV(estimator=self._model, param_grid=random_grid, cv=KFold(3), n_jobs=-1)
        lr_random.fit(dataset,np.array(labels).ravel())
        for k in lr_random.best_params_:
            self.parameters[k].value = lr_random.best_params_[k]
        return lr_random


class IRKNeighborsClassifier(IRClassification):
    def __init__(self):
        super(IRKNeighborsClassifier, self).__init__("kNeighborsClassifier",
                                                   [IRNumPar("n_neighbors", 1, "int", 1, 101, 1),
                                                    IRCatPar('weights', 'uniform',["uniform", "distance"]),
                                                    IRNumPar('p', 'int', 1, arr=[1,2])],  # TODO: if I want to pass a list of values?
                                                   KNeighborsClassifier)
        self._param_setted = False

    def parameter_tune(self, result, dataset, labels):
        random_grid = {p:np.arange(d.min_v, d.max_v, d.step) for p,d in self.parameters.items() if d.v_type!='categorical'}
        # Random search of parameters, using 5 fold cross validation, search across 100 different combinations, and use all available cores
        kn_random = HalvingGridSearchCV(estimator=self._model, param_grid=random_grid, cv=KFold(3), n_jobs=-1)
        kn_random.fit(dataset,np.array(labels).ravel())#.values)
        print(kn_random.best_params_.items)
        for k in kn_random.best_params_:
            self.parameters[k].value = kn_random.best_params_[k]
        return kn_random


class IRAdaBoostClassifier(IRClassification):
    def __init__(self):
        super(IRAdaBoostClassifier, self).__init__("adaBoostClassifier",
                                                   [IRNumPar("n_estimators", 100, "int", 50, 150, 10)],  # TODO: if I want to pass a list of values?
                                                   AdaBoostClassifier)
        self._param_setted = False

    def parameter_tune(self, result, dataset, labels):
        random_grid = {p:np.arange(d.min_v, d.max_v, d.step) for p,d in self.parameters.items() if d.v_type!='categorical'}
        # Random search of parameters, using 5 fold cross validation, search across 100 different combinations, and use all available cores
        ab_random = HalvingGridSearchCV(estimator=self._model, param_grid=random_grid,  cv=KFold(3), n_jobs=-1)
        ab_random.fit(dataset, np.array(labels).ravel())
        print(ab_random.best_params_.items)
        for k in ab_random.best_params_:
            self.parameters[k].value = ab_random.best_params_[k]
        return ab_random

class IRGenericClassification(IROpOptions):
    def __init__(self):
        super(IRGenericClassification, self).__init__([IRAutoClassification(),  IRRandomForest(), IRLogisticRegression(), IRKNeighborsClassifier(), IRAdaBoostClassifier()], "autoClassification")



