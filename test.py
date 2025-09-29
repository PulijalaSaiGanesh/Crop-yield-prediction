# Import pandas for data handling: used to read and manipulate the dataset
import pandas as pd

# Load the dataset from Excel file: reads the synthetic crop yield data into a DataFrame
# This could also be pd.read_csv("file.csv") if it were a CSV, but here it's Excel
df = pd.read_excel("crop_yield.csv.xlsx")   # or pd.read_csv("file.csv")

# Print the first 5 rows of the DataFrame: displays a preview of the data to verify loading
# Helps confirm the structure and values in the dataset
print(df.head())

# Extract features (X) and target (y): X are the input variables, y is the output to predict
# Features: Area, Annual_Rainfall, Fertilizer, Pesticide; Target: Yield
X = df[["Area", "Annual_Rainfall", "Fertilizer", "Pesticide"]]
y = df["Yield"]

# Import train_test_split from sklearn: function to split data into training and testing sets
from sklearn.model_selection import train_test_split

# Split the data: 80% for training the model, 20% for testing its performance
# random_state=42 ensures the split is reproducible
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Import RandomForestRegressor: the machine learning model for regression tasks
from sklearn.ensemble import RandomForestRegressor

# Create and train the Random Forest model: initializes with 100 trees, fits on training data
# The model learns patterns from X_train to predict y_train
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Import metrics for evaluation: mean_squared_error (MSE) and r2_score for model performance
from sklearn.metrics import mean_squared_error, r2_score

# Make predictions on the test set: uses the trained model to predict yields for unseen data
y_pred = model.predict(X_test)

# Print Mean Squared Error: measures average squared difference between predicted and actual values
# Lower MSE indicates better fit
print("MSE:", mean_squared_error(y_test, y_pred))

# Print R2 Score: measures proportion of variance explained by the model (0 to 1, higher is better)
# 1.0 means perfect predictions
print("R2 Score:", r2_score(y_test, y_pred))

# Display predicted yields for the first 10 test samples: compares actual vs predicted for inspection
# Loops through up to 10 samples, printing formatted values
print("\nPredicted Yields for first 10 test samples:")
for i in range(min(10, len(y_pred))):
    print(f"Sample {i+1}: Actual Yield = {y_test.iloc[i]:.4f}, Predicted Yield = {y_pred[i]:.4f}")
