import simplejson as json
import pandas as pd
from .mime_types import InputSelectionMimeDtype, InputCheckboxMimeDtype, InputTextMimeDtype

def normalize_inputable_dataframe(df):
    df_dict = {}
    for cindex, col in enumerate(df.columns):
        if isinstance(df.dtypes[cindex], InputSelectionMimeDtype) or isinstance(df.dtypes[cindex], InputCheckboxMimeDtype) or isinstance(df.dtypes[cindex], InputTextMimeDtype):
            df_dict[col] = []
            for rindex in range(df.shape[0]):
                df_dict[col].append(json.loads(df.at[rindex, col])['input'])
        else:
            df_dict[col] = df[col].tolist()

    return pd.DataFrame(df_dict)
