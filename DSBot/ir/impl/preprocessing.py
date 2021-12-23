from abc import abstractmethod

import pandas as pd
import numpy as np
from sklearn.impute._iterative import IterativeImputer
from sklearn.preprocessing import StandardScaler, MinMaxScaler, LabelEncoder
from pandas.api.types import is_numeric_dtype
from ir.ir_operations import IROp, IROpOptions
from utils import *

class IRPreprocessing(IROp):
    def __init__(self, name, parameters=None, model = None):
        super(IRPreprocessing, self).__init__(name, parameters if parameters is not None else [])
        #self.parameter = parameters['value']  # FIXME: use self.get_param('value'), but it will raise UnknownParameter
        self.labels = None

    @abstractmethod
    def parameter_tune(self, dataset):
        pass

    def set_model(self, result):
        self._param_setted = True

    #TDB cosa deve restituire questa funzione?
    def run(self, result, session_id):
        pass


class IROneHotEncode(IRPreprocessing):
    def __init__(self):
        super(IROneHotEncode, self).__init__("oneHotEncode")

    def parameter_tune(self, dataset):
        # TODO: implement
        pass

    def run(self, result, session_id, **kwargs):
        dataset = get_last_dataset(result)
        cols = dataset.columns
        num_cols = dataset._get_numeric_data().columns
        cat_dataset = pd.get_dummies(dataset, columns=list(set(cols) - set(num_cols)))
        dataset = pd.concat([cat_dataset, dataset[num_cols]], axis=1)
        result['new_dataset'] = dataset
        print('onehotencode', dataset.shape)
        return result

class IRLabelOperation(IROp):
    def __init__(self, name, parameters=None, model = None):
        super(IRLabelOperation, self).__init__(name, parameters if parameters is not None else [])
        #self.parameter = parameters['value']  # FIXME: use self.get_param('value'), but it will raise UnknownParameter
        self.labels = None

    @abstractmethod
    def parameter_tune(self, dataset):
        pass

    def set_model(self, result):
        dataset = get_last_dataset(result)
        if self.parameter == None:
            self.parameter_tune(dataset)
        #for p,v in self.parameters.items():
        #    self._model.__setattr__(p,v.value)
        self._param_setted = True

    #TDB cosa deve restituire questa funzione?
    def run(self, result, session_id, **kwargs):
        pass

class IRLabelRemove(IRLabelOperation):

    def __init__(self):
        super(IRLabelRemove, self).__init__("labelRemove")

    def parameter_tune(self, dataset):
        # TODO: implement
        pass

    def run(self, result, session_id, **kwargs):
        label = result['labels']
        #print('labels', label.shape)
        if 'new_dataset' in result:
            dataset = result['new_dataset']
            dataset = dataset.drop(label, axis=1)
            print(dataset.shape)
            label = result['new_dataset'][label]
            print(len(dataset))
            print(len(label))

            if len(dataset)<len(label):
                label = label[set(dataset.index.values)]

        else:
            dataset = result['original_dataset'].ds
            print(dataset.shape)
            dataset = dataset.drop(label, axis=1)
            label = result['original_dataset'].ds[label]
        print(type(label))
        if result['original_dataset'].hasCategoricalLabel:
            if len(set(label.values))>2:
                label = LabelEncoder().fit_transform(label)
                print('encoded', type(label))
            else:
                label = label.replace(list(set(label))[0],0).replace(list(set(label))[1],1)
                print('replaced', type(label))
            label = pd.DataFrame(label)
        print(type(label))

        result['labels']=label
        result['new_dataset'] = dataset

        return result

class IRLabelAppend(IRLabelOperation):

    def __init__(self):
        super(IRLabelAppend, self).__init__("labelAppend")

    def parameter_tune(self, dataset):
        # TODO: implement
        pass

    def run(self, result, session_id, **kwargs):
        label = result['labels']
        #print('labels', label.shape)
        dataset = result['new_dataset']
        dataset[result['original_dataset'].label] = label
        result['new_dataset'] = dataset
        print(dataset)
        return result

class IRGenericLabelOperations(IROpOptions):
    def __init__(self):
        super(IRGenericLabelOperations, self).__init__([IRLabelRemove(), IRLabelAppend()],
                                                     "labelRemove")


class IROutliersRemove(IRPreprocessing):
    def __init__(self):
        super(IROutliersRemove, self).__init__("outliersRemove")

    def parameter_tune(self, dataset):
        # TODO: implement
        pass

    def run(self, result, session_id, **kwargs):
        sio = kwargs.get('socketio', None)
        if 'new_dataset' in result:
            dataset = result['new_dataset']
        else:
            dataset = result['original_dataset'].ds

        value_dataset = dataset.drop(list(result['original_dataset'].cat_cols), axis=1)
        print('len dataset', len(dataset))
        #df = dataset.drop(list(result['original_dataset'].cat_cols), axis=1)
        index_old = dataset.index.values
        value_dataset.index = np.arange(len(dataset))
        ds = value_dataset[((np.abs(value_dataset-value_dataset.mean()))<=(3*value_dataset.std())).sum(axis=1)>=0.9*value_dataset.shape[1]]
        perc_outliers = (len(ds)/len(dataset))*100
        notify_user(f'The {perc_outliers:.3f}% of the rows are outliers. I will remove them.', socketio=sio)
        if ds.shape[1]!=0 and ds.shape[0]!=0:
            print('len ds', ds.shape)
            result['new_dataset'] = ds
            if result['original_dataset'].hasLabel:
                label = pd.DataFrame(result['labels'])
                #print(label)
                label.index = np.arange(0, len(value_dataset))
                label = label.drop(set(value_dataset.index) - set(ds.index))
                result['labels'] = pd.DataFrame(label)#label.T.values
                #print(result['labels'] )
            index_new = pd.DataFrame(index_old).drop(set(value_dataset.index) - set(ds.index))
            print('len index', len(index_new))
            ds.index = index_new.iloc[:,0].values

            if len(result['original_dataset'].cat_cols)!=0:
                cat_dataset = dataset[list(result['original_dataset'].cat_cols)]
                cat_dataset.index = value_dataset.index
                cat_dataset = cat_dataset.T[index_new.index].T
                cat_dataset.index = index_new.iloc[:, 0].values
                ds = pd.concat([cat_dataset, ds], axis=1)
            result['new_dataset'] = ds
        return result

class IRStandardization(IRPreprocessing):
    def __init__(self):
        super(IRStandardization, self).__init__("standardization")

    def parameter_tune(self, dataset):
        # TODO: implement
        pass

    def run(self, result, session_id, **kwargs):
        print('STANDARDIZATION')
        dataset = get_last_dataset(result)
        dataset = pd.DataFrame(StandardScaler().fit_transform(dataset), index=dataset.index, columns=dataset.columns)
        result['new_dataset'] = dataset
        print(dataset)
        return result

class IRNormalization(IRPreprocessing):
    def __init__(self):
        super(IRNormalization, self).__init__("normalization")

    def parameter_tune(self, dataset):
        # TODO: implement
        pass

    def run(self, result, session_id, **kwargs):
        dataset = get_last_dataset(result)
        #dataset = dataset.drop(list(result['original_dataset'].cat_cols), axis=1)
        #df = dataset.drop(list(result['original_dataset'].cat_cols), axis=1)
        cat_dataset = dataset[result['original_dataset'].cat_cols]
        values_dataset = dataset.drop(list(result['original_dataset'].cat_cols), axis=1)
        values_dataset = pd.DataFrame(MinMaxScaler().fit_transform(values_dataset), index=values_dataset,
                                      columns=values_dataset.columns)
        # df = dataset.drop(list(result['original_dataset'].cat_cols), axis=1)
        dataset = pd.concat([cat_dataset, values_dataset], axis=1)
        result['new_dataset'] = dataset
        return result

class IRGenericPreprocessing(IROpOptions):
    def __init__(self):
        super(IRGenericPreprocessing, self).__init__([IRLabelRemove(), IROneHotEncode(), IROutliersRemove(), IRStandardization(), IRNormalization()],
                                                     "labelRemove")


