import requests
from urllib.parse import urljoin, urlparse
import re
import time
from datetime import datetime
import json
import logging
import os
import random
from dataclasses import dataclass

# Set up logging
logging.basicConfig(
    filename='robots_sitemap_log.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Global User-Agent list
USER_AGENT_LIST = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    'Mozilla/5.0 (Linux; Android 5.0; Nexus 5 Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Mobile Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:55.0) Gecko/20100101 Firefox/55.0'
]

@dataclass
class RobotsAnalysis:
    user_agents: list
    disallowed_paths: list
    allowed_paths: list
    crawl_delay: list
    sitemaps: list

def is_valid_url(url: str) -> bool:
    """
    Validate URL format.
    """
    parsed_url = urlparse(url)
    return bool(parsed_url.scheme and parsed_url.netloc)

def is_server_reachable(url: str) -> bool:
    """
    Check if the server is reachable using HEAD or GET.
    """
    try:
        headers = {'User-Agent': random.choice(USER_AGENT_LIST)}
        response = requests.head(url, headers=headers, timeout=5)
        if response.status_code in [200, 301, 302]:
            return True
        # Fallback to GET if HEAD fails
        response = requests.get(url, headers=headers, timeout=5)
        return response.status_code in [200, 301, 302]
    except requests.exceptions.RequestException as e:
        logging.error(f"Server unreachable for {url}: {e}")
        return False

def create_target_directory(url: str) -> str:
    """
    Create a directory for the target URL.
    """
    dir_name = re.sub(r'[^a-zA-Z0-9]', '_', url.split("://")[-1])[:255]
    target_directory = os.path.join(os.getcwd(), dir_name)

    os.makedirs(target_directory, exist_ok=True)
    logging.info(f"Created directory: {target_directory}")

    return target_directory

def fetch_with_retry(url: str, retries=2, delay=5) -> requests.Response:
    """
    Retry fetching a URL in case of failure with exponential backoff.
    """
    for attempt in range(retries):
        try:
            headers = {'User-Agent': random.choice(USER_AGENT_LIST)}
            logging.debug(f"Attempt {attempt + 1} to fetch {url}")
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                return response
            else:
                logging.warning(f"Attempt {attempt + 1}: Failed with status {response.status_code}")
        except requests.exceptions.RequestException as e:
            logging.error(f"Attempt {attempt + 1}: Error - {e}")
        time.sleep(delay * (2 ** attempt))  # Exponential backoff
    return None

def fetch_robots_txt(url: str, target_directory: str):
    robots_url = url.rstrip('/') + '/robots.txt'  # Ensure URL ends with '/'
    response = fetch_with_retry(robots_url)
    
    if response:
        if response.status_code == 200:
            logging.info("robots.txt content retrieved successfully.")
            analysis_results = analyze_robots_txt(response.text)
            save_analysis_result(analysis_results, os.path.join(target_directory, 'robots_analysis.json'))
            save_robots_txt(response.text, target_directory)
        handle_response_status(response)

def analyze_robots_txt(content: str) -> RobotsAnalysis:
    user_agents, disallowed_paths, allowed_paths, crawl_delay, sitemaps = [], [], [], [], []

    for line in content.splitlines():
        line = line.strip()
        if line.startswith("User-agent:"):
            user_agents.append(line[len("User-agent:"):].strip())
        elif line.startswith("Disallow:"):
            disallowed_paths.append(line[len("Disallow:"):].strip())
        elif line.startswith("Allow:"):
            allowed_paths.append(line[len("Allow:"):].strip())
        elif line.startswith("Crawl-delay:"):
            crawl_delay.append(line[len("Crawl-delay:"):].strip())
        elif line.startswith("Sitemap:"):
            sitemaps.append(line[len("Sitemap:"):].strip())

    analysis = RobotsAnalysis(
        user_agents=user_agents,
        disallowed_paths=disallowed_paths,
        allowed_paths=allowed_paths,
        crawl_delay=crawl_delay,
        sitemaps=sitemaps
    )

    logging.info("Robots.txt Analysis: {}".format(analysis))
    return analysis

def handle_response_status(response: requests.Response):
    """
    Handle different HTTP response statuses.
    """
    code = response.status_code
    if code == 404:
        logging.warning(f"robots.txt not found (404) at {response.url}")
    elif code == 403:
        logging.warning(f"Access forbidden (403) - unable to access robots.txt at {response.url}")
    elif code >= 500:
        logging.error(f"Server error (5xx) encountered: {code} - {response.url}")
    else:
        logging.error(f"Unexpected status code {code}: {response.reason}")

def fetch_sitemap(url: str, target_directory: str):
    sitemap_url = urljoin(url, 'sitemap.xml')
    response = fetch_with_retry(sitemap_url)

    if response:
        if response.status_code == 200:
            logging.info("Sitemap found.")
            save_data_to_file(response.text, os.path.join(target_directory, 'sitemap.xml'))
        else:
            logging.warning(f"Failed to fetch sitemap: {response.status_code} - {sitemap_url}")

def save_robots_txt(content: str, target_directory: str):
    filename = f"robots_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    save_data_to_file(content, os.path.join(target_directory, filename))

def save_analysis_result(analysis: RobotsAnalysis, filename: str):
    with open(filename, 'w') as file:
        json.dump(analysis.__dict__, file, indent=4)  # Use __dict__ for dataclass
    logging.info(f"Saved robots.txt analysis to '{filename}'")

def save_data_to_file(data: str, filename: str):
    with open(filename, 'w') as file:
        file.write(data)
    logging.info(f"Saved data to '{filename}'")

def fetch_with_retry_prompt(fetch_function, url, target_directory, file_type):
    retry_fetch = True
    while retry_fetch:
        fetch_function(url, target_directory)
        continue_fetching = input(f"Do you want to retry fetching {file_type}? (yes/no): ").strip().lower()
        if continue_fetching != 'yes':
            break

if __name__ == "__main__":
    # Prompt user for the URL interactively
    url = input("Please enter the URL: ")

    # Validate URL
    while not is_valid_url(url) or not is_server_reachable(url):
        print("Invalid URL or server unreachable. Please enter a valid URL.")
        url = input("Please enter the URL: ")

    target_directory = create_target_directory(url)

    # Fetch robots.txt with retries
    fetch_with_retry_prompt(fetch_robots_txt, url, target_directory, 'robots.txt')

    # Fetch sitemap with retries
    fetch_with_retry_prompt(fetch_sitemap, url, target_directory, 'sitemap.xml')
