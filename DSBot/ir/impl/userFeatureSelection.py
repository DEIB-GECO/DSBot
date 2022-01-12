from abc import abstractmethod

import numpy as np
import pandas as pd
from ir.ir_exceptions import LabelsNotAvailable, ClassifierNotAvailable
from ir.ir_operations import IROp, IROpOptions
from utils import ask_user, notify_user
from difflib import SequenceMatcher


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
        sio = kwargs.get('socketio', None)
        if 'transformed_ds' in result:
            dataset = result['transformed_ds']
        elif 'new_dataset' in result:
            dataset = result['new_dataset']
        else:
            dataset = result['original_dataset'].ds

        reply = ask_user('List the features you want to remove using a comma to separate them: '+ ','.join(dataset.columns),
                         self.message_queue,
                         socketio=sio)
        print(f"Uscita: {reply}")
        reply = [x.strip() for x in reply.split(',')]
        for i in reply:
            if i in dataset:
                dataset = dataset.drop(i, axis=1)
            else:
                for c in dataset.columns:
                    if SequenceMatcher(None, c.strip().lower(), i.strip().lower()).ratio() > 0.75:
                        dataset = dataset.drop(c, axis=1)
        notify_user(f"Ok, I will consider only columns {','.join(dataset.columns)}")
        print(dataset)
        result['transformed_ds'] = dataset
        return result

class IRGenericUserFeatureSelection(IROpOptions):
    def __init__(self):
        super(IRGenericUserFeatureSelection, self).__init__([IRUserFeatureSelection("userFeatureSelection")], "userFeatureSelection")
