from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from ir.ir_operations import IROp, IROpOptions
from ir.ir_parameters import IRNumPar
import math
import numpy as np
import pandas as pd
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
import matplotlib.pyplot as plt


class IRPerformance(IROp):
    def __init__(self, name, parameters, model=None):
        super(IRPerformance, self).__init__(name, parameters)
        #self._model = model(**{v.name: v.value for v in parameters})

class IRConfusionMatrix(IRPerformance):
    def __init__(self):
        super(IRConfusionMatrix, self).__init__("confusionMatrix",[], ConfusionMatrixDisplay)

    def parameter_tune(self, dataset):
        pass

    def run(self, result, session_id):
        n_classes = set(result['labels'].T.values[0])
        pred = np.array(result['predicted_labels'])
        y = result['y_test']
        cm = confusion_matrix(y, pred, labels=n_classes)
        disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels = n_classes)
        plt.title('Confusion Matrix')
        plt.savefig('./temp/temp_' + str(session_id) + '/confusionMatrix.png')
        if 'plot' not in result:
            result['plot'] = ['./temp/temp_' + str(session_id) + '/confusionMatrix.png']
        else:
            result['plot'].append('./temp/temp_' + str(session_id) + '/confusionMatrix.png')
        result['original_dataset'].name_plot = './temp/temp_' + str(session_id) + '/confusionMatrix.png'
        return result


class IRRegressionPerformance(IRPerformance):
    def __init__(self):
        super(IRRegressionPerformance, self).__init__("regressionPerformance", [])  # TODO: before, model was passed to IROp.parameters. is this correct?



    def run(self, result, session_id):
        def flatten(L):
            for item in L:
                try:
                    yield from flatten(item)
                except TypeError:
                    yield item

        pred = np.array(result['predicted_labels']).flatten()
        y = np.array(list(flatten(result['y_test'])))
        r2 = r2_score(y, pred)
        mse = mean_squared_error(y, pred)
        rmse = math.sqrt(mean_squared_error(y, pred))
        mae = mean_absolute_error(y, pred)
        performance = pd.DataFrame([r2,mse,rmse,mae], index =['r2','mse','rmse','mae'], columns=['Measure'])
        result['regressionPerformance'] = performance
        return result

class IRGenericPerformance(IROpOptions):
    def __init__(self):
        super(IRGenericPerformance, self).__init__([IRRegressionPerformance(), IRConfusionMatrix()], "regressionPerformance")