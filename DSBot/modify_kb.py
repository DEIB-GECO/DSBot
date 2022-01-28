import json

with open('kb.json') as json_file:
    kb_sets = {frozenset(k.strip().split(',')): v for k, v in json.load(json_file).items()}

for k,v in kb_sets.items():
    for v1 in v:
        index_list = v.index(v1)
        if 'userFeatureSelection' in v1:
            if 'zeroVarianceRemove' not in v1:
                v1.remove('userFeatureSelection')
                v2 = ['userFeatureSelection']
                v2 += v1
            else:
                v1.remove('zeroVarianceRemove')
                v1.remove('userFeatureSelection')
                v2 = ['zeroVarianceRemove','userFeatureSelection']
                v2 += v1

            v[index_list] = v2
kb = {}
for k in kb_sets:
    kb[','.join(set(k))] = kb_sets[k]

with open('kb.json', 'w') as f:
    json.dump(kb, f)