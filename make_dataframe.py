import pickle
import pandas as pd
import numpy as np

def get_obs_data(obs):
    field_guide = pickle.load(open('sebs_field_guide.p', 'rb'))
    patient_drug_nums = list(range(len(obs["patient"]["drug"])))
    patient_reaction_nums = list(range(len(obs["patient"]["reaction"])))
    column_data = []
    for key in field_guide.index:
        if field_guide.loc[key, 'Level'] == 'none':
            try:
                column_data.append(obs[key])
            except:
                column_data.append(np.nan)
        elif field_guide.loc[key, 'Level'] == 'patient':
            try:
                column_data.append(obs["patient"][key])
            except:
                column_data.append(np.nan)
        elif field_guide.loc[key, 'Level'] == ('patient', 'reaction'):
            try:
                reactions = []
                for i in patient_reaction_nums:
                    reactions.append(obs["patient"]["reaction"][i][key])
                column_data.append(reactions)
            except:
                column_data.append(np.nan)
        elif field_guide.loc[key, 'Level'] == ('patient', 'drug'):
            try:
                drugs_info = []
                for i in patient_drug_nums:
                    drugs_info.append(obs["patient"]["drug"][i][key])
                column_data.append(drugs_info)
            except:
                column_data.append(np.nan)
        elif field_guide.loc[key, 'Level'] == ('patient', 'drug', 'activesubstance'):
            try: 
                substances = []
                for i in patient_drug_nums:
                    substances.append(obs["patient"]["drug"][i]["activesubstance"][key])
                column_data.append(substances)
            except:
                column_data.append(np.nan)
        df = pd.DataFrame(column_data).T
    return df


def get_all_data(data):
    field_guide = pickle.load(open('sebs_field_guide.p', 'rb'))
    dfs =[]
    for i in range(len(data['results'])):
        dfs.append(get_obs_data(data['results'][i]))
    df = pd.concat(dfs)
    df.columns = field_guide.index
    return df