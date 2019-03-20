import postprocess

def process_clinical_trails_row(row, key_column_name, predictor):
    """
    Params:
        row - clinical trails row
        key_column_name - column_name of key
        predictor - predictor function: ner = predictor(input_text)

    Return:
        row_key - the key of row (None empty)
        predicted_ners - analyzed row

    """
    predicted_ners = dict()
    for col_name, col_val in row.items():
        if col_name == key_column_name:  # is a key to identify row
            row_key = col_val
        else:  # is text, predict
            ner_result = predictor(col_val)  # predict
            ner_result = postprocess.ner_result_format(ner_result)  # format
            predicted_ners[col_name] = ner_result
    return row_key, predicted_ners