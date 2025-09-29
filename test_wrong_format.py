# Import requests library: used for making HTTP requests to test the Flask API endpoints
import requests

# Define the URL of the prediction endpoint: the local Flask server running on port 5000
url = 'http://localhost:5000/predict'

# Open the test file in binary mode: 'sample_wrong_format.csv' is a CSV file, not Excel
# This tests file format validation; the server only accepts .xlsx
with open('sample_wrong_format.csv', 'rb') as f:
    # Prepare the files dictionary: specify filename and MIME type as 'text/csv'
    # This simulates uploading a non-Excel file
    files = {'file': ('sample_wrong_format.csv', f, 'text/csv')}

    # Send a POST request: the server should reject non-.xlsx files
    response = requests.post(url, files=files)

# Print the HTTP status code: should be 400 for invalid format
print("Status Code:", response.status_code)

# Print the response text: displays the error message about file type
print("Response Text:")
print(response.text)
