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