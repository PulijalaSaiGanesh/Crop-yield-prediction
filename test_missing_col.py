# Import requests library: used for making HTTP requests to test the Flask API endpoints
import requests

# Define the URL of the prediction endpoint: the local Flask server running on port 5000
url = 'http://localhost:5000/predict'

# Open the test file in binary mode: 'sample_missing_col.xlsx' is an Excel file with missing required columns
# This simulates a user uploading a file with incomplete data
with open('sample_missing_col.xlsx', 'rb') as f:
    # Prepare the files dictionary for the POST request: 'file' is the form field name
    # Specify filename and MIME type for proper handling by the server
    files = {'file': ('sample_missing_col.xlsx', f, 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')}

    # Send a POST request to the predict endpoint: uploads the file and expects a response
    # The server should detect missing columns and return an error
    response = requests.post(url, files=files)

# Print the HTTP status code: e.g., 400 for bad request if columns are missing
print("Status Code:", response.status_code)

# Print the response text: displays the server's message, like error details
print("Response Text:")
print(response.text)
