from abc import abstractmethod

from ir.ir_exceptions import LabelsNotAvailable
from ir.ir_operations import IROp, IROpOptions
from ir.ir_parameters import IRNumPar, IRCatPar
from sklearn.experimental import enable_halving_search_cv
from sklearn.model_selection import GridSearchCV, HalvingRandomSearchCV
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.model_selection import train_test_split, KFold
from tpot import TPOTRegressor
from sklearn.metrics import accuracy_score
from sklearn.model_selection import StratifiedKFold
from utils import *
import numpy as np
import time

class IRRegression(IROp):
    def __init__(self, name, parameters, model = None):
        super(IRRegression, self).__init__(name,parameters)
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
        self.parameter_tune(result, dataset, labels)
        for p,v in self.parameters.items():
            self._model.__setattr__(p,self.parameters[p].value)
        self._param_setted = True

    def get_labels(self):
        if self.labels is None:
            raise LabelsNotAvailable
        return self.labels

    #TDB cosa deve restituire questa funzione?
    def run(self, result, session_id):
        if not self._param_setted:
            self.set_model(result)

        dataset = get_last_dataset(result)
        labels = result['labels'].values

        print('PARAMETERS', self.parameters)
        result['predicted_labels'] = []
        result['y_test'] = []
        result['feat_imp'] = []

        for train_index, test_index in StratifiedKFold(5, shuffle=True).split(dataset,labels):
            result['predicted_labels'] += list(self._model.fit(dataset.values[train_index], np.array(labels[train_index]).ravel()).predict(dataset.values[test_index]))
            result['y_test'] += labels[test_index]

        result['regressor'] = self._model
        result['original_dataset'].measures.update({p:self.parameters[p].value for p,v in self.parameters.items()})
        return result

class IRAutoRegression(IRRegression):
    def __init__(self):
        super(IRAutoRegression, self).__init__("autoRegression",
                                               [IRNumPar("generations", 5, "int", 2, 10, 1),
                                                # TODO: what is the maximum? Which first value give?
                                                IRNumPar("population_size", 50, "int", 10, 100, 10),
                                                IRNumPar('verbosity', 2, "int", 2, 2, 1),
                                                IRNumPar('n_jobs', -1, "int", -1, -1, 1),
                                                IRCatPar('scoring', 'neg_mean_squared_error', ['neg_mean_squared_error']),
                                                IRCatPar('cv', None, [None])],  # TODO: if I want to pass a list of values?
                                             TPOTRegressor)
        self._param_setted = False

    def parameter_tune(self, result, dataset, labels):
        pass

    def run(self, result, session_id):
        start_time = time.time()
        if not self._param_setted:
            self.set_model(result)
        dataset = get_last_dataset(result)
        labels = result['labels'].values
        scores = {}
        for i in IRGenericRegression().all_models:
            if i.name != 'autoRegression':
                print('MODEL', i.name)
                model = i
                result_tuning = model.parameter_tune(result, dataset, labels)
                scores[model.name] = {'model': model, 'parameters': result_tuning.best_params_,
                                      'score': result_tuning.best_score_}
        # print(scores)
        max_v = 0
        print(scores)
        for k, v in scores.items():
            print(v['score'])
            if max_v < v['score']:
                max_v = v['score']
                extracted_best_model = type(v['model']._model)(
                    **{name: value for name, value in v['parameters'].items()})
                print('CHOSEN MODEL', extracted_best_model)
                print(v['parameters'])

        # decorators.MAX_EVAL_SECS = 100
        result['predicted_labels'] = []
        result['y_test'] = []
        result['y_score'] = []
        result['feat_imp'] = []
        # model = self._model
        # model.fit(dataset, np.array(labels).ravel())
        # model.export('tpot_exported_pipeline.py')
        # exctracted_best_model = model.fitted_pipeline_.steps[-1][1]
        print(extracted_best_model)
        result['regressor'] = extracted_best_model  # .fit(dataset, labels)
        acc = []

        for train_index, test_index in StratifiedKFold(5, shuffle=True).split(dataset,labels):

            extracted_best_model.fit(dataset.values[train_index], np.array(labels[train_index]).ravel())
            pred = extracted_best_model.predict(dataset.values[test_index])

            if result['predicted_labels'] != []:
                result['predicted_labels'] = np.concatenate((result['predicted_labels'], pred))
                # result['y_score'] = np.concatenate((result['y_score'], model.predict_proba(x_test)))
            else:
                result['predicted_labels'] = pred
                # result['y_score'] = model.predict_proba(x_test)

            # exctracted_best_model = model.fitted_pipeline_.steps[-1][1]

            if result['y_score'] != []:
                result['y_test'] = np.vstack((result['y_test'], labels[test_index]))
                try:
                    result['y_score'] = np.vstack(
                        (result['y_score'], extracted_best_model.predict_proba(dataset.values[test_index])))
                except AttributeError:
                    result['y_score'] = np.vstack(
                        (result['y_score'], extracted_best_model.decision_function(dataset.values[test_index])))
            else:
                result['y_test'] = labels[test_index]
                try:
                    result['y_score'] = extracted_best_model.predict_proba(dataset.values[test_index])
                except AttributeError:
                    result['y_score'] = extracted_best_model.decision_function(dataset.values[test_index])

            acc.append(accuracy_score(labels[test_index], pred))

        mean_acc = np.array(acc).mean()
        print('ACCURACY', mean_acc)
        print('TIME: ', time.time() - start_time)
        self._param_setted = False
        return result

class IRLinearRegression(IRRegression):
    def __init__(self):
        super(IRLinearRegression, self).__init__("linearRegression",
                                             [],  # TODO: if I want to pass a list of values?
                                             LinearRegression)
        self._param_setted = False

    def parameter_tune(self, result, dataset, labels):
        pass

class IRRidgeRegression(IRRegression):
    def __init__(self):
        super(IRRidgeRegression, self).__init__("ridgeRegression",
                                             [IRNumPar('alpha', 1, "int", 0, 1, 0.01)],  # TODO: if I want to pass a list of values?
                                             Ridge)
        self._param_setted = False

    def parameter_tune(self, result, dataset, labels):
        random_grid = {p:(np.arange(d.min_v, d.max_v, d.step) if (d.v_type!='categorical' and d.possible_val==[]) else d.possible_val) for p,d in self.parameters.items()}
        # Random search of parameters, using 5 fold cross validation, search across 100 different combinations, and use all available cores
        search = HalvingRandomSearchCV(estimator=self._model, param_distributions=random_grid,scoring='neg_mean_absolute_error', cv=StratifiedKFold(3), n_jobs=-1)
        # perform the search
        search.fit(dataset, labels)
        for k,v in search.best_params_.items():
            self.parameters[k].value = v
        return search


class IRGenericRegression(IROpOptions):
    def __init__(self):
        super(IRGenericRegression, self).__init__([IRAutoRegression(), IRLinearRegression(), IRRidgeRegression()], "autoRegression")