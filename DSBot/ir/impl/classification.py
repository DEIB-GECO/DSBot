from abc import abstractmethod

from ir.ir_exceptions import LabelsNotAvailable
from ir.ir_operations import IROp, IROpOptions
from ir.ir_parameters import IRNumPar

from sklearn.model_selection import RandomizedSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import label_binarize
from sklearn.model_selection import train_test_split, KFold
import numpy as np


class IRClassification(IROp):
    def __init__(self, name, parameters, model = None):
        super(IRClassification, self).__init__(name,parameters)
        self._model = model(**{v.name: v.value for v in parameters})
        self.labels = None

    @abstractmethod
    def parameter_tune(self, dataset):
        pass

    def set_model(self, result):
        if 'new_dataset' in result:
            dataset = result['new_dataset']
        else:
            dataset = result['original_dataset'].ds
        labels = result['labels']
        self.parameter_tune(dataset, labels)
        for p,v in self.parameters.items():
            print(p,v)
            self._model.__setattr__(p,self.parameters[p].value)
        self._param_setted = True

    def get_labels(self):
        if self.labels is None:
            raise LabelsNotAvailable
        return self.labels

    #TDB cosa deve restituire questa funzione?
    def run(self, result, session_id):
        print(self._param_setted)
        if not self._param_setted:
            self.set_model(result)

        if 'new_dataset' in result:
            dataset = result['new_dataset']
        else:
            dataset = result['original_dataset'].ds
        labels = result['labels']
        n_classes = set(result['labels'])
        print('PARAMETERSSSS', self.parameters)
        predicted = []
        #kf = KFold(n_splits=4)
        result['predicted_labels'] = []
        result['y_score'] = []
        for x_train, x_test, y_train, y_test in zip(result['x_train'],result['x_test'],result['y_train'],result['y_test']):
            print(x_train.shape, y_train.shape)
            print(y_train)
            #y_train = np.array([i[0] for i in label_binarize(y_train, classes=list(n_classes))])#.reshape(1, -1).T
            #print(y_train.shape)
            #print(y_train)
            #aaaa
            y_train = y_train.reshape((x_train.shape[0],1))
            print(x_train.shape, y_train.shape)
            try:
                #print((self._model.fit(train_features, train_labels).predict(test_features)))
                result['classifier']= self._model.fit(x_train, y_train)
                predicted += list(self._model.fit(x_train, y_train).predict(x_test))
            except:
                predicted += list(self._model.fit(x_train, y_train).predict(x_test))

            result['y_score'].append(self._model.predict_proba(x_test))
        #result['y_test'] = y_test
        #result['y_score'] = y_score
        result['predicted_labels'].append(predicted)
        result['original_dataset'].measures.update({p: self.parameters[p].value for p, v in self.parameters.items()})
        '''
        for train_index, test_index in kf.split(dataset):
            train_features, test_features = dataset.values[train_index], dataset.values[test_index]
            train_labels, test_labels = labels.values[train_index], labels.values[test_index]
            try:
                #print((self._model.fit(train_features, train_labels).predict(test_features)))
                self._model.fit(train_features, train_labels)
                predicted += list(self._model.fit(train_features, train_labels).predict(test_features))
            except:
                predicted += list(self._model.fit(train_features, train_labels).predict(test_features))
        '''


        return result



class IRRandomForest(IRClassification):
    def __init__(self):
        super(IRRandomForest, self).__init__("randomForest",
                                             [IRNumPar("n_estimators", 100, "int", 100, 150, 10),  # TODO: what is the maximum? Which first value give?
                                              IRNumPar("max_depth", 10, "int", 10, 22, 11),  # TODO: what is the maximum?
                                              IRNumPar("min_samples_split", 2, "int", 2, 5, 3),
                                              IRNumPar("min_samples_leaf", 1, "int", 1, 2, 1)],  # TODO: if I want to pass a list of values?
                                             RandomForestClassifier)
        self._param_setted = False

    def parameter_tune(self, dataset, labels):
        # Number of trees in random forest
        n_estimators = [int(x) for x in np.linspace(start=self.parameters['n_estimators'].min_v, stop=self.parameters['n_estimators'].max_v, num=self.parameters['n_estimators'].step)]
        # Number of features to consider at every split
        #max_features = ['auto', 'sqrt']
        # Maximum number of levels in tree
        max_depth = [int(x) for x in np.linspace(self.parameters['max_depth'].min_v, self.parameters['max_depth'].max_v, num=self.parameters['max_depth'].step)]
        max_depth.append(None)
        # Minimum number of samples required to split a node
        min_samples_split = np.arange(self.parameters['min_samples_split'].min_v, self.parameters['min_samples_split'].max_v, self.parameters['min_samples_split'].step)
        # Minimum number of samples required at each leaf node
        min_samples_leaf = np.arange(self.parameters['min_samples_leaf'].min_v, self.parameters['min_samples_leaf'].max_v, self.parameters['min_samples_leaf'].step)
        # Method of selecting samples for training each tree
        #bootstrap = [True, False]
        # Create the random grid
        random_grid = {'n_estimators': n_estimators,
                       'max_depth': max_depth,
                       'min_samples_split': min_samples_split,
                       'min_samples_leaf': min_samples_leaf}


        # Use the random grid to search for best hyperparameters
        # First create the base model to tune
        rf = RandomForestClassifier()
        # Random search of parameters, using 3 fold cross validation,
        # search across 100 different combinations, and use all available cores
        rf_random = RandomizedSearchCV(estimator=rf, param_distributions=random_grid, n_iter=100, cv=3, verbose=2,
                                       random_state=42, n_jobs=-1)
        print('ds', dataset)
        print('labels', labels)
        # Fit the random search model
        print(dataset.shape)
        print(labels.shape)
        #print(labels.values)

        print(set(labels))
        rf_random.fit(dataset, labels)
        print(rf_random.best_params_.items)
        for k in rf_random.best_params_:
            self.parameters[k].value = rf_random.best_params_[k]
        return self.parameters


class IRLogisticRegression(IRClassification):
    def __init__(self):
        super(IRLogisticRegression, self).__init__("logisticRegression",
                                                   [IRNumPar("max_iter", 100, "int", 100, 1000, 10)],  # TODO: if I want to pass a list of values?
                                                   LogisticRegression)
        self._param_setted = False

    def parameter_tune(self, dataset, labels):
        max_iter = [int(x) for x in np.linspace(self.parameters['max_iter'].min_v, self.parameters['max_iter'].max_v, num=self.parameters['max_iter'].step)]

        random_grid = {'max_iter': max_iter}


        # Use the random grid to search for best hyperparameters
        # First create the base model to tune
        lr = LogisticRegression()
        # Random search of parameters, using 3 fold cross validation,
        # search across 100 different combinations, and use all available cores
        lr_random = RandomizedSearchCV(estimator=lr, param_distributions=random_grid, n_iter=100, cv=3, verbose=2,
                                       random_state=42, n_jobs=-1)
        print('ds', dataset)
        print('labels', labels)
        # Fit the random search model
        print(dataset.shape)
        print(labels.shape)
        print(set(labels.values))
        lr_random.fit(dataset, labels.values)
        print(lr_random.best_params_.items)
        for k in lr_random.best_params_:
            self.parameters[k].value = lr_random.best_params_[k]
        return self.parameters

class IRGenericClassification(IROpOptions):
    def __init__(self):
        super(IRGenericClassification, self).__init__([IRRandomForest(), IRLogisticRegression()], "randomForest")