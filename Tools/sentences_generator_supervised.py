import random

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

synonyms_classification = ['classes', 'classification', 'classes according to the label', 'division of the data according to the label']
synonyms_prediction = ['prediction', 'predictions']
synonyms_regression = ['regression']
synonyms_classification_verbs = ['can you classify the data', 'i want you to classify the data', 'classify data', 'predict classes among data']
synonyms_prediction_verbs = ['can you predict the label', 'predict data', 'predict label in my data', 'predict the label', 'i want you to predict the label',
                             'forecast the label', 'i want you to forecast the label']
synonyms_classification_verbs_with_data = ['can you classify the', 'i want you to classify the', 'classify', 'predict classes according to']
synonyms_prediction_verbs_with_data = ['can you predict the', 'predict ', 'predict the ', 'i want you to predict',
                             'forecast', 'i want you to forecast the ']
synonyms_classification_with_data = ['classes according to', 'classification using', 'division of the data according to' ]
synonyms_prediction_with_data = ['prediction of', 'forecast the', 'predict the']

verbs = ['can you find',  'i want', 'can you compute', 'i want to compute',  'i want to identify', 'perform', 'compute']
plot_verbs = ['can i see', 'can you show', 'show me', 'can i visualize','plot', 'draw', 'can you draw', 'i want to see', 'i want to visualize']


synonyms_userFeatureSel = ['according to', 'selecting only', 'considering only', 'if you consider only', 'if you select', 'looking at', 'keeping into consideration',
                           'taking into account', 'taking into consideration only', 'filtering out']

sentences_fS_class = []
list_target = []
for f in synonyms_userFeatureSel:
    for v in verbs:
        for s in synonyms_classification:
            for h in headers_label:
                sentences_fS_class.append(f + ' ' + ', '.join(random.sample(h[1],random.randint(1,len(h[1]))))+ ' ' + v + ' ' + s)
                list_target.append('userFeatureSelection classification')

# for f in synonyms_userFeatureSel:
#     for v in verbs:
#         for s in synonyms_classification_with_data:
#             for h in headers_label:
#                 sentences_fS_class.append(f + ' ' + ', '.join(random.sample(h[1],random.randint(1,len(h[1]))))+ ' ' + v + ' ' + s + ' ' + h[0])
#                 list_target.append('userFeatureSelection classification')

for f in synonyms_userFeatureSel:
    for v in plot_verbs:
        for s in synonyms_classification:
            for h in headers_label:
                sentences_fS_class.append(f + ' ' + ', '.join(random.sample(h[1],random.randint(1,len(h[1]))))+ ' ' + v + ' ' + s)
                list_target.append('userFeatureSelection classification plot')

# for f in synonyms_userFeatureSel:
#     for v in plot_verbs:
#         for s in synonyms_classification_with_data:
#             for h in headers_label:
#                 sentences_fS_class.append(f + ' ' + ', '.join(random.sample(h[1],random.randint(1,len(h[1]))))+ ' ' + v + ' ' + s + ' ' + h[0])
#                 list_target.append('userFeatureSelection classification plot')


with open('../DSBot/wf/src-train2.txt','a') as f:
    for s in sentences_fS_class:
        f.write('\n')
        f.write(s)
        #f.write('\n')

with open('../DSBot/wf/tgt-train2.txt','a') as f:
    for s in list_target:
        f.write('\n')
        f.write(s)

sentences_fS_pred = []
list_target = []
for f in synonyms_userFeatureSel:
    for v in verbs:
        for s in synonyms_prediction:
            for h in headers_label:
                sentences_fS_pred.append(f + ' ' + ', '.join(random.sample(h[1],random.randint(1,len(h[1]))))+ ' ' + v + ' ' + s)
                list_target.append('userFeatureSelection prediction')

# for f in synonyms_userFeatureSel:
#     for v in verbs:
#         for s in synonyms_prediction_with_data:
#             for h in headers_label:
#                 sentences_fS_pred.append(f + ' ' + ', '.join(random.sample(h[1],random.randint(1,len(h[1]))))+ ' ' + v + ' ' + s + ' ' + h[0])
#                 list_target.append('userFeatureSelection prediction')

for f in synonyms_userFeatureSel:
    for v in plot_verbs:
        for s in synonyms_prediction:
            for h in headers_label:
                sentences_fS_pred.append(f + ' ' + ', '.join(random.sample(h[1],random.randint(1,len(h[1]))))+ ' ' + v + ' ' + s)
                list_target.append('userFeatureSelection prediction plot')

# for f in synonyms_userFeatureSel:
#     for v in plot_verbs:
#         for s in synonyms_prediction_with_data:
#             for h in headers_label:
#                 sentences_fS_pred.append(f + ' ' + ', '.join(random.sample(h[1],random.randint(1,len(h[1]))))+ ' ' + v + ' ' + s + ' ' + h[0])
#                 list_target.append('userFeatureSelection prediction plot')

with open('../DSBot/wf/src-train2.txt','a') as f:
    for s in sentences_fS_pred:
        f.write('\n')
        f.write(s)
        #f.write('\n')

with open('../DSBot/wf/tgt-train2.txt','a') as f:
    for s in list_target:
        f.write('\n')
        f.write(s)

sentences_fS_class = []
list_target = []
for f in synonyms_userFeatureSel:
    for s in synonyms_classification_verbs:
        for h in headers_label:
            sentences_fS_class.append(f + ' ' + ', '.join(random.sample(h[1],random.randint(1,len(h[1]))))+ ' ' + ' ' + s)
            list_target.append('userFeatureSelection classification')

# for f in synonyms_userFeatureSel:
#     for s in synonyms_classification_verbs_with_data:
#         for h in headers_label:
#             sentences_fS_class.append(f + ' ' + ', '.join(random.sample(h[1],random.randint(1,len(h[1]))))+ ' ' + s + ' ' + h[0])
#             list_target.append('userFeatureSelection classification')

for f in synonyms_userFeatureSel:
    for s in synonyms_classification_verbs:
        for h in headers_label:
            sentences_fS_class.append(f + ' ' + ', '.join(random.sample(h[1],random.randint(1,len(h[1]))))+ ' ' + s)
            list_target.append('userFeatureSelection classification plot')

# for f in synonyms_userFeatureSel:
#     for s in synonyms_classification_verbs_with_data:
#         for h in headers_label:
#             sentences_fS_class.append(f + ' ' + ', '.join(random.sample(h[1],random.randint(1,len(h[1]))))+ ' ' +  s + ' ' + h[0])
#             list_target.append('userFeatureSelection classification plot')

with open('../DSBot/wf/src-train2.txt','a') as f:
    for s in sentences_fS_class:
        f.write('\n')
        f.write(s)
        #f.write('\n')

with open('../DSBot/wf/tgt-train2.txt','a') as f:
    for s in list_target:
        f.write('\n')
        f.write(s)

sentences_fS_pred = []
list_target = []
for f in synonyms_userFeatureSel:
    for s in synonyms_prediction_verbs:
        for h in headers_label:
            sentences_fS_pred.append(f + ' ' +', '.join(random.sample(h[1],random.randint(1,len(h[1]))))+ ' '  + s)
            list_target.append('userFeatureSelection prediction')

# for f in synonyms_userFeatureSel:
#     for s in synonyms_prediction_verbs_with_data:
#         for h in headers_label:
#             sentences_fS_pred.append(f + ' ' + ', '.join(random.sample(h[1],random.randint(1,len(h[1]))))+ ' ' + s + ' ' + h[0])
#             list_target.append('userFeatureSelection prediction')

for f in synonyms_userFeatureSel:
    for s in synonyms_prediction_verbs:
        for h in headers_label:
            sentences_fS_pred.append(f + ' ' + ', '.join(random.sample(h[1],random.randint(1,len(h[1]))))+ ' ' + s)
            list_target.append('userFeatureSelection prediction plot')
#
# for f in synonyms_userFeatureSel:
#     for s in synonyms_prediction_verbs_with_data:
#         for h in headers_label:
#             sentences_fS_pred.append(f + ' ' +', '.join(random.sample(h[1],random.randint(1,len(h[1]))))+ ' '  + s + ' ' + h[0])
#             list_target.append('userFeatureSelection prediction plot')

with open('../DSBot/wf/src-train2.txt','a') as f:
    for s in sentences_fS_pred:
        f.write('\n')
        f.write(s)
        #f.write('\n')

with open('../DSBot/wf/tgt-train2.txt','a') as f:
    for s in list_target:
        f.write('\n')
        f.write(s)

sentences_classification = []
list_target = []

for s in synonyms_classification_verbs:
    sentences_classification.append(s)
    list_target.append('classification')
#
# for s in synonyms_classification_verbs_with_data:
#     for h in headers_label:
#         sentences_classification.append(s + ' ' + h[0])
#         list_target.append('classification')

with open('../DSBot/wf/src-train2.txt','a') as f:
    for s in sentences_classification:
        f.write('\n')
        f.write(s)
        #f.write('\n')

with open('../DSBot/wf/tgt-train2.txt','a') as f:
    for s in list_target:
        f.write('\n')
        f.write(s)


sentences_prediction = []
list_target = []

for s in synonyms_prediction_verbs:
    sentences_prediction.append(s)
    list_target.append('prediction')
#
# for s in synonyms_prediction_verbs_with_data:
#     for h in headers_label:
#         sentences_prediction.append(s + ' ' + h[0])
#         list_target.append('prediction')

with open('../DSBot/wf/src-train2.txt','a') as f:
    for s in sentences_prediction:
        f.write('\n')
        f.write(s)
        #f.write('\n')

with open('../DSBot/wf/tgt-train2.txt','a') as f:
    for s in list_target:
        f.write('\n')
        f.write(s)


sentences_classification = []
list_target = []
for v in verbs:
    for s in synonyms_classification:
        sentences_classification.append(v+' '+s)
        list_target.append('classification')
#
# for v in verbs:
#     for s in synonyms_classification_with_data:
#         for h in headers_label:
#             sentences_classification.append(v + ' ' + s + ' ' + h[0])
#             list_target.append('classification')

for v in plot_verbs:
    for s in synonyms_classification:
        sentences_classification.append(v+' '+s)
        list_target.append('classification plot')
# for v in plot_verbs:
#     for s in synonyms_classification_with_data:
#         for h in headers_label:
#             sentences_classification.append(v + ' ' + s + ' ' + h[0])
#             list_target.append('classification plot')

with open('../DSBot/wf/src-train2.txt','a') as f:
    for s in sentences_classification:
        f.write('\n')
        f.write(s)
        #f.write('\n')

with open('../DSBot/wf/tgt-train2.txt','a') as f:
    for s in list_target:
        f.write('\n')
        f.write(s)

sentences_prediction = []
list_target = []
for v in verbs:
    for s in synonyms_prediction:
        sentences_prediction.append(v+' '+s)
        list_target.append('prediction')

# for v in verbs:
#     for s in synonyms_prediction_with_data:
#         for h in headers_label:
#             sentences_prediction.append(v + ' ' + s + ' ' + h[0])
#             list_target.append('prediction')

for v in plot_verbs:
    for s in synonyms_prediction:
        sentences_prediction.append(v+' '+s)
        list_target.append('prediction plot')
# for v in plot_verbs:
#     for s in synonyms_prediction_with_data:
#         for h in headers_label:
#             sentences_prediction.append(v + ' ' + s + ' ' + h[0])
#             list_target.append('prediction plot')

with open('../DSBot/wf/src-train2.txt','a') as f:
    for s in sentences_prediction:
        f.write('\n')
        f.write(s)
        #f.write('\n')

with open('../DSBot/wf/tgt-train2.txt','a') as f:
    for s in list_target:
        f.write('\n')
        f.write(s)

sentences_regression = []
list_target = []
for v in verbs:
    for s in synonyms_regression:
        sentences_prediction.append(v+' '+s)
        list_target.append('regression')

for v in plot_verbs:
    for s in synonyms_regression:
        sentences_prediction.append(v+' '+s)
        list_target.append('regression plot')

with open('../DSBot/wf/src-train2.txt','a') as f:
    for s in sentences_prediction:
        f.write('\n')
        f.write(s)
        #f.write('\n')

with open('../DSBot/wf/tgt-train2.txt','a') as f:
    for s in list_target:
        f.write('\n')
        f.write(s)