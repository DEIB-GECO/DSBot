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
print(type(voc))
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

print(rec_inside('autoClassification',voc['prediction']))


#print(recursive_items(voc, {}))
#voc = [k for k, v in recursive_items(voc)]# if k not in ['description', 'explanation', 'example', 'values']]
#print(voc)