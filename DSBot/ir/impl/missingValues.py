from abc import abstractmethod

import pandas as pd
import numpy as np
from sklearn.impute._iterative import IterativeImputer
from sklearn.preprocessing import StandardScaler, MinMaxScaler, LabelEncoder
from pandas.api.types import is_numeric_dtype
from ir.ir_operations import IROp, IROpOptions
from utils import ask_user
import asyncio
import time
from flask_socketio import SocketIO, emit
from app import sio

class IRMissingValuesHandle(IROp):
    def __init__(self, name, parameters=None, model = None ):
        super(IRMissingValuesHandle, self).__init__(name, parameters if parameters is not None else [])
        #self.parameter = parameters['value']  # FIXME: use self.get_param('value'), but it will raise UnknownParameter
        self.labels = None
        #self.message_queue = message_queue


    def parameter_tune(self, dataset):
        pass

    def set_model(self, result):
        if 'new_dataset' in result:
            dataset = result['new_dataset']
        else:
            dataset = result['original_dataset'].ds
        if self.parameter == None:
            self.parameter_tune(dataset)
        #for p,v in self.parameters.items():
        #    self._model.__setattr__(p,v.value)
        self._param_setted = True

    def question(self, ir, session_id):
        print(ir)
        ir_new = [x.name for x in ir]

        ir_new[ir_new.index(self.name)] = ask_user('Ciao vuoi togliere o no i dati mancanti?')
        print(ir_new)
        return ir_new

    #TDB cosa deve restituire questa funzione?
    def run(self, result, session_id, **kwargs):
        print('hey')
        if 'new_dataset' in result:
            dataset = result['new_dataset']
        else:
            dataset = result['original_dataset'].ds
        ask_user('Do you want to REMOVE the missing values or to FILL them?')
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

        if reply=='remove':
            print('remove')
            ask_user('I will remove them!')
            result = IRMissingValuesRemove().run(result, session_id)

        else:
            print('fill')
            ask_user('I will fill them!')
            result = IRMissingValuesFill().run(result, session_id)

        # if (dataset.isna().sum(axis=1)>0).sum()<0.05*len(dataset):
        #     result = IRMissingValuesRemove().run(result, session_id)
        # else:
        #     if (dataset.isna().sum(axis=1) > 0).sum() < 0.2 * len(dataset):
        #         result = IRMissingValuesFill().run(result, session_id)
        #     else:
        #         pass
                #AskModuleToUser(self, [IRMissingValuesRemove,IRMissingValuesFill])
        return result


class IRMissingValuesRemove(IRMissingValuesHandle):
    def __init__(self):
        super(IRMissingValuesRemove, self).__init__("missingValuesRemove")


    def parameter_tune(self, dataset):
        # TODO: implement
        pass

    def run(self, result, session_id):
        if 'new_dataset' in result:
            dataset = result['new_dataset']
        else:
            dataset = result['original_dataset'].ds

        dataset = dataset.dropna()
        result['new_dataset'] = dataset
        print('missingvalremove', dataset.shape)
        print(dataset.head())
        return result

class IRMissingValuesFill(IRMissingValuesHandle):
    def __init__(self):
        super(IRMissingValuesFill, self).__init__("missingValuesFill")

    def parameter_tune(self, dataset):
        pass

    def run(self, result, session_id):
        if 'new_dataset' in result:
            dataset = result['new_dataset']
        else:
            dataset = result['original_dataset'].ds

        imp = IterativeImputer(max_iter=10, random_state=0)
        if len(result['original_dataset'].cat_cols) > 0:
            values_col = dataset.columns.difference(result['original_dataset'].cat_cols)
            if len(values_col)>0:
                values_dataset = pd.DataFrame(imp.fit_transform(dataset[values_col]))
                values_dataset.columns = values_col
                cat_dataset = dataset[result['original_dataset'].cat_cols].apply(lambda col: col.fillna(col.value_counts().index[0]))
                dataset = pd.concat([cat_dataset, values_dataset],axis=1)
            else:
                cat_dataset = dataset[result['original_dataset'].cat_cols].apply(
                    lambda col: col.fillna(col.value_counts().index[0]))
                dataset = cat_dataset
        else:
            dataset = pd.DataFrame(imp.fit_transform(dataset))

        #dataset = dataset.apply(lambda col: col.fillna(self.parameter))
        result['new_dataset'] = dataset
        print('missingvalfill', dataset.shape)

        return result

class IRGenericMissingValues(IROpOptions):
    def __init__(self):
        super(IRGenericMissingValues, self).__init__([IRMissingValuesHandle('missingValuesHandle'), IRMissingValuesRemove(), IRMissingValuesFill()],
                                                     "missingValuesHandle")

    def run(self, **kwargs):
        ask_user('Do you want to REMOVE the missing values or to FILL them?')
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

        if reply == 'remove':
            print('remove')
            ask_user('I will remove them!')
            result = IRMissingValuesRemove()#.run(result, session_id)

        else:
            print('fill')
            ask_user('I will fill them!')
            result = IRMissingValuesFill()#.run(result, session_id)
        return result