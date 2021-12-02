headers_label = [('Diagnosis',
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
                  'students')
               ]

headers_nolabel = [(["Kingdom", "DNAtype" ,"SpeciesID" ,"Ncodons" ,"SpeciesName" , "codon"],
                   'sequences'),
                   (["buying","maint","doors","persons","lug_boot","safety"],
                    'cars')]

synonyms_clustering = ['groups', 'clusters', 'sets', 'similar samples', 'groups of similar samples', 'sets of similar samples', 'sets of similar elements',
                       'elements which are similar', 'elements that are uniform', 'uniform samples']
synonyms_relation = ['relations', 'relations among features', 'relations among columns', 'associations between features', 'associations between columns',
                     'links between features', 'links between columns', 'connections between features', 'connections between columns', 'interconnections',
                     'interrelations']
synonyms_correlation = ['correlation', 'correlation among features', 'correlation among columns']
synonyms_associationRules = ['association rules', 'rules of association between features', 'rules that associates features', 'rules of association between columns',
                             'rules that associate columns', 'association rules between features', 'association rules between columns']
synonyms_outliersDetection = ['strange data', 'strange samples', 'anomalies in data', 'anomalies in samples', 'anomalies in my data', 'strange sample among my data',
                              'outliers in data','incoherent data', 'incoherent samples', 'outliers among samples', 'irregularities between samples',
                              'anomalies between samples']

synonyms_clustering_with_data = ['groups of', 'sets of', 'clusters of', 'similar samples of', 'sets of similar',  'groups of similar','uniform' ]
synonyms_relation_with_data = ['relations among', 'associations among', 'associations between', 'links between', 'connections between', 'interconnections among']
synonyms_correlation_with_data = ['correlations among']
synonyms_associationRules_with_data = ['rules of association between', 'rules that associates','association rules between']
synonyms_outliersDetection_with_data = ['strange samples among', 'anomalies in', 'outliers in','inchoerent', 'irregularities among']

verbs = ['can you find',  'i want', 'can you compute', 'do they exist', 'i want to compute', 'are there', 'i want to identify', 'let\'s search for', 'look for']
plot_verbs = ['can i see', 'can you show', 'show me', 'can i visualize','plot', 'draw', 'can you draw', 'i want to see', 'i want to visualize']

sentences_correlation = []
list_target = []
for v in verbs:
    for s in synonyms_correlation:
        sentences_correlation.append(v+' '+s)
        list_target.append('correlation')

for v in verbs:
    for s in synonyms_correlation_with_data:
        for h in headers_nolabel:
            sentences_correlation.append(v + ' ' + s + ' ' + h[1])
            list_target.append('correlation')

for v in plot_verbs:
    for s in synonyms_correlation:
        sentences_correlation.append(v+' '+s)
        list_target.append('correlation plot')
for v in plot_verbs:
    for s in synonyms_correlation_with_data:
        for h in headers_nolabel:
            sentences_correlation.append(v + ' ' + s + ' ' + h[1])
            list_target.append('correlation plot')

print(len(sentences_correlation))
print(len(list_target))
with open('../DSBot/wf/src-train2.txt','a') as f:
    for s in sentences_correlation:
        f.write('\n')
        f.write(s)
        #f.write('\n')

with open('../DSBot/wf/tgt-train2.txt','a') as f:
    for s in list_target:
        f.write('\n')
        f.write(s)

sentences_relation = []
list_target = []
for v in verbs:
    for s in synonyms_relation:
        sentences_relation.append(v+' '+s)
        list_target.append('relation')

for v in verbs:
    for s in synonyms_relation_with_data:
        for h in headers_nolabel:
            sentences_relation.append(v + ' ' + s + ' ' + h[1])
            list_target.append('relation')

for v in plot_verbs:
    for s in synonyms_relation:
        sentences_relation.append(v+' '+s)
        list_target.append('relation plot')
for v in plot_verbs:
    for s in synonyms_relation_with_data:
        for h in headers_nolabel:
            sentences_relation.append(v + ' ' + s + ' ' + h[1])
            list_target.append('relation plot')

print(len(sentences_relation))
print(len(list_target))
with open('../DSBot/wf/src-train2.txt','a') as f:
    for s in sentences_relation:
        f.write('\n')
        f.write(s)
        #f.write('\n')

with open('../DSBot/wf/tgt-train2.txt','a') as f:
    for s in list_target:
        f.write('\n')
        f.write(s)

sentences_associationRules = []
list_target = []
for v in verbs:
    for s in synonyms_associationRules:
        sentences_associationRules.append(v+' '+s)
        list_target.append('associationRules')

for v in verbs:
    for s in synonyms_associationRules_with_data:
        for h in headers_nolabel:
            sentences_associationRules.append(v + ' ' + s + ' ' + h[1])
            list_target.append('associationRules')

for v in plot_verbs:
    for s in synonyms_associationRules:
        sentences_associationRules.append(v+' '+s)
        list_target.append('associationRules tableAssociationRules')
for v in plot_verbs:
    for s in synonyms_associationRules_with_data:
        for h in headers_nolabel:
            sentences_associationRules.append(v + ' ' + s + ' ' + h[1])
            list_target.append('associationRules tableAssociationRules')

print(len(sentences_associationRules))
print(len(list_target))
with open('../DSBot/wf/src-train2.txt','a') as f:
    for s in sentences_associationRules:
        f.write('\n')
        f.write(s)
        #f.write('\n')

with open('../DSBot/wf/tgt-train2.txt','a') as f:
    for s in list_target:
        f.write('\n')
        f.write(s)

sentences_outliersDetection = []
list_target = []
for v in verbs:
    for s in synonyms_outliersDetection:
        sentences_outliersDetection.append(v+' '+s)
        list_target.append('outliersDetection')

for v in verbs:
    for s in synonyms_outliersDetection_with_data:
        for h in headers_nolabel:
            sentences_outliersDetection.append(v + ' ' + s + ' ' + h[1])
            list_target.append('outliersDetection')

for v in plot_verbs:
    for s in synonyms_outliersDetection:
        sentences_outliersDetection.append(v+' '+s)
        list_target.append('outliersDetection plot')
for v in plot_verbs:
    for s in synonyms_outliersDetection_with_data:
        for h in headers_nolabel:
            sentences_outliersDetection.append(v + ' ' + s + ' ' + h[1])
            list_target.append('outliersDetection plot')

print(len(sentences_outliersDetection))
print(len(list_target))

with open('../DSBot/wf/src-train2.txt','a') as f:
    for s in sentences_outliersDetection:
        f.write('\n')
        f.write(s)
        #f.write('\n')

with open('../DSBot/wf/tgt-train2.txt','a') as f:
    for s in list_target:
        f.write('\n')
        f.write(s)

sentences_clustering = []
list_target = []
for v in verbs:
    for s in synonyms_clustering:
        sentences_clustering.append(v+' '+s)
        list_target.append('clustering')

for v in verbs:
    for s in synonyms_clustering_with_data:
        for h in headers_nolabel:
            sentences_clustering.append(v + ' ' + s + ' ' + h[1])
            list_target.append('clustering')

for v in plot_verbs:
    for s in synonyms_clustering:
        sentences_clustering.append(v+' '+s)
        list_target.append('clustering plot')
for v in plot_verbs:
    for s in synonyms_clustering_with_data:
        for h in headers_nolabel:
            sentences_clustering.append(v + ' ' + s + ' ' + h[1])
            list_target.append('clustering plot')
print(sentences_clustering)
print(len(sentences_clustering))
print(len(list_target))

#with open('../DSBot/wf/src-train2.txt','a') as f:
#    for s in sentences_clustering:
#        f.write(s)
#        f.write('\n')

#with open('../DSBot/wf/tgt-train2.txt','a') as f:
#    for s in list_target:
#        f.write(s)
#        f.write('\n')