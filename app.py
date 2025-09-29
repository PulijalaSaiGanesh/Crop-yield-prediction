# Import necessary libraries for the Flask web application and machine learning
# Flask: Framework for building web apps, provides request handling and template rendering
# pandas (pd): For data manipulation, reading Excel files, and handling DataFrames
# sklearn modules: For machine learning - RandomForestRegressor for ensemble predictions, train_test_split for data splitting
# webbrowser: To automatically open the app in a browser
# threading and time: For running the browser opener in a separate thread with a delay
from flask import Flask, request, render_template
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor

import webbrowser
import threading
import time

# Create a Flask application instance: this is the core of the web app, handling routes and requests
# __name__ tells Flask where to look for templates and static files
app = Flask(__name__)

# Load and prepare the training data: read the dataset from crop_yield.csv.xlsx
# This data is used to train the machine learning models
df = pd.read_excel("crop_yield.csv.xlsx")

# Encode categorical columns: convert categorical variables to numerical using one-hot encoding
# Categorical columns: Crop, Crop_Year, Season, State
categorical_cols = ['Crop', 'Crop_Year', 'Season', 'State']
df_encoded = pd.get_dummies(df, columns=categorical_cols, drop_first=True)

# Extract features (X) and target (y): features are all columns except Yield, target is Yield
X = df_encoded.drop('Yield', axis=1)
y = df_encoded['Yield']

# Split the data into training and testing sets: 80% for training, 20% for testing
# random_state=42 ensures consistent splits across runs for reproducibility
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the Random Forest Regressor model: an ensemble method that builds multiple decision trees
# n_estimators=100 means 100 trees; random_state for consistency
# This model is trained on the training data to learn patterns for yield prediction
model_rf = RandomForestRegressor(n_estimators=100, random_state=42)
model_rf.fit(X_train, y_train)

# Train the XGBoost Regressor model: extreme gradient boosting for improved predictions
# n_estimators=100 means 100 boosting rounds; random_state for consistency
model_xgb = XGBRegressor(n_estimators=100, random_state=42)
model_xgb.fit(X_train, y_train)

# Get feature importance from the trained Random Forest: measures how much each feature contributes to predictions
# This helps understand which variables are most influential
feature_importances_rf = model_rf.feature_importances_
feature_names = list(X.columns)
feature_data_rf = list(zip(feature_names, feature_importances_rf))

# Get feature importance from the trained XGBoost
feature_importances_xgb = model_xgb.feature_importances_
feature_data_xgb = list(zip(feature_names, feature_importances_xgb))

# Define the root route ('/'): handles GET requests to display the upload form
# Renders the index.html template, which contains the file upload interface
@app.route('/')
def index():
    return render_template('index.html')

# Define the predict route ('/predict'): handles POST requests for file uploads and predictions
# This is the main endpoint where users upload data and get yield predictions
@app.route('/predict', methods=['POST'])
def predict():
    # Check if a file was uploaded in the request: 'file' is the form field name from index.html
    # If no file key, return an error message with HTTP 400 (Bad Request)
    if 'file' not in request.files:
        return "No file uploaded", 400

    # Retrieve the uploaded file from the request
    file = request.files['file']

    # Check if the file has a filename: ensures something was selected, not an empty upload
    # If empty, return error
    if file.filename == '':
        return "No file selected", 400

    # Validate file format: only .xlsx files are accepted for Excel compatibility
    # If not .xlsx, return error message
    if not file.filename.endswith('.xlsx'):
        return "Please upload an Excel (.xlsx) file", 400

    # Try to process the uploaded file: wrap in try-except to catch any reading or processing errors
    try:
        # Read the uploaded Excel file into a pandas DataFrame: assumes tabular data with headers
        df_upload = pd.read_excel(file)

        # Define required columns: the features needed for prediction (same as training data)
        required_cols = ['Crop', 'Crop_Year', 'Season', 'State', 'Area', 'Production', 'Annual_Rainfall', 'Fertilizer', 'Pesticide']

        # Check for missing columns: list comprehension to find any required cols not in the upload
        missing_cols = [col for col in required_cols if col not in df_upload.columns]

        # If any columns are missing, return an error listing them
        if missing_cols:
            return f"Missing required columns: {', '.join(missing_cols)}", 400

        # Encode categorical columns in the uploaded data: use the same encoding as training data
        df_upload_encoded = pd.get_dummies(df_upload, columns=categorical_cols, drop_first=True)

        # Align columns with training data: ensure the same columns, fill missing with 0
        X_new = df_upload_encoded.reindex(columns=X.columns, fill_value=0)

        # Make predictions using the trained Random Forest model: outputs predicted yields
        pred_rf = model_rf.predict(X_new)

        # Make predictions using the trained XGBoost model
        pred_xgb = model_xgb.predict(X_new)

        # Check if actual yields are provided: if 'Yield' column exists, use it for error calculation
        # Convert to list for easy handling in template
        actual = df_upload['Yield'].tolist() if 'Yield' in df_upload.columns else None

        # Prepare input data for display: select original columns for table
        display_cols = ['Crop', 'Crop_Year', 'Season', 'State', 'Area', 'Production', 'Annual_Rainfall', 'Fertilizer', 'Pesticide']
        input_data = df_upload[display_cols].to_dict('records')

        # Initialize error variables: will hold percentage errors if actual yields are available
        rf_errors = None
        xgb_errors = None

        # If actual yields are provided, calculate percentage errors for RF and XGBoost models
        # Error = ((predicted - actual) / actual) * 100; shows over/under estimation
        if actual is not None:
            rf_errors = [((pred - act) / act * 100) for pred, act in zip(pred_rf, actual)]
            xgb_errors = [((pred - act) / act * 100) for pred, act in zip(pred_xgb, actual)]

        # Render the results template: pass all data (predictions, inputs, errors, feature importance) to results.html
        # This displays the predictions in a table format
        return render_template('results.html', rf_preds=pred_rf, xgb_preds=pred_xgb, actual=actual, length=len(pred_rf), feature_data_rf=feature_data_rf, feature_data_xgb=feature_data_xgb, input_data=input_data, rf_errors=rf_errors, xgb_errors=xgb_errors)

    # Catch any exceptions during processing: return a generic error message with details
    except Exception as e:
        return f"Error processing file: {str(e)}", 500

# Run the app if this script is executed directly (not imported): standard Flask pattern
if __name__ == '__main__':
    # Define a function to open the browser: waits 1.5 seconds for server startup, then opens localhost:5000
    def open_browser():
        time.sleep(1.5)  # Wait for the server to start
        webbrowser.open_new('http://localhost:5000')

    # Start the browser opener in a separate thread: daemon=True means it exits when main thread does
    # This allows the app to run without blocking on browser open
    thread = threading.Thread(target=open_browser)
    thread.daemon = True
    thread.start()

    # Run the Flask app in debug mode: enables auto-reload on changes and detailed error pages
    app.run(debug=True)
