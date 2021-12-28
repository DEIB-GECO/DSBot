from ir.ir_exceptions import CorrelationNotAvailable
from ir.ir_operations import IROp, IROpOptions
from utils import *

class IRCorrelation(IROp):
    def __init__(self, name, model = None):
        super(IRCorrelation, self).__init__(name, [])  # TODO: before, model was passed to IROp.parameters. is this correct?
        self._model = model
        self.correlation = None

    def get_correlation(self):
        if self.correlation is None:
            raise CorrelationNotAvailable
        return self.correlation

    #TDB cosa deve restituire questa funzione?
    def run(self, result, session_id, **kwargs):
        sio = kwargs.get('socketio', None)
        if 'transformed_ds' in result:
            dataset = result['transformed_ds']
        elif 'new_dataset' in result:
            dataset = result['new_dataset']
        else:
            dataset = result['original_dataset'].ds
        print(dataset)
        correlation = dataset.corr(method=self._model)
        result['correlation'] = correlation
        print([result['correlation'][c].isna().sum() for c in result['correlation'].columns])
        cols2drop = [c for c in result['correlation'].columns if result['correlation'][c].isna().sum()>0.9*len(result['correlation'])]
        if len(cols2drop)>0:
            result['correlation'] = result['correlation'].drop(cols2drop,axis=1)
            result['correlation'] = result['correlation'].dropna()
            notify_user('I had to remove some columns after computing the correlation, probably because some features do not vary.', socketio=sio)
        print(result['correlation'])

        return result

class IRPearson(IRCorrelation):
    def __init__(self):
        super(IRPearson, self).__init__("pearson", 'pearson')


class IRSpearman(IRCorrelation):
    def __init__(self):
        super(IRSpearman, self).__init__("spearman", 'spearman')


class IRGenericCorrelation(IROpOptions):
    def __init__(self):
        super(IRGenericCorrelation, self).__init__([IRPearson(), IRSpearman()], "pearson")
