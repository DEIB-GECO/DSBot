def get_last_dataset(result):
    if 'new_dataset' in result:
        return result['new_dataset']
    else:
        return result['original_dataset'].ds
