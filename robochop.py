import requests

def fetch_robots_txt(url):
    if not url.endswith('/'):
        url += '/'
    
    robots_url = url + 'robots.txt'
    try:
        response = requests.get(robots_url)
        
        if response.status_code == 200:
            print("robots.txt content:")
            print(response.text)
        elif response.status_code == 404:
            print("robots.txt not found (404)")
        elif response.status_code == 403:
            print("Access forbidden (403) - unable to access robots.txt")
        else:
            print(f"Failed to fetch robots.txt: {response.status_code} - {response.reason}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

# Prompting user for the target URL
target_url = input("Enter the website URL (including http:// or https://): ")
fetch_robots_txt(target_url)
