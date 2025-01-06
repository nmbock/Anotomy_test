import pandas as pd

# Load the dataset
file_path = r"C:\Users\nathan\Documents\Padova_Lessons\Privacy Preserving Information Access\Final Presentation\archive\Sleep_health_and_lifestyle_dataset.csv"
data = pd.read_csv(file_path)

# Fix missing values in the sensitive attribute
sensitive_attribute = 'Sleep Disorder'
data[sensitive_attribute] = data[sensitive_attribute].fillna('None')

# Define quasi-identifiers
quasi_identifiers = ['Age', 'Gender', 'Occupation']

# Anatomy Function
def anatomy_anonymization(dataset, quasi_identifiers, sensitive_attribute):
    """
    Applies Anatomy anonymization to the dataset.
    Separates quasi-identifiers and sensitive attributes into two tables.
    """
    print("\nStarting Anatomy Anonymization...")

    groups = dataset.groupby(quasi_identifiers)
    qit = []  # Quasi-Identifier Table
    st = []   # Sensitive Table
    group_id = 0

    for _, group in groups:
        group_id += 1
        for _, row in group.iterrows():
            qit.append({'Group ID': group_id, **row[quasi_identifiers].to_dict()})
        
        sensitive_counts = group[sensitive_attribute].value_counts()
        for sensitive_value, count in sensitive_counts.items():
            st.append({'Group ID': group_id, sensitive_attribute: sensitive_value, 'Count': count})

    print("Anatomy completed.")
    return pd.DataFrame(qit), pd.DataFrame(st)

# Apply Anatomy
qit, st = anatomy_anonymization(data, quasi_identifiers, sensitive_attribute)

# Display Results
print("\nSample Quasi-Identifier Table (QIT):")
print(qit.head())

print("\nSample Sensitive Table (ST):")
print(st.head())

# Updated Function to Include Sensitive Condition
def query_using_anatomy(qit, st, age_condition, occupation_condition, sensitive_condition):
    """
    Executes a query using QIT and ST with age, occupation, and sensitive conditions.
    Returns the count of matching records based on the conditions.
    """
    print("\nExecuting query using Anatomy...")

    # Step 1: Filter QIT for the age and occupation conditions
    filtered_qit = qit[qit['Age'].apply(age_condition) & (qit['Occupation'] == occupation_condition)]

    # Step 2: Get relevant Group IDs from filtered QIT
    relevant_groups = filtered_qit['Group ID'].unique()

    # Step 3: Filter ST for the relevant groups and sensitive condition
    filtered_st = st[(st['Group ID'].isin(relevant_groups)) & st[sensitive_attribute].apply(sensitive_condition)]

    print("\nFiltered ST rows:")
    print(filtered_st)  # Display matching rows in ST

    # Step 4: Sum up the counts for the sensitive values
    count = filtered_st['Count'].sum()

    print(f"\nQuery result (Anatomy): {count} matching records found.")
    return count

# Define conditions for the query
age_condition = lambda age: 25 <= age <= 45
occupation_condition = "Nurse"
sensitive_condition = lambda disorder: disorder == "None"

# Execute query with age, occupation, and sensitive conditions
anatomy_result = query_using_anatomy(qit, st, age_condition, occupation_condition, sensitive_condition)

# Compare with original data
original_result = data[
    (data['Age'].apply(age_condition)) & 
    (data['Occupation'] == occupation_condition) & 
    (data[sensitive_attribute].apply(sensitive_condition))
]
print(f"\nQuery result from the original dataset:\n{original_result}")
print(f"original result: {len(original_result)} matching records found.")
