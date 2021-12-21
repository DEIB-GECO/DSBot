from abc import ABC, abstractmethod
import json
from http.client import HTTPConnection
from pathlib import Path
from typing import Dict, Any

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


def parse(utterance: str):
    """ Runs the interpreter to parse the given utterance and returns a dictionary containing the parsed data.

    If no intent can be extracted from the provided utterance, this returns an empty dictionary.

    :param utterance: the text input from the user
    :return: a dictionary containing the detected intent and corresponding entities if any exists.
    """
    connection = HTTPConnection(host='localhost', port=5005)
    connection.request("POST", "/model/parse", json.dumps({"text": utterance}))
    response = json.loads(connection.getresponse().read())
    print("RESPONSE:" + str(response))
    return response


def prepare_standard_response(message, state, pipeline):
    new_pipeline_string = pipeline_array_to_string(pipeline)
    response = {'message': message, 'comprehension_state': state, 'comprehension_pipeline': new_pipeline_string}
    print("prepared response is", str(response))
    return response


def retrieve_specific_entity_value(entities_list, entity_name):
    for entity in entities_list:
        if entity['entity'] == entity_name:
            return entity['value']
    return


def retrieve_entities_values(entities_list):
    values_list = []
    for entity in entities_list:
        values_list.append(entity['value'])
    return values_list


class ComprehensionConversationState(ABC):
    """
    Every chat state has 2 methods:
     - generate that generate the sentence to prompt to the user before its response
     - handle that takes user input and decides the following state
    """

    @abstractmethod
    def generate(self, pipeline_array, dataset):
        pass

    @abstractmethod
    def handle(self, user_message_parsed, pipeline_array, dataset):
        pass


class Reformulation(ComprehensionConversationState):

    def generate(self, pipeline_array, dataset):
        pass

    def handle(self, user_message_parsed, pipeline_array, dataset):
        if user_message_parsed['intent']['name'] == 'affirm':
            response = prepare_standard_response('ok, we can proceed', 'comprehension_end', pipeline_array)
            return response
        elif user_message_parsed['intent']['name'] == 'deny':
            next_state = AlgorithmVerificationPrediction()
            response = next_state.generate(pipeline_array, dataset)
            incipit = "I think I misinterpreted your original request. I will ask you some questions to better understand what you want to do. "
            response["message"] = incipit + response["message"]
            return response
        elif user_message_parsed['intent']['name'] in ['don_t_know', 'clarification_request']:
            return self.help(pipeline_array)
        elif user_message_parsed['intent']['name'] == 'example':
            return self.example(pipeline_array)
        else:
            return prepare_standard_response('I did not understand, sorry', 'reformulation', pipeline_array)

    def help(self, pipeline_array):
        for module in pipeline_array:
            module_family = retrieve_family(module)
            if module_family in algorithm_modules:
                explanation = retrieve_message(module_family, 'explanation').capitalize() + ' Have I understood ' \
                                                                                            'correctly your ' \
                                                                                            'request? '
                return prepare_standard_response(explanation, 'reformulation', pipeline_array)
        return prepare_standard_response('I was not able to reformulate you analysis, do you want to continue anyway?',
                                         'reformulation', pipeline_array)

    def example(self, pipeline_array):
        for module in pipeline_array:
            module_family = retrieve_family(module)
            if module_family in algorithm_modules:
                explanation = retrieve_message(module_family, 'example').capitalize() + ' Is this what you want?'
                return prepare_standard_response(explanation, 'reformulation', pipeline_array)
        return prepare_standard_response('ciaooo', 'reformulation', pipeline_array)


class AlgorithmVerificationPrediction(ComprehensionConversationState):

    def generate(self, pipeline_array, dataset):
        if dataset.hasLabel:
            return prepare_standard_response(
                "I see that you indicated the presence of a label in your dataset. Do you want to try to predict " \
                "its value from the other data? ", 'algorithm_verification_prediction', pipeline_array)
        else:
            next_state = AlgorithmVerificationRelationships()
            return next_state.generate(pipeline_array, dataset)

    def handle(self, user_message_parsed, pipeline_array, dataset):
        if user_message_parsed['intent']['name'] == 'deny':
            next_state = AlgorithmVerificationRelationships()
            return next_state.generate(pipeline_array, dataset)
        elif user_message_parsed['intent']['name'] == 'affirm':
            next_state = RegressionOrClassification()
            return next_state.generate(pipeline_array, dataset)
        elif user_message_parsed['intent']['name'] in ['don_t_know', 'clarification_request']:
            return self.help(pipeline_array, dataset)
        elif user_message_parsed['intent']['name'] == 'example':
            return self.example(pipeline_array, dataset)

    def help(self, pipeline_array, dataset):
        base_sentence = "Predicting a value means training an algorithm to predict a target value -  the value " \
                        "contained in the \"label\" column - starting from the other data. "
        end_sentence = "Do you want to perform this kind of analysis? "
        if dataset.hasCategoricalLabel:
            label_sentence = "Since the column you indicated as label seems to describe categories, I suggest to use a " \
                             "classification algorithm. "
            show = "classification"
        else:
            label_sentence = "Since the column you indicated as label seems to describe a value, I suggest to use a " \
                             "regression algorithm."
            show = "regression"
        to_return = prepare_standard_response(base_sentence + label_sentence + end_sentence,
                                              'algorithm_verification_prediction', pipeline_array)
        to_return['show'] = show
        return to_return

    def example(self, pipeline_array, dataset):
        if dataset.hasCategoricalLabel:
            label_sentence = "Suppose you own a helmet company, you gather data along the productive process for " \
                             "every helmet (e.g. amount of plastic, temperature in the mold, etc.), and you take note " \
                             "of the outcome of the security test of every item. With a prediction algorithm, " \
                             "you can try to predict with the data you are gathering whether a helmet will pass the " \
                             "security test. On top of that, you can run a further analysis, going to understand" \
                             " which data influence the most the outcome of the security test. "
        else:
            label_sentence = "Suppose you are the owner of vineyard and every year you collect information about the " \
                             "harvest (e.g., average temperature, rain amount, etc.), together with a score (1-10) of " \
                             "the quality of the wine you produce from the harvest. With a prediction algorithm, " \
                             "you can try to predict the quality of the wine for the next harvest. you can run a " \
                             "further analysis, going to understand which data influence the most the outcome of the " \
                             "wine quality. "
        return prepare_standard_response(label_sentence + "Are you interested in this kind of analysis?",
                                         'algorithm_verification_prediction', pipeline_array)


class AlgorithmVerificationRelationships(ComprehensionConversationState):

    def generate(self, pipeline_array, dataset):
        return prepare_standard_response("Are you interested in finding relations in your data?",
                                         'algorithm_verification_relationship', pipeline_array)

    def handle(self, user_message_parsed, pipeline_array, dataset):
        if user_message_parsed['intent']['name'] == 'deny':
            next_state = AlgorithmVerificationClustering()
            return next_state.generate(pipeline_array, dataset)
        elif user_message_parsed['intent']['name'] == 'affirm':
            next_state = CorrelationOrAssociationRules()
            return next_state.generate(pipeline_array, dataset)
        elif user_message_parsed['intent']['name'] in ['don_t_know', 'clarification_request']:
            return self.help(pipeline_array, dataset)
        elif user_message_parsed['intent']['name'] == 'example':
            return self.example(pipeline_array, dataset, user_message_parsed)
        else:
            return prepare_standard_response("Sorry, I didn't understand your request, can you reformulate it?",
                                             'comprehension_end', pipeline_array)

    def help(self, pipeline_array, dataset):
        show = ""
        if dataset.onlyCategorical:
            relation_sentence = 'Your dataset is set up to use Association Rules, an algorithm that scans your table to ' \
                                'try to elicit rules that describe the data in your table. That rules are in the form of ' \
                                '"if-then" clauses, for example "if the customer buys a shirt and a pair of trousers, ' \
                                'then he buy also a pair of socks". '
            show = 'association_rules'
        elif not dataset.categorical:
            relation_sentence = 'Your dataset is set up to use correlations, an algorithm that scans your dataset to ' \
                                'find columns that are linearly dependent one each other. '
            show = 'association_rules'
        else:
            relation_sentence = 'We can find 2 kind of relations on your data, association rules, rules in the form of ' \
                                '\"if->then\" clauses that describe behaviours in your dataset, or correlation, ' \
                                'linear dependence between variables in your table. '

        end_sentence = 'Are you interested in this kind of analysis?'
        standard_response = prepare_standard_response(relation_sentence + end_sentence,
                                                      'algorithm_verification_relationship',
                                                      pipeline_array)
        if show == "":
            return standard_response
        return {**standard_response, 'show': show}

    def example(self, pipeline_array, dataset, user_message_parsed):
        user_entities = retrieve_entities_values(user_message_parsed['entities'])
        association_rules_sentence = 'suppose you are the owner of an eCommerce, applying association rules on the ' \
                                     'purchase history of your website you may discover that if a customer buys a ' \
                                     'monitor, then it is very likely he will buy a HDMI cable. With this information,' \
                                     ' you can suggest HDMI cables to the users who add some monitor in the shopping ' \
                                     'chart to increase your revenue '
        correlation_sentence = 'suppose you are a teacher and you have a file filled with students records: age, ' \
                               'time spent studying, absences, GPA, etc. Looking for regression in your data you ' \
                               'might discover that the GPA is inversely correlated with the GPA -that is, ' \
                               'the lower the number of absences, the higher the GPA. Then, you could crate ' \
                               'incentives to encourage students attending your lessons '
        end_sentence = 'Are you interested in this kind of approach?'
        if dataset.onlyCategorical or 'association_rules' in user_entities:
            return prepare_standard_response(association_rules_sentence.capitalize() + end_sentence,
                                             'algorithm_verification_relationship', pipeline_array)
        elif not dataset.categorical or 'correlation' in user_entities:
            return prepare_standard_response(correlation_sentence.capitalize() + end_sentence,
                                             'algorithm_verification_relationship', pipeline_array)
        else:
            relation_sentence = "You can find relations with two algorithms: association rules and correlation " \
                                "analysis: " + association_rules_sentence + "With correlation, instead, " \
                                + correlation_sentence + "So, are you interested in finding relations in your data? "
            return prepare_standard_response(relation_sentence, 'algorithm_verification_relationship', pipeline_array)


class AlgorithmVerificationClustering(ComprehensionConversationState):

    def generate(self, pipeline_array, dataset):
        return prepare_standard_response("Are you interested grouping your data by similarities?",
                                         'algorithm_verification_clustering', pipeline_array)

    def handle(self, user_message_parsed, pipeline_array, dataset):
        if user_message_parsed['intent']['name'] == 'deny':
            if not dataset.hasLabel:
                next_state = AlgorithmVerificationPredictionIfNotLabel()
                return next_state.generate(pipeline_array, dataset)
            else:
                return prepare_standard_response('I am sorry, I did not understand what you prefer. Can you repeat it, '
                                          'using different words?',
                                          'algorithm_verification_clustering', pipeline_array)
        elif user_message_parsed['intent']['name'] == 'affirm':
            return prepare_standard_response('Ok, we will proceed with clustering analysis!', 'comprehension_end',
                                             ['clustering'])
        elif user_message_parsed['intent']['name'] in ['don_t_know', 'clarification_request']:
            return self.help(pipeline_array, dataset)
        elif user_message_parsed['intent']['name'] == 'example':
            return self.example(pipeline_array, dataset)
        else:
            return prepare_standard_response('TBD', 'comprehension_end', pipeline_array)

    def help(self, pipeline_array, dataset):
        sentence = "Grouping items means applying clustering algorithm: an analysis that aims at finding groups of " \
                   "data similar each other (clusters). This kind of analysis doesn't require any additional " \
                   "information from you, it works in total autonomy. Are you interested in this kind of analysis?"
        standard_response = prepare_standard_response(sentence, 'algorithm_verification_clustering', pipeline_array)
        standard_response['show'] = 'clustering'
        return standard_response

    def example(self, pipeline_array, dataset):
        sentence = "Suppose you are a shop owner and you have demographic information about customers who subscribed " \
                   "you fidelity plan. With clustering, you can group them by similarity, obtaining groups of people " \
                   "that represent your customer base. You can use this information to create promotion tailored to " \
                   "your customers. Are you interested in this kind of analysis?"
        return prepare_standard_response(sentence, 'algorithm_verification_clustering', pipeline_array)


class AlgorithmVerificationPredictionIfNotLabel(ComprehensionConversationState):
    def generate(self, pipeline_array, dataset):
        sentence = "Do you want to try to predict a the value of a column in your dataset, using the data in the " \
                   "other columns? "
        return prepare_standard_response(sentence, 'algorithm_verification_prediction_if_not_label', pipeline_array)

    def handle(self, user_message_parsed, pipeline_array, dataset):
        if user_message_parsed['intent']['name'] == 'deny':
            sentence = "Oh no, we were not able to find anything suitable for you." \
                       "I suggest to start over and try describe what you want to do with different words"
            print("Ehilaaaa")
            return prepare_standard_response(sentence, "algorithm_verification_prediction_if_not_label", pipeline_array)
        elif user_message_parsed['intent']['name'] == 'affirm':
            pass
            # TODO: chiedi label e poi dopo chiama classification or regression
            # next_state = RegressionOrClassification()
            # return next_state.generate(pipeline_array, dataset)
        elif user_message_parsed['intent']['name'] in ['don_t_know', 'clarification_request']:
            return self.help(pipeline_array, dataset)
        elif user_message_parsed['intent']['name'] == 'example':
            return self.example(pipeline_array, dataset)

    def help(self, pipeline_array, dataset):
        sentence = "Predicting a value means training an algorithm to predict a target value - that we will call  " \
                   "\"label\" - starting from the other data. Do you want to perform this kind of analysis? "
        to_return = prepare_standard_response(sentence,
                                              'algorithm_verification_prediction_if_not_label', pipeline_array)
        to_return['show'] = "classification"
        return to_return

    def example(self, pipeline_array, dataset):
        label_sentence = "Suppose you own a helmet company, you gather data along the productive process for " \
                         "every helmet (e.g. amount of plastic, temperature in the mold, etc.), and you take note " \
                         "of the outcome of the security test of every item. With a prediction algorithm, " \
                         "you can try to predict with the data you are gathering whether a helmet will pass the " \
                         "security test. On top of that, you can run a further analysis, going to understand" \
                         " which data influence the most the outcome of the security test. "
        return prepare_standard_response(label_sentence + "Are you interested in this kind of analysis?",
                                         'algorithm_verification_prediction_if_not_label', pipeline_array)


class RegressionOrClassification(ComprehensionConversationState):

    def generate(self, pipeline_array, dataset):
        next_state = FeatureImportanceOrNot()
        if not dataset.hasCategoricalLabel:
            return next_state.generate(['regression'], dataset)
        else:
            return next_state.generate(['classification'], dataset)

    def handle(self, user_message_parsed, pipeline_array, dataset):
        pass


class FeatureImportanceOrNot(ComprehensionConversationState):
    def generate(self, pipeline_array, dataset):
        operation_keyword = 'classification' if 'classification' in pipeline_array else 'regression'
        sentence = "Given the composition of your dataset, we will use a" + operation_keyword.capitalize() + \
                   "Algorithm to predict the value contained in column" + dataset.label + ". Are you interested in " \
                                                                                          "the prediction itself, " \
                                                                                          "or are you more interested " \
                                                                                          "in understanding which are " \
                                                                                          "the most influencing " \
                                                                                          "factors in determining the " \
                                                                                          "prediction? "
        return prepare_standard_response(sentence, "feature_importance_or_not", pipeline_array)

    def handle(self, user_message_parsed, pipeline_array, dataset):
        user_entities = retrieve_entities_values(user_message_parsed['entities'])
        print("USer entities", str(user_entities))
        if len(user_entities) > 0:
            if user_entities[0] in ['first', '1', 'prediction', 'classification', 'regression']:
                return prepare_standard_response("Ok, we can proceed!", "comprehension_end", pipeline_array)
            elif user_entities[0] in ['second', '2', 'features_importance', 'last']:
                pipeline_array.append('featureImportance')
                return prepare_standard_response(
                    "Ok, we will perform a Feature Importance analysis, to highlight which are the most important " \
                    "factors in the prediction outcome", "comprehension_end", pipeline_array)
        return prepare_standard_response('I am sorry, I did not understand what you prefer. Can you repeat it, '
                                         'using different words?', 'feature_importance_or_not', pipeline_array)


class CorrelationOrAssociationRules(ComprehensionConversationState):

    def generate(self, pipeline_array, dataset):
        if dataset.onlyCategorical:
            return prepare_standard_response(
                'Given the composition of your dataset, we will apply association rules algorithm to find ' \
                'relationships between your data in the form of "if -> then" rules', 'comprehension_end', \
                ['associationRules'])
        elif not dataset.categorical:
            return prepare_standard_response(
                'Given the composition of your dataset, we will use correlation to find direct relationships ' \
                'between columns in your table', 'comprehension_end', ['correlation'])
        return prepare_standard_response(
            'Are you more interested in finding direct relationships between numerical columns, or rules in the ' \
            '"if -> then" form that describe behaviours of more columns? ', 'correlation_or_association_rules', \
            pipeline_array)

    def handle(self, user_message_parsed, pipeline_array, dataset):
        if user_message_parsed['intent']['name'] == 'preference':
            user_interest = retrieve_entities_values(user_message_parsed['entities'])
            if len(user_interest) > 0:
                if user_interest[0] in ['correlation', 'first', '1']:
                    return prepare_standard_response('Ok, we will proceed with correlation analysis!',
                                                     'comprehension_end', ['correlation'])
                elif user_interest[0] in ['association_rules', 'second', '2']:
                    return prepare_standard_response('Ok, we will proceed with association rules analysis!',
                                                     'comprehension_end', [
                                                         'associationRules'])

        return prepare_standard_response(
            'I am sorry, I did not understand what you prefer. Can you repeat it, using different words?', \
            'correlation_or_association_rules', pipeline_array)


class LabelRequestIfNotInsertedBefore(ComprehensionConversationState):

    def generate(self, pipeline_array, dataset):
        message = "Perfect! To do that, though, I need to understand which are is column you want to predict. " \
                  "Please, can write me just the name of that column? "
        print("le colonne sono: ", dataset.ds.columns())
        return prepare_standard_response(message, "label_request", pipeline_array)

    def handle(self, user_message_parsed, pipeline_array, dataset):
        pass


switcher = {
    'reformulation': Reformulation,
    'algorithm_verification_prediction': AlgorithmVerificationPrediction,
    'algorithm_verification_relationship': AlgorithmVerificationRelationships,
    'algorithm_verification_clustering': AlgorithmVerificationClustering,
    'algorithm_verification_prediction_if_not_label': AlgorithmVerificationPredictionIfNotLabel,
    'regression_or_classification': RegressionOrClassification,
    'correlation_or_association_rules': CorrelationOrAssociationRules,
    'feature_importance_or_not': FeatureImportanceOrNot,
    'label_request': LabelRequestIfNotInsertedBefore
}


def pipeline_array_to_string(pipeline_array):
    pipeline_string = ''
    for item in pipeline_array:
        pipeline_string = pipeline_string + ' ' + item
    return pipeline_string


def comprehension_conversation_handler(user_payload, dataset):
    print("invocata su ", user_payload)
    user_message_parsed = parse(user_payload['message'])
    print("user intent is:" + str(user_message_parsed))
    user_utterance = user_payload['message']
    conversation_state = user_payload['comprehension_state']
    pipeline_array = user_payload['comprehension_pipeline']

    # I create a class instance of the object of the state in which we are
    func = switcher.get(conversation_state, "nothing")()

    # Execute the function
    result = func.handle(user_message_parsed, pipeline_array, dataset)
    print("RESULT è", result)
    # new_pipeline_string = pipeline_array_to_string(pipeline_array)
    process_complete = {'complete': True} if result['comprehension_state'] == 'comprehension_end' else {}
    # return {'message': new_message, 'comprehension_state': new_state, 'comprehension_pipeline': new_pipeline_string, **process_complete}
    return {**result, **process_complete}
