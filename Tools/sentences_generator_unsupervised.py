import random

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
auxiliary_plusverbs = ['can you', 'i want to', 'let\'s', 'could you', 'i would like to', 'i would', '', 'are you able to', 'do you manage to', 'shall we', 'may you', 'might you', 'would you']
auxiliary_plusnouns = ['i want', 'are there', 'look for', 'let\'s search for', 'perform', 'compute', 'do', 'do they exist', 'analyze', 'have you' ,'shall we look for']
verbs = ['find',  'compute', 'perform', 'identify', 'analyze', 'look for', 'search for', 'produce', 'consider', 'inspect', 'investigate' ] # usa condizionale --> dividere parte i want to/can/could (spezzare verbo semantico)
plot_verbs = ['see', 'show', 'show me', 'visualize','plot', 'draw', 'look at','observe', 'spot', 'view', 'watch', 'inspect','display','exhibit' , 'present', 'expose'
              'foresee']
clustering_verbs = ['cluster', 'assemble', 'group','associate','gather','aggregate','collect']
synonyms_data = ['data','samples','rows', 'my data','examples','information']

synonyms_userFeatureSel = ['according to', 'selecting only', 'considering only', 'if you consider only', 'if you select', 'looking at', 'keeping into consideration',
                           'taking into account', 'taking into consideration only', 'filtering out']

sentences_fS_aR = []
list_target = []
for f in synonyms_userFeatureSel:
    for v in verbs:
        for s in synonyms_associationRules:
            for h in headers_nolabel:
                sentences_fS_aR.append(f + ' ' + ', '.join(random.sample(h[0],random.randint(1,len(h[0]))))+ ' ' + v + ' ' + s)
                list_target.append('userFeatureSelection associationRules')
                break

# for f in synonyms_userFeatureSel:
#     for v in verbs:
#         for s in synonyms_associationRules_with_data:
#             for h in headers_nolabel:
#                 sentences_fS_aR.append(f + ' ' + ', '.join(random.sample(h[0],random.randint(1,len(h[0]))))+ ' ' + v + ' ' + s + ' ' + h[1])
#                 list_target.append('userFeatureSelection associationRules')

for f in synonyms_userFeatureSel:
    for v in plot_verbs:
        for s in synonyms_associationRules:
            for h in headers_nolabel:
                sentences_fS_aR.append(f + ' ' + ', '.join(random.sample(h[0],random.randint(1,len(h[0]))))+ ' ' + v + ' ' + s)
                list_target.append('userFeatureSelection associationRules plot')
                break

# for f in synonyms_userFeatureSel:
#     for v in plot_verbs:
#         for s in synonyms_associationRules_with_data:
#             for h in headers_nolabel:
#                 sentences_fS_aR.append(f + ' ' + ', '.join(random.sample(h[0],random.randint(1,len(h[0]))))+ ' ' + v + ' ' + s + ' ' + h[1])
#                 list_target.append('userFeatureSelection associationRules plot')

with open('../DSBot/wf/src-val.txt','a') as f:
    for s in sentences_fS_aR:
        f.write('\n')
        f.write(s)
        #f.write('\n')

with open('../DSBot/wf/tgt-val.txt','a') as f:
    for s in list_target:
        f.write('\n')
        f.write(s)

sentences_fS_oD = []
list_target = []
for f in synonyms_userFeatureSel:
    for v in verbs:
        for s in synonyms_outliersDetection:
            for h in headers_nolabel:
                sentences_fS_oD.append(f + ' ' + ', '.join(random.sample(h[0],random.randint(1,len(h[0]))))+ ' ' + v + ' ' + s)
                list_target.append('userFeatureSelection outliersDetection')
                break

# for f in synonyms_userFeatureSel:
#     for v in verbs:
#         for s in synonyms_outliersDetection_with_data:
#             for h in headers_nolabel:
#                 sentences_fS_oD.append(f + ' ' + ', '.join(random.sample(h[0],random.randint(1,len(h[0]))))+ ' ' + v + ' ' + s + ' ' + h[1])
#                 list_target.append('userFeatureSelection outliersDetection')

for f in synonyms_userFeatureSel:
    for v in plot_verbs:
        for s in synonyms_outliersDetection:
            for h in headers_nolabel:
                sentences_fS_oD.append(f + ' ' + ', '.join(random.sample(h[0],random.randint(1,len(h[0]))))+ ' ' + v + ' ' + s)
                list_target.append('userFeatureSelection outliersDetection plot')
                break

# for f in synonyms_userFeatureSel:
#     for v in plot_verbs:
#         for s in synonyms_outliersDetection_with_data:
#             for h in headers_nolabel:
#                 sentences_fS_oD.append(f + ' ' + ', '.join(random.sample(h[0],random.randint(1,len(h[0]))))+ ' ' + v + ' ' + s + ' ' + h[1])
#                 list_target.append('userFeatureSelection outliersDetection plot')

with open('../DSBot/wf/src-val.txt','a') as f:
    for s in sentences_fS_oD:
        f.write('\n')
        f.write(s)
        #f.write('\n')

with open('../DSBot/wf/tgt-val.txt','a') as f:
    for s in list_target:
        f.write('\n')
        f.write(s)

sentences_fS_clustering = []
list_target = []
for f in synonyms_userFeatureSel:
    for v in verbs:
        for s in synonyms_clustering:
            for h in headers_nolabel:
                sentences_fS_clustering.append(f + ' ' + ', '.join(random.sample(h[0],random.randint(1,len(h[0]))))+ ' ' + v + ' ' + s)
                list_target.append('userFeatureSelection clustering')
                break

# for f in synonyms_userFeatureSel:
#     for v in verbs:
#         for s in synonyms_clustering_with_data:
#             for h in headers_nolabel:
#                 sentences_fS_clustering.append(f + ' ' + ', '.join(random.sample(h[0],random.randint(1,len(h[0]))))+ ' ' + v + ' ' + s + ' ' + h[1])
#                 list_target.append('userFeatureSelection clustering')

for f in synonyms_userFeatureSel:
    for v in plot_verbs:
        for s in synonyms_clustering:
            for h in headers_nolabel:
                sentences_fS_clustering.append(f + ' ' + ', '.join(random.sample(h[0],random.randint(1,len(h[0]))))+ ' ' + v + ' ' + s)
                list_target.append('userFeatureSelection clustering plot')
                break

# for f in synonyms_userFeatureSel:
#     for v in plot_verbs:
#         for s in synonyms_clustering_with_data:
#             for h in headers_nolabel:
#                 sentences_fS_clustering.append(f + ' ' + ', '.join(random.sample(h[0],random.randint(1,len(h[0]))))+ ' ' + v + ' ' + s + ' ' + h[1])
#                 list_target.append('userFeatureSelection clustering plot')

with open('../DSBot/wf/src-val.txt','a') as f:
    for s in sentences_fS_clustering:
        f.write('\n')
        f.write(s)
        #f.write('\n')

with open('../DSBot/wf/tgt-val.txt','a') as f:
    for s in list_target:
        f.write('\n')
        f.write(s)



sentences_correlation = []
list_target = []
for v in verbs:
    for s in synonyms_correlation:
        sentences_correlation.append(v+' '+s)
        list_target.append('correlation')
        break

# for v in verbs:
#     for s in synonyms_correlation_with_data:
#         for h in headers_nolabel:
#             sentences_correlation.append(v + ' ' + s + ' ' + h[1])
#             list_target.append('correlation')

for v in plot_verbs:
    for s in synonyms_correlation:
        sentences_correlation.append(v+' '+s)
        list_target.append('correlation plot')
        break
# for v in plot_verbs:
#     for s in synonyms_correlation_with_data:
#         for h in headers_nolabel:
#             sentences_correlation.append(v + ' ' + s + ' ' + h[1])
#             list_target.append('correlation plot')


with open('../DSBot/wf/src-val.txt','a') as f:
    for s in sentences_correlation:
        f.write('\n')
        f.write(s)
        #f.write('\n')

with open('../DSBot/wf/tgt-val.txt','a') as f:
    for s in list_target:
        f.write('\n')
        f.write(s)

sentences_relation = []
list_target = []
for v in verbs:
    for s in synonyms_relation:
        sentences_relation.append(v+' '+s)
        list_target.append('relation')
        break

# for v in verbs:
#     for s in synonyms_relation_with_data:
#         for h in headers_nolabel:
#             sentences_relation.append(v + ' ' + s + ' ' + h[1])
#             list_target.append('relation')

for v in plot_verbs:
    for s in synonyms_relation:
        sentences_relation.append(v+' '+s)
        list_target.append('relation plot')
        break
# for v in plot_verbs:
#     for s in synonyms_relation_with_data:
#         for h in headers_nolabel:
#             sentences_relation.append(v + ' ' + s + ' ' + h[1])
#             list_target.append('relation plot')

with open('../DSBot/wf/src-val.txt','a') as f:
    for s in sentences_relation:
        f.write('\n')
        f.write(s)
        #f.write('\n')

with open('../DSBot/wf/tgt-val.txt','a') as f:
    for s in list_target:
        f.write('\n')
        f.write(s)

sentences_associationRules = []
list_target = []
for v in verbs:
    for s in synonyms_associationRules:
        sentences_associationRules.append(v+' '+s)
        list_target.append('associationRules')
        break

# for v in verbs:
#     for s in synonyms_associationRules_with_data:
#         for h in headers_nolabel:
#             sentences_associationRules.append(v + ' ' + s + ' ' + h[1])
#             list_target.append('associationRules')

for v in plot_verbs:
    for s in synonyms_associationRules:
        sentences_associationRules.append(v+' '+s)
        list_target.append('associationRules plot')
        break
# for v in plot_verbs:
#     for s in synonyms_associationRules_with_data:
#         for h in headers_nolabel:
#             sentences_associationRules.append(v + ' ' + s + ' ' + h[1])
#             list_target.append('associationRules plot')


with open('../DSBot/wf/src-val.txt','a') as f:
    for s in sentences_associationRules:
        f.write('\n')
        f.write(s)
        #f.write('\n')

with open('../DSBot/wf/tgt-val.txt','a') as f:
    for s in list_target:
        f.write('\n')
        f.write(s)

sentences_outliersDetection = []
list_target = []
for v in verbs:
    for s in synonyms_outliersDetection:
        sentences_outliersDetection.append(v+' '+s)
        list_target.append('outliersDetection')
        break

# for v in verbs:
#     for s in synonyms_outliersDetection_with_data:
#         for h in headers_nolabel:
#             sentences_outliersDetection.append(v + ' ' + s + ' ' + h[1])
#             list_target.append('outliersDetection')

for v in plot_verbs:
    for s in synonyms_outliersDetection:
        sentences_outliersDetection.append(v+' '+s)
        list_target.append('outliersDetection plot')
        break
# for v in plot_verbs:
#     for s in synonyms_outliersDetection_with_data:
#         for h in headers_nolabel:
#             sentences_outliersDetection.append(v + ' ' + s + ' ' + h[1])
#             list_target.append('outliersDetection plot')

with open('../DSBot/wf/src-val.txt','a') as f:
    for s in sentences_outliersDetection:
        f.write('\n')
        f.write(s)
        #f.write('\n')

with open('../DSBot/wf/tgt-val.txt','a') as f:
    for s in list_target:
        f.write('\n')
        f.write(s)

sentences_clustering = []
list_target = []
for v in verbs:
    for s in synonyms_clustering:
        sentences_clustering.append(v+' '+s)
        list_target.append('clustering')
        break

# for v in verbs:
#     for s in synonyms_clustering_with_data:
#         for h in headers_nolabel:
#             sentences_clustering.append(v + ' ' + s + ' ' + h[1])
#             list_target.append('clustering')

for v in plot_verbs:
    for s in synonyms_clustering:
        sentences_clustering.append(v+' '+s)
        list_target.append('clustering plot')
        break
# for v in plot_verbs:
#     for s in synonyms_clustering_with_data:
#         for h in headers_nolabel:
#             sentences_clustering.append(v + ' ' + s + ' ' + h[1])
#             list_target.append('clustering plot')


with open('../DSBot/wf/src-val.txt','a') as f:
    for s in sentences_clustering:
        f.write('\n')
        f.write(s)

with open('../DSBot/wf/tgt-val.txt','a') as f:
    for s in list_target:
        f.write('\n')
        f.write(s)