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
    def __init__(self, ds):
        self.ds = ds
        self.name_plot = None
        self.hasLabel = False
        self.label = ''
        self.hasCategoricalLabel = False
        self.measures = {}


    def more_features(self):
        return self.ds.shape[1]>2

    def set_label(self, label):
        selected_label = []
        for r in [1,0.95,0.9,0.85,0.8,0.75]:
            for c in self.ds.columns:
                if SequenceMatcher(None, c.strip().lower(), label.strip().lower()).ratio()>r:
                    selected_label.append(c)
            if len(selected_label)>0:
                break
        print(selected_label)
        if len(selected_label)==1:
            self.label = selected_label[0]
            self.hasLabel = True
            # If the label column is numeric and the values in the column are more than 5 then the label is not considered categorical
            if not (len(pd.DataFrame(self.ds[self.label])._get_numeric_data().columns)==1 and len(set(self.ds[self.label]))>5):
                self.hasCategoricalLabel = True
            return True
        else:
            return False

    def set_characteristics(self):
        if self.ds is not None:
            self.missingValues = self.missing_values()
            self.categorical, self.onlyCategorical, self.cat_cols = self.categorical_columns()
            self.zeroVariance = self.zero_variance()
            self.outliers = self.has_outliers()
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


    def filter_kb(self, kb):
        properties = ['missingValues',
                      'categorical',
                      'onlyCategorical',
                      'zeroVariance',
                      'hasLabel',
                      'moreFeatures',
                      'outliers',
                      'hasCategoricalLabel']
        key = frozenset(filter(lambda x : getattr(self, x), properties))
        if len(key)==0:
            key=frozenset(['ds'])
        return kb[key]
