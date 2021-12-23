import json
with open('kbSynonyms.json') as json_file:
    voc = json.load(json_file)

def recursive_items(dictionary, new_dict):
    for key, value in dictionary.items():
        print(key)
        if key not in new_dict:
            new_dict[key]=[]
        if type(value) is dict:
            for k, v in value.items():
                if k not in ['description', 'explanation', 'example', 'values']:
                    new_dict[key].append(k)
            return recursive_items(value, new_dict)
        else:
            if key not in ['description', 'explanation', 'example', 'values']:
                return new_dict
            else:
                pass

def rec(k, v, voc):
    for key in k:
        if type(voc[key]) is voc and v in voc[key]['values']:
            return True
    else:
        for key in k:
            if type(voc) is dict and type(voc[key]) is dict and 'values' in voc[key]:
                print(voc[key]['values'])
                for k2,v2 in voc[key]['values'].items():
                    print(k2,v2)
                    if 'values' in v2:
                        return rec(v2,v,v2)
                    else:
                        return False

def rec_inside(chiave, dizio):
    if 'values' not in dizio:
        return False
    elif chiave in dizio['values']:
        return True
    else:
        for k in dizio['values']:
            return rec_inside(chiave, dizio['values'][k])


def sin(k1,k2, d, acc=0):
    if (k1 in d) and (k2 in d):
        return False
    elif acc == 2:
        return True
    elif k1 in d:
        if acc==1:
            return True
        nd = d[k1].get("values", {})
        if k2 in nd:
            return True
        else:
            return any([sin(k1,k2, nd[k].get("values", {}), acc=acc+1) for k in nd.keys()])
    elif k2 in d:
        if acc==1:
             return True
        nd = d[k2].get("values", {})
        if k1 in nd:
            return True
        else:
            return any([sin(k1,k2, nd[k].get("values", {}), acc=acc+1) for k in nd.keys()])
    else:
        res = False
        for k in d.keys():
            #print(k)
            res = res or sin(k1,k2, d[k].get("values", {}), acc=0)
        return res

l= ['autoClassification', 'prediction', 'clustering', 'featureSelection', 'unsupervisedFeatureSelection',
          'logisticRegression', 'kmeans', 'classification', 'regression', 'userFeatureSelection', 'lasso',
          'plot', 'scatterplot', 'featureImportance', 'outliersDetection', 'selectKBest', 'correlation',
          'associationRules', 'relation', 'pearson', 'randomForest', 'dbscan']

#print(sin("autoClassification","classification",voc))
for a in l:
     for b in l:
         print(a,b, sin(a,b,voc))
#print(recursive_items(voc, {}))
#voc = [k for k, v in recursive_items(voc)]# if k not in ['description', 'explanation', 'example', 'values']]
#print(voc)