import pandas as pd
import json

class KnowledgeBase:
    def __init__(self):
        with open('kb.json') as json_file:
            self.kb = {frozenset(k.strip().split(',')):v for k,v in json.load(json_file).items()}
        with open('kb_synonyms.json') as json_file:
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
    print(features)
    print(operations)




