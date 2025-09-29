# Import pandas for data manipulation and reading Excel files
import pandas as pd

# Load the user's own Excel dataset: reads the data from Total_cropyield.xlsx into a pandas DataFrame
# This assumes the file contains the necessary columns for training (Area, Annual_Rainfall, Fertilizer, Pesticide, Yield)
df = pd.read_excel("Total_cropyield.xlsx")

# Save the loaded DataFrame to the expected training data file: exports the user's dataset for use in the main application
# index=False prevents adding an extra index column to the file, keeping it clean
# The app.py loads from "crop_yield.csv.xlsx", so we save it with this name
df.to_excel("crop_yield.csv.xlsx", index=False)

# Print a confirmation message to the console: informs the user that the dataset has been successfully loaded and saved
# This is useful for debugging and verifying script execution
print("Dataset loaded from Total_cropyield.xlsx and saved as crop_yield.csv.xlsx")
