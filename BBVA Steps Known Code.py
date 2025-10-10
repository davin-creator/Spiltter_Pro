import pandas as pd
import numpy as np


bbva = pd.read_csv(input("paste path of Data"), header=0)

bbva.fillna(0,inplace=True)

bbva["Event_unique_users_afiliacion_basica-app_page_visit"] = (
    bbva["Event_unique_users_afiliacion_basica-app_page_visit"]
    .astype(str)
    .str.replace(",", "")               # remove commas like 3,250
    .str.strip()                        # remove spaces
)

bbva["Event_unique_users_afiliacion_basica-app_step_2"] = (
    bbva["Event_unique_users_afiliacion_basica-app_step_2"]
    .astype(str)
    .str.replace(",", "")               # remove commas like 3,250
    .str.strip()                        # remove spaces
)

bbva["Event_unique_users_afiliacion_basica-app_step_3"] = (
    bbva["Event_unique_users_afiliacion_basica-app_step_3"]
    .astype(str)
    .str.replace(",", "")               # remove commas like 3,250
    .str.strip()                        # remove spaces
)

bbva["Event_unique_users_afiliacion_basica-app_step_4"] = (
    bbva["Event_unique_users_afiliacion_basica-app_step_4"]
    .astype(str)
    .str.replace(",", "")               # remove commas like 3,250
    .str.strip()                        # remove spaces
)

bbva["Event_unique_users_afiliacion_basica-app_step_5"] = (
    bbva["Event_unique_users_afiliacion_basica-app_step_5"]
    .astype(str)
    .str.replace(",", "")               # remove commas like 3,250
    .str.strip()                        # remove spaces
)

bbva["Event_unique_users_afiliacion_basica-app_step_6"] = (
    bbva["Event_unique_users_afiliacion_basica-app_step_6"]
    .astype(str)
    .str.replace(",", "")               # remove commas like 3,250
    .str.strip()                        # remove spaces
)

bbva["Event_unique_users_afiliacion_basica-app_step_7"] = (
    bbva["Event_unique_users_afiliacion_basica-app_step_7"]
    .astype(str)
    .str.replace(",", "")               # remove commas like 3,250
    .str.strip()                        # remove spaces
)

bbva["Event_unique_users_afiliacion_basica-app_online_purchases"] = (
    bbva["Event_unique_users_afiliacion_basica-app_online_purchases"]
    .astype(str)
    .str.replace(",", "")               # remove commas like 3,250
    .str.strip()                        # remove spaces
)


#Change Data types from object to float
bbva["Event_unique_users_afiliacion_basica-app_page_visit"] = bbva["Event_unique_users_afiliacion_basica-app_page_visit"].astype(float)
bbva['Event_unique_users_afiliacion_basica-app_step_2'] = bbva['Event_unique_users_afiliacion_basica-app_step_2'].astype(float)
bbva['Event_unique_users_afiliacion_basica-app_step_3'] = bbva['Event_unique_users_afiliacion_basica-app_step_3'].astype(float)
bbva['Event_unique_users_afiliacion_basica-app_step_4'] = bbva['Event_unique_users_afiliacion_basica-app_step_4'].astype(float)
bbva['Event_unique_users_afiliacion_basica-app_step_5'] = bbva['Event_unique_users_afiliacion_basica-app_step_5'].astype(float)
bbva['Event_unique_users_afiliacion_basica-app_step_7'] = bbva['Event_unique_users_afiliacion_basica-app_step_7'].astype(float)
bbva['Event_unique_users_afiliacion_basica-app_step_6'] = bbva['Event_unique_users_afiliacion_basica-app_step_6'].astype(float)
bbva['Event_unique_users_afiliacion_basica-app_online_purchases'] = bbva['Event_unique_users_afiliacion_basica-app_online_purchases'].astype(float)

#Step to Comparison each step
bbva['Step2-Step1'] = bbva["Event_unique_users_afiliacion_basica-app_step_2"] <= bbva["Event_unique_users_afiliacion_basica-app_page_visit"]
bbva['step3-step2'] = bbva["Event_unique_users_afiliacion_basica-app_step_3"] <= bbva["Event_unique_users_afiliacion_basica-app_step_2"]
bbva['step4-step3'] = bbva["Event_unique_users_afiliacion_basica-app_step_4"] <= bbva["Event_unique_users_afiliacion_basica-app_step_3"]
bbva['step5-step4'] = bbva["Event_unique_users_afiliacion_basica-app_step_5"] <= bbva["Event_unique_users_afiliacion_basica-app_step_4"]
bbva['step6-step5'] = bbva["Event_unique_users_afiliacion_basica-app_step_6"] <= bbva["Event_unique_users_afiliacion_basica-app_step_5"]
bbva['step7-step6'] = bbva["Event_unique_users_afiliacion_basica-app_online_purchases"] <= bbva["Event_unique_users_afiliacion_basica-app_step_6"]

bbva_filter = bbva[['Media_source', 'Step2-Step1','step3-step2','step4-step3','step5-step4','step6-step5','step7-step6']]

bbva_mixed_Data = bbva[['Media_source', 'Event_unique_users_afiliacion_basica-app_page_visit','Event_unique_users_afiliacion_basica-app_step_2','Step2-Step1','Event_unique_users_afiliacion_basica-app_step_3','step3-step2','Event_unique_users_afiliacion_basica-app_step_4','step4-step3','Event_unique_users_afiliacion_basica-app_step_5','step5-step4','Event_unique_users_afiliacion_basica-app_step_6','step6-step5','Event_unique_users_afiliacion_basica-app_online_purchases','step7-step6']]

bbva_mixed_Data.to_csv("BBVA_True_False_Data.csv",index=False)

# Step columns (the boolean ones)
step_cols = ['Step2-Step1','step3-step2','step4-step3','step5-step4','step6-step5','step7-step6']
num_cols = bbva_mixed_Data[['Media_source','Event_unique_users_afiliacion_basica-app_page_visit','Event_unique_users_afiliacion_basica-app_step_2','Event_unique_users_afiliacion_basica-app_step_3','Event_unique_users_afiliacion_basica-app_step_4','Event_unique_users_afiliacion_basica-app_step_5','Event_unique_users_afiliacion_basica-app_step_6','Event_unique_users_afiliacion_basica-app_online_purchases']]

# Filter rows where at least one step is False
df_any_false = bbva_mixed_Data[(bbva_mixed_Data[step_cols] == False).any(axis=1)]

# Keep only Media_source and step columns (optional)
df_any_false = df_any_false[['Media_source'] + step_cols]

merge_data = pd.merge(df_any_false, num_cols, on='Media_source', how='inner')

merge_data = merge_data[['Media_source', 'Event_unique_users_afiliacion_basica-app_page_visit','Event_unique_users_afiliacion_basica-app_step_2','Step2-Step1','Event_unique_users_afiliacion_basica-app_step_3','step3-step2','Event_unique_users_afiliacion_basica-app_step_4','step4-step3','Event_unique_users_afiliacion_basica-app_step_5','step5-step4','Event_unique_users_afiliacion_basica-app_step_6','step6-step5','Event_unique_users_afiliacion_basica-app_online_purchases','step7-step6']]

# Save result to a new CSV
merge_data.to_csv("BBVA_False_Data.csv", index=False)




