
def apply_agesex_edits(cc_dct, age, sex):
    
    # age/sex edits. see "I0V05ED2.TXT"
    elst0 = ["C9100","C9101","C9102",
              "C9500","C9501","C9502",
              "C7400","C7401","C7402","C7410","C7411","C7412",
              "C7490","C7491","C7492"]
    elst1 = ["J410","J411","J418","J42","J440","J441","J4481","J4489"]
    elst2 = ["K55011","K55012","K55019","K55021","K55022",
              "K55029","K55031","K55032","K55039","K55041","K55042",
              "K55049","K55051","K55052","K55059","K55061","K55062",
              "K55069","K5530", "K5531", "K5532", "K5533"]
    elst3 = ["C50011","C50012","C50019","C50021","C50022","C50029",
              "C50111","C50112","C50119","C50121","C50122","C50129",
              "C50211","C50212","C50219","C50221","C50222","C50229",
              "C50311","C50312","C50319","C50321","C50322","C50329",
              "C50411","C50412","C50419","C50421","C50422","C50429",
              "C50511","C50512","C50519","C50521","C50522","C50529",
              "C50611","C50612","C50619","C50621","C50622","C50629",
              "C50811","C50812","C50819","C50821","C50822","C50829",
              "C50911","C50912","C50919","C50921","C50922","C50929"]
    elst4 = ["J430","J431","J432","J438","J439","J449","J982",
                "J983"]
    elst5 = ["P0500","P0501","P0502","P0503","P0504","P0505",
              "P0506","P0507","P0508","P0509","P0510","P0511",
              "P0512","P0513","P0514","P0515","P0516","P0517",
              "P0518","P0519","P052", "P059", "P0700","P0701",
              "P0702","P0703","P0710","P0714","P0715","P0716",
              "P0717","P0718","P0720","P0721","P0722","P0723",
              "P0724","P0725","P0726","P0730","P0731","P0732",
              "P0733","P0734","P0735","P0736","P0737","P0738",
              "P0739","P080", "P081", "P0821","P0822" ]
    elst6 = ["Q894"]
    elst7 = ["K551","K558","K559",
              "P041", "P0411","P0412","P0413","P0414","P0415",
              "P0416","P0417","P0418","P0419","P041A",
              "P042", "P043", "P0440","P0441","P0442","P0449",
              "P045", "P046", "P048", "P0481","P0489",
              "P049", "P930", "P938", "P961", "P962",
              "Q390", "Q391", "Q392", "Q393", "Q394", "Q6410",
              "Q6411","Q6412","Q6419","Q790", "Q791", "Q792",
              "Q793", "Q794", "Q7951"]
    elst8 = ["P270","P271","P278","P279"]
    elst9 = ["F3481"]
    elst10 = ["D66","D67"]

    if age < 18:
        # Split acute lymphoid and other acute leukemias
        # except  myeloid diagnoses to age 18+ (HCC 8)and age <18 (HCC 9)
        # Split adrenal gland cancer diagnoses to age 18+ (HCC 10) and age <18 (HCC 9).
        for dx in (dx for dx in elst0 if dx in cc_dct):
            cc_dct[dx] = "HHS_HCC009"
        # Split chronic bronchitis diagnoses to age 18+ (HCC 160) and age <18 (HCC 161).
        for dx in (dx for dx in elst1 if dx in cc_dct):
            cc_dct[dx] = "HHS_HCC161_1"
          
    if age < 2:
        # Split acute vascular insufficiency of intestine diagnosis to age 2+ (HCC 154) and age <2 (HCC 42).
        for dx in (dx for dx in elst2 if dx in cc_dct):
            cc_dct[dx] = "HHS_HCC042"
        # Split emphysema diagnoses, if age <2 out of payment model.
        for dx in (dx for dx in elst4 if dx in cc_dct):
            cc_dct[dx] = "HHS_HCC_NA"
    if age < 50:
        # Split breast cancer diagnoses to age 50+ (HCC 12) and age <50 (HCC 11).
        for dx in (dx for dx in elst3 if dx in cc_dct):
            cc_dct[dx] = "HHS_HCC011"
    if age > 1:
        # Edit for newborn low birthweight. If age 1+ out of payment model.
        for dx in (dx for dx in elst5 if dx in cc_dct):
            cc_dct[dx] = "HHS_HCC_NA"
    if age >= 1:
        # Split conjoined twins diagnoses to age 1+ (HCC 97)and age <1 (HCC 247).
        for dx in (dx for dx in elst6 if dx in cc_dct):
            cc_dct[dx] = "HHS_HCC097"
    if age >= 2:
        # If age 2+ out of payment model.
        for dx in (dx for dx in elst7 if dx in cc_dct):
            cc_dct[dx] = "HHS_HCC_NA"
        # Split chronic respiratory disease arising in the perinatal period 
        # diagnoses to age 2+ (HCC 162) and age <2 (HCC 127).
        for dx in (dx for dx in elst8 if dx in cc_dct):
            cc_dct[dx] = "HHS_HCC162"
    if age < 6 or age > 18:
        # Edit for targeted age of diagnosis. If age <6 or age >18 out of payment model.
        for dx in (dx for dx in elst9 if dx in cc_dct):
            cc_dct[dx] = "HHS_HCC_NA"
    if sex == "F":
        # Split hemophilia diagnoses to male (HCC 66) and female (HCC 75).
        for dx in (dx for dx in elst10 if dx in cc_dct):
            cc_dct[dx] = "HHS_HCC075"

    cc_dct = {dx:cc for dx, cc in cc_dct.items() if cc != "HHS_HCC_NA"}

    return cc_dct

