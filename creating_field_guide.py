import numpy as np
import pandas as pd
import json
import pickle


def create_field_guide():
    with open('drug-event-0001-of-0035.json') as json_file:
        data = json.load(json_file)
    
    obs1 = data['results'][0]
    #creating a dataframe with index as irreducible keys from the json file, a description from the FDA website
    #their datatype, and which level of the json they were retrieved from beginning with 
    #data['results'][0].keys() = obs1.keys() => level 0

    vars1 = [x for x in obs1.keys()] # level 0
    vars2 = [x for x in obs1['patient'].keys()] # level 1
    vars3 = [x for x in obs1['patient']['reaction'][0].keys()] #level 2
    vars4 = [x for x in obs1['patient']['drug'][0].keys()] # level 2
    vars5 = [x for x in obs1['patient']['drug'][0]['activesubstance'].keys()] # level 3

    variables = vars1 + vars2 + vars3 + vars4 + vars5

    info = pd.DataFrame(np.zeros((len(variables),3), 'str'), index = variables, columns = ['Description', 'Values', 'dType'])

    pd.options.display.max_colwidth = 500
    
    level_array1 = ['none' for x in info.index if x in vars1]
    level_array2 = ['patient' for x in info.index if x in vars2]
    level_array3 = [('patient', 'reaction') for x in info.index if x in vars3]
    level_array4 = [('patient', 'drug') for x in info.index if x in vars4]
    level_array5 = [('patient', 'drug', 'activesubstance') for x in info.index if x in vars5]
    level_arrays = level_array1 + level_array2 + level_array3 + level_array4 + level_array5
    info['Level'] = level_arrays

    # Now to fill in the dataframe
    info.loc['receivedate', 'Description'] = 'Date that the report was first received by FDA.'
    info.loc['receivedate', 'dType'] = 'str'
    info.loc['receivedate', 'Values'] = 'YYYMMDD'
    
    info.loc['transmissiondate', 'Description'] = 'Date that the record was created. This may be earlier than the date the record   was received by the FDA.'
    info.loc['transmissiondate', 'dType'] = 'str'
    info.loc['transmissiondate', 'Values'] ='YYYMMDD'

    info.loc['fulfillexpeditecriteria', 'Description'] = 'Identifies expedited reports (those that were processed within 15 days).'
    info.loc['fulfillexpeditecriteria', 'dType'] = 'str'
    info.loc['fulfillexpeditecriteria', 'Values'] = [{'1': 'Yes', '2': 'No'}]

    info.loc['occurcountry', 'Description'] = 'The name of the country where the event occurred.'
    info.loc['occurcountry', 'dType'] = 'str'
    info.loc['occurcountry', 'Values'] = 'country name'

    info.loc['receiptdate', 'Description'] = 'Date that the most recent information in the report was received by FDA.'
    info.loc['receiptdate', 'dType'] = 'str'
    info.loc['receiptdate', 'Values'] = 'YYYMMDD'

    info.loc['serious', 'Description'] = 'Seriousness of the adverse event.'
    info.loc['serious', 'dType'] = 'str'
    info.loc['serious', 'Values'] = [{'1': 'The adverse event resulted in death, a life threatening condition, hospitalization, disability, congenital anomaly, or other serious condition',\
                                 '2': 'The adverse event did not result in any of the above'}]

    info.loc['companynumb', 'Description'] = 'Identifier for the company providing the report. This is self-assigned.'
    info.loc['companynumb', 'dType'] = 'str'
    info.loc['companynumb', 'Values'] = '?'

    info.loc['safetyreportid', 'Description'] = 'The 8-digit Safety Report ID number, also known as the case report number or case ID. The first 7 digits (before the hyphen) identify an individual report and the last digit (after the hyphen) is a checksum. This field can be used to identify or find a specific adverse event report.'
    info.loc['safetyreportid', 'dType'] = 'str'
    info.loc['safetyreportid', 'Values'] = '8-digit Safety Report ID number'

    info.loc['patientsex', 'Description'] = 'The sex of the patient.'
    info.loc['patientsex', 'dType'] = 'str'
    info.loc['patientsex', 'Values'] = [{'0': 'Unknown', '1': 'Male', '2':'Female'}]

    info.loc['reactionmeddrapt', 'Description'] = 'Patient reaction, as a MedDRA term. Note that these terms are encoded in British English. For instance, diarrhea is spelled diarrohea. MedDRA is a standardized medical terminology.'
    info.loc['reactionmeddrapt', 'dType'] = 'str'
    info.loc['reactionmeddrapt', 'Values'] = '?'

    info.loc['reactionoutcome', 'Description'] = 'Outcome of the reaction in reactionmeddrapt at the time of last observation.'
    info.loc['reactionoutcome', 'dType'] = 'str'
    info.loc['reactionoutcome', 'Values'] = [{'1': 'Recovered/resolved', '2': 'Recovering/resolving',\
                                         '3': 'Not recovered/not resolved', '4': 'Recovered/resolved with sequelae (consequent health issues)',\
                                         '5': 'Fatal', '6': 'Unknown'}]

    info.loc['medicinalproduct', 'Description'] = 'Drug name. This may be the valid trade name of the product (such as ADVIL or ALEVE) or the generic name (such as IBUPROFEN). This field is not systematically normalized. It may contain misspellings or idiosyncratic descriptions of drugs, such as combination products such as those used for birth control.'
    info.loc['medicinalproduct', 'dType'] = 'str'
    info.loc['medicinalproduct', 'Values'] = '?'

    info.loc['drugindication', 'Description'] = 'Indication for the drug’s use.'
    info.loc['drugindication', 'dType'] = 'str'
    info.loc['drugindication', 'Values'] = '?'

    info.loc['drugcharacterization', 'Description'] = 'Reported role of the drug in the adverse event report. These values are not validated by FDA.'
    info.loc['drugcharacterization', 'dType'] = 'str'
    info.loc['drugcharacterization', 'Values'] = [{'1': 'Suspect (the drug was considered by the reporter to be the cause)',\
                                              '2': 'Concomitant (the drug was reported as being taken along with the suspect drug)',\
                                              '3': 'Interacting (the drug was considered by the reporter to have interacted with the suspect drug)'}]

    info.loc['drugadministrationroute', 'Description'] = 'The drug’s route of administration.'
    info.loc['drugadministrationroute', 'dType'] = 'str'
    info.loc['drugadministrationroute', 'Values'] = [{'001': 'Auricular (otic)', '002': 'Buccal', '003': 'Cutaneous', '004': 'Dental', '005': 'Endocervical',\
                                                 '006': 'Endosinusial', '007': 'Endotracheal', '008': 'Epidural', '009': 'Extra-amniotic', '010': 'Hemodialysis',\
                                                 '011': 'Intra corpus cavernosum', '012': 'Intra-amniotic', '013': 'Intra-arterial', '014': 'Intra-articular',\
                                                 '015': 'Intra-uterine', '016': 'Intracardiac', '017': 'Intracavernous', '018': 'Intracerebral', '019': 'Intracervical',\
                                                 '020': 'Intracisternal', '021': 'Intracorneal', '022': 'Intracoronary', '023': 'Intradermal', '024': 'Intradiscal (intraspinal)',\
                                                 '025': 'Intrahepatic', '026': 'Intralesional', '027': 'Intralymphatic', '028': 'Intramedullar (bone marrow)', '029': 'Intrameningeal',\
                                                 '030': 'Intramuscular', '031': 'Intraocular', '032': 'Intrapericardial', '033': 'Intraperitoneal', '034': 'Intrapleural',\
                                                 '035': 'Intrasynovial', '036': 'Intratumor', '037': 'Intrathecal', '038': 'Intrathoracic', '039': 'Intratracheal',\
                                                 '040': 'Intravenous bolus', '041': 'Intravenous drip', '042': 'Intravenous (not otherwise specified)', '043': 'Intravesical',\
                                                 '044': 'Iontophoresis', '045': 'Nasal', '046': 'Occlusive dressing technique', '047': 'Ophthalmic', '048': 'Oral',\
                                                 '049': 'Oropharingeal', '050': 'Other', '051': 'Parenteral', '052': 'Periarticular', '053': 'Perineural', '054': 'Rectal',\
                                                 '055': 'Respiratory (inhalation)', '056': 'Retrobulbar', '057': 'Sunconjunctival', '058': 'Subcutaneous', '059': 'Subdermal',\
                                                 '060': 'Sublingual', '061': 'Topical', '062': 'Transdermal', '063': 'Transmammary', '064': 'Transplacental',\
                                                 '065': 'Unknown', '066': 'Urethral', '067': 'Vaginal'}]

    info.loc['drugseparatedosagenumb', 'Description'] = 'The number of separate doses that were administered.'
    info.loc['drugseparatedosagenumb', 'dType'] = 'str'
    info.loc['drugseparatedosagenumb', 'Values'] = '?'

    info.loc['drugstructuredosageunit', 'Description'] = 'The unit for the field drugstructuredosagenumb. For example, mg in 300 mg.'
    info.loc['drugstructuredosageunit', 'dType'] = 'str'
    info.loc['drugstructuredosageunit', 'Values'] = [{'001': 'kg (kilograms)', '002': 'g (grams)', '003': 'mg (milligrams)', '004': 'µg (micrograms)'}]

    info.loc['drugbatchnumb', 'Description'] = 'Drug product lot number, if provided.'
    info.loc['drugbatchnumb', 'dType'] = 'str'
    info.loc['drugbatchnumb', 'Values'] = '?'

    info.loc['drugintervaldosageunitnumb', 'Description'] = 'Number of units in the field drugintervaldosagedefinition'
    info.loc['drugintervaldosageunitnumb', 'dType'] = 'str'
    info.loc['drugintervaldosageunitnumb', 'Values'] = '?'

    info.loc['drugdosagetext', 'Description'] = 'Additional detail about the dosage taken. Frequently unknown, but occasionally including information like a brief textual description of the schedule of administration.'
    info.loc['drugdosagetext', 'dType'] = 'str'
    info.loc['drugdosagetext', 'Values'] = '?'

    info.loc['actiondrug', 'Description'] = 'Actions taken with the drug.'
    info.loc['actiondrug', 'dType'] = 'str'
    info.loc['actiondrug', 'Values'] = [{'1': 'Drug withdrawn', '2': 'Dose reduced', '3': 'Dose increased',
                                    '4': 'Dose not changed', '5': 'Unknown', '6': 'Not applicable'}]
    
    info.loc['drugintervaldosagedefinition', 'Description'] = 'The unit for the interval in the field drugintervaldosageunitnumb.'
    info.loc['drugintervaldosagedefinition', 'dType'] = 'str'
    info.loc['drugintervaldosagedefinition', 'Values'] = [{'801': 'Year', '802': 'Month', '803': 'Week', '804': 'Day', '805': 'Hour', '806': 'Minute',  '807': 'Trimester', '810': 'Cyclical', '811': 'Trimester', '812': 'As necessary', '813': 'Total'}]

    info.loc['drugauthorizationnumb', 'Description'] = 'Drug authorization or application number (NDA or ANDA), if provided.'
    info.loc['drugauthorizationnumb', 'dType'] = 'str'
    info.loc['drugauthorizationnumb', 'Values'] = '?'

    info.loc['drugdosageform', 'Description'] = 'The drug’s dosage form. There is no standard, but values may include terms like tablet or solution for injection.'
    info.loc['drugdosageform', 'dType'] = 'str'
    info.loc['drugdosageform', 'Values'] = '?'

    info.loc['drugstructuredosagenumb', 'Description'] = 'The number portion of a dosage; when combined with drugstructuredosageunit the complete dosage information is represented. For example, 300 in 300 mg.'
    info.loc['drugstructuredosagenumb', 'dType'] = 'str'
    info.loc['drugstructuredosagenumb', 'Values'] = '?'

    info.loc['activesubstancename', 'Description'] = 'Product active ingredient, which may be different than other drug identifiers (when provided).'
    info.loc['activesubstancename', 'dType'] = 'str'
    info.loc['activesubstancename', 'Values'] = 'name'


    to_drop = ['receivedateformat', 'patient', 'sender', 'primarysource', 'duplicate', 'reportduplicate', \
           'receiver', 'safetyreportversion', 'transmissiondateformat', 'primarysourcecountry',\
          'reactionmeddraversionpt', 'reaction', 'drug', 'openfda', 'activesubstance', 'receiptdateformat', 'reporttype']

    final_info = info.drop(index = to_drop)

    pickle.dump(final_info, open('sebs_field_guide.p', 'wb'))
    final_info.to_csv(r'sebs_field_guide.csv')
    return