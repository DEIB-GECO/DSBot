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

verbs = ['can you find',  'i want', 'can you compute', 'do they exist', 'i want to compute', 'are there', 'i want to identify']
plot_verbs = ['can i see', 'can you show', 'show me', 'can i visualize','plot', 'draw', 'can you draw', 'i want to see', 'i want to visualize']

