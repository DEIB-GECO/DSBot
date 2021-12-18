import pandas as pd
from sklearn.impute._iterative import IterativeImputer
from ir.ir_operations import IROp, IROpOptions
from utils import ask_user, get_last_dataset


class IRMissingValuesHandle(IROp):
    def __init__(self, name, parameters=None, model = None ):
        super(IRMissingValuesHandle, self).__init__(name, parameters if parameters is not None else [])
        #self.parameter = parameters['value']  # FIXME: use self.get_param('value'), but it will raise UnknownParameter
        self.labels = None

    def parameter_tune(self, dataset):
        pass

    def set_model(self, result):
        self._param_setted = True

    #TDB cosa deve restituire questa funzione?
    def run(self, result, session_id, **kwargs):
        dataset = get_last_dataset(result)
        col_drop = []
        for c in dataset.columns:
            if dataset[c].isna().sum() > 0.5 * len(dataset):
                col_drop.append(c)
        dataset = dataset.drop(col_drop,axis=1)
        result['new_dataset'] = dataset
        if (dataset.isna().sum(axis=1) > 0).sum() < 0.05 * len(dataset):
            print('meno del 5% di mv')
            result = IRMissingValuesRemove().run(result, session_id)
        else:
            if (dataset.isna().sum(axis=1) > 0).sum() < 0.10 * len(dataset):
                result = IRMissingValuesFill().run(result, session_id)
            else:
                reply = ask_user('Do you want to REMOVE the rows with missing values or to FILL them?',
                                 self.message_queue,
                                 socketio= kwargs['socketio'] if ('socketio' in kwargs) else None)

                if reply=='remove':
                    ask_user('I will remove them!',
                                 self.message_queue,
                                 socketio= kwargs['socketio'] if ('socketio' in kwargs) else None)
                    result = IRMissingValuesRemove().run(result, session_id)

                else:
                    ask_user('I will fill them!',
                                 self.message_queue,
                                 socketio= kwargs['socketio'] if ('socketio' in kwargs) else None)
                    result = IRMissingValuesFill().run(result, session_id)

        return result


class IRMissingValuesRemove(IRMissingValuesHandle):
    def __init__(self):
        super(IRMissingValuesRemove, self).__init__("missingValuesRemove")

    def parameter_tune(self, dataset):
        # TODO: implement
        pass

    def run(self, result, session_id):
        result['new_dataset'] = get_last_dataset(result).dropna()

        print('missingvalremove', get_last_dataset(result).shape)
        print(get_last_dataset(result).head())
        return result

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
            dataset = pd.DataFrame(imp.fit_transform(dataset))

        #dataset = dataset.apply(lambda col: col.fillna(self.parameter))
        result['new_dataset'] = dataset
        print('missingvalfill', dataset.shape)

        return result

class IRGenericMissingValues(IROpOptions):
    def __init__(self):
        super(IRGenericMissingValues, self).__init__([IRMissingValuesHandle('missingValuesHandle'), IRMissingValuesRemove(), IRMissingValuesFill()],
                                                     "missingValuesHandle")