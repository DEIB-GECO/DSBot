import pandas as pd
from sklearn.impute._iterative import IterativeImputer
from ir.ir_operations import IROp, IROpOptions
from utils import *


class IRMissingValuesHandle(IROp):
    def __init__(self, name, parameters=None, model = None ):
        super(IRMissingValuesHandle, self).__init__(name, parameters if parameters is not None else [])
        self.labels = None

    def parameter_tune(self, dataset):
        pass

    def set_model(self, result):
        self._param_setted = True

    #TDB cosa deve restituire questa funzione?
    def run(self, result, session_id, **kwargs):
        dataset = get_last_dataset(result)
        sio = kwargs.get('socketio', None)
        cols2drop = list(filter(lambda c: dataset[c].isna().sum() > 0.5 * len(dataset), dataset.columns))
        for c in cols2drop:
            notify_user(f'Feature "{c}" has {dataset[c].isna().sum()/len(dataset)*100:.3f}% missing values. I will remove it.',
                        socketio= sio)

        dataset = dataset.drop(cols2drop,axis=1)
        result['new_dataset'] = dataset
        perc_row_mv = (dataset.isna().sum(axis=1) >0).sum()/len(dataset)*100
        notify_user(f'The {perc_row_mv:.3f}% of the rows have at least a missing value.', socketio=sio)
        if perc_row_mv < 5.:
            notify_user(f'I will remove those rows.', socketio=sio)
            return IRMissingValuesRemove().run(result, session_id)
        elif perc_row_mv < 10.:
            notify_user(f'I will infer the missing values.', socketio=sio)
            return IRMissingValuesFill().run(result, session_id)
        else:
            notify_user('Do you want to REMOVE or to FILL the rows with missing values?',socketio=sio)
            reply = ask_user_binary_option("Remove", "Fill", self.message_queue, socketio=sio)
            if reply=='Remove':
                notify_user('Ok, I will remove them.',socketio=sio)
                return IRMissingValuesRemove().run(result, session_id)
            else:
                notify_user('Ok, I will fill them.', socketio=sio)
                return IRMissingValuesFill().run(result, session_id)

    def write(self, session_id):
        with open(f'temp/temp_{session_id}/code.py', 'a') as f:
            f.write('cols2drop = list(filter(lambda c: dataset[c].isna().sum() > 0.5 * len(dataset), dataset.columns))\n')
            f.write('dataset = dataset.drop(cols2drop,axis=1)\n')

class IRMissingValuesRemove(IRMissingValuesHandle):
    def __init__(self):
        super(IRMissingValuesRemove, self).__init__("missingValuesRemove")

    def parameter_tune(self, dataset):
        pass

    def run(self, result, session_id):
        result['new_dataset'] = get_last_dataset(result).dropna()
        return result

    def write(self, session_id):
        with open(f'temp/temp_{session_id}/code.py', 'a') as f:
            f.write('dataset = dataset.dropna()\n')

class IRMissingValuesFill(IRMissingValuesHandle):
    def __init__(self):
        super(IRMissingValuesFill, self).__init__("missingValuesFill")

    def parameter_tune(self, dataset):
        pass

    def run(self, result, session_id):
        dataset = get_last_dataset(result)

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
            dataset = pd.DataFrame(imp.fit_transform(dataset), columns=dataset.columns)

        #dataset = dataset.apply(lambda col: col.fillna(self.parameter))
        result['new_dataset'] = dataset
        print('missingvalfill', dataset.shape)

        return result

    def write(self, session_id):
        with open(f'temp/temp_{session_id}/code.py', 'a') as f:
            f.write('from sklearn.impute._iterative import IterativeImputer')
            f.write('imp = IterativeImputer(max_iter=10, random_state=0)\n')
            f.write('if len(original_dataset.cat_cols) > 0:\n')
            f.write('\tvalues_col = dataset.columns.difference(original_dataset.cat_cols)\n')
            f.write('\tif len(values_col)>0:\n')
            f.write('\t\tvalues_dataset = pd.DataFrame(imp.fit_transform(dataset[values_col]))\n')
            f.write('\t\tvalues_dataset.columns = values_col\n')
            f.write('\t\tcat_dataset = dataset[original_dataset.cat_cols].apply(lambda col: col.fillna(col.value_counts().index[0]))\n')
            f.write('\t\tdataset = pd.concat([cat_dataset, values_dataset],axis=1)\n')
            f.write('\telse:\n')
            f.write('\t\tcat_dataset = dataset[original_dataset.cat_cols].apply(lambda col: col.fillna(col.value_counts().index[0]))\n')
            f.write('\t\tdataset = cat_dataset\n')
            f.write('else:\n')
            f.write('dataset = pd.DataFrame(imp.fit_transform(dataset), columns=dataset.columns))\n')

class IRGenericMissingValues(IROpOptions):
    def __init__(self):
        super(IRGenericMissingValues, self).__init__([IRMissingValuesHandle('missingValuesHandle'), IRMissingValuesRemove(), IRMissingValuesFill()],
                                                     "missingValuesHandle")