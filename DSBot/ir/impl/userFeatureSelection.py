from abc import abstractmethod

import numpy as np
import pandas as pd
from ir.ir_exceptions import LabelsNotAvailable, ClassifierNotAvailable
from ir.ir_operations import IROp, IROpOptions
from ir.ir_parameters import IRNumPar
from ir.modules.laplace import Laplace
from sklearn.feature_selection import VarianceThreshold
from sklearn.feature_selection import SelectKBest, SelectPercentile
from utils import ask_user
import asyncio

class IRUserFeatureSelection(IROp):
    def __init__(self, name, parameters=None, model = None):
        super(IRUserFeatureSelection, self).__init__(name,parameters if parameters is not None else [])
        #self._model = model(**{v.name: v.value for v in parameters if hasattr(self, v.name)})
        #self.labels = None


    def parameter_tune(self, dataset):
        pass

    def set_model(self, dataset):
        self.parameter_tune(dataset)
        for p,v in self.parameters.items():
            if hasattr(self._model,p):
                self._model.__setattr__(p,v.value)
        #self._param_setted = True

    def get_labels(self):
        if self.labels is None:
            raise LabelsNotAvailable
        return self.labels

    #TDB cosa deve restituire questa funzione?
    def run(self, result, session_id, **kwargs):
        if 'transformed_ds' in result:
            dataset = result['transformed_ds']
        elif 'new_dataset' in result:
            dataset = result['new_dataset']
        else:
            dataset = result['original_dataset'].ds

        ask_user('List the features you want to remove using a comma to separate them: '+ ','.join(dataset.columns))

        print(self.message_queue)
        self.message_queue.clean()
        while True:
            asyncio.sleep(100)
            if self.message_queue.has_message():
                reply = self.message_queue.pop()
                break
            if 'socketio' in kwargs:
                kwargs['socketio'].sleep(0)
        if 'socketio' in kwargs:
            kwargs['socketio'].sleep(0)

        reply = [x.strip() for x in reply.split(',')]
        for i in reply:
            dataset = dataset.drop(i, axis=1)
        result['transformed_ds'] = dataset
        return result

class IRGenericUserFeatureSelection(IROpOptions):
    def __init__(self):
        super(IRGenericUserFeatureSelection, self).__init__([IRUserFeatureSelection("userFeatureSelection")], "userFeatureSelection")
