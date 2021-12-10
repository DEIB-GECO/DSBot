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
synonyms_featureSel = ['select some features', 'extract some features', 'select some columns', 'extract some columns','considering some features', 'using some features']

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

synonyms_data = ['data','samples','rows', 'examples','information']

auxiliary_plusverbs = ['can you', 'i want to', 'let\'s', 'could you', 'i would like to', 'i would', '', 'are you able to', 'do you manage to', 'shall we',
                       'may you', 'might you', 'would you']
auxiliary_plusnouns = ['i want', 'are there', 'look for', 'let\'s search for', 'perform', 'compute', 'do', 'do they exist', 'analyze', 'have you' ,'shall we look for']

verbs = ['find',  'compute', 'perform', 'identify', 'analyze', 'look for', 'search for', 'produce', 'consider', 'inspect', 'investigate' ] # usa condizionale --> dividere parte i want to/can/could (spezzare verbo semantico)
plot_verbs = ['see', 'show', 'show me', 'visualize','plot', 'draw', 'look at','observe', 'spot', 'view', 'watch', 'inspect','display','exhibit' , 'present', 'expose'
              'foresee']

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
#DONE INSERTED
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

print('prediction', len(sent))

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

print('correlation', len(sent))


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


print('featureSelection', len(sent))

# DONE, INSERTED
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

print('prediction',len(sent))

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

print('outliersDetection',len(sent))
