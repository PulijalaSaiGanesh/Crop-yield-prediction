# Import requests library: used for making HTTP requests to test the Flask API endpoints
import requests

# Define the URL of the prediction endpoint: the local Flask server running on port 5000
url = 'http://localhost:5000/predict'

# Open the test file in binary mode: 'sample_no_yield.xlsx' is an Excel file without the 'Yield' column
# This tests prediction-only scenarios where actual yields aren't provided for error calculation
with open('sample_no_yield.xlsx', 'rb') as f:
    # Prepare the files dictionary: 'file' is the form field, using the file object directly
    # MIME type is inferred by requests, but this works for .xlsx
    files = {'file': f}

    # Send a POST request to the predict endpoint: uploads the file for prediction
    # Server should process and return predictions without errors
    response = requests.post(url, files=files)

# Print the HTTP status code: should be 200 if successful
print("Status Code:", response.status_code)

# Print the response text: displays the HTML results page or error message
print("Response Text:")
print(response.text)
