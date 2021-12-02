from abc import abstractmethod

from ir.ir_exceptions import LabelsNotAvailable
from ir.ir_operations import IROp, IROpOptions
from ir.ir_parameters import IRNumPar, IRCatPar
from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.model_selection import train_test_split, KFold
from tpot import TPOTRegressor
import numpy as np


class IRRegression(IROp):
    def __init__(self, name, parameters, model = None):
        super(IRRegression, self).__init__(name,parameters)
        self._model = model(**{v.name: v.value for v in parameters})
        self.labels = None

    @abstractmethod
    def parameter_tune(self, dataset):
        pass

    def set_model(self, result):
        if 'transformed_ds' in result:
            dataset = result['transformed_ds']
        elif 'new_dataset' in result:
            dataset = result['new_dataset']
        else:
            dataset = result['original_dataset'].ds
        labels = result['labels']
        self.parameter_tune(dataset, labels)
        for p,v in self.parameters.items():
            print(p,v)
            self._model.__setattr__(p,self.parameters[p].value)
        self._param_setted = True

    def get_labels(self):
        if self.labels is None:
            raise LabelsNotAvailable
        return self.labels

    #TDB cosa deve restituire questa funzione?
    def run(self, result, session_id):
        print(self._param_setted)
        if not self._param_setted:
            self.set_model(result)

        if 'transformed_ds' in result:
            dataset = result['transformed_ds']
        elif 'new_dataset' in result:
            dataset = result['new_dataset']
        else:
            dataset = result['original_dataset'].ds

        print('PARAMETERSSSS', self.parameters)
        result['predicted_labels'] = []
        result['y_score'] = []
        result['feat_imp'] = []

        for x_train, x_test, y_train, y_test in zip(result['x_train'], result['x_test'], result['y_train'],
                                                    result['y_test']):
            result['predicted_labels'] += list(self._model.fit(x_train, y_train).predict(x_test))

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

    def parameter_tune(self, dataset, labels):
        pass

    def run(self, result, session_id):
        if not self._param_setted:
            self.set_model(result)
        if 'transformed_ds' in result:
            dataset = result['transformed_ds']
        elif 'new_dataset' in result:
            dataset = result['new_dataset']
        else:
            dataset = result['original_dataset'].ds
        labels = result['labels'].values
        result['predicted_labels'] = []
        result['y_score'] = []
        result['feat_imp'] = []

        for x_train, x_test, y_train,y_test in zip(result['x_train'],result['x_test'],result['y_train'],result['y_test']):

            model = self._model
            model.fit(x_train, y_train.ravel())

            #print(type(model.predict_proba(x_test)))
            if result['predicted_labels']!=[]:
                result['predicted_labels'] = np.concatenate((result['predicted_labels'],model.predict(x_test)))
                #result['y_score'] = np.concatenate((result['y_score'], model.predict_proba(x_test)))
            else:
                result['predicted_labels'] = model.predict(x_test)
            exctracted_best_model = model.fitted_pipeline_.steps[-1][1]
            result['regressor'] = exctracted_best_model.fit(x_train, y_train.ravel())
                #result['y_score'] = model.predict_proba(x_test)
        print(result['predicted_labels'] )
        #print(result['y_score'])
        result['y_score'] = result['predicted_labels']

        self._param_setted = False
        return result

class IRLinearRegression(IRRegression):
    def __init__(self):
        super(IRLinearRegression, self).__init__("linearRegression",
                                             [],  # TODO: if I want to pass a list of values?
                                             LinearRegression)
        self._param_setted = False

    def parameter_tune(self, dataset, labels):
        pass

class IRRidgeRegression(IRRegression):
    def __init__(self):
        super(IRRidgeRegression, self).__init__("ridgeRegression",
                                             [IRNumPar('alpha', 1, "int", 0, 1, 0.01)],  # TODO: if I want to pass a list of values?
                                             Ridge)
        self._param_setted = False

    def parameter_tune(self, dataset, labels):
        grid = dict()
        grid['alpha'] = np.arange(self.parameters['alpha'].min_v, self.parameters['alpha'].max_v, self.parameters['alpha'].step)
        # define search
        search = GridSearchCV(self._model, grid, scoring='neg_mean_absolute_error', cv=KFold(5, shuffle=True), n_jobs=-1)
        # perform the search
        search.fit(dataset, labels)
        for k,v in search.best_params_.items():
            self.parameters[k].value = v


class IRGenericRegression(IROpOptions):
    def __init__(self):
        super(IRGenericRegression, self).__init__([IRAutoRegression(), IRLinearRegression(), IRRidgeRegression()], "autoRegression")