import pandas as pd
import json

class KnowledgeBase:
    def __init__(self):
        with open('kb.json') as json_file:
            self.kb = {frozenset(k.strip().split(',')):v for k,v in json.load(json_file).items()}
        with open('kbSynonyms.json') as json_file:
            self.voc = json.load(json_file)


def create_kb_json():
    kb = pd.read_excel('kb.xlsx', sheet_name='Foglio4', header=None)
    d = {}
    for i in kb.index:
        ds = [x.strip() for x in kb[0][i].split(',')]
        ds.sort()
        ds = ','.join(ds)
        if ds in d:
            d[ds].append([x for x in kb.T[i].values[1:] if not pd.isna(x)])
        else:
            d[ds] = [[x for x in kb.T[i].values[1:] if not pd.isna(x)]]
    with open('kb.json','w') as f:
        json.dump(d, f)

def kb_values():
    with open('kb.json') as json_file:
        kb = {frozenset(k.strip().split(',')): v for k, v in json.load(json_file).items()}
    features = set()
    operations = set()
    for k,v in kb.items():
        features.update(set(k))
        operations.update({x for y in v for x in y })
    #print(features)
    #print(operations)
    properties = ['missingValues',
                  'categorical',
                  'onlyCategorical',
                  'zeroVariance',
                  'hasLabel',
                  'moreFeatures',
                  'outliers',
                  'hasCategoricalLabel']
    from itertools import compress, product
    def combinations(items):
        return ( set(compress(items,mask)) for mask in product(*[[0,1]]*len(items)) )
    ds_feat = [set(x) for x in kb.keys()]
    comb = [set(x) for x in list(combinations(properties)) if not len(x)==0]
    class_pipeline_nofs = []
    class_pipeline_fs = []
    regr_pipeline_nofs = []
    regr_pipeline_fs = []
    ar_pipeline_nofs = []
    ar_pipeline_fs = []
    outDet_pipeline = []
    fs_pipeline = []
    for i in comb:
        if 'hasCategoricalLabel' in i and 'hasLabel' not in i:
            comb.remove(i)
        if 'onlyCategorical' in i and 'categorical' not in i and i in comb:
            comb.remove(i)
    for i in comb:
        if 'hasLabel' in i:
            if 'hasCategoricalLabel' in i:
                if 'moreFeatures' in i:
                    class_pipeline_fs.append(i)
                else:
                    class_pipeline_nofs.append(i)
            else:
                if 'moreFeatures' in i:
                    regr_pipeline_fs.append(i)
                else:
                    regr_pipeline_nofs.append(i)
        if 'onlyCategorical' in i:
            if 'moreFeatures' in i:
                ar_pipeline_fs.append(i)
            else:
                ar_pipeline_nofs.append(i)
        if 'outliers' in i:
            outDet_pipeline.append(i)
        if 'moreFeatures' in i:
            fs_pipeline.append(i)

    print('all comb', len(comb))
    print('classif_nofs', len(class_pipeline_nofs), 'classif_fs', len(class_pipeline_fs))
    print('reg_nofs', len(regr_pipeline_nofs), 'reg_fs', len(regr_pipeline_fs))
    print('ar_nofs', len(ar_pipeline_nofs), 'ar_fs', len(ar_pipeline_fs))
    print('outDet', len(outDet_pipeline))
    print('fs', len(fs_pipeline))

    diff = set([tuple(x) for x in comb]) - set([tuple(x) for x in ds_feat])
    print(len(diff))
    for i in set([tuple(x) for x in comb]) - set([tuple(x) for x in ds_feat]):
        if set(i) in ds_feat and i in diff:
            diff.remove(i)
    print(len(diff))
    #print(diff)
    import copy
    dict_pipelines = {}
    for i in comb:
        p = []
        dict_pipelines[','.join(i)] = []
        #CLASSIFICATION
        if i in [set(x) for x in class_pipeline_nofs]:
            print('CLASSIFICATION')
            p=[]
            if 'zeroVariance' in i:
                p.append('zeroVarianceRemove')
            if 'missingValues' in i:
                p.append('missingValuesHandle')
            p.append('labelRemove')
            if 'outliers' in i:
                p.append('outliersRemove')
            if 'categorical' in i:
                p.append('oneHotEncode')
            p1 = copy.deepcopy(p)
            p.append('standardization')
            p2 = copy.deepcopy(p)
            p.append('autoClassification')
            p1.append('randomForest')
            p2.append('logisticRegression')
            p_1 = copy.deepcopy(p)
            p1_1 = copy.deepcopy(p1)
            p2_1 = copy.deepcopy(p2)
            p.append('roc')
            p1.append('roc')
            p2.append('roc')
            p_1 += ['featureImportance','featureImportancePlot']
            p1_1+= ['featureImportance','featureImportancePlot']
            p2_1+= ['featureImportance','featureImportancePlot']
            dict_pipelines[','.join(i)] += [p,p_1,p1,p1_1,p2,p2_1]
        if i in [set(x) for x in class_pipeline_fs]:
            p=[]
            if 'zeroVariance' in i:
                p.append('zeroVarianceRemove')
            if 'missingValues' in i:
                p.append('missingValuesHandle')
            p.append('labelRemove')
            if 'outliers' in i:
                p.append('outliersRemove')
            if 'categorical' in i:
                p.append('oneHotEncode')
            p1 = copy.deepcopy(p)
            p.append('standardization')
            p2 = copy.deepcopy(p)
            p.append('autoClassification')
            p1.append('randomForest')
            p2.append('logisticRegression')
            p_1 = copy.deepcopy(p)
            p1_1 = copy.deepcopy(p1)
            p2_1 = copy.deepcopy(p2)
            p.append('roc')
            p1.append('roc')
            p2.append('roc')
            p_1 += ['featureImportance', 'featureImportancePlot']
            p1_1 += ['featureImportance', 'featureImportancePlot']
            p2_1 += ['featureImportance', 'featureImportancePlot']
            dict_pipelines[','.join(i)]+=[p,p_1,p1,p1_1,p2,p2_1]
            p=[]
            if 'zeroVariance' in i:
                p.append('zeroVarianceRemove')
            if 'missingValues' in i:
                p.append('missingValuesHandle')
            p.append('labelRemove')
            if 'outliers' in i:
                p.append('outliersRemove')
            if 'categorical' in i:
                p.append('oneHotEncode')
            p__1 = copy.deepcopy(p)
            p.append('standardization')
            p.append('lasso')
            p__1.append('userFeatureSelection')
            p1 = copy.deepcopy(p)
            p2 = copy.deepcopy(p)
            p1__1 = copy.deepcopy(p__1)
            p2__1 = copy.deepcopy(p__1)
            p.append('autoClassification')
            p1.append('randomForest')
            p1.remove('standardization')
            p2.append('logisticRegression')
            p__1.append('autoClassification')
            p1__1.append('randomForest')
            p1__1.remove('standardization')
            p2__1.append('logisticRegression')
            p_1 = copy.deepcopy(p)
            p1_1 = copy.deepcopy(p1)
            p2_1 = copy.deepcopy(p2)
            p_1__1 = copy.deepcopy(p__1)
            p1_1__1 = copy.deepcopy(p1__1)
            p2_1__1 = copy.deepcopy(p2__1)
            p.append('roc')
            p1.append('roc')
            p2.append('roc')
            p__1.append('roc')
            p1__1.append('roc')
            p2__1.append('roc')
            p_1 += ['featureImportance', 'featureImportancePlot']
            p1_1 += ['featureImportance', 'featureImportancePlot']
            p2_1 += ['featureImportance', 'featureImportancePlot']
            p_1__1 +=['featureImportance', 'featureImportancePlot']
            p1_1__1 += ['featureImportance', 'featureImportancePlot']
            p2_1__1 += ['featureImportance', 'featureImportancePlot']
            dict_pipelines[','.join(i)]+=[p,p_1,p1,p1_1,p2,p2_1, p__1, p_1__1,p1__1,p1_1__1,p2__1,p2_1__1]
        #REGRESSION
        if i in [set(x) for x in regr_pipeline_nofs]:
            p=[]
            if 'zeroVariance' in i:
                p.append('zeroVarianceRemove')
            if 'missingValues' in i:
                p.append('missingValuesHandle')
            p.append('labelRemove')
            if 'outliers' in i:
                p.append('outliersRemove')
            if 'categorical' in i:
                p.append('oneHotEncode')
            p.append('standardization')
            p1 = copy.deepcopy(p)
            p2 = copy.deepcopy(p)
            p.append('autoRegression')
            p1.append('linearRegression')
            p2.append('ridgeRegression')
            p_1 = copy.deepcopy(p)
            p1_1 = copy.deepcopy(p1)
            p2_1 = copy.deepcopy(p2)
            p += ['regressionPerformance', 'tableRegression']
            p1 += ['regressionPerformance', 'tableRegression']
            p2 += ['regressionPerformance', 'tableRegression']
            p_1 += ['featureImportance', 'featureImportancePlot']
            p1_1 += ['featureImportance', 'featureImportancePlot']
            p2_1 += ['featureImportance', 'featureImportancePlot']
            dict_pipelines[','.join(i)]+=[p,p_1,p1,p1_1,p2,p2_1]
        if i in [set(x) for x in regr_pipeline_fs]:
            p=[]
            if 'zeroVariance' in i:
                p.append('zeroVarianceRemove')
            if 'missingValues' in i:
                p.append('missingValuesHandle')
            p.append('labelRemove')
            if 'outliers' in i:
                p.append('outliersRemove')
            if 'categorical' in i:
                p.append('oneHotEncode')
            p.append('standardization')
            p1 = copy.deepcopy(p)
            p2 = copy.deepcopy(p)
            p.append('autoRegression')
            p1.append('linearRegression')
            p2.append('ridgeRegression')
            p_1 = copy.deepcopy(p)
            p1_1 = copy.deepcopy(p1)
            p2_1 = copy.deepcopy(p2)
            p += ['regressionPerformance','tableRegression']
            p1 += ['regressionPerformance','tableRegression']
            p2 += ['regressionPerformance','tableRegression']
            p_1 += ['featureImportance', 'featureImportancePlot']
            p1_1 += ['featureImportance', 'featureImportancePlot']
            p2_1 += ['featureImportance', 'featureImportancePlot']
            dict_pipelines[','.join(i)]+=[p,p_1,p1,p1_1,p2,p2_1]
            p=[]
            if 'zeroVariance' in i:
                p.append('zeroVarianceRemove')
            if 'missingValues' in i:
                p.append('missingValuesHandle')
            p.append('labelRemove')
            if 'outliers' in i:
                p.append('outliersRemove')
            if 'categorical' in i:
                p.append('oneHotEncode')
            p.append('standardization')
            p__1 = copy.deepcopy(p)
            p.append('lasso')
            p__1.append('userFeatureSelection')
            p1 = copy.deepcopy(p)
            p2 = copy.deepcopy(p)
            p1__1 = copy.deepcopy(p__1)
            p2__1 = copy.deepcopy(p__1)
            p.append('autoRegression')
            p1.append('linearRegression')
            p2.append('ridgeRegression')
            p__1.append('autoRegression')
            p1__1.append('linearRegression')
            p2__1.append('ridgeRegression')
            p_1 = copy.deepcopy(p)
            p1_1 = copy.deepcopy(p1)
            p2_1 = copy.deepcopy(p2)
            p_1__1 = copy.deepcopy(p__1)
            p1_1__1 = copy.deepcopy(p1__1)
            p2_1__1 = copy.deepcopy(p2__1)
            p.append('roc')
            p1.append('roc')
            p2.append('roc')
            p__1.append('roc')
            p1__1.append('roc')
            p2__1.append('roc')
            p_1 += ['featureImportance', 'featureImportancePlot']
            p1_1 += ['featureImportance', 'featureImportancePlot']
            p2_1 += ['featureImportance', 'featureImportancePlot']
            p_1__1 += ['featureImportance', 'featureImportancePlot']
            p1_1__1 += ['featureImportance', 'featureImportancePlot']
            p2_1__1 += ['featureImportance', 'featureImportancePlot']
            dict_pipelines[','.join(i)]+=[p,p_1,p1,p1_1,p2,p2_1, p__1, p_1__1,p1__1,p1_1__1,p2__1,p2_1__1]
        # FEATURE SELECTION, CLUSTERING WITH FS
        if i in [set(x) for x in fs_pipeline]:
            p=[]
            if 'zeroVariance' in i:
                p.append('zeroVarianceRemove')
            if 'missingValues' in i:
                p.append('missingValuesHandle')
            if 'hasLabel' in i:
                p.append('labelRemove')
            if 'outliers' in i:
                p.append('outliersRemove')
            if 'categorical' in i:
                p.append('oneHotEncode')
            if 'hasLabel' in i:
                p += ['lasso','lassoPlot']
                dict_pipelines[','.join(i)] += [p]
            # TODO: else and add method plot results of laplace as implementation
            p=[]
            if 'zeroVariance' in i:
                p.append('zeroVarianceRemove')
            if 'missingValues' in i:
                p.append('missingValuesHandle')
            if 'hasLabel' in i:
                p.append('labelRemove')
            p.append('standardization')
            if 'outliers' in i:
                p.append('outliersRemove')
            if 'categorical' in i:
                p.append('oneHotEncode')
            p1 = copy.deepcopy(p)
            p2 = copy.deepcopy(p)
            p += ['kmeans','pca2','scatterplot']
            p1 += ['agglomerativeClustering','pca2','scatterplot']
            p2 += ['dbscan','pca2','scatterplot']
            dict_pipelines[','.join(i)] += [p, p1, p2]
            p = []
            if 'zeroVariance' in i:
                p.append('zeroVarianceRemove')
            if 'missingValues' in i:
                p.append('missingValuesHandle')
            if 'hasLabel' in i:
                p.append('labelRemove')
            p.append('standardization')
            if 'outliers' in i:
                p.append('outliersRemove')
            if 'categorical' in i:
                p.append('oneHotEncode')
            p_1 = copy.deepcopy(p)
            p.append('laplace')
            p1 = copy.deepcopy(p)
            p2 = copy.deepcopy(p)
            p += ['kmeans', 'pca2', 'scatterplot']
            p1 += ['agglomerativeClustering', 'pca2', 'scatterplot']
            p2 += ['dbscan', 'pca2', 'scatterplot']
            p_1.append('userFeatureSelection')
            p1_1 = copy.deepcopy(p_1)
            p2_1 = copy.deepcopy(p_1)
            p_1 += ['kmeans', 'pca2', 'scatterplot']
            p1_1 += ['agglomerativeClustering', 'pca2', 'scatterplot']
            p2_1 += ['dbscan', 'pca2', 'scatterplot']
            dict_pipelines[','.join(i)] += [p, p1, p2, p_1, p1_1, p2_1]
        # ASSOC RULES
        if i in  [set(x) for x in ar_pipeline_nofs]:
            p=[]
            if 'zeroVariance' in i:
                p.append('zeroVarianceRemove')
            if 'missingValues' in i:
                p.append('missingValuesHandle')
            if 'hasLabel' in i:
                p.append('labelRemove')
            if 'outliers' in i:
                p.append('outliersRemove')
            p.append('oneHotEncode')
            if 'hasLabel' in i:
                p.append('labelAppend')
            p += ['associationRules', 'tableAssociationRules']
            dict_pipelines[','.join(i)] += [p]
        if i in  [set(x) for x in ar_pipeline_fs]:
            p=[]
            if 'zeroVariance' in i:
                p.append('zeroVarianceRemove')
            if 'missingValues' in i:
                p.append('missingValuesHandle')
            if 'hasLabel' in i:
                p.append('labelRemove')
            if 'outliers' in i:
                p.append('outliersRemove')
            p.append('oneHotEncode')
            if 'hasLabel' in i:
                p.append('labelAppend')
            p += ['associationRules', 'tableAssociationRules']
            dict_pipelines[','.join(i)] += [p]
            p = []
            if 'zeroVariance' in i:
                p.append('zeroVarianceRemove')
            if 'missingValues' in i:
                p.append('missingValuesHandle')
            if 'hasLabel' in i:
                p.append('labelRemove')
            if 'outliers' in i:
                p.append('outliersRemove')
            p.append('oneHotEncode')
            if 'hasLabel' in i:
                p.append('labelAppend')
            p1 = copy.deepcopy(p)
            p += ['laplace','associationRules', 'tableAssociationRules']
            p1 += ['userFeatureSelection', 'associationRules', 'tableAssociationRules']
            dict_pipelines[','.join(i)] += [p,p1]

        # OUTDET
        if i in [set(x) for x in outDet_pipeline]:
            p=[]
            if 'zeroVariance' in i:
                p.append('zeroVarianceRemove')
            if 'missingValues' in i:
                p.append('missingValuesHandle')
            if 'hasLabel' in i:
                p.append('labelRemove')
            p.append('standardization')
            if 'categorical' in i:
                p.append('oneHotEncode')
            p += ['outliersDetection', 'pca2', 'scatterplot']
            dict_pipelines[','.join(i)] += [p]
        # CLUST
        if i not in [set(x) for x in fs_pipeline]:
            p=[]
            if 'zeroVariance' in i:
                p.append('zeroVarianceRemove')
            if 'missingValues' in i:
                p.append('missingValuesHandle')
            if 'hasLabel' in i:
                p.append('labelRemove')
            p.append('standardization')
            if 'outliers' in i:
                p.append('outliersRemove')
            if 'categorical' in i:
                p.append('oneHotEncode')
            p1 = copy.deepcopy(p)
            p2 = copy.deepcopy(p)
            p += ['kmeans','pca2','scatterplot']
            p1 += ['agglomerativeClustering','pca2','scatterplot']
            p2 += ['dbscan','pca2','scatterplot']
            dict_pipelines[','.join(i)] += [p, p1, p2]

        p = []
        if 'zeroVariance' in i:
            p.append('zeroVarianceRemove')
        if 'missingValues' in i:
            p.append('missingValuesHandle')
        if 'hasLabel' in i:
            p.append('labelRemove')
        if 'outliers' in i:
            p.append('outliersRemove')
        if 'categorical' in i:
            p.append('oneHotEncode')
        p1 = copy.deepcopy(p)
        p+=['pearson', 'clustermap']
        p1 += ['spearman', 'clustermap']
        dict_pipelines[','.join(i)] += [p, p1]
    print(len([x for k,v in dict_pipelines.items() for x in v]))
    with open('kb2.json','w') as f:
        json.dump(dict_pipelines, f)
    try_list = [(x,y) for x,v in dict_pipelines.items() for y in v]
    kb_df = pd.DataFrame.from_records(try_list)
    kb_df = pd.concat([pd.DataFrame(kb_df[0]),pd.DataFrame(kb_df[1].to_list())],axis=1)
    print(kb_df.head())
    kb_df.to_excel('kb2.xlsx', header=None, index=None)

def update_kb(new_feat, new_op):
    with open('kb.json') as json_file:
        kb_sets = {frozenset(k.strip().split(',')): v for k, v in json.load(json_file).items()}

    new_keys = {}
    for k in kb_sets.keys():
        if 'moreFeatures' in k:
            new_k = set(k)
            new_k.add(new_feat)
            #new_keys[k] = kb_sets[k]
            for i in kb_sets[k]:
                new_val = []
                count = 0
                for j in i:
                    if j=='zeroVarianceRemove' or j=='missingValuesHandle':
                        new_val.append(j)
                    elif j!='zeroVarianceRemove' and j!='missingValuesHandle' and count==0:
                        new_val.append(new_op)
                        count +=1
                    else:
                        new_val.append(j)
                new_keys[frozenset(new_k)] = new_val

    kb_sets.update(new_keys)
    kb = {}
    for k in kb_sets:
        kb[','.join(set(k))] = kb_sets[k]

    with open('kb.json', 'w') as f:
        json.dump(kb, f)
    try_list = [(x, y) for x, v in kb.items() for y in v]
    kb_df = pd.DataFrame.from_records(try_list)
    kb_df = pd.concat([pd.DataFrame(kb_df[0]), pd.DataFrame(kb_df[1].to_list())], axis=1)
    print(kb_df.head())
    kb_df.to_excel('kb.xlsx', header=None, index=None)

#update_kb('strongCorrelatedFeatures','correlatedFeaturesRemove')