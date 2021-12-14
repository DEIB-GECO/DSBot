import pandas as pd
import json

class KnowledgeBase:
    def __init__(self):
        #self.kb = pd.read_excel('kb.xlsx', sheet_name='Foglio4', header=None)
        with open('kb.json') as json_file:
            self.kb = json.load(json_file)
        print(self.kb)
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

