import random

headers = [('Diagnosis',
                  ['radius', 'texture','perimeter','area','smoothness','compactness','concavity','concave points','symmetry','fractal dimension'],
                  'patients'),
                 ('Y',
                  ['destination','passager','weather','temperature','time','coupon','expiration','gender','age','maritalStatus','has_Children','education',
                   'occupation','income','Bar','CoffeeHouse','CarryAway','RestaurantLessThan20','Restaurant20To50','toCoupon_GEQ15min','toCoupon_GEQ25min',
                   'direction_same','direction_opp'],
                  'people'),
                 ('area',
                  ['X','Y','month','day','FFMC','DMC','DC','ISI','temp','RH','wind','rain'],
                  'areas'),
                 ('G3',
                  ['school','sex','age','address','famsize','Pstatus','Medu','Fedu','Mjob','Fjob','reason','guardian','traveltime','studytime','failures',
                   'schoolsup','famsup','paid','activities','nursery','higher','internet','romantic','famrel','freetime','goout','Dalc','Walc','health',
                   'absences','G1','G2'],
                  'students'),
                  (None,
                   ["Kingdom", "DNAtype" ,"SpeciesID" ,"Ncodons" ,"SpeciesName" , "codon"],
                   'sequences'),
                   (None,
                    ["buying","maint","doors","persons","lug_boot","safety"],
                    'cars')
               ]

synonyms_clustering = ['groups', 'clusters', 'sets', 'similar samples', 'groups of similar samples', 'sets of similar samples', 'sets of similar elements',
                       'elements which are similar', 'elements that are uniform', 'uniform samples']
synonyms_clustering_with_data = ['groups of', 'sets of', 'clusters of', 'similar samples of', 'sets of similar',  'groups of similar','uniform' ]
synonyms_clustering_verbs = ['cluster', 'assemble', 'group','associate','gather','aggregate','collect']

synonyms_relation = ['relations', 'relations among features', 'relations among columns', 'associations between features', 'associations between columns',
                     'links between features', 'links between columns', 'connections between features', 'connections between columns', 'interconnections',
                     'interrelations']
synonyms_relation_with_data = ['relations among', 'associations among', 'associations between', 'links between', 'connections between', 'interconnections among']

synonyms_correlation = ['correlation', 'correlation among features', 'correlation among columns']
synonyms_correlation_with_data = ['correlations among', 'correlations between']

synonyms_associationRules = ['association rules', 'rules of association between features', 'rules that associates features', 'rules of association between columns',
                             'rules that associate columns', 'association rules between features', 'association rules between columns']
synonyms_associationRules_with_data = ['rules of association between', 'rules that associates','association rules between']

synonyms_outliersDetection = ['strange data', 'strange samples', 'anomalies in data', 'anomalies in samples', 'anomalies in my data', 'strange sample among my data',
                              'outliers in data','incoherent data', 'incoherent samples', 'outliers among samples', 'irregularities between samples',
                              'anomalies between samples']
synonyms_outliersDetection_with_data = ['strange samples among', 'anomalies in', 'outliers in','inchoerent', 'irregularities among']
synonyms_outliersDetection_verbs_nodata = ['detect outliers', 'discover outliers']
synonyms_outliersDetection_verbs_with_data = ['detect outliers in', 'discover outliers in']

synonyms_userFeatureSel = ['according to', 'selecting only', 'considering only', 'if you consider only', 'if you select', 'looking at', 'keeping into consideration',
                           'taking into account', 'taking into consideration only', 'filtering out']
synonyms_featureSel = ['select some features', 'extract some features', 'select some columns', 'extract some columns','considering some features', 'using some features',
                       'select the relevant features', 'extract the features', 'use only some features',
                       'use only some columns', 'select only some columns'
                                                'extract only some columns', 'extract some columns',
                       'select the relevant columns', 'consider only some features', 'consider some columns'
                       ]

synonyms_classification = ['classes', 'classification', 'classes according to the label', 'division of the data according to the label']
synonyms_classification_with_data = ['classes according to', 'classification using', 'division of the data according to' ]
synonyms_classification_verbs_nodata = ['classify', 'predict classes in my data', 'assign classes in the data', 'classify the data','predict classes among my data',
                                        'predict classes of my data']
synonyms_classification_verbs_with_data = ['classify the', 'classify', 'predict classes according to', 'predict the', 'predict classes of', 'assign classes in']

synonyms_prediction = ['prediction', 'predictions']
synonyms_prediction_with_data = ['prediction of']
synonyms_prediction_verbs_nodata = ['predict the label', 'predict data', 'predict the data','predict label in my data', 'predict the label',
                             'forecast the label', 'determine the label']
synonyms_prediction_verbs_with_data = ['predict the', 'predict', 'forecast', 'determine']

synonyms_regression = ['regression']

synonyms_extraction = ['extract', 'select', 'retrieve']

synonyms_importantFeatures = ['the most important features', 'the most important columns', 'the features that are more significant', 'the features that classify better',
                              'the columns that classify better', 'the columns that identify the groups', 'the most relevant features', 'the most relevant columns']

synonyms_afterclass = ['after the classification', 'after having classified', 'after classifying the data', 'after considering the classes of the data',
                       'once you have classified my data', 'once the classification is computed']

synonyms_afterclass_with_data = ['after the classification of', 'after having classified the', 'after classifying the', 'after considering the classes of',
                       'once you have classified']

synonyms_afterpred = ['after the prediction', 'after having predicted', 'after predicting the data', 'after prediction the data',
                       'once you have predicted my data', 'once the prediction is computed']

synonyms_afterpred_with_data = ['after the prediction of', 'after having predicted the', 'after prediction the', 'after forecasting',
                       'once you have predicted']

synonym_then = ['then', ',', 'after that', ';', 'subsequently', 'later','next', 'on top of that', 'moreover']


synonyms_data = ['data','samples','rows', 'examples','information']

auxiliary_plusverbs = ['can you', 'i want to', 'let\'s', 'could you', 'i would like to', 'i would', '', 'are you able to', 'do you manage to', 'shall we',
                       'may you', 'might you', 'would you']
auxiliary_plusnouns = ['i want', 'are there', 'look for', 'let\'s search for', 'perform', 'compute', 'do', 'do they exist', 'analyze', 'have you' ,'shall we look for']

verbs = ['find',  'compute', 'perform', 'identify', 'analyze', 'look for', 'search for', 'produce', 'consider', 'inspect', 'investigate' ] # usa condizionale --> dividere parte i want to/can/could (spezzare verbo semantico)
plot_verbs = ['see', 'show', 'show me', 'visualize','plot', 'draw', 'look at','observe', 'spot', 'view', 'watch', 'inspect','display','exhibit' , 'present', 'expose','foresee']

'''with open('../DSBot/wf/src-train2.txt','a') as f:
    for s in sent:
        f.write('\n')
        f.write(s)
        #f.write('\n')

with open('../DSBot/wf/tgt-train2.txt','a') as f:
    for s in targ:
        f.write('\n')
        f.write(s)
'''
sent = []
targ = []
for av in auxiliary_plusnouns:
    for c in synonyms_clustering_with_data:
        for d in headers:
            sent.append(av + ' '  + c + ' ' + d[-1])
            targ.append('clustering')
print('clustering', len(sent))
with open('../DSBot/wf/src-train2.txt','a') as f:
    for s in sent:
        f.write('\n')
        f.write(s)
        #f.write('\n')

with open('../DSBot/wf/tgt-train2.txt','a') as f:
    for s in targ:
        f.write('\n')
        f.write(s)
sent = []
targ = []
for av in auxiliary_plusnouns:
    for c in synonyms_classification_with_data:
        for d in headers:
            sent.append(av + ' ' + c + ' ' + d[-1])
            targ.append('classification')
print('classification', len(sent))
with open('../DSBot/wf/src-train2.txt','a') as f:
    for s in sent:
        f.write('\n')
        f.write(s)
        #f.write('\n')

with open('../DSBot/wf/tgt-train2.txt','a') as f:
    for s in targ:
        f.write('\n')
        f.write(s)
sent = []
targ = []
for av in auxiliary_plusnouns:
    for c in synonyms_prediction_with_data:
        for d in headers:
            sent.append(av + ' ' +c + ' ' + d[-1])
            targ.append('prediction')
print('prediction', len(sent)*3)
with open('../DSBot/wf/src-train2.txt','a') as f:
    for s in sent:
        f.write('\n')
        f.write(s)
        #f.write('\n')

with open('../DSBot/wf/tgt-train2.txt','a') as f:
    for s in targ:
        f.write('\n')
        f.write(s)
sent = []
targ = []
for av in auxiliary_plusnouns:
    for c in synonyms_relation_with_data:
        for d in headers:
            sent.append(av + ' ' + c + ' ' + d[-1])
            targ.append('relation')
print('relation', len(sent))
with open('../DSBot/wf/src-train2.txt','a') as f:
    for s in sent:
        f.write('\n')
        f.write(s)
        #f.write('\n')

with open('../DSBot/wf/tgt-train2.txt','a') as f:
    for s in targ:
        f.write('\n')
        f.write(s)
sent = []
targ = []
for av in auxiliary_plusnouns:
    for c in synonyms_associationRules_with_data:
        for d in headers:
            sent.append(av + ' ' + c + ' ' + d[-1])
            targ.append('associationRules')
print('associationRules', len(sent)*2)

with open('../DSBot/wf/src-train2.txt','a') as f:
    for s in sent:
        f.write('\n')
        f.write(s)
        #f.write('\n')

with open('../DSBot/wf/tgt-train2.txt','a') as f:
    for s in targ:
        f.write('\n')
        f.write(s)
with open('../DSBot/wf/src-train2.txt','a') as f:
    for s in sent:
        f.write('\n')
        f.write(s)
        #f.write('\n')

with open('../DSBot/wf/tgt-train2.txt','a') as f:
    for s in targ:
        f.write('\n')
        f.write(s)
sent = []
targ = []
for av in auxiliary_plusnouns:
    for c in synonyms_correlation_with_data:
        for d in headers:
            sent.append(av + ' ' +  c + ' ' + d[-1])
            targ.append('correlation')
print('correlation', len(sent)*2)
with open('../DSBot/wf/src-train2.txt','a') as f:
    for s in sent:
        f.write('\n')
        f.write(s)
        #f.write('\n')

with open('../DSBot/wf/tgt-train2.txt','a') as f:
    for s in targ:
        f.write('\n')
        f.write(s)

sent = []
targ = []
for av in auxiliary_plusnouns:
    for c in synonyms_outliersDetection_with_data:
        for d in headers:
            sent.append(av + ' ' +  c + ' ' + d[-1])
            targ.append('outliersDetection')
print('outliersDetection', len(sent))
with open('../DSBot/wf/src-train2.txt','a') as f:
    for s in sent:
        f.write('\n')
        f.write(s)
        #f.write('\n')

with open('../DSBot/wf/tgt-train2.txt','a') as f:
    for s in targ:
        f.write('\n')
        f.write(s)

sent = []
targ = []
for av in auxiliary_plusnouns:
    for c in synonyms_clustering:
        sent.append(av+' '+c)
        targ.append('clustering plot')
    for c in synonyms_clustering_with_data:
        for d in synonyms_data:
            sent.append(av + ' ' + c+' '+d)
            targ.append('clustering plot')

print('clustering', len(sent))

with open('../DSBot/wf/src-train2.txt','a') as f:
    for s in sent:
        f.write('\n')
        f.write(s)
        #f.write('\n')

with open('../DSBot/wf/tgt-train2.txt','a') as f:
    for s in targ:
        f.write('\n')
        f.write(s)

sent = []
targ = []
for av in auxiliary_plusnouns:
    for c in synonyms_classification:
        sent.append(av+' '+c)
        targ.append('classification')
    for c in synonyms_classification_with_data:
        for d in synonyms_data:
            sent.append(av + ' ' + c+' '+d)
            targ.append('classification')

print('classification', len(sent))
with open('../DSBot/wf/src-train2.txt','a') as f:
    for s in sent:
        f.write('\n')
        f.write(s)
        #f.write('\n')

with open('../DSBot/wf/tgt-train2.txt','a') as f:
    for s in targ:
        f.write('\n')
        f.write(s)
sent = []
targ = []
for av in auxiliary_plusnouns:
    for c in synonyms_prediction:
        sent.append(av+' '+c)
        targ.append('prediction')
    for c in synonyms_prediction_with_data:
        for d in synonyms_data:
            sent.append(av + ' ' + c+' '+d)
            targ.append('prediction')

print('prediction', len(sent)*3)
with open('../DSBot/wf/src-train2.txt','a') as f:
    for s in sent:
        f.write('\n')
        f.write(s)
        #f.write('\n')

with open('../DSBot/wf/tgt-train2.txt','a') as f:
    for s in targ:
        f.write('\n')
        f.write(s)
sent = []
targ = []
for av in auxiliary_plusnouns:
    for c in synonyms_relation:
        sent.append(av+' '+c)
        targ.append('relation')
    for c in synonyms_relation_with_data:
        for d in synonyms_data:
            sent.append(av + ' ' +c+' '+d)
            targ.append('relation')

print('relation', len(sent))
with open('../DSBot/wf/src-train2.txt','a') as f:
    for s in sent:
        f.write('\n')
        f.write(s)
        #f.write('\n')

with open('../DSBot/wf/tgt-train2.txt','a') as f:
    for s in targ:
        f.write('\n')
        f.write(s)
sent = []
targ = []
for av in auxiliary_plusnouns:
    for c in synonyms_associationRules:
        sent.append(av+' '+c)
        targ.append('associationRules')
    for c in synonyms_associationRules_with_data:
        for d in synonyms_data:
            sent.append(av + ' ' + c+' '+d)
            targ.append('associationRules')

print('associationRules', len(sent))
with open('../DSBot/wf/src-train2.txt','a') as f:
    for s in sent:
        f.write('\n')
        f.write(s)
        #f.write('\n')

with open('../DSBot/wf/tgt-train2.txt','a') as f:
    for s in targ:
        f.write('\n')
        f.write(s)
sent = []
targ = []
for av in auxiliary_plusnouns:
    for c in synonyms_correlation:
        sent.append(av+' '+c)
        targ.append('correlation')
    for c in synonyms_correlation_with_data:
        for d in synonyms_data:
            sent.append(av + ' ' +c+' '+d)
            targ.append('correlation')

print('correlation', len(sent)*2)
with open('../DSBot/wf/src-train2.txt','a') as f:
    for s in sent:
        f.write('\n')
        f.write(s)
        #f.write('\n')

with open('../DSBot/wf/tgt-train2.txt','a') as f:
    for s in targ:
        f.write('\n')
        f.write(s)

sent = []
targ = []
for av in auxiliary_plusnouns:
    for c in synonyms_outliersDetection:
        sent.append(av+' '+c)
        targ.append('outliersDetection')
    for c in synonyms_outliersDetection_with_data:
        for d in synonyms_data:
            sent.append(av + ' ' + c+' '+d)
            targ.append('outliersDetection')

print('outliersDetection', len(sent))
with open('../DSBot/wf/src-train2.txt','a') as f:
    for s in sent:
        f.write('\n')
        f.write(s)
        #f.write('\n')

with open('../DSBot/wf/tgt-train2.txt','a') as f:
    for s in targ:
        f.write('\n')
        f.write(s)

#done
sent = []
targ = []
for x in synonyms_userFeatureSel:
    for v in synonyms_clustering_verbs:
        for d in headers:
            num = random.randint(1,len(d[1]))
            if num==2:
                sent.append(x + ' ' + ' and '.join(random.sample(d[1], num)) + ' ' + v)
            else:
                sent.append(x+' '+', '.join(random.sample(d[1],num))+' '+v)
            targ.append('userFeatureSelection clustering')
    for v in verbs:
        for a in synonyms_clustering:
            for d in headers:
                num = random.randint(1,len(d[1]))
                if num==2:
                    sent.append(x + ' ' + ' and '.join(random.sample(d[1], num)) + ' ' + v+ ' ' + a)
                else:
                    sent.append(x+' '+', '.join(random.sample(d[1],num))+' '+v + ' ' + a)
                targ.append('userFeatureSelection clustering')
print('ufs clustering', len(sent))

sent = []
targ = []
for x in synonyms_userFeatureSel:
    for v in synonyms_classification_verbs_nodata:
        for d in headers:
            num = random.randint(1,len(d[1]))
            if num==2:
                sent.append(x + ' ' + ' and '.join(random.sample(d[1], num)) + ' ' + v)
            else:
                sent.append(x+' '+', '.join(random.sample(d[1],num))+' '+v)
            targ.append('userFeatureSelection classification')
    for v in verbs:
        for a in synonyms_classification:
            for d in headers:
                num = random.randint(1,len(d[1]))
                if num==2:
                    sent.append(x + ' ' + ' and '.join(random.sample(d[1], num)) + ' ' + v+ ' ' + a)
                else:
                    sent.append(x+' '+', '.join(random.sample(d[1],num))+' '+v + ' ' + a)
                targ.append('userFeatureSelection classification')
print('ufs classification', len(sent))

sent = []
targ = []
for x in synonyms_userFeatureSel:
    for v in synonyms_prediction_verbs_nodata:
        for d in headers:
            num = random.randint(1,len(d[1]))
            if num==2:
                sent.append(x + ' ' + ' and '.join(random.sample(d[1], num)) + ' ' + v)
            else:
                sent.append(x+' '+', '.join(random.sample(d[1],num))+' '+v)
            targ.append('userFeatureSelection prediction')
    for v in verbs:
        for a in synonyms_classification:
            for d in headers:
                num = random.randint(1,len(d[1]))
                if num==2:
                    sent.append(x + ' ' + ' and '.join(random.sample(d[1], num)) + ' ' + v+ ' ' + a)
                else:
                    sent.append(x+' '+', '.join(random.sample(d[1],num))+' '+v + ' ' + a)
                targ.append('userFeatureSelection prediction')
print('ufs prediction', len(sent))


sent = []
targ = []
for x in synonyms_userFeatureSel:
    for v in verbs:
        for a in synonyms_associationRules:
            for d in headers:
                num = random.randint(1,len(d[1]))
                if num==2:
                    sent.append(x + ' ' + ' and '.join(random.sample(d[1], num)) + ' ' + v+ ' ' + a)
                else:
                    sent.append(x+' '+', '.join(random.sample(d[1],num))+' '+v + ' ' + a)
                targ.append('userFeatureSelection associationRules')
print('ufs associationRules', len(sent))


sent = []
targ = []
for x in synonyms_userFeatureSel:
    for v in verbs:
        for a in synonyms_correlation:
            for d in headers:
                num = random.randint(1,len(d[1]))
                if num==2:
                    sent.append(x + ' ' + ' and '.join(random.sample(d[1], num)) + ' ' + v+ ' ' + a)
                else:
                    sent.append(x+' '+', '.join(random.sample(d[1],num))+' '+v + ' ' + a)
                targ.append('userFeatureSelection correlation')
print('ufs correlation', len(sent))


sent = []
targ = []
for x in synonyms_userFeatureSel:
    for v in verbs:
        for a in synonyms_outliersDetection:
            for d in headers:
                num = random.randint(1,len(d[1]))
                if num==2:
                    sent.append(x + ' ' + ' and '.join(random.sample(d[1], num)) + ' ' + v+ ' ' + a)
                else:
                    sent.append(x+' '+', '.join(random.sample(d[1],num))+' '+v + ' ' + a)
                targ.append('userFeatureSelection outliersDetection')
print('ufs outliersDetection', len(sent))



sent = []
targ = []
for x in synonyms_userFeatureSel:
    for v in verbs:
        for a in synonyms_relation:
            for d in headers:
                num = random.randint(1,len(d[1]))
                if num==2:
                    sent.append(x + ' ' + ' and '.join(random.sample(d[1], num)) + ' ' + v+ ' ' + a)
                else:
                    sent.append(x+' '+', '.join(random.sample(d[1],num))+' '+v + ' ' + a)
                targ.append('userFeatureSelection relation')
print('ufs relation', len(sent))

# DONE
sent = []
targ = []
for a in synonyms_afterclass_with_data:
    for av in auxiliary_plusverbs:
        for v in synonyms_extraction:
            for i in synonyms_importantFeatures:
                for d in headers:
                    if d[0]!=None:
                        sent.append(a + ' '+ d[0].lower()+' '+ av + ' ' + v + ' ' + i)
                    else:
                        sent.append(a + ' ' + d[-1].lower() + ' ' + av + ' ' + v + ' ' + i)
                    targ.append('classification featureImportance')
print('classification featureImportance', len(sent))

sent = []
targ = []
for a in synonyms_afterpred_with_data:
    for av in auxiliary_plusverbs:
        for v in synonyms_extraction:
            for i in synonyms_importantFeatures:
                for d in headers:
                    if d[0] != None:
                        sent.append(a + ' ' + d[0].lower() + ' ' + av + ' ' + v + ' ' + i)
                    else:
                        sent.append(a + ' ' + d[-1].lower() + ' ' + av + ' ' + v + ' ' + i)
                    targ.append('prediction featureImportance')
print('prediction featureImportance', len(sent))

sent = []
targ = []
for a in synonyms_afterclass_with_data:
    for av in auxiliary_plusverbs:
        for v in plot_verbs:
            for i in synonyms_importantFeatures:
                for d in headers:
                    if d[0] != None:
                        sent.append(a + ' ' + d[0].lower() + ' ' + av + ' ' + v + ' ' + i)
                    targ.append('classification featureImportance plot')
print('classification featureImportance plot', len(sent))

sent = []
targ = []
for a in synonyms_afterpred_with_data:
    for av in auxiliary_plusverbs:
        for v in plot_verbs:
            for i in synonyms_importantFeatures:
                for d in headers:
                    if d[0] != None:
                        sent.append(a + ' ' + d[0].lower() + ' ' + av + ' ' + v + ' ' + i)
                    targ.append('prediction featureImportance plot')
print('prediction featureImportance plot', len(sent))

# DONE INSERTED
sent = []
targ = []
for a in synonyms_afterclass:
    for av in auxiliary_plusverbs:
        for v in synonyms_extraction:
            for i in synonyms_importantFeatures:
                sent.append(a + ' '+ av + ' ' + v + ' ' + i)
                targ.append('classification featureImportance')
print('classification featureImportance', len(sent))


sent = []
targ = []
for a in synonyms_afterpred:
    for av in auxiliary_plusverbs:
        for v in synonyms_extraction:
            for i in synonyms_importantFeatures:
                sent.append(a + ' '+ av + ' ' + v + ' ' + i)
                targ.append('prediction featureImportance')
print('prediction featureImportance', len(sent))

sent = []
targ = []
for a in synonyms_afterclass:
    for av in auxiliary_plusverbs:
        for v in plot_verbs:
            for i in synonyms_importantFeatures:
                sent.append(a + ' '+ av + ' ' + v + ' ' + i)
                targ.append('classification featureImportance plot')
print('classification featureImportance plot', len(sent))

sent = []
targ = []
for a in synonyms_afterpred:
    for av in auxiliary_plusverbs:
        for v in plot_verbs:
            for i in synonyms_importantFeatures:
                sent.append(a + ' '+ av + ' ' + v + ' ' + i)
                targ.append('prediction featureImportance plot')
print('prediction featureImportance plot', len(sent))


#DONE
sent = []
targ = []
for av in auxiliary_plusverbs:
    for v in plot_verbs:
        for c in synonyms_clustering_with_data:
            for d in headers:
                sent.append(av + ' ' + v + ' ' + c + ' ' + d[-1])
                targ.append('clustering plot')
print('clustering', len(sent))

sent = []
targ = []
for av in auxiliary_plusverbs:
    for v in plot_verbs:
        for c in synonyms_classification_with_data:
            for d in headers:
                sent.append(av + ' ' + v + ' ' + c + ' ' + d[-1])
                targ.append('classification plot')
print('classification', len(sent))

sent = []
targ = []
for av in auxiliary_plusverbs:
    for v in plot_verbs:
        for c in synonyms_prediction_with_data:
            for d in headers:
                sent.append(av + ' ' + v + ' ' + c + ' ' + d[-1])
                targ.append('prediction plot')
print('prediction', len(sent)*2)

sent = []
targ = []
for av in auxiliary_plusverbs:
    for v in verbs:
        for c in synonyms_relation_with_data:
            for d in headers:
                sent.append(av + ' ' + v + ' ' + c + ' ' + d[-1])
                targ.append('relation plot')
print('relation', len(sent))

sent = []
targ = []
for av in auxiliary_plusverbs:
    for v in plot_verbs:
        for c in synonyms_associationRules_with_data:
            for d in headers:
                sent.append(av + ' ' + v + ' ' + c + ' ' + d[-1])
                targ.append('associationRules plot')
print('associationRules', len(sent))


sent = []
targ = []
for av in auxiliary_plusverbs:
    for v in plot_verbs:
        for c in synonyms_correlation_with_data:
            for d in headers:
                sent.append(av + ' ' + v + ' ' + c + ' ' + d[-1])
                targ.append('correlation plot')
print('correlation', len(sent))

sent = []
targ = []
for av in auxiliary_plusverbs:
    for v in plot_verbs:
        for c in synonyms_outliersDetection_with_data:
            for d in headers:
                sent.append(av + ' ' + v + ' ' + c + ' ' + d[-1])
                targ.append('outliersDetection plot')
print('outliersDetection', len(sent))


# DONE INSERTED
sent = []
targ = []
for av in auxiliary_plusverbs:
    for v in verbs:
        for c in synonyms_clustering_with_data:
            for d in headers:
                sent.append(av + ' ' + v + ' ' + c + ' ' + d[-1])
                targ.append('clustering')
print('clustering', len(sent))

sent = []
targ = []
for av in auxiliary_plusverbs:
    for v in verbs:
        for c in synonyms_classification_with_data:
            for d in headers:
                sent.append(av + ' ' + v + ' ' + c + ' ' + d[-1])
                targ.append('classification')
print('classification', len(sent))

sent = []
targ = []
for av in auxiliary_plusverbs:
    for v in verbs:
        for c in synonyms_prediction_with_data:
            for d in headers:
                sent.append(av + ' ' + v + ' ' + c + ' ' + d[-1])
                targ.append('prediction')
print('prediction', len(sent)*3)

sent = []
targ = []
for av in auxiliary_plusverbs:
    for v in verbs:
        for c in synonyms_relation_with_data:
            for d in headers:
                sent.append(av + ' ' + v + ' ' + c + ' ' + d[-1])
                targ.append('relation')
print('relation', len(sent))

sent = []
targ = []
for av in auxiliary_plusverbs:
    for v in verbs:
        for c in synonyms_associationRules_with_data:
            for d in headers:
                sent.append(av + ' ' + v + ' ' + c + ' ' + d[-1])
                targ.append('associationRules')
print('associationRules', len(sent))


sent = []
targ = []
for av in auxiliary_plusverbs:
    for v in verbs:
        for c in synonyms_correlation_with_data:
            for d in headers:
                sent.append(av + ' ' + v + ' ' + c + ' ' + d[-1])
                targ.append('correlation')
print('correlation', len(sent)*2)


sent = []
targ = []
for av in auxiliary_plusverbs:
    for v in verbs:
        for c in synonyms_outliersDetection_with_data:
            for d in headers:
                sent.append(av + ' ' + v + ' ' + c + ' ' + d[-1])
                targ.append('outliersDetection')
print('outliersDetection', len(sent))


sent = []
targ = []
for av in auxiliary_plusverbs:
    for v in plot_verbs:
        for c in synonyms_clustering:
            sent.append(av+' '+v+ ' '+c)
            targ.append('clustering plot')
        for c in synonyms_clustering_with_data:
            for d in synonyms_data:
                sent.append(av + ' ' + v+' '+c+' '+d)
                targ.append('clustering plot')

print('clustering', len(sent))

sent = []
targ = []
for av in auxiliary_plusverbs:
    for v in plot_verbs:
        for c in synonyms_classification:
            sent.append(av+' '+v+ ' '+c)
            targ.append('classification plot')
        for c in synonyms_classification_with_data:
            for d in synonyms_data:
                sent.append(av + ' ' + v+' '+c+' '+d)
                targ.append('classification plot')

print('classification', len(sent))

sent = []
targ = []
for av in auxiliary_plusverbs:
    for v in plot_verbs:
        for c in synonyms_prediction:
            sent.append(av+' '+v+ ' '+c)
            targ.append('prediction plot')
        for c in synonyms_prediction_with_data:
            for d in synonyms_data:
                sent.append(av + ' ' + v+' '+c+' '+d)
                targ.append('prediction plot')

print('prediction', len(sent)*3)

sent = []
targ = []
for av in auxiliary_plusverbs:
    for v in plot_verbs:
        for c in synonyms_relation:
            sent.append(av+' '+v+ ' '+c)
            targ.append('relation plot')
        for c in synonyms_relation_with_data:
            for d in synonyms_data:
                sent.append(av + ' ' + v+' '+c+' '+d)
                targ.append('relation plot')

print('relation', len(sent))

sent = []
targ = []
for av in auxiliary_plusverbs:
    for v in plot_verbs:
        for c in synonyms_associationRules:
            sent.append(av+' '+v+ ' '+c)
            targ.append('associationRules plot')
        for c in synonyms_associationRules_with_data:
            for d in synonyms_data:
                sent.append(av + ' ' + v+' '+c+' '+d)
                targ.append('associationRules plot')

print('associationRules', len(sent))

sent = []
targ = []
for av in auxiliary_plusverbs:
    for v in plot_verbs:
        for c in synonyms_correlation:
            sent.append(av+' '+v+ ' '+c)
            targ.append('correlation plot')
        for c in synonyms_correlation_with_data:
            for d in synonyms_data:
                sent.append(av + ' ' + v+' '+c+' '+d)
                targ.append('correlation plot')

print('correlation', len(sent)*2)

sent = []
targ = []
for av in auxiliary_plusverbs:
    for v in plot_verbs:
        for c in synonyms_outliersDetection:
            sent.append(av+' '+v+ ' '+c)
            targ.append('outliersDetection plot')
        for c in synonyms_outliersDetection_with_data:
            for d in synonyms_data:
                sent.append(av + ' ' + v+' '+c+' '+d)
                targ.append('outliersDetection plot')

print('outliersDetection', len(sent))

sent = []
targ = []
for av in auxiliary_plusverbs:
    for v in verbs:
        for c in synonyms_clustering:
            sent.append(av+' '+v+ ' '+c)
            targ.append('clustering')
        for c in synonyms_clustering_with_data:
            for d in synonyms_data:
                sent.append(av + ' ' + v+' '+c+' '+d)
                targ.append('clustering')
print('clustering', len(sent))


sent = []
targ = []
for av in auxiliary_plusverbs:
    for v in verbs:
        for c in synonyms_classification:
            sent.append(av+' '+v+ ' '+c)
            targ.append('classification')
        for c in synonyms_classification_with_data:
            for d in synonyms_data:
                sent.append(av + ' ' + v+' '+c+' '+d)
                targ.append('classification')

print('classification', len(sent))

sent = []
targ = []
for av in auxiliary_plusverbs:
    for v in verbs:
        for c in synonyms_prediction:
            sent.append(av+' '+v+ ' '+c)
            targ.append('prediction')
        for c in synonyms_prediction_with_data:
            for d in synonyms_data:
                sent.append(av + ' ' + v+' '+c+' '+d)
                targ.append('prediction')

print('prediction', len(sent)*3)

sent = []
targ = []
for av in auxiliary_plusverbs:
    for v in verbs:
        for c in synonyms_relation:
            sent.append(av+' '+v+ ' '+c)
            targ.append('relation')
        for c in synonyms_relation_with_data:
            for d in synonyms_data:
                sent.append(av + ' ' + v+' '+c+' '+d)
                targ.append('relation')

print('relation', len(sent))

sent = []
targ = []
for av in auxiliary_plusverbs:
    for v in verbs:
        for c in synonyms_associationRules:
            sent.append(av+' '+v+ ' '+c)
            targ.append('associationRules')
        for c in synonyms_associationRules_with_data:
            for d in synonyms_data:
                sent.append(av + ' ' + v+' '+c+' '+d)
                targ.append('associationRules')

print('associationRules', len(sent))

sent = []
targ = []
for av in auxiliary_plusverbs:
    for v in verbs:
        for c in synonyms_correlation:
            sent.append(av+' '+v+ ' '+c)
            targ.append('correlation')
        for c in synonyms_correlation_with_data:
            for d in synonyms_data:
                sent.append(av + ' ' + v+' '+c+' '+d)
                targ.append('correlation')

print('correlation', len(sent)*2)


sent = []
targ = []
for av in auxiliary_plusverbs:
    for v in verbs:
        for c in synonyms_outliersDetection:
            sent.append(av+' '+v+ ' '+c)
            targ.append('outliersDetection')
        for c in synonyms_outliersDetection_with_data:
            for d in synonyms_data:
                sent.append(av + ' ' + v+' '+c+' '+d)
                targ.append('outliersDetection')

print('outliersDetection', len(sent))

sent = []
targ = []
for av in auxiliary_plusverbs:
    for c in synonyms_featureSel:
        sent.append(av+ ' '+c)
        targ.append('featureSelection')

print('featureSelection', len(sent)*4)

sent = []
targ = []
for av in auxiliary_plusverbs:
    for v in synonyms_clustering_verbs:
        sent.append(av+' '+v)
        targ.append('clustering')
        for d in synonyms_data:
            sent.append(av + ' ' + v+' '+d)
            targ.append('clustering')

print('clustering', len(sent))

sent = []
targ = []
for av in auxiliary_plusverbs:
    for v in synonyms_classification_verbs_nodata:
        sent.append(av+' '+v)
        targ.append('classification')
    for v in synonyms_classification_verbs_with_data:
        for d in synonyms_data:
            sent.append(av + ' ' + v+' '+d)
            targ.append('classification')

print('classification', len(sent))

sent = []
targ = []
for av in auxiliary_plusverbs:
    for v in synonyms_prediction_verbs_nodata:
        sent.append(av+' '+v)
        targ.append('prediction')
    for v in synonyms_prediction_verbs_with_data:
        for d in synonyms_data:
            sent.append(av + ' ' + v+' '+d)
            targ.append('prediction')

print('prediction',len(sent)*2)

sent = []
targ = []
for av in auxiliary_plusverbs:
    for v in synonyms_outliersDetection_verbs_nodata:
        sent.append(av+' '+v)
        targ.append('outliersDetection')
    for v in synonyms_outliersDetection_verbs_with_data:
        for d in synonyms_data:
            sent.append(av + ' ' + v+' '+d)
            targ.append('outliersDetection')

print('outliersDetection',len(sent)*3)