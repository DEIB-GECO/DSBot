def rec_inside(chiave, dizio):
    if 'values' not in dizio:
        return False
    elif chiave in dizio['values']:
        return True
    else:
        for k in dizio['values']:
            return rec_inside(chiave, dizio['values'][k])