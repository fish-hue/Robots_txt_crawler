import requests
from urllib.parse import urljoin
import re
from datetime import datetime
import logging

# Set up logging
logging.basicConfig(
    filename='robots_sitemap_log.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Global User-Agent Header
USER_AGENT_HEADER = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

def is_valid_url(url: str) -> bool:
    """
    Validates the URL format.
    
    Parameters:
    - url: The URL string to validate.

    Returns:
    - True if the URL format is valid, False otherwise.
    """
    url_pattern = re.compile(r'^(http|https)://[a-zA-Z0-9.-]+(?:\.[a-zA-Z]{2,})+')
    return bool(url_pattern.match(url))


def fetch_robots_txt(url: str):
    """
    Fetches the robots.txt file from the specified URL.
    
    Parameters:
    - url: The base URL of the website.
    """
    if not url.endswith('/'):
        url += '/'
    
    robots_url = url + 'robots.txt'
    try:
        logging.debug(f"Fetching {robots_url}...")

        response = requests.get(robots_url, headers=USER_AGENT_HEADER)
        logging.debug(f"HTTP Status Code: {response.status_code}")

        if response.status_code == 200:
            logging.info("robots.txt content retrieved successfully.")
            print("robots.txt content:")
            print(response.text)

            # Save the robots.txt to a file with a timestamp
            save_robots_txt(response.text)

            # Analyze robots.txt content
            analyze_robots_txt(response.text)

        elif response.status_code == 404:
            logging.warning(f"robots.txt not found (404) at {robots_url}")
            print("robots.txt not found (404)")

        elif response.status_code == 403:
            logging.warning(f"Access forbidden (403) - unable to access robots.txt at {robots_url}")
            print("Access forbidden (403) - unable to access robots.txt")

        else:
            logging.error(f"Failed to fetch robots.txt: {response.status_code} - {response.reason}")
            print(f"Failed to fetch robots.txt: {response.status_code} - {response.reason}")

        # Print HTTP headers
        logging.debug("HTTP Headers:")
        headers = response.headers
        for key, value in headers.items():
            print(f"{key}: {value}")
            logging.debug(f"{key}: {value}")

    except requests.exceptions.RequestException as e:
        logging.error(f"An error occurred while fetching robots.txt: {e}")
        print(f"An error occurred while fetching robots.txt: {e}")

def analyze_robots_txt(content: str):
    """
    Analyzes the robots.txt content to extract User-agent and Disallow paths.
    
    Parameters:
    - content: The content of the robots.txt.
    """
    user_agents = re.findall(r'User-agent: (.+)', content)
    disallowed_paths = [path.strip() for path in re.findall(r'Disallow: (.+)', content)]
    allowed_paths = [path.strip() for path in re.findall(r'Allow: (.+)', content)]
    crawl_delay = re.findall(r'Crawl-delay: (\d+)', content)
    sitemaps = re.findall(r'Sitemap: (.+)', content)

    print("\nAnalysis of robots.txt:")
    print(f"Found User-Agents: {', '.join(user_agents)}")
    print(f"Disallowed Paths: {', '.join(disallowed_paths)}")
    print(f"Allowed Paths: {', '.join(allowed_paths)}")
    print(f"Crawl-Delay: {', '.join(crawl_delay)}")
    print(f"Sitemaps: {', '.join(sitemaps)}")

    logging.info(f"Found User-Agents: {', '.join(user_agents)}")
    logging.info(f"Disallowed Paths: {', '.join(disallowed_paths)}")
    logging.info(f"Allowed Paths: {', '.join(allowed_paths)}")
    logging.info(f"Crawl-Delay: {', '.join(crawl_delay)}")
    logging.info(f"Sitemaps: {', '.join(sitemaps)}")

def fetch_sitemap(url: str):
    """
    Attempts to fetch the sitemap.xml from the provided URL.
    
    Parameters:
    - url: The base URL of the website.
    """
    sitemap_url = urljoin(url, 'sitemap.xml')
    try:
        logging.debug(f"Fetching {sitemap_url}...")

        response = requests.get(sitemap_url, headers=USER_AGENT_HEADER)

        if response.status_code == 200:
            logging.info("Sitemap found.")
            print("\nSitemap found:")
            print(response.text)
        elif response.status_code == 404:
            logging.warning(f"Sitemap not found (404) at {sitemap_url}")
            print("Sitemap not found (404)")
        else:
            logging.error(f"Failed to fetch sitemap: {response.status_code} - {response.reason}")
            print(f"Failed to fetch sitemap: {response.status_code} - {response.reason}")
    except requests.exceptions.RequestException as e:
        logging.error(f"An error occurred while fetching the sitemap: {e}")
        print(f"An error occurred while fetching the sitemap: {e}")

def save_robots_txt(content: str):
    """
    Saves the content of robots.txt with a timestamped filename.
    
    Parameters:
    - content: The content of robots.txt to save.
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"robots_{timestamp}.txt"
    
    with open(filename, 'w') as file:
        file.write(content)
    logging.info(f"Saved robots.txt to '{filename}'")
    print(f"Saved robots.txt to '{filename}'")

def main():
    while True:
        target_url = input("Enter the website URL (including http:// or https://): ")
        
        if is_valid_url(target_url):
            break
        else:
            print("Invalid URL format. Please include http:// or https:// and a valid domain.")
    
    fetch_robots_txt(target_url)
    
    # Fetch the sitemap after fetching robots.txt
    fetch_sitemap(target_url)

    print("\nProcess completed successfully.")

if __name__ == "__main__":
    main()
