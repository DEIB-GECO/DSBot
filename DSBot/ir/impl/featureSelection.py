from abc import abstractmethod

import numpy as np
from ir.ir_exceptions import LabelsNotAvailable
from ir.ir_operations import IROp, IROpOptions
from ir.ir_parameters import IRPar
from ir.modules.laplace import Laplace

class IRFeatureSelection(IROp):
    def __init__(self, name, parameters, model = None):
        super(IRFeatureSelection, self).__init__(name,parameters)
        self._model = model(**{v.name: v.value for v in parameters})
        self.labels = None

    @abstractmethod
    def parameter_tune(self, dataset):
        pass

    def set_model(self, result):
        self.parameter_tune(result)
        for p,v in self.parameters.items():
            self._model.__setattr__(p,v.value)
        self._param_setted = True

    def get_labels(self):
        if self.labels is None:
            raise LabelsNotAvailable
        return self.labels

    #TDB cosa deve restituire questa funzione?
    def run(self, result, session_id):
        if 'new_dataset' in result:
            dataset = result['new_dataset']
        else:
            dataset = result['original_dataset'].ds
        if not self._param_setted:
            self.set_model(dataset)
        try:
            transformed_ds = self._model.fit_transform(dataset.values)
        except:
            transformed_ds = self._model.fit_transform(dataset.values)
        self.transformed_ds = transformed_ds
        if 'transformed_ds' not in result:
            result['transformed_ds'] = self.transformed_ds
        return result

class IRLaplace(IRFeatureSelection):
    def __init__(self):
        super(IRLaplace, self).__init__("laplace",
                                    [],  # TODO: what are minimum and maximum?
                                    Laplace)

    def parameter_tune(self, dataset):
        pass

    def run(self, result, session_id):
        if 'new_dataset' in result:
            dataset = result['new_dataset']
        else:
            dataset = result['original_dataset'].ds
        if not self._param_setted:
            self.set_model(dataset)
        try:
            transformed_ds = self._model.fit_transform(dataset.values)
        except:
            transformed_ds = self._model.fit_transform(dataset.values)
        self.transformed_ds = transformed_ds
        if 'transformed_ds' not in result:
            result['transformed_ds'] = self.transformed_ds
            print('laplace' , result['transformed_ds'])
        return result




class IRGenericFeatureSelection(IROpOptions):
    def __init__(self):
        super(IRGenericFeatureSelection, self).__init__([IRLaplace()], "laplace")