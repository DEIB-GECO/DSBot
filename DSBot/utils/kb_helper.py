import json


def rec_inside(chiave, dizio):
    if 'values' not in dizio:
        return False
    elif chiave in dizio['values']:
        return True
    else:
        for k in dizio['values']:
            return rec_inside(chiave, dizio['values'][k])


def get_term_path(term):
    """ get_term_path function takes a DSL and returns the path inside the knowledge base tree to get to the term.

        :param term: the term to retrieve the path of
        :return: a list of terms that represents the path inside the
        knowledge base to get to the element, if a path exist. The list is empty otherwise.
    """
    def get_term_path_helper(term, knowledge_base):
        for element_key in knowledge_base:
            print("Sto guardando ", element_key)
            if element_key == term:
                return [term]
            elif 'values' in knowledge_base[element_key]:
                siblings_path = get_term_path_helper(term, knowledge_base[element_key]['values'])
                if len(siblings_path) > 0:
                    siblings_path.insert(0, element_key)
                    return siblings_path
        return []

    with open('./kbSynonyms.json', "r") as knowledge_base_file:
        knowledge_base = json.loads(knowledge_base_file.read())

    path_list = get_term_path_helper(term, knowledge_base)
    return path_list


def get_field_from_path(path, field):
    """
    This function returns the text of the field passed as a parameter, in the path element that occupies the lowest position of the knowledge base.
    For example, if the path is a b c, the field is x, the function retrieve the string contained in c[x] if exists, otherwise b[x], otherwise a[x].
    If the field is not found in any element, the function returns the empty strings.

    :param path: a valid path of items in the knowledge base
    :param field: the field of whom to retrieve the string in the knowledge base
    :return: the string in the contained in field of the lowest element of the path in the tree that has that field
    """
    def get_field_from_path_helper(path, field, knowledge_base):
        if len(path) > 1:
            #print("A")
            element = path.pop(0)
            retrieved_string = get_field_from_path_helper(path, field, knowledge_base[element]["values"])
            #print("fatto, la sringa è ", retrieved_string, "l'elemento ", element, knowledge_base)
            if retrieved_string == "" and field in knowledge_base[element]:
                retrieved_string = knowledge_base[element][field]
        elif field in knowledge_base[path[0]]:
            #print("B", knowledge_base)
            retrieved_string = knowledge_base[path[0]][field]
        else:
            #print("C", knowledge_base)
            retrieved_string = ""
        return retrieved_string

    with open('./kbSynonyms.json', "r") as knowledge_base_file:
        knowledge_base = json.loads(knowledge_base_file.read())

    textual_description = get_field_from_path_helper(path, field, knowledge_base)
    return textual_description

list =  get_term_path("varianceThreshold")
print("la lista è ", list)
descr = get_field_from_path(list, "description")
print("La ddescrizione è ", descr)