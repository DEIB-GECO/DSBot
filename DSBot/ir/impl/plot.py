from abc import abstractmethod

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
from seaborn import scatterplot, clustermap
from matplotlib.pyplot import scatter

from ir.ir_exceptions import LabelsNotAvailable, PCADataNotAvailable
from ir.ir_operations import IROp, IROpOptions
from ir.ir_parameters import IRPar


class IRPlot(IROp):
    def __init__(self, name, parameters, model = None):
        super(IRPlot, self).__init__(name,parameters)
        self._model = model
        self.labels = None

    @abstractmethod
    def parameter_tune(self, dataset):
        pass

    def set_model(self, result):
        if 'new_dataset' in result:
            dataset = result['new_dataset']
        else:
            dataset = result['original_dataset']
        self.parameter_tune(dataset)
        for p,v in self.parameters.items():
            self._model.__setattr__(p,v.value)
        self._param_setted = True

    def get_labels(self):
        if self.labels is None:
            raise LabelsNotAvailable
        return self.labels

    #TDB cosa deve restituire questa funzione?
    def run(self, result):
        if 'new_dataset' in result:
            dataset = result['new_dataset']
        else:
            dataset = result['original_dataset']
        if not self._param_setted:
            self.set_model(dataset)
        try:
            self._model.fit_predict(dataset.ds.values)
        except:
            self._model.fit_predict(dataset)
        self.labels = self._model.labels_
        result['plot'] = self.labels
        return result

class IRScatterplot(IRPlot):
    def __init__(self):
        super(IRScatterplot, self).__init__("scatterplot",
                                            [],
                                            scatter)

    def parameter_tune(self, dataset):
        pass

    def run(self, result):
        if 'labels' not in result:
            raise LabelsNotAvailable
        else:
            u_labels = np.unique(result['labels'])

        if 'transformed_ds' not in result:
            raise PCADataNotAvailable
        else:
            transformed_ds = result['transformed_ds']

        #for i in u_labels:
        #    ax = scatter(transformed_ds[result['labels'] == i, 0], transformed_ds[result['labels'] == i, 1], label=i)

        if 'plot' not in result:
            result['plot'] = ["u_labels = np.unique(result['labels'])\nfor i in u_labels:\n\tax = plt.scatter(result['transformed_ds'][result['labels'] == i, 0], result['transformed_ds'][result['labels'] == i, 1], label=i)"]
        else:
            result['plot'].append("u_labels = np.unique(result['labels'])\nfor i in u_labels:\n\tax = plt.scatter(result['transformed_ds'][result['labels'] == i, 0], result['transformed_ds'][result['labels'] == i, 1], label=i)")
        return  result


class IRClustermap(IRPlot):
    def __init__(self):
        super(IRClustermap, self).__init__("clustermap",
                                           [],
                                           clustermap)

    def parameter_tune(self, dataset):
        pass

    def run(self, result):
        if 'transformed_ds' not in result:
            raise PCADataNotAvailable
        else:
            transformed_ds = result['transformed_ds']

        plt.figure(figsize=(15, 15))
        matplotlib.rcParams.update({'font.size': 18})

        cg = clustermap(transformed_ds, cmap='binary', xticklabels=False, yticklabels=False)
        cg.ax_row_dendrogram.set_visible(False)
        ax = cg.ax_heatmap

        if 'plot' not in result:
            result['plot'] = ax

        return  result

# FIXME: this class was commented out because the implementation raises errors
class IRGenericPlot(IROpOptions):
     def __init__(self):
         super(IRGenericPlot, self).__init__([IRScatterplot(), IRClustermap()], "scatterplot")
