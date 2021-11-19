from abc import ABC, abstractmethod
import json
from pathlib import Path

algorithm_modules = ['clustering', 'classification', 'correlation', 'associationRules', 'regression']

"""
Every chat state has 2 methods: 
 - generate that generate the sentence to prompt to the user before its response
 - handle that takes user input and decides the following state
"""


class ComprehensionConversationState(ABC):

    @abstractmethod
    def generate(self, pipeline_array):
        pass

    @abstractmethod
    def handle(self, user_utterance, pipeline_array):
        pass


class Reformulation(ComprehensionConversationState):

    def generate(self):
        pass

    def handle(self, user_utterance, pipeline_array):
        if user_utterance == 'yes':
            return 'ok, we can proceed', 'comprehension_end', pipeline_array
            # TODO qui dobbiamo iniziare a creare la pipeline, non prima!
        else:
            next_state = AlgorithmVerfication()
            return next_state.generate(pipeline_array)


class AlgorithmVerfication(ComprehensionConversationState):

    def generate(self, pipeline_array):
        with open('./kb.json', "r") as knowledge_base_file:
            knowledge_base = json.loads(knowledge_base_file.read())
        for user_module in pipeline_array:
            for algorithm_family in algorithm_modules:
                if user_module in knowledge_base[algorithm_family]:
                    with open(Path(__file__).parent / 'text_productions.json', "r") as process_file:
                        producible_sentences = json.loads(process_file.read())
                    return 'You want to apply ' + producible_sentences[algorithm_family]["readableName"] + \
                           ', don\'t you?', 'algorithm_verification', pipeline_array

        return 'Non ho trovato la unit', "algorithm_verification", pipeline_array

    def handle(self, user_utterance, pipeline_array):
        print("AlgorithmVerificatio.handle eseguito")
        if user_utterance == 'no':
            next_state = AlgorithmFamilySelection()
            return next_state.generate(pipeline_array)
        elif user_utterance == 'yes':
            return 'ok, we can proceed', 'comprehension_end', pipeline_array


class AlgorithmFamilySelection(ComprehensionConversationState):

    def generate(self, pipeline_array):
        print("AlgorithmFamilySelection eseguito")
        return 'What do you want to do? Cluster your data, predict some continuous value, predict some label, ' \
               'find some rules, or finding correlation among columns?', 'algorithm_family_selection', pipeline_array

    def handle(self, user_utterance, pipeline_array):
        if user_utterance not in algorithm_modules:
            return "Sorry, the module you chose seems not to exist", 'algorithm_family_selection', pipeline_array
        else:
            pipeline_array = [pipeline_module.replace(pipeline_module, user_utterance) for pipeline_module in pipeline_array]
        return "Ok I changed the pipeline, now it is_: " + str(pipeline_array), 'comprehension_end', pipeline_array


switcher = {
    'reformulation': Reformulation,
    'algorithm_verification': AlgorithmVerfication,
    'algorithm_family_selection': AlgorithmFamilySelection
}


def pipeline_array_to_string(pipeline_array):
    pipeline_string = ''
    for item in pipeline_array:
        pipeline_string = pipeline_string + ' ' + item
    return pipeline_string


def comprehension_conversation_handler(user_payload):
    print(user_payload)
    user_utterance = user_payload['message']
    conversation_state = user_payload['comprehension_state']
    pipeline_array = user_payload['comprehension_pipeline']

    # I create a class instance of the object of the state in which we are
    func = switcher.get(conversation_state, "nothing")()

    # Execute the function
    new_message, new_state, new_pipeline_array = func.handle(user_utterance, pipeline_array)
    new_pipeline_string = pipeline_array_to_string(pipeline_array)
    return {'message': new_message, 'comprehension_state': new_state, 'comprehension_pipeline': new_pipeline_string}
