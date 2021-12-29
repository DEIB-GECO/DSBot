def get_last_dataset(result):
    if 'transformed_ds' in result:
        dataset = result['transformed_ds']
    elif 'new_dataset' in result:
        dataset = result['new_dataset']
    else:
        dataset = result['original_dataset'].ds
    return dataset
