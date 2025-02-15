# Last Update: 15.02.25

import numpy as np
import pandas as pd
import json

file_path_to_data_folder = 'C:/Users/emred/OneDrive/Masaüstü/Docs/3rd Year/Spring/CENG404 - Special Topics in CENG/Repository/data'

ground_truth_df = pd.read_csv(file_path_to_data_folder + '/mimic-cxr-2.1.0-test-set-labeled.csv')

results_df = pd.read_json(file_path_to_data_folder + '/output.json')

results_df = results_df.drop_duplicates(subset = ['report_name'], keep = 'last')

ground_truth_ids = {id for id in ground_truth_df['study_id']}

results_ids = {int(id.replace("s", "")) for id in results_df['report_name']}

missing_ids = {id for id in ground_truth_ids if id not in results_ids}

with open (file_path_to_data_folder + '/relevant_reports.json', 'r') as file:
    data = json.load(file)

filtered_data = [entry for entry in data if int(entry['study_id'].replace("s", "")) in missing_ids]

output_file = file_path_to_data_folder + "/filtered_data.json"

with open(output_file, "w") as file:
    json.dump(filtered_data, file, indent = 4)

print(f'Filtered data is saved into {output_file}.')