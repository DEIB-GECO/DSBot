import os
import pandas as pd
from kb import KnowledgeBase
from scipy.spatial.distance import pdist, squareform
from sklearn.preprocessing import StandardScaler
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer
from sklearn.decomposition import PCA
from difflib import SequenceMatcher
import numpy as np

class Dataset:
    def __init__(self, ds, label=None):
        self.ds = ds
        self.name_plot = None
        self.hasLabel = False
        self.measures = {}


    def more_features(self):
        if self.ds.shape[1]>2:
            return True
        else:
            False

    def set_label(self, label):
        for c in self.ds.columns:
            if SequenceMatcher(None, c.strip().lower(), label.strip().lower()).ratio()>0.75:
                label = c
        self.label = label
        self.hasLabel = True
        if len(pd.DataFrame(self.ds[label])._get_numeric_data().columns) == 1:
            self.hasCategoricalLabel = False
        else:
            self.hasCategoricalLabel = True

    def set_characteristics(self):
        if self.ds is not None:
            self.missingValues, self.categorical, self.onlyCategorical, self.zeroVariance, self.outliers = self.check_ds()
        self.moreFeatures = self.more_features()
        print('mv',self.missingValues, 'cat',self.categorical,'zv', self.zeroVariance, 'mf',self.moreFeatures, 'outliers', self.outliers)

    def missing_values(self):
        return (self.ds.isnull().sum().sum())>0

    def zero_variance(self):
        var = self.ds.std(axis=1)
        return (var==0).sum()>0

    def categorical_columns(self):
        ds = self.ds
        if self.hasLabel:
            ds = ds.drop(self.label,axis=1)
        cols = ds.columns
        num_cols = ds._get_numeric_data().columns
        return len(list(set(cols) - set(num_cols))) > 0, len(num_cols)==0, list(set(cols) - set(num_cols))

    def has_outliers(self):
        df = self.ds.drop(list(self.cat_cols), axis=1)
        if self.hasLabel:
            ds = df.drop(self.label,axis=1)

        if len(df[((np.abs(df-df.mean()))<=(3*df.std())).sum(axis=1)<=0.9*df.shape[1]])< len(df):
            return True
        return False

    def curse_of_dim(self):
        data = StandardScaler().fit_transform(self.ds)
        eucl = squareform(pdist(data.values))
        max_dist = eucl.max()
        min_dist = eucl[eucl.nonzero()].min()
        res = (max_dist-min_dist)/min_dist
        return res<1

    def dim_reduction(self):
        self.ds = PCA(len(self.ds.index)).fit_transform(self.ds)

    def check_ds(self):
        missing_val = self.missing_values()
        categorical, only_categorical, self.cat_cols = self.categorical_columns()
        zero_var = self.zero_variance()
        outliers = self.has_outliers()
        return missing_val, categorical, only_categorical, zero_var, outliers

    def filter_kb(self, kb):
        drop = []
        for i in self.__dict__:
            if (str(i) in ['missingValues','categorical','onlyCategorical','zeroVariance','hasLabel','moreFeatures', 'outliers']):
                if getattr(self, i):
                    for j in range(len(kb)):
                        kb_val = [i.strip() for i in kb.values[j,0].split(',')]
                        if not i in kb_val:
                            drop.append(j)
                else:
                    for j in range(len(kb)):
                        kb_val = [i.strip() for i in kb.values[j,0].split(',')]
                        if i in kb_val:
                            drop.append(j)

        kb = kb.drop(drop)
        return kb

def filter_kb(kb, request):
    req = request.split(' ')
    indices = []
    for index, row in kb.iterrows():
        if  all(item in row.values for item in req):
            indices.append(index)
    kb = kb.T[indices].T
    return kb
'''
kb = KnowledgeBase().kb
print(kb)
import seaborn as sns
titanic = sns.load_dataset('titanic')
titanic_ds = Dataset(titanic)
titanic_ds.filter_kb(kb)
from needleman_wunsch import NW
print(kb.values[0,1:])

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    from pydataset import data
    import seaborn as sns
    from clustering import Kmeans
    from plot import Plot
    titanic = sns.load_dataset('titanic')
    titanic_ds = Dataset(titanic)
    #print('titanic', titanic_ds.missingValues, titanic_ds.categorical)
    #print(titanic_ds.one_hot_encode())
    #print(titanic_ds.dataset.head())
    #print(titanic_ds.dataset.shape)
    #kmeans = Kmeans(titanic_ds.dataset, n_clust=3).res
    #scatterplot = Plot(titanic_ds).scatter(kmeans.labels)

    #os.system("onmt_translate -model ./wf/run/model_step_1000.pt -src wf/try.txt -output ./wf/pred_1000.txt -gpu -1 -verbose")
   # with open("wf/pred_1000.txt", 'r') as f:
    #    x = f.readlines()
    #print(x)
    #workflow =  x[0].strip().split(' ')
    #print(workflow)

    #kb = KnowledgeBase().kb
    #print(kb)
    #request = 'kmeans scatterplot'
    #kb = filter_kb(kb, request)
    #print(kb)
'''

