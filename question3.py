import pandas as pd
# Load the sample diagnosis data into a pandas DataFrame
diagnosis_data = pd.read_csv("sample_dx.csv")
# Define the 3 groups of interested diagnosis codes
group_A = ["C83.0", "C83.00", "C83.01", "C83.02", "C83.03"]
group_B = ["C91", "C91.1", "C91.10", "C91.11", "C91.12"]
group_C = ["C95.10", "C95.90"]

# Create a new column indicating which group the diagnosis code belongs to
diagnosis_data["group"] = "None"
diagnosis_data.loc[diagnosis_data["claim_code"].isin(group_A), "group"] = "A"
diagnosis_data.loc[diagnosis_data["claim_code"].isin(group_B), "group"] = "B"
diagnosis_data.loc[diagnosis_data["claim_code"].isin(group_C), "group"] = "C"
diagnosis_data['service_date'] = pd.to_datetime(diagnosis_data['service_date'])
diagnosis_data['Month'] = diagnosis_data['service_date'].dt.month
# Group the data by patient ID and month
grouped = diagnosis_data.groupby(["patient_id", "Month"])
# Count the number of patient-month groups that have diagnosis codes from two different groups
patients_collection = set()
count = 0
for name, group in grouped:
    groups = set(group['group'])
    if 'None' in groups:
        groups.remove('None')
    if len(groups) > 1:
        # patients get two different groups of diagnosis within different months (count multiple times)
        count+=1
        # patients get two different groups of diagnosis within one month (one patient only count once)
        patients_collection.add(name[0])

print(f"Number of patients with diagnosis codes from two different groups within the same month(count multiple times):{count}")
print(f"Number of patients with diagnosis codes from two different groups within the same month(one patient only count once): {len(patients_collection)}")
# Number of patients with diagnosis codes from two different groups within the same month(count multiple times):89
# Number of patients with diagnosis codes from two different groups within the same month(one patient only count once): 78