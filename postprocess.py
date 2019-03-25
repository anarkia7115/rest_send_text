import configparser
config = configparser.ConfigParser()
config.read("./config.ini")


def ner_result_format(ner_result):
    """
    Params:
        ner_result - dict, having keys {'ents', 'text', 'title'}
            |- ents
                |- start: int
                |- end: int
                |- label (DISO, PRGE, CHED)
                |- text
    Returns:
        list of dict:
            |- start: int
            |- end: int
            |- label (DISO, PRGE, CHED)
            |- text
    """
    if ner_result is None:
        return None
    else:
        return ner_result['ents']


def save_dict_rows():
    output_file = config["PATHS"]["row_records"]
    import preprocess
    dict_rows = preprocess.load_clinical_trails_text(None, 'dict')
    import data_helpers
    data_helpers.dict_save(dict_rows, output_file)

if __name__ == "__main__":
    save_dict_rows()