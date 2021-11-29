from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from ir.ir_operations import IROp, IROpOptions
from ir.ir_parameters import IRNumPar
import math
import numpy as np
import pandas as pd


class IRPerformance(IROp):
    def __init__(self, name, parameters, model=None):
        super(IRPerformance, self).__init__(name, parameters)
        #self._model = model(**{v.name: v.value for v in parameters})


class IRRegressionPerformance(IRPerformance):
    def __init__(self):
        super(IRRegressionPerformance, self).__init__("regressionPerformance", [])  # TODO: before, model was passed to IROp.parameters. is this correct?



    def run(self, result, session_id):
        pred = np.array(result['predicted_labels']).flatten()
        print(pred)
        y = np.array(result['y_test']).flatten()
        print(y)
        r2 = r2_score(y, pred)
        mse = mean_squared_error(y, pred)
        rmse = math.sqrt(mean_squared_error(y, pred))
        mae = mean_absolute_error(y, pred)
        performance = pd.DataFrame([r2,mse,rmse,mae], index =['r2','mse','rmse','mae'], columns=['Measure'])
        result['regressionPerformance'] = performance
        return result

class IRGenericPerformance(IROpOptions):
    def __init__(self):
        super(IRGenericPerformance, self).__init__([IRRegressionPerformance()], "regressionPerformance")