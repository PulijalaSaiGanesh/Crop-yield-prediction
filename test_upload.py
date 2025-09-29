# Import requests library: used for making HTTP requests to test the Flask API endpoints
import requests

# Define the URL of the prediction endpoint: the local Flask server running on port 5000
url = 'http://localhost:5000/predict'

# Prepare the files dictionary: open 'sample.xlsx' in binary mode and assign to 'file' field
# 'sample.xlsx' is a valid Excel file with all required columns, including Yield for error calc
files = {'file': open('sample.xlsx', 'rb')}

# Send a POST request to the predict endpoint: uploads the file and expects successful prediction
# Server should process, predict, and return HTML results
response = requests.post(url, files=files)

# Print the HTTP status code: should be 200 for success
print("Status Code:", response.status_code)

# Print the response text: displays the full HTML page with predictions and tables
print("Response Text:")
print(response.text)
