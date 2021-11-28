from abc import ABC, abstractmethod
import json
from pathlib import Path

algorithm_modules = ['clustering', 'classification', 'correlation', 'associationRules', 'regression']

"""
Utility function to retireve the family of a module
"""


def retrieve_family(module):
    with open('./kb.json', "r") as knowledge_base_file:
        knowledge_base = json.loads(knowledge_base_file.read())
    for algorithm_family in algorithm_modules:
        if module in knowledge_base[algorithm_family]:
            return algorithm_family
    return


def retrieve_message(module, sentence_type):
    with open(Path(__file__).parent / 'text_productions.json', "r") as process_file:
        producible_sentences = json.loads(process_file.read())
    return producible_sentences[module][sentence_type]


"""
Every chat state has 2 methods: 
 - generate that generate the sentence to prompt to the user before its response
 - handle that takes user input and decides the following state
"""


class ComprehensionConversationState(ABC):

    @abstractmethod
    def generate(self, pipeline_array, dataset):
        pass

    @abstractmethod
    def handle(self, user_utterance, pipeline_array, dataset):
        pass


class Reformulation(ComprehensionConversationState):

    def generate(self, pipeline_array, dataset):
        pass

    def handle(self, user_utterance, pipeline_array, dataset):
        if user_utterance == 'yes':
            return 'ok, we can proceed', 'comprehension_end', pipeline_array
            # TODO qui dobbiamo iniziare a creare la pipeline, non prima!
        elif user_utterance == 'no':
            next_state = AlgorithmVerificationPrediction()
            return next_state.generate(pipeline_array, dataset)
        elif user_utterance == 'Can you explain it better?':
            return self.help(pipeline_array)
        elif user_utterance == 'Can you provide me an example?':
            return self.example(pipeline_array)
        else:
            return 'I did not understand, sorry', 'reformulation', pipeline_array

    def help(self, pipeline_array):
        for module in pipeline_array:
            module_family = retrieve_family(module)
            if module_family in algorithm_modules:
                explanation = retrieve_message(module_family, 'explanation').capitalize() + ' Have I understood ' \
                                                                                            'correctly your ' \
                                                                                            'request? '
                return explanation, 'reformulation', pipeline_array
        return 'ciaooo', 'reformulation', pipeline_array

    def example(self, pipeline_array):
        for module in pipeline_array:
            module_family = retrieve_family(module)
            if module_family in algorithm_modules:
                explanation = retrieve_message(module_family, 'example').capitalize() + ' Is this what you want?'
                return explanation, 'reformulation', pipeline_array
        return 'ciaooo', 'reformulation', pipeline_array


class AlgorithmVerfication(ComprehensionConversationState):

    def generate(self, pipeline_array, dataset):
        for user_module in pipeline_array:
            algorithm_family = retrieve_family(user_module)
            if algorithm_family:
                with open(Path(__file__).parent / 'text_productions.json', "r") as process_file:
                    producible_sentences = json.loads(process_file.read())
                return 'You want to apply ' + producible_sentences[algorithm_family]["readableName"] + \
                       ', don\'t you?', 'algorithm_verification', pipeline_array

        return 'Non ho trovato la unit', "algorithm_verification", pipeline_array

    def handle(self, user_utterance, pipeline_array, dataset):
        print("AlgorithmVerification.handle eseguito")
        if user_utterance == 'no':
            next_state = AlgorithmVerfication()
            return next_state.generate(pipeline_array, dataset)
        elif user_utterance == 'yes':
            return 'ok, we can proceed', 'comprehension_end', pipeline_array
        else:
            return 'TBD', 'comprehension_end', pipeline_array


class AlgorithmVerificationPrediction(ComprehensionConversationState):

    def generate(self, pipeline_array, dataset):
        if dataset.hasLabel:
            return "I see that you indicated the presence of a label in your dataset. Do you want to try to predict " \
                   "its value from the other data? ", 'algorithm_verification_prediction', pipeline_array
        else:
            next_state = AlgorithmVerificationRelationships()
            return next_state.generate()

    def handle(self, user_utterance, pipeline_array, dataset):
        if user_utterance == 'no':
            next_state = AlgorithmVerificationRelationships()
            return next_state.generate(pipeline_array, dataset)
        elif user_utterance == 'yes':
            next_state = RegressionOrClassification()
            return next_state.generate(pipeline_array, dataset)
        else:
            return 'TBD', 'comprehension_end', pipeline_array


class AlgorithmVerificationRelationships(ComprehensionConversationState):

    def generate(self, pipeline_array, dataset):
        return "Are you interested in finding direct relationships between the columns of your dataset? For example " \
               "you might discover that at the increase of the value of the column X, the column Y increases in all " \
               "the data rows as well, or that the presence of feature A and feature B inside the data row imply the " \
               "presence of feature C.", \
               'algorithm_verification_relationship', pipeline_array

    def handle(self, user_utterance, pipeline_array, dataset):
        if user_utterance == 'no':
            next_state = AlgorithmVerificationClustering()
            return next_state.generate(pipeline_array, dataset)
        elif user_utterance == 'yes':
            next_state = CorrelationOrAssociationRules()
            return next_state.generate(pipeline_array, dataset)
        else:
            return 'TBD', 'comprehension_end', pipeline_array


class AlgorithmVerificationClustering(ComprehensionConversationState):

    def generate(self, pipeline_array, dataset):
        return "Are you interested in making groups that contain similar data points? In this way, you can categorize " \
               "your data into similar groups and see how these groups are formed.", \
               'algorithm_verification_relationship', pipeline_array

    def handle(self, user_utterance, pipeline_array, dataset):
        if user_utterance == 'no':
            next_state = AlgorithmVerificationRelationships()
            return next_state.generate(pipeline_array, dataset)
        elif user_utterance == 'yes':
            return 'Ok, we will proceed with clustering analysis!', 'comprehension_end', ['clustering']
        else:
            return 'TBD', 'comprehension_end', pipeline_array


class RegressionOrClassification(ComprehensionConversationState):

    def generate(self, pipeline_array, dataset):
        next_state = FeatureImportanceOrNot()
        if not dataset.hasCategoricalLabel:
            return next_state.generate(['regression'], dataset)
        else:
            return next_state.generate(['classification'], dataset)

    def handle(self, user_utterance, pipeline_array, dataset):
        pass


class FeatureImportanceOrNot(ComprehensionConversationState):
    def generate(self, pipeline_array, dataset):
        operation_keyword = 'classification' if 'classification' in pipeline_array else 'regression'
        return f"Given the composition of your dataset, we will use a {operation_keyword.capitalize()} Algorithm to predict the" \
               f" value contained in column {dataset.label}. Are you interested in the prediction itself, or are you " \
               "more interested in understanding which are the most influencing factors in determining the prediction?", \
               "feature_importance_or_not", pipeline_array

    def handle(self, user_utterance, pipeline_array, dataset):
        if user_utterance == 'I am only interested in the prediction':
            return "Ok, we can proceed!", "comprehension_end", pipeline_array
        elif user_utterance == 'I am interested more in the factors that influence the prediction':
            pipeline_array.append('featureImportance')
            return "Ok, we will perform a Feature Importance analysis, to highlight which are the most important " \
                   "factors in the prediction outcome", "comprehension_end", pipeline_array


class CorrelationOrAssociationRules(ComprehensionConversationState):

    def generate(self, pipeline_array, dataset):
        if dataset.onlyCategorical:
            return 'Given the composition of your dataset, we will apply association rules algorithm to find ' \
                   'relationships between your data in the form of "if -> then" rules', 'comprehension_end', \
                   ['associationRules']
        elif not dataset.categorical:
            return 'Given the composition of your dataset, we will use correlation to find direct relationships ' \
                   'between columns in your table', 'comprehension_end', ['correlation']
        return 'Are you more interested in finding direct relationships between numerical columns, or rules in the ' \
               '"if -> then" form that describe behaviours of more columns? ', 'correlation_or_association_rules', \
               pipeline_array

    def handle(self, user_utterance, pipeline_array, dataset):
        if user_utterance == 'direct':
            return 'Ok, we will proceed with correlation analysis!', 'comprehension_end', ['correlation']
        elif user_utterance == 'rules':
            return 'Ok, we will proceed with association rules analysis!', 'comprehension_end', ['associationRules']
        else:
            next_state = AlgorithmVerificationRelationships()
            return next_state.generate(pipeline_array, dataset)


switcher = {
    'reformulation': Reformulation,
    'algorithm_verification': AlgorithmVerfication,
    'algorithm_verification_prediction': AlgorithmVerificationPrediction,
    'algorithm_verification_relationship': AlgorithmVerificationPrediction,
    'algorithm_verification_clustering': AlgorithmVerificationClustering,
    'regression_or_classification': RegressionOrClassification,
    'correlation_or_association_rules': CorrelationOrAssociationRules,
    'feature_importance_or_not': FeatureImportanceOrNot
}


def pipeline_array_to_string(pipeline_array):
    pipeline_string = ''
    for item in pipeline_array:
        pipeline_string = pipeline_string + ' ' + item
    return pipeline_string


def comprehension_conversation_handler(user_payload, dataset):
    print(user_payload)
    user_utterance = user_payload['message']
    conversation_state = user_payload['comprehension_state']
    pipeline_array = user_payload['comprehension_pipeline']

    # I create a class instance of the object of the state in which we are
    func = switcher.get(conversation_state, "nothing")()

    # Execute the function
    new_message, new_state, new_pipeline_array = func.handle(user_utterance, pipeline_array, dataset)
    new_pipeline_string = pipeline_array_to_string(pipeline_array)
    return {'message': new_message, 'comprehension_state': new_state, 'comprehension_pipeline': new_pipeline_string}
