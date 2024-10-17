from collections import Counter
import numpy as np

def _adult(cc_lst):

    x = Counter(cc_lst)

    # Mandatory HCC assignments for adults
    # Removed in this version, present in V0519F3M

    # Severe Illness HCCs (see %macro SEVERE_LIST)
    severe_lst = [
        "HHS_HCC002", "HHS_HCC003", "HHS_HCC004", "HHS_HCC006", "HHS_HCC018", 
        "HHS_HCC023", "HHS_HCC034","HHS_HCC041", "HHS_HCC042", "HHS_HCC096",
        "HHS_HCC121", "HHS_HCC122", "HHS_HCC125", "HHS_HCC126", "HHS_HCC127",
        "HHS_HCC128", "HHS_HCC129", "HHS_HCC135", "HHS_HCC145", "HHS_HCC156",
        "HHS_HCC158", "HHS_HCC163", "HHS_HCC183", "HHS_HCC218", "HHS_HCC223",
        "HHS_HCC251"
        ]
    # Transplant HCCs (see %macro TRANSPLANT_LIST)
    transplant_lst = [
        "HHS_HCC018", "HHS_HCC034", "HHS_HCC041", "HHS_HCC128", "HHS_HCC129",
        "HHS_HCC158", "HHS_HCC183", "HHS_HCC251"
    ]

    # Group Adult Variables  (see %macro GENERATE_ADULT_VARIABLES)

    gvars = {
            "G01": ["HHS_HCC019", "HHS_HCC020", "HHS_HCC021"],
            "G02B": ["HHS_HCC026", "HHS_HCC027"],
            "G04": ["HHS_HCC061", "HHS_HCC062"],
            "G06A": ["HHS_HCC067", "HHS_HCC068","HHS_HCC069"],
            "G07A": ["HHS_HCC070", "HHS_HCC071"],
            "G08": ["HHS_HCC073", "HHS_HCC074"],
            "G09A": ["HHS_HCC081", "HHS_HCC082"],
            "G09C": ["HHS_HCC083", "HHS_HCC084"],
            "G10": ["HHS_HCC106", "HHS_HCC107"],
            "G11": ["HHS_HCC108", "HHS_HCC109"],
            "G12": ["HHS_HCC117", "HHS_HCC119"],
            "G13": ["HHS_HCC126", "HHS_HCC127"],
            "G14": ["HHS_HCC128", "HHS_HCC129"],
            "G15A": ["HHS_HCC160", "HHS_HCC161_1", "HHS_HCC161_2"],
            "G16": ["HHS_HCC187", "HHS_HCC188"],
            "G17A": ["HHS_HCC204", "HHS_HCC205"],
            "G18A": ["HHS_HCC207", "HHS_HCC208"],
            "G21": ["HHS_HCC137","HHS_HCC138","HHS_HCC139"],
            "G24": ["HHS_HCC018","HHS_HCC183"]
            }

    rxc_interactions = {
        "RXC_01_x_HCC001" : ( "RXC_01", "HHS_HCC001"),
        "RXC_02_x_HCC037_1_036_035s_034" : ("RXC_02", ["HHS_HCC037_1","HHS_HCC034","HHS_HCC035_1","HHS_HCC035_2", "HHS_HCC036"]),
        "RXC_03_x_HCC142" : ("RXC_03", "HHS_HCC142"),
        "RXC_04_x_HCC184_183_187_188" : ("RXC_04", ["HHS_HCC184", "HHS_HCC183","HHS_HCC187", "HHS_HCC188"]),
        "RXC_05_x_HCC048_041" : ("RXC_05", ["HHS_HCC048","HHS_HCC041"]),
        "RXC_06_x_HCC018_019_020_021" : ("RXC_06", ["HHS_HCC018","HHS_HCC019","HHS_HCC020", "HHS_HCC021"]),
        "RXC_07_x_HCC018_019_020_021" : ("RXC_07", ["HHS_HCC018","HHS_HCC019","HHS_HCC020","HHS_HCC021"]),
        "RXC_08_x_HCC118" : ("RXC_08","HHS_HCC118"),
        # RXC09 x HCC56 or 57 and HCC48 or 41 is a more complex case
        "RXC_09_x_HCC056_057_and_048_041" : ("RXC_09", lambda x: (x["HHS_HCC056"] > 0 or x["HHS_HCC057"] > 0) and
                                                                 (x["HHS_HCC048"] > 0 or x["HHS_HCC041"] > 0)),
        "RXC_09_x_HCC056" : ("RXC_09", "HHS_HCC056"),
        "RXC_09_x_HCC057": ("RXC_09", "HHS_HCC057"),
        "RXC_09_x_HCC048_041": ("RXC_09", ["HHS_HCC048","HHS_HCC041"]),
        "RXC_10_x_HCC159_158": ("RXC_10", ["HHS_HCC159", "HHS_HCC158"]),
    }

    # Apply Group Adult Variable Mappings

    for group, conditions in gvars.items():
        if any(x[condition] > 0 for condition in conditions):
            x[group]=1
            for condition in conditions:
                x[condition] = 0

    # Calculate HCC_CNT (excluding HCC022)
    hcc_cnt= sum(1 for k, v in x.items() if k.startswith("HHS_HCC") and v > 0 and k != "HHS_HCC022")

    # Severe illness interactions
    severe=any(x[hcc] > 0 for hcc in severe_lst)
    if severe:
        for i in range (1,11):
            if i == 10:
                x[f"SEVERE_HCC_COUNT{i}PLUS"] = 1 if hcc_cnt >= i else 0
            else:
                x[f"SEVERE_HCC_COUNT{i}"] = 1 if hcc_cnt == i else 0

    # Transplant interactions
    transplant = any(x[hcc] >0 for hcc in transplant_lst)
    if transplant:
        for i in range (4,9): # Only 4+ transplant HCCs give HCC Count
            if i == 8:
                x[f"TRANSPLANT_HCC_COUNT{i}PLUS" ] = 1 if hcc_cnt >= i else 0
            else:
                x[f"TRANSPLANT_HCC_COUNT{i}"] = 1 if hcc_cnt == i else 0

    # Enrolment Duration Flags
    for i in range(1,7):
        x[f"HCC_EED{i}"] = 1 if hcc_cnt > 0 and x.get("ENROLDURATION") == i else 0

    # RXC Interactions
    for interaction, (rxc, condition) in rxc_interactions.items():
        if isinstance(condition,str):
            x[interaction] = x[rxc] * (x[condition] > 0)
        elif isinstance(condition, list):
            x[interaction] = x[rxc] * any(x[hcc] > 0 for hcc in condition)
        elif callable(condition):
            x[interaction] = x[rxc] * condition(x)

    cc_lst = [k for k, v in x.items() if v > 0]

    return cc_lst
   
   
def _child(cc_lst):

    x = Counter(cc_lst)

    # Mandatory HCC assignments for children
    # Removed in this version, present in V0519F3M

    # Severe Illness HCCs (see %macro SEVERE_LIST)
    severe_lst = [
        "HHS_HCC002", "HHS_HCC003", "HHS_HCC004", "HHS_HCC006", "HHS_HCC018",
        "HHS_HCC023", "HHS_HCC034", "HHS_HCC041", "HHS_HCC042", "HHS_HCC096",
        "HHS_HCC121", "HHS_HCC122", "HHS_HCC125", "HHS_HCC126", "HHS_HCC127",
        "HHS_HCC128", "HHS_HCC129", "HHS_HCC135", "HHS_HCC145", "HHS_HCC156",
        "HHS_HCC158", "HHS_HCC163", "HHS_HCC183", "HHS_HCC218", "HHS_HCC223",
        "HHS_HCC251"
    ]
    # Transplant HCCs (see %macro TRANSPLANT_LIST)
    transplant_lst = [
        "HHS_HCC018", "HHS_HCC034", "HHS_HCC041", "HHS_HCC128", "HHS_HCC129",
        "HHS_HCC158", "HHS_HCC183", "HHS_HCC251"
    ]

    # Group Adult Variables  (see %macro GENERATE_CHILD_VARIABLES)

    gvars = {
        "G01": ["HHS_HCC019", "HHS_HCC020", "HHS_HCC021"],
        "G02B": ["HHS_HCC026", "HHS_HCC027"],
        "G02D": ["HHS_HCC028", "HHS_HCC029"],
        "G03": ["HHS_HCC054", "HHS_HCC055"],
        "G04": ["HHS_HCC061", "HHS_HCC062"],
        "G06A": ["HHS_HCC067", "HHS_HCC068", "HHS_HCC069"],
        "G07A": ["HHS_HCC070", "HHS_HCC071"],
        "G08": ["HHS_HCC073", "HHS_HCC074"],
        "G09A": ["HHS_HCC081", "HHS_HCC082"],
        "G09C": ["HHS_HCC083", "HHS_HCC084"],
        "G10": ["HHS_HCC106", "HHS_HCC107"],
        "G11": ["HHS_HCC108", "HHS_HCC109"],
        "G12": ["HHS_HCC117", "HHS_HCC119"],
        "G13": ["HHS_HCC126", "HHS_HCC127"],
        "G14": ["HHS_HCC128", "HHS_HCC129"],
        "G16": ["HHS_HCC187", "HHS_HCC188"],
        "G17A": ["HHS_HCC204", "HHS_HCC205"],
        "G18A": ["HHS_HCC207", "HHS_HCC208"],
        "G19B": ["HHS_HCC210", "HHS_HCC211"],
        "G22": ["HHS_HCC234", "HHS_HCC254"],
        "G23": ["HHS_HCC131", "HHS_HCC132"]
    }

    # Apply Group Child Variable Mappings

    for group, conditions in gvars.items():
        if any(x[condition] > 0 for condition in conditions):
            x[group] = 1
            for condition in conditions:
                x[condition] = 0

    # Calculate HCC_CNT (excluding HCC022)
    hcc_cnt = sum(1 for k, v in x.items() if k.startswith("HHS_HCC") and v > 0 and k != "HHS_HCC022")

    # Severe illness interactions
    severe = any(x[hcc] > 0 for hcc in severe_lst)
    if severe:
        for i in range(1, 9):
            if i in (6,7):
                x[f"SEVERE_HCC_COUNT6_7"] = 1 if hcc_cnt in (6,7) else 0
            elif i == 8:
                x[f"SEVERE_HCC_COUNT8PLUS"] = 1 if hcc_cnt >= 8 else 0
            else:
                x[f"SEVERE_HCC_COUNT{i}"] = 1 if hcc_cnt == i else 0

    # Transplant interactions
    transplant = any(x[hcc] > 0 for hcc in transplant_lst)
    if transplant:
        x[f"TRANSPLANT_HCC_COUNT4PLUS"] = 1 if hcc_cnt >= 4 else 0

    # No Enrolment Duration Flags and RXC Interactions for Child

    # Final list of HCCs
    cc_lst = [k for k, v in x.items() if v > 0]

    return cc_lst

def _infant(cc_lst, age):

    x = Counter(cc_lst)
    z = Counter()

    # Mandatory HCC assignments for infants
    # Removed in this version, present in V0519F3M

    severity = {
        5: ["HHS_HCC008", "HHS_HCC018","HHS_HCC034", "HHS_HCC041","HHS_HCC042","HHS_HCC125","HHS_HCC128",
            "HHS_HCC129","HHS_HCC130","HHS_HCC137","HHS_HCC158", "HHS_HCC183","HHS_HCC184","HHS_HCC251"],
        4: ["HHS_HCC002", "HHS_HCC009", "HHS_HCC026", "HHS_HCC030", "HHS_HCC035_1", "HHS_HCC035_2","HHS_HCC064",
            "HHS_HCC067","HHS_HCC068","HHS_HCC073","HHS_HCC106","HHS_HCC107","HHS_HCC111", "HHS_HCC112","HHS_HCC115",
            "HHS_HCC122","HHS_HCC126","HHS_HCC127","HHS_HCC131","HHS_HCC135","HHS_HCC138","HHS_HCC145","HHS_HCC146",
            "HHS_HCC154","HHS_HCC156","HHS_HCC163","HHS_HCC187","HHS_HCC253"],
        3: ["HHS_HCC001","HHS_HCC003","HHS_HCC006","HHS_HCC010","HHS_HCC011","HHS_HCC012","HHS_HCC027", "HHS_HCC045",
            "HHS_HCC054", "HHS_HCC055", "HHS_HCC061","HHS_HCC063", "HHS_HCC066", "HHS_HCC074", "HHS_HCC075",
            "HHS_HCC081", "HHS_HCC082", "HHS_HCC083", "HHS_HCC084","HHS_HCC096","HHS_HCC108", "HHS_HCC109",
            "HHS_HCC110", "HHS_HCC113", "HHS_HCC114", "HHS_HCC117", "HHS_HCC119", "HHS_HCC121", "HHS_HCC132",
            "HHS_HCC139", "HHS_HCC142", "HHS_HCC149", "HHS_HCC150", "HHS_HCC159", "HHS_HCC218", "HHS_HCC223",
            "HHS_HCC226", "HHS_HCC228"],
        2: ["HHS_HCC004", "HHS_HCC013", "HHS_HCC019", "HHS_HCC020", "HHS_HCC021", "HHS_HCC023", "HHS_HCC028",
            "HHS_HCC029", "HHS_HCC036", "HHS_HCC046", "HHS_HCC047", "HHS_HCC048", "HHS_HCC056", "HHS_HCC057",
            "HHS_HCC062", "HHS_HCC069", "HHS_HCC070", "HHS_HCC097", "HHS_HCC120", "HHS_HCC151", "HHS_HCC153",
            "HHS_HCC160", "HHS_HCC161_1", "HHS_HCC162", "HHS_HCC188", "HHS_HCC217", "HHS_HCC219"],
        1: ["HHS_HCC037_1", "HHS_HCC037_2", "HHS_HCC071", "HHS_HCC102", "HHS_HCC103", "HHS_HCC118", "HHS_HCC161_2",
            "HHS_HCC234", "HHS_HCC254"]
    }

    for level, hccs in severity.items():
        if any(x[hcc] for hcc in hccs):
            z[f'IHCC_Severity{level}'] = 1
            break
    else:
        z['IHCC_Severity1'] = 1

    # Maturity Levels
    if age ==1:
        z["IHCC_Age1"] = 1
    else:
        if x["HHS_HCC242"] > 0 or x["HHS_HCC243"] > 0 or  x["HHS_HCC244"] >0:
            z["IHCC_Extremely_Immature"] = 1
        elif x["HHS_HCC245"] > 0 or x["HHS_HCC246"] > 0:
            z["IHCC_Immature"] = 1
        elif x["HHS_HCC247"] > 0 or x["HHS_HCC248"] > 0:
            z["IHCC_Premature_Multiples"] = 1
        elif x["HHS_HCC249"] >0:
            z["IHCC_Term"] = 1
        else:
            z['IHCC_Term'] = 1

    # Impose hierachy
    if z["IHCC_Extremely_Immature"]:
        z['IHCC_Immature'] = z['IHCC_Premature_Multiples'] = z['IHCC_Term'] = z['IHCC_Age1'] = 0
    elif z['IHCC_Immature']:
        z['IHCC_Premature_Multiples'] = z['IHCC_Term'] = z['IHCC_Age1'] = 0
    elif z['IHCC_Premature_Multiples']:
        z['IHCC_Term'] = z['IHCC_Age1'] = 0
    elif z['IHCC_Term']:
        z['IHCC_Term'] = 1

    # Severity and maturity interactions
    for sev in range(1,6):
        for mat in ["Extremely_Immature", "Immature", "Premature_Multiples", "Term", "Age1"]    :
            if z[f'IHCC_Severity{sev}'] and z[f'IHCC_{mat}']:
                z[f'{mat}_x_SEVERITY{sev}'] = 1

    # Final list of HCCs
    cc_lst = [k for k, v in x.items() if v > 0] + [k.upper() for k, v in z.items() if v > 0]
   
    return cc_lst


def create_interactions(cc_lst, agegroup, age):
    
    cc_lst = cc_lst
    if agegroup == "Adult":
        cc_lst = _adult(cc_lst)
    elif agegroup == "Child":
        cc_lst = _child(cc_lst)
    elif agegroup == "Infant":
        cc_lst = _infant(cc_lst, age)

    return cc_lst


