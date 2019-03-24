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
