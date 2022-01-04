import random

headers_label = [('Diagnosis',
                  ['radius', 'texture','perimeter','area','smoothness','compactness','concavity','concave points','symmetry','fractal dimension'],
                  'patients')]#,
               #   ('Y',
               #    ['destination','passager','weather','temperature','time','coupon','expiration','gender','age','maritalStatus','has_Children','education',
               #     'occupation','income','Bar','CoffeeHouse','CarryAway','RestaurantLessThan20','Restaurant20To50','toCoupon_GEQ15min','toCoupon_GEQ25min',
               #     'direction_same','direction_opp'],
               #    'people'),
               #   ('area',
               #    ['X','Y','month','day','FFMC','DMC','DC','ISI','temp','RH','wind','rain'],
               #    'areas'),
               #   ('G3',
               #    ['school','sex','age','address','famsize','Pstatus','Medu','Fedu','Mjob','Fjob','reason','guardian','traveltime','studytime','failures',
               #     'schoolsup','famsup','paid','activities','nursery','higher','internet','romantic','famrel','freetime','goout','Dalc','Walc','health',
               #     'absences','G1','G2'],
               #    'students')
               # ]

headers_nolabel = [(["Kingdom", "DNAtype" ,"SpeciesID" ,"Ncodons" ,"SpeciesName" , "codon"],
                   'sequences')]
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
synonyms_extraction = ['i want to extract', 'can you find', 'can you define', 'i want to select', 'extract', 'select', 'retrieve']
synonyms_importantFeatures = ['the most important features', 'the most important columns', 'the features that are more significant', 'the features that classify better',
                              'the columns that classify better', 'the columns that identify the groups', 'the most relevant features', 'the most relevant columns']
synonyms_afterclass = ['after the classification', 'after having classified', 'after classifying the data', 'after considering the classes of the data',
                       'once you have classified my data', 'once the classification is computed']
synonyms_afterclass_with_data = ['after the classification of', 'after having classified the', 'after classifying the', 'after considering the classes of',
                       'once you have classified']
synonyms_afterpred = ['after the prediction', 'after having predicted', 'after predicting the data', 'after prediction the data',
                       'once you have predicted my data', 'once the prediction is computed']
synonyms_afterpred_with_data = ['after the prediciton of', 'after having predicted the', 'after prediction the', 'after forecasting',
                       'once you have predicted']

synonyms_featureSel = ['select the relevant features','extract the features','use only some features','use only some columns','select only some columns',
                       'extract only some columns','extract some columns','select the relevant columns','consider only some features','consider some columns']
synonym_then = ['then', ',', 'after that', ';', 'subsequently', 'later','next', 'on top of that', 'moreover']

#with open('../DSBot/wf/src-val2.txt','a') as f:
#    for s in ['correlation']*1000:
#        f.write('\n')
#        f.write(s)
        #f.write('\n')

#with open('../DSBot/wf/tgt-val2.txt','a') as f:
#    for s in ['correlation']*1000:
#        f.write('\n')
#        f.write(s)

sentences_fS_aR = []
list_target = []

for f in synonyms_featureSel:
    for t in synonym_then:
        for v in verbs:
            for s in synonyms_classification:
                for h in headers_nolabel:
                    if len(sentences_fS_aR) <= 12396:
                        sentences_fS_aR.append(f + ' ' +  t + ' ' + v + ' ' + s)
                        list_target.append('featureSelection classification')
                        break

for f in synonyms_featureSel:
    for t in synonym_then:
        for v in verbs:
            for s in synonyms_classification_with_data:
                for h in headers_nolabel:
                    if len(sentences_fS_aR) <= 12396:
                        sentences_fS_aR.append(f + ' ' + t + ' ' + v + ' ' + s + ' ' + h[1])
                        list_target.append('featureSelection classification')
                        break

for f in synonyms_featureSel:
    for t in synonym_then:
        for v in plot_verbs:
            for f in synonyms_importantFeatures:
                for a in synonyms_afterclass:
                    if len(sentences_fS_aR) <= 12396:
                        sentences_fS_aR.append(v + ' ' + f + ' ' +a)
                        list_target.append('featureSelection classification featureImportance plot')
                        break

for f in synonyms_featureSel:
    for t in synonym_then:
        for v in plot_verbs:
            for f in synonyms_importantFeatures:
                for a in synonyms_afterclass:
                    if len(sentences_fS_aR) <= 12396:
                        sentences_fS_aR.append(v + ' ' + f + ' ' + a)
                        list_target.append('featureSelection classification featureImportance plot')
                        break
print(len(sentences_fS_aR), len(list_target))
with open('../DSBot/wf/src-val.txt','a') as f:
    for s in sentences_fS_aR:
        f.write('\n')
        f.write(s)
        #f.write('\n')

with open('../DSBot/wf/tgt-val.txt','a') as f:
    for s in list_target:
        f.write('\n')
        f.write(s)

sentences_prediction = []
list_target = []
for s in synonyms_prediction_verbs:
    for v in synonyms_extraction:
        for f in synonyms_importantFeatures:
            sentences_prediction.append(s + 'and' + v + f)
            list_target.append('prediction featureImportance')
            break

for s in synonyms_prediction_verbs_with_data:
    for v in synonyms_extraction:
        for f in synonyms_importantFeatures:
            for h in headers_label:
                sentences_prediction.append(s + ' ' + h[0] + 'and' + v + f)
                list_target.append('prediction featureImportance')
                break
print(len(sentences_prediction), len(list_target))
with open('../DSBot/wf/src-val.txt','a') as f:
    for s in sentences_prediction:
        f.write('\n')
        f.write(s)
        #f.write('\n')

with open('../DSBot/wf/tgt-val.txt','a') as f:
    for s in list_target:
        f.write('\n')
        f.write(s)

sentences_prediction = []
list_target = []

for v in plot_verbs:
    for f in synonyms_importantFeatures:
        for a in synonyms_afterpred:
            sentences_prediction.append(v + f + a)
            list_target.append('prediction featureImportance plot')
            break

for v in synonyms_extraction:
    for f in synonyms_importantFeatures:
        for a in synonyms_afterpred_with_data:
            for h in headers_label:
                sentences_prediction.append(v + f + a + ' ' + h[0])
                list_target.append('prediction featureImportance plot')
                break
print(len(sentences_prediction), len(list_target))
with open('../DSBot/wf/src-val.txt','a') as f:
    for s in sentences_prediction:
        f.write('\n')
        f.write(s)
        #f.write('\n')

with open('../DSBot/wf/tgt-val.txt','a') as f:
    for s in list_target:
        f.write('\n')
        f.write(s)
sentences_classification = []
list_target = []

#for s in synonyms_classification_verbs:
for v in plot_verbs:
    for f in synonyms_importantFeatures:
        for a in synonyms_afterclass:
            sentences_classification.append(v + f + a)
            list_target.append('classification featureImportance plot')
            break


for v in synonyms_extraction:
    for f in synonyms_importantFeatures:
        for a in synonyms_afterclass_with_data:
            for h in headers_label:
                sentences_classification.append(v + f + a + ' ' + h[0])
                list_target.append('classification featureImportance plot')
                break
print(len(sentences_classification), len(list_target))
with open('../DSBot/wf/src-val.txt','a') as f:
    for s in sentences_classification:
        f.write('\n')
        f.write(s)
        #f.write('\n')

with open('../DSBot/wf/tgt-val.txt','a') as f:
    for s in list_target:
        f.write('\n')
        f.write(s)


sentences_classification = []
list_target = []

for s in synonyms_classification_verbs:
    for v in synonyms_extraction:
        for f in synonyms_importantFeatures:
            sentences_classification.append(s + 'and' + v + f)
            list_target.append('classification featureImportance')
            break

for s in synonyms_classification_verbs_with_data:
    for v in synonyms_extraction:
        for f in synonyms_importantFeatures:
            for h in headers_label:
                sentences_classification.append(s + ' ' + h[0] + 'and' + v + f)
                list_target.append('classification featureImportance')
                break
print(len(sentences_classification), len(list_target))
with open('../DSBot/wf/src-val.txt','a') as f:
    for s in sentences_classification:
        f.write('\n')
        f.write(s)
        #f.write('\n')

with open('../DSBot/wf/tgt-val.txt','a') as f:
    for s in list_target:
        f.write('\n')
        f.write(s)
sentences_fS_class = []
list_target = []
for f in synonyms_userFeatureSel:
    for v in verbs:
        for s in synonyms_classification:
            for h in headers_label:
                if random.randint(1,len(h[1]))==2:
                    sentences_fS_class.append(f + ' ' + ' and '.join(random.sample(h[1],2)) + ' ' + v + ' ' + s)
                    list_target.append('userFeatureSelection classification')
                    break

for f in synonyms_userFeatureSel:
    for v in verbs:
        for s in synonyms_classification_with_data:
            for h in headers_label:
                if random.randint(1,len(h[1]))==2:
                    #sentences_fS_class.append(f + ' ' + ' and '.join(random.sample(h[1],2)) + ' ' + v + ' ' + s)
                    sentences_fS_class.append(f + ' ' + ' and '.join(random.sample(h[1],2))+ ' ' + v + ' ' + s + ' ' + h[0])
                    list_target.append('userFeatureSelection classification')
                    break

for f in synonyms_userFeatureSel:
    for v in plot_verbs:
        for s in synonyms_classification:
            for h in headers_label:
                if random.randint(1, len(h[1])) == 2:
                    sentences_fS_class.append(f + ' ' + ' and '.join(random.sample(h[1],2)) + ' ' + v + ' ' + s)
                    list_target.append('userFeatureSelection classification plot')
                    break

for f in synonyms_userFeatureSel:
    for v in plot_verbs:
        for s in synonyms_classification_with_data:
            for h in headers_label:
                if random.randint(1, len(h[1])) == 2:
                    sentences_fS_class.append(f + ' ' + ' and '.join(random.sample(h[1],2)) + ' ' + v + ' ' + s + ' ' + h[0])
                    list_target.append('userFeatureSelection classification plot')
                    break

print(len(sentences_fS_class), len(list_target))
with open('../DSBot/wf/src-val.txt','a') as f:
    for s in sentences_fS_class:
        f.write('\n')
        f.write(s)
        #f.write('\n')

with open('../DSBot/wf/tgt-val.txt','a') as f:
    for s in list_target:
        f.write('\n')
        f.write(s)

sentences_fS_pred = []
list_target = []
for f in synonyms_userFeatureSel:
    for v in verbs:
        for s in synonyms_prediction:
            for h in headers_label:
                if random.randint(1, len(h[1])) == 2:
                    sentences_fS_pred.append(f + ' ' + ' and '.join(random.sample(h[1],2)) + ' ' + v + ' ' + s)
                    list_target.append('userFeatureSelection prediction')
                    break

for f in synonyms_userFeatureSel:
    for v in verbs:
        for s in synonyms_prediction_with_data:
            for h in headers_label:
                if random.randint(1, len(h[1])) == 2:
                    sentences_fS_pred.append(f + ' ' + ' and '.join(random.sample(h[1],2)) + ' ' + v + ' ' + s + ' ' + h[0])
                    list_target.append('userFeatureSelection prediction')
                    break

for f in synonyms_userFeatureSel:
    for v in plot_verbs:
        for s in synonyms_prediction:
            for h in headers_label:
                if random.randint(1, len(h[1])) == 2:
                    sentences_fS_pred.append(f + ' ' + ' and '.join(random.sample(h[1],2))+ ' ' + v + ' ' + s)
                    list_target.append('userFeatureSelection prediction plot')
                    break

for f in synonyms_userFeatureSel:
    for v in plot_verbs:
        for s in synonyms_prediction_with_data:
            for h in headers_label:
                if random.randint(1, len(h[1])) == 2:
                    sentences_fS_pred.append(f + ' ' + ' and '.join(random.sample(h[1],2)) + ' ' + v + ' ' + s + ' ' + h[0])
                    list_target.append('userFeatureSelection prediction plot')
                    break
print(len(sentences_fS_pred), len(list_target))
with open('../DSBot/wf/src-val.txt','a') as f:
    for s in sentences_fS_pred:
        f.write('\n')
        f.write(s)
        #f.write('\n')

with open('../DSBot/wf/tgt-val.txt','a') as f:
    for s in list_target:
        f.write('\n')
        f.write(s)


sentences_fS_class = []
list_target = []
for f in synonyms_userFeatureSel:
    for v in verbs:
        for s in synonyms_classification:
            for h in headers_label:
                sentences_fS_class.append(f + ' ' + ', '.join(random.sample(h[1],random.randint(1,len(h[1]))))+ ' ' + v + ' ' + s)
                list_target.append('userFeatureSelection classification')
                break

for f in synonyms_userFeatureSel:
    for v in verbs:
        for s in synonyms_classification_with_data:
            for h in headers_label:
                sentences_fS_class.append(f + ' ' + ', '.join(random.sample(h[1],random.randint(1,len(h[1]))))+ ' ' + v + ' ' + s + ' ' + h[0])
                list_target.append('userFeatureSelection classification')
                break

for f in synonyms_userFeatureSel:
    for v in plot_verbs:
        for s in synonyms_classification:
            for h in headers_label:
                sentences_fS_class.append(f + ' ' + ', '.join(random.sample(h[1],random.randint(1,len(h[1]))))+ ' ' + v + ' ' + s)
                list_target.append('userFeatureSelection classification plot')
                break

for f in synonyms_userFeatureSel:
    for v in plot_verbs:
        for s in synonyms_classification_with_data:
            for h in headers_label:
                sentences_fS_class.append(f + ' ' + ', '.join(random.sample(h[1],random.randint(1,len(h[1]))))+ ' ' + v + ' ' + s + ' ' + h[0])
                list_target.append('userFeatureSelection classification plot')
                break

print(len(sentences_fS_class), len(list_target))
with open('../DSBot/wf/src-val.txt','a') as f:
    for s in sentences_fS_class:
        f.write('\n')
        f.write(s)
        #f.write('\n')

with open('../DSBot/wf/tgt-val.txt','a') as f:
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
                break

for f in synonyms_userFeatureSel:
    for v in verbs:
        for s in synonyms_prediction_with_data:
            for h in headers_label:
                sentences_fS_pred.append(f + ' ' + ', '.join(random.sample(h[1],random.randint(1,len(h[1]))))+ ' ' + v + ' ' + s + ' ' + h[0])
                list_target.append('userFeatureSelection prediction')
                break

for f in synonyms_userFeatureSel:
    for v in plot_verbs:
        for s in synonyms_prediction:
            for h in headers_label:
                sentences_fS_pred.append(f + ' ' + ', '.join(random.sample(h[1],random.randint(1,len(h[1]))))+ ' ' + v + ' ' + s)
                list_target.append('userFeatureSelection prediction plot')
                break

for f in synonyms_userFeatureSel:
    for v in plot_verbs:
        for s in synonyms_prediction_with_data:
            for h in headers_label:
                sentences_fS_pred.append(f + ' ' + ', '.join(random.sample(h[1],random.randint(1,len(h[1]))))+ ' ' + v + ' ' + s + ' ' + h[0])
                list_target.append('userFeatureSelection prediction plot')
                break
print(len(sentences_fS_pred), len(list_target))
with open('../DSBot/wf/src-val.txt','a') as f:
    for s in sentences_fS_pred:
        f.write('\n')
        f.write(s)
        #f.write('\n')

with open('../DSBot/wf/tgt-val.txt','a') as f:
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
            break

for f in synonyms_userFeatureSel:
    for s in synonyms_classification_verbs_with_data:
        for h in headers_label:
            sentences_fS_class.append(f + ' ' + ', '.join(random.sample(h[1],random.randint(1,len(h[1]))))+ ' ' + s + ' ' + h[0])
            list_target.append('userFeatureSelection classification')
            break

for f in synonyms_userFeatureSel:
    for s in synonyms_classification_verbs:
        for h in headers_label:
            sentences_fS_class.append(f + ' ' + ', '.join(random.sample(h[1],random.randint(1,len(h[1]))))+ ' ' + s)
            list_target.append('userFeatureSelection classification plot')
            break

for f in synonyms_userFeatureSel:
    for s in synonyms_classification_verbs_with_data:
        for h in headers_label:
            sentences_fS_class.append(f + ' ' + ', '.join(random.sample(h[1],random.randint(1,len(h[1]))))+ ' ' +  s + ' ' + h[0])
            list_target.append('userFeatureSelection classification plot')
            break
print(len(sentences_fS_class), len(list_target))
with open('../DSBot/wf/src-val.txt','a') as f:
    for s in sentences_fS_class:
        f.write('\n')
        f.write(s)
        #f.write('\n')

with open('../DSBot/wf/tgt-val.txt','a') as f:
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
            break

for f in synonyms_userFeatureSel:
    for s in synonyms_prediction_verbs_with_data:
        for h in headers_label:
            sentences_fS_pred.append(f + ' ' + ', '.join(random.sample(h[1],random.randint(1,len(h[1]))))+ ' ' + s + ' ' + h[0])
            list_target.append('userFeatureSelection prediction')
            break

for f in synonyms_userFeatureSel:
    for s in synonyms_prediction_verbs:
        for h in headers_label:
            sentences_fS_pred.append(f + ' ' + ', '.join(random.sample(h[1],random.randint(1,len(h[1]))))+ ' ' + s)
            list_target.append('userFeatureSelection prediction plot')
            break
#
for f in synonyms_userFeatureSel:
    for s in synonyms_prediction_verbs_with_data:
        for h in headers_label:
            sentences_fS_pred.append(f + ' ' +', '.join(random.sample(h[1],random.randint(1,len(h[1]))))+ ' '  + s + ' ' + h[0])
            list_target.append('userFeatureSelection prediction plot')
            break
print(len(sentences_fS_pred), len(list_target))
with open('../DSBot/wf/src-val.txt','a') as f:
    for s in sentences_fS_pred:
        f.write('\n')
        f.write(s)
        #f.write('\n')

with open('../DSBot/wf/tgt-val.txt','a') as f:
    for s in list_target:
        f.write('\n')
        f.write(s)



sentences_classification = []
list_target = []

for s in synonyms_classification_verbs:
    sentences_classification.append(s)
    list_target.append('classification')
    break

for s in synonyms_classification_verbs_with_data:
    for h in headers_label:
        sentences_classification.append(s + ' ' + h[0])
        list_target.append('classification')
        break
print(len(sentences_classification), len(list_target))
with open('../DSBot/wf/src-val.txt','a') as f:
    for s in sentences_classification:
        f.write('\n')
        f.write(s)
        #f.write('\n')

with open('../DSBot/wf/tgt-val.txt','a') as f:
    for s in list_target:
        f.write('\n')
        f.write(s)


sentences_prediction = []
list_target = []

for s in synonyms_prediction_verbs:
    sentences_prediction.append(s)
    list_target.append('prediction')
    break
for s in synonyms_prediction_verbs_with_data:
    for h in headers_label:
        sentences_prediction.append(s + ' ' + h[0])
        list_target.append('prediction')
        break
print(len(sentences_prediction), len(list_target))
with open('../DSBot/wf/src-val.txt','a') as f:
    for s in sentences_prediction:
        f.write('\n')
        f.write(s)
        break

with open('../DSBot/wf/tgt-val.txt','a') as f:
    for s in list_target:
        f.write('\n')
        f.write(s)
        break


sentences_classification = []
list_target = []
for v in verbs:
    for s in synonyms_classification:
        sentences_classification.append(v+' '+s)
        list_target.append('classification')
        break

for v in verbs:
    for s in synonyms_classification_with_data:
        for h in headers_label:
            sentences_classification.append(v + ' ' + s + ' ' + h[0])
            list_target.append('classification')
            break
for v in plot_verbs:
    for s in synonyms_classification:
        sentences_classification.append(v+' '+s)
        list_target.append('classification plot')
        break
for v in plot_verbs:
    for s in synonyms_classification_with_data:
        for h in headers_label:
            sentences_classification.append(v + ' ' + s + ' ' + h[0])
            list_target.append('classification plot')
            break
print(len(sentences_classification), len(list_target))
with open('../DSBot/wf/src-val.txt','a') as f:
    for s in sentences_classification:
        f.write('\n')
        f.write(s)
        #f.write('\n')

with open('../DSBot/wf/tgt-val.txt','a') as f:
    for s in list_target:
        f.write('\n')
        f.write(s)

sentences_prediction = []
list_target = []
for v in verbs:
    for s in synonyms_prediction:
        sentences_prediction.append(v+' '+s)
        list_target.append('prediction')
        break
for v in verbs:
    for s in synonyms_prediction_with_data:
        for h in headers_label:
            sentences_prediction.append(v + ' ' + s + ' ' + h[0])
            list_target.append('prediction')
            break
for v in plot_verbs:
    for s in synonyms_prediction:
        sentences_prediction.append(v+' '+s)
        list_target.append('prediction plot')
        break
for v in plot_verbs:
    for s in synonyms_prediction_with_data:
        for h in headers_label:
            sentences_prediction.append(v + ' ' + s + ' ' + h[0])
            list_target.append('prediction plot')
            break
print(len(sentences_prediction), len(list_target))
with open('../DSBot/wf/src-val.txt','a') as f:
    for s in sentences_prediction:
        f.write('\n')
        f.write(s)
        #f.write('\n')

with open('../DSBot/wf/tgt-val.txt','a') as f:
    for s in list_target:
        f.write('\n')
        f.write(s)

sentences_regression = []
list_target = []
for v in verbs:
    for s in synonyms_regression:
        sentences_regression.append(v+' '+s)
        list_target.append('regression')
        break

for v in plot_verbs:
    for s in synonyms_regression:
        sentences_regression.append(v+' '+s)
        list_target.append('regression plot')
        break
print(len(sentences_regression), len(list_target))
with open('../DSBot/wf/src-val.txt','a') as f:
    for s in sentences_regression:
        f.write('\n')
        f.write(s)


with open('../DSBot/wf/tgt-val.txt','a') as f:
    for s in list_target:
        f.write('\n')
        f.write(s)

