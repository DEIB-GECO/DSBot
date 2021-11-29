from abc import abstractmethod

from ir.ir_exceptions import LabelsNotAvailable
from ir.ir_operations import IROp, IROpOptions
from ir.ir_parameters import IRNumPar

from sklearn.linear_model import LinearRegression, Ridge
from sklearn.model_selection import train_test_split, KFold
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
                                             [],  # TODO: if I want to pass a list of values?
                                             Ridge)
        self._param_setted = False

    def parameter_tune(self, dataset, labels):
        pass


class IRGenericRegression(IROpOptions):
    def __init__(self):
        super(IRGenericRegression, self).__init__([IRLinearRegression(), IRRidgeRegression()], "linearRegression")