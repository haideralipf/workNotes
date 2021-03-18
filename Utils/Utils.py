Utils

def pandas_json_to_dict(cell):
    import json
    with pd.option_context("display.max_colwidth", None):
        val = cell.to_string(index=False)
        val = val.replace("\'", "\"")
        val = val.replace(" ", "")
        return json.loads(val)