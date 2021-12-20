import json
from pathlib import Path

from utils.kb_helper import get_field_from_path, get_term_path

introductory_sentence = "Let me understand if I interpreted well your request. "
final_sentence = " Is it right?"


def summary_producer(operations_array, label):
    print("Summary producer, array è: " + str(operations_array))
    with open(Path(__file__).parent / 'text_productions.json', "r") as process_file:
        producible_sentences = json.loads(process_file.read())
    # with open('./kb_synonyms.json', "r") as knowledge_base_file:
    #   knowledge_base = json.loads(knowledge_base_file.read())

    sentences_array = []
    for user_module in operations_array:
        user_module_path = get_term_path(user_module)
        user_module_sentence = get_field_from_path(user_module_path, "summary")
        print("User module", user_module_path, "sentence: ", user_module_sentence)
        if user_module_sentence != "":
            sentences_array.append(user_module_sentence)
    #    for algorithm_family in knowledge_base.keys():
    #        if user_module in knowledge_base[algorithm_family]:
    #            sentences_array.append(producible_sentences[algorithm_family]['summary'])

    # sentences_array = [producible_sentences[sentence]["summary"] for sentence in operations_array]
    sentences_array = list(filter(None, sentences_array))
    sentences_number = len(sentences_array)

    print("La lista è lunga: ", sentences_array)
    if sentences_number == 1:
        central_sentence = sentences_array[0].capitalize()
    elif sentences_number == 2:
        central_sentence = f"First, {sentences_array[0]} Then, {sentences_array[1]}"
    elif sentences_number > 2:
        central_sentence = f"First, {sentences_array[0]} Then, {sentences_array[1]}{' '.join([str(elem) for elem in sentences_array[2:-2]])} Finally, {sentences_array[-1]}"
    else:
        central_sentence = ""
    print(str(operations_array))
    to_replace = f"'{label}'" if label != "" else "a"
    central_sentence = central_sentence.replace('##label##', to_replace)
    return introductory_sentence + central_sentence + final_sentence
