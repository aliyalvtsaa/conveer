import pandas as pd
from sklearn.impute import KNNImputer
from flask import Flask, request, jsonify
import joblib

# Step 1: Train the imputer
df = pd.read_csv('/Users/aliyasta/Downloads/datasets.csv')  # Load your training data
df['REASON'] = df['REASON'].replace(['HomeImp', 'DebtCon'], [0, 1])
df['JOB'] = df['JOB'].replace(['Other', 'Sales', 'Office', 'Mgr', 'ProfExe', 'Self'], [0, 1, 2, 3, 4, 5])
target_column = 'BAD'

# Remove rows with missing values
df = df.dropna(subset=df.columns)

# Separate features and target variable
X_train = df.drop(target_column, axis=1)
y_train = df[target_column]

# Train the imputer
imputer = KNNImputer(n_neighbors=5)  # Example: using KNNImputer
imputer.fit(X_train)

# Step 2: Save the trained imputer
joblib.dump(imputer, '/Users/aliyasta/imputer_model.joblib')

# Step 3: Create an API
app = Flask(__name__)

# Step 4: Load the imputer in the API
imputer = joblib.load('/Users/aliyasta/imputer_model.joblib')

# Step 5: Accept input and perform imputation
@app.route('/impute', methods=['POST'])
def impute_missing_values():
    input_data = request.json  # Assumes JSON data with missing values
    
    # Convert input data to DataFrame
    df_input = pd.DataFrame(input_data)
    
    # Perform imputation
    imputed_data = pd.DataFrame(imputer.transform(df_input), columns=df_input.columns)
    
    # Step 6: Return the imputed data
    return jsonify(imputed_data.to_dict(orient='records'))

# Step 7: Deploy the API
if __name__ == '__main__':
    app.run()