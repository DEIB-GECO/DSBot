from abc import abstractmethod

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import seaborn as sns
from seaborn import scatterplot, clustermap
from matplotlib.pyplot import scatter, plot, boxplot
from sklearn.metrics import RocCurveDisplay
from seaborn import barplot
from sklearn.metrics import roc_curve, auc
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import label_binarize
from sklearn.metrics import roc_auc_score
from scipy import interp
from itertools import cycle
from ir.ir_exceptions import LabelsNotAvailable, PCADataNotAvailable, CorrelationNotAvailable, RulesNotAvailable
from ir.ir_operations import IROp, IROpOptions
from ir.ir_parameters import IRNumPar
from autoviz.AutoViz_Class import AutoViz_Class#Instantiate the AutoViz class


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
            dataset = result['original_dataset'].ds
        self.parameter_tune(dataset)
        for p,v in self.parameters.items():
            self._model.__setattr__(p,v.value)
        self._param_setted = True

    def get_labels(self):
        if self.labels is None:
            raise LabelsNotAvailable
        return self.labels

    #TDB cosa deve restituire questa funzione?
    def run(self, result, session_id):
        AV = AutoViz_Class()
        if 'new_dataset' in result:
            dataset = result['new_dataset']
        else:
            dataset = result['original_dataset'].ds
        fig = plt.figure()
        ax = AV.AutoViz("",sep=",", depVar="", dfte= dataset, verbose=2)

        plt.savefig('./temp/temp_' + str(session_id) + '/auto_plot.png')
        if 'plot' not in result:
            result['plot'] = ['./temp/temp_' + str(session_id) + '/auto_plot.png']
            # result['plot'] = ["u_labels = np.unique(result['labels'])\nfor i in u_labels:\n\tax = plt.scatter(result['transformed_ds'][result['labels'] == i, 0], result['transformed_ds'][result['labels'] == i, 1], label=i)"]
        else:
            result['plot'].append('./temp/temp_' + str(session_id) + '/auto_plot.png')
            # result['plot'].append("u_labels = np.unique(result['labels'])\nfor i in u_labels:\n\tax = plt.scatter(result['transformed_ds'][result['labels'] == i, 0], result['transformed_ds'][result['labels'] == i, 1], label=i)")

        result['original_dataset'].name_plot = './temp/temp_' + str(session_id) + '/auto_plot.png'
        return result

class IRScatterplot(IRPlot):
    def __init__(self):
        super(IRScatterplot, self).__init__("scatterplot",
                                            [],
                                            scatter)

    def parameter_tune(self, dataset):
        pass

    def run(self, result, session_id):
        if 'labels' not in result:
            raise LabelsNotAvailable
        else:
            u_labels = np.unique(result['labels'])

        if 'transformed_ds' not in result:
            raise PCADataNotAvailable
        else:
            transformed_ds = result['transformed_ds']

        fig = plt.figure()
        for i in u_labels:
            ax = scatter(transformed_ds[result['labels'] == i, 0], transformed_ds[result['labels'] == i, 1], label=i)
        plt.savefig('./temp/temp_' + str(session_id) + '/scatter.png')
        if 'plot' not in result:
            result['plot'] = ['./temp/temp_' + str(session_id) + '/scatter.png']
            #result['plot'] = ["u_labels = np.unique(result['labels'])\nfor i in u_labels:\n\tax = plt.scatter(result['transformed_ds'][result['labels'] == i, 0], result['transformed_ds'][result['labels'] == i, 1], label=i)"]
        else:
            result['plot'].append('./temp/temp_' + str(session_id) + '/scatter.png')
            #result['plot'].append("u_labels = np.unique(result['labels'])\nfor i in u_labels:\n\tax = plt.scatter(result['transformed_ds'][result['labels'] == i, 0], result['transformed_ds'][result['labels'] == i, 1], label=i)")

        result['original_dataset'].name_plot = './temp/temp_' + str(session_id) + '/scatter.png'

        # plt.show()
        return  result

class IRScatterAssociationRules(IRPlot):
    def __init__(self):
        super(IRScatterAssociationRules, self).__init__("scatterAssociationRules",
                                            [],
                                            scatter)

    def parameter_tune(self, dataset):
        pass

    def run(self, result, session_id):
        if 'associationRules' not in result:
            raise RulesNotAvailable
        else:
            rules = result['associationRules']
        fig, (ax1) = plt.subplots(3, figsize=(15, 30))
        ax1[0].scatter(rules['support'], rules['confidence'], alpha=0.5)
        ax1[0].set_xlabel('support')
        ax1[0].set_ylabel('confidence')
        ax1[0].set_title('Support vs Confidence')
        ax1[1].scatter(rules['support'], rules['lift'], alpha=0.5)
        ax1[1].set_xlabel('support')
        ax1[1].set_ylabel('lift')
        ax1[1].set_title('Support vs Lift')
        fit = np.polyfit(rules['lift'], rules['confidence'], 1)
        fit_fn = np.poly1d(fit)
        ax1[2].plot(rules['lift'], rules['confidence'], 'yo', rules['lift'],
                    fit_fn(rules['lift']))
        plt.savefig('./temp/temp_' + str(session_id) + '/scatter_associationRules.png')
        if 'plot' not in result:
            result['plot'] = ['./temp/temp_' + str(session_id) + '/scatter_associationRules.png']
            #result['plot'] = ["u_labels = np.unique(result['labels'])\nfor i in u_labels:\n\tax = plt.scatter(result['transformed_ds'][result['labels'] == i, 0], result['transformed_ds'][result['labels'] == i, 1], label=i)"]
        else:
            result['plot'].append('./temp/temp_' + str(session_id) + '/scatter_associationRules.png')
            #result['plot'].append("u_labels = np.unique(result['labels'])\nfor i in u_labels:\n\tax = plt.scatter(result['transformed_ds'][result['labels'] == i, 0], result['transformed_ds'][result['labels'] == i, 1], label=i)")

        result['original_dataset'].name_plot = './temp/temp_' + str(session_id) + '/scatter_associationRules.png'

        # plt.show()
        return  result

class IRDistplot(IRPlot):
    def __init__(self):
        super(IRDistplot, self).__init__("distplot",
                                            [],
                                            plot)

    def parameter_tune(self, dataset):
        pass

    #def run(self, result, session_id):
    #    pass
    #
    #     if 'transformed_ds' not in result:
    #         transformed_ds = result['original_dataset'].ds
    #     else:
    #         transformed_ds = result['transformed_ds']
    #
    #     fig = plt.figure()
    #     ax = plot(transformed_ds)
    #     plt.savefig('./temp/temp_' + str(session_id) + '/distplot.png')
    #     if 'plot' not in result:
    #         result['plot'] = ['./temp/temp_' + str(session_id) + '/distplot.png']
    #         #result['plot'] = ["u_labels = np.unique(result['labels'])\nfor i in u_labels:\n\tax = plt.scatter(result['transformed_ds'][result['labels'] == i, 0], result['transformed_ds'][result['labels'] == i, 1], label=i)"]
    #     else:
    #         result['plot'].append('./temp/temp_' + str(session_id) + '/distplot.png')
    #         #result['plot'].append("u_labels = np.unique(result['labels'])\nfor i in u_labels:\n\tax = plt.scatter(result['transformed_ds'][result['labels'] == i, 0], result['transformed_ds'][result['labels'] == i, 1], label=i)")
    #
    #     result['original_dataset'].name_plot = './temp/temp_' + str(session_id) + '/distplot.png'
    #
    #     # plt.show()
    #     return  result

class IRBoxplot(IRPlot):
    def __init__(self):
        super(IRBoxplot, self).__init__("boxplot",
                                            [],
                                            boxplot)

    def parameter_tune(self, dataset):
        pass

    #def run(self, result, session_id):
    #    pass
    #
    #     if 'transformed_ds' not in result:
    #         transformed_ds = result['original_dataset'].ds
    #     else:
    #         transformed_ds = result['transformed_ds']
    #
    #     fig = plt.figure()
    #     ax = boxplot(transformed_ds)
    #     plt.savefig('./temp/temp_' + str(session_id) + '/boxplot.png')
    #     if 'plot' not in result:
    #         result['plot'] = ['./temp/temp_' + str(session_id) + '/boxplot.png']
    #         #result['plot'] = ["u_labels = np.unique(result['labels'])\nfor i in u_labels:\n\tax = plt.scatter(result['transformed_ds'][result['labels'] == i, 0], result['transformed_ds'][result['labels'] == i, 1], label=i)"]
    #     else:
    #         result['plot'].append('./temp/temp_' + str(session_id) + '/boxplot.png')
    #         #result['plot'].append("u_labels = np.unique(result['labels'])\nfor i in u_labels:\n\tax = plt.scatter(result['transformed_ds'][result['labels'] == i, 0], result['transformed_ds'][result['labels'] == i, 1], label=i)")
    #
    #     result['original_dataset'].name_plot = './temp/temp_' + str(session_id) + '/boxplot.png'
    #
    #     # plt.show()
    #     return  result


class IRBarplot(IRPlot):
    def __init__(self):
        super(IRBarplot, self).__init__("barplot",
                                            [],
                                            barplot)

    def parameter_tune(self, dataset):
        pass

    #def run(self, result, session_id):
    #    pass
    #
    #     if 'transformed_ds' not in result:
    #         transformed_ds = result['original_dataset'].ds
    #     else:
    #         transformed_ds = result['transformed_ds']
    #
    #     fig = plt.figure()
    #     ax = barplot(transformed_ds)
    #     plt.savefig('./temp/temp_' + str(session_id) + '/barplot.png')
    #     if 'plot' not in result:
    #         result['plot'] = ['./temp/temp_' + str(session_id) + '/barplot.png']
    #         #result['plot'] = ["u_labels = np.unique(result['labels'])\nfor i in u_labels:\n\tax = plt.scatter(result['transformed_ds'][result['labels'] == i, 0], result['transformed_ds'][result['labels'] == i, 1], label=i)"]
    #     else:
    #         result['plot'].append('./temp/temp_' + str(session_id) + '/barplot.png')
    #         #result['plot'].append("u_labels = np.unique(result['labels'])\nfor i in u_labels:\n\tax = plt.scatter(result['transformed_ds'][result['labels'] == i, 0], result['transformed_ds'][result['labels'] == i, 1], label=i)")
    #
    #     result['original_dataset'].name_plot = './temp/temp_' + str(session_id) + '/barplot.png'

        # plt.show()
    #    return  result

class IRClustermap(IRPlot):
    def __init__(self):
        super(IRClustermap, self).__init__("clustermap",
                                           [],
                                           clustermap)

    def parameter_tune(self, dataset):
        pass

    def run(self, result, session_id):
        if 'correlation' not in result:
            raise CorrelationNotAvailable
        else:
            correlation = result['correlation']

        plt.figure(figsize=(15, 15))
        matplotlib.rcParams.update({'font.size': 18})

        cg = clustermap(correlation, cmap='binary')#, xticklabels=False, yticklabels=False)
        cg.ax_row_dendrogram.set_visible(False)
        cg.ax_col_dendrogram.set_visible(False)
        ax = cg.ax_heatmap
        plt.savefig('./temp/temp_' + str(session_id) + '/clustermap.png')
        if 'plot' not in result:
            result['plot'] = ['./temp/temp_' + str(session_id) + '/clustermap.png']
            # result['plot'] = ["u_labels = np.unique(result['labels'])\nfor i in u_labels:\n\tax = plt.scatter(result['transformed_ds'][result['labels'] == i, 0], result['transformed_ds'][result['labels'] == i, 1], label=i)"]
        else:
            result['plot'].append('./temp/temp_' + str(session_id) + '/clustermap.png')
            # result['plot'].append("u_labels = np.unique(result['labels'])\nfor i in u_labels:\n\tax = plt.scatter(result['transformed_ds'][result['labels'] == i, 0], result['transformed_ds'][result['labels'] == i, 1], label=i)")

        result['original_dataset'].name_plot = './temp/temp_' + str(session_id) + '/clustermap.png'

        return  result


class IRROC(IRPlot):
    def __init__(self):
        super(IRROC, self).__init__("roc",[], roc_curve)

    def parameter_tune(self, dataset):
        pass

    def run(self, result, session_id):
        lw = 2
        n_classes = set(result['labels'])
        tprs = []
        aucs = []
        mean_fpr = np.linspace(0, 1, 100)
        fig, ax = plt.subplots()
        #if len(n_classes) > 2:
        print(range(len(result['x_test'])))
        i=0
        print(len(result['x_test']))
        print(len(result['y_test']))
        for x_test, y_test in zip(result['x_test'], result['y_test']):
            #y_test_bin =  label_binarize(result['y_test'], classes=list(n_classes))
            viz = RocCurveDisplay.from_estimator(
                result['classifier'],
                x_test,
                y_test,
                name="ROC fold {}".format(i),
                alpha=0.3,
                lw=1,
                ax=ax,
            )
            i += 1
            interp_tpr = np.interp(mean_fpr, viz.fpr, viz.tpr)
            interp_tpr[0] = 0.0
            tprs.append(interp_tpr)
            aucs.append(viz.roc_auc)

        ax.plot([0, 1], [0, 1], linestyle="--", lw=2, color="r", label="Chance", alpha=0.8)
        mean_tpr = np.mean(tprs, axis=0)
        mean_tpr[-1] = 1.0
        mean_auc = auc(mean_fpr, mean_tpr)
        std_auc = np.std(aucs)
        ax.plot(
            mean_fpr,
            mean_tpr,
            color="b",
            label=r"Mean ROC (AUC = %0.2f $\pm$ %0.2f)" % (mean_auc, std_auc),
            lw=2,
            alpha=0.8,
        )
        std_tpr = np.std(tprs, axis=0)
        tprs_upper = np.minimum(mean_tpr + std_tpr, 1)
        tprs_lower = np.maximum(mean_tpr - std_tpr, 0)
        ax.fill_between(
            mean_fpr,
            tprs_lower,
            tprs_upper,
            color="grey",
            alpha=0.2,
            label=r"$\pm$ 1 std. dev.",
        )

        ax.set(
            xlim=[-0.05, 1.05],
            ylim=[-0.05, 1.05],
            title="Receiver operating characteristic example",
        )
        ax.legend(loc="lower right")

        #plt.show()
        plt.savefig('./temp/temp_' + str(session_id) + '/roc.png')
        if 'plot' not in result:
            result['plot'] = ['./temp/temp_' + str(session_id) + '/roc.png']
            # result['plot'] = ["u_labels = np.unique(result['labels'])\nfor i in u_labels:\n\tax = plt.scatter(result['transformed_ds'][result['labels'] == i, 0], result['transformed_ds'][result['labels'] == i, 1], label=i)"]
        else:
            result['plot'].append('./temp/temp_' + str(session_id) + '/roc.png')
            # result['plot'].append("u_labels = np.unique(result['labels'])\nfor i in u_labels:\n\tax = plt.scatter(result['transformed_ds'][result['labels'] == i, 0], result['transformed_ds'][result['labels'] == i, 1], label=i)")

        result['original_dataset'].name_plot = './temp/temp_' + str(session_id) + '/roc.png'
        #result['original_dataset'].measures['auc'] = roc_auc
        return result
        '''
        try:
            plt.figure()
            y_test_bin = label_binarize(result['y_test'], classes=list(n_classes))
            if len(n_classes)>2:
                fpr = dict()
                tpr = dict()
                roc_auc = dict()
                for i in range(len(n_classes)):
                    fpr[i], tpr[i], _ = roc_curve(y_test_bin[:, i], np.array(result['y_score'])[:,i])
                    roc_auc[i] = auc(fpr[i], tpr[i])
                colors = cycle(['aqua', 'darkorange', 'cornflowerblue'])
                for i, color in zip(range(len(n_classes)), colors):
                    plt.plot(fpr[i], tpr[i], color=color, lw=2,
                             label='ROC curve of class {0} (area = {1:0.2f})'
                                   ''.format(i, roc_auc[i]))
            else:
                fpr, tpr, _ = roc_curve(y_test_bin, np.array(result['y_score'])[:,0])
                roc_auc = auc(fpr, tpr)
                plt.plot(fpr, tpr, color='aqua', lw=2,
                             label='ROC curve (area = {0:0.2f})'.format( roc_auc))

        except:
            plt.figure()


        plt.plot([0, 1], [0, 1], 'k--', lw=lw)
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title('Receiver operating characteristic')
        plt.legend(loc="lower right")
        '''





# FIXME: this class was commented out because the implementation raises errors
class IRGenericPlot(IROpOptions):
     def __init__(self):
         super(IRGenericPlot, self).__init__([IRScatterplot(), IRDistplot(), IRBoxplot(), IRBarplot()], "scatterplot") # FIXME: IRClustermap(),IRROC(),, IRScatterAssociationRules()
