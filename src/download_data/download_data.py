import requests
from datetime import datetime
def download_zip(zip_url):
    # GitHub raw file URL of the ZIP file
    

    # Send a GET request to fetch the raw content of the ZIP file
    response = requests.get(zip_url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Save the content of the ZIP file to a local file
        current_date = datetime.now().strftime("%Y-%m-%d")
        with open(f'../../data/raw/redial_dataset_{current_date}.zip', 'wb') as f:
            f.write(response.content)
        print('ZIP file downloaded successfully.')
    else:
        print('Failed to fetch data from GitHub:', response.status_code)

if __name__ == "__main__":
    zip_url = 'https://github.com/ReDialData/website/raw/data/redial_dataset.zip'
    download_zip(zip_url)