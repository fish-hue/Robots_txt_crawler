# Basic.py Robots.txt Fetcher

`basic.py` is a simple Python script that retrieves and displays the content of a website's `robots.txt` file. This file is used by webmasters to manage how search engines crawl and index their sites.

## Overview

This script prompts the user for a website URL and then constructs the appropriate URL for its `robots.txt` file. It makes a GET request to retrieve the contents and handles various potential HTTP status codes to inform the user of the result.

## Features

- Fetches the `robots.txt` file from a given website URL.
- Handles the following HTTP status codes:
  - **200:** Successfully fetched `robots.txt`. Displays its content.
  - **404:** The `robots.txt` file was not found on the server.
  - **403:** Access to the `robots.txt` file is forbidden.
- Catches and displays errors related to HTTP requests.

## Requirements

- Python 3.x
- `requests` library (can be installed via pip)

```bash
pip install requests
```

## Usage

1. Ensure Python and pip are installed on your system.
2. Clone or download the script.
3. Open a terminal and navigate to the directory containing the script.
4. Run the script using Python:

```bash
python basic.py
```

5. When prompted, enter the full URL of the website (including `http://` or `https://`).

Example input: 

```
Enter the website URL (including http:// or https://): https://example.com
```

## Example Output

- If the `robots.txt` file exists and is accessible:

```
robots.txt content:
User-agent: *
Disallow: /private/
```

- If the `robots.txt` file is not found:

```
robots.txt not found (404)
```

- If access to `robots.txt` is forbidden:

```
Access forbidden (403) - unable to access robots.txt
```

- For other status codes:

```
Failed to fetch robots.txt: <status_code> - <reason>
```

## Contributing

Contributions are welcome! If you have suggestions for improvements or new features, please feel free to submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


# Advanced.py Robots.txt and Sitemap Fetcher

`advanced.py` is a Python script designed to retrieve and analyze a website's `robots.txt` file, as well as its sitemap. The script logs its actions and handles various networking issues, retrying operations where necessary.

## Overview

This script allows users to input a website URL and subsequently fetch and analyze the `robots.txt` and `sitemap.xml` files from that URL. It logs detailed information about each operation, including any errors encountered, and saves the results in a structured format.

## Features

- Validates the input URL before making requests.
- Checks if the server is reachable using `HEAD` and `GET` requests.
- Allows automatic retries for fetching URLs with an exponential backoff strategy.
- Analyzes the contents of the `robots.txt` file, identifying user agents, disallowed paths, allowed paths, crawl delays, and sitemaps.
- Saves the analysis of `robots.txt` in a JSON format.
- Fetches and saves the `sitemap.xml` if available.
- Creates a target directory for each website based on its URL for organized file storage.
- Logs all activities and errors for easy debugging.

## Requirements

- Python 3.x
- `requests` library (can be installed using pip)

```bash
pip install requests
```

## Usage

1. Ensure Python 3 and pip are installed on your system.
2. Clone or download the script.
3. Navigate to the directory containing the script using a terminal.
4. Run the script with the following command:

```bash
python advanced.py
```

5. When prompted, enter the full URL of the website (including `http://` or `https://`).

Example input:

```
Please enter the URL: https://example.com
```

The script will validate the URL, create a directory for storing results, and attempt to fetch the `robots.txt` file and the sitemap.

## Example Output

The script will log its progress and output relevant information, such as:

- Successful retrieval of `robots.txt` content.
- Analysis results of the `robots.txt` file in JSON format.
- Status of the sitemap fetching.

If errors occur, warnings and error messages will be logged accordingly:

```
robots.txt content retrieved successfully.
Saved robots.txt analysis to 'path/to/directory/robots_analysis.json'
Sitemap found.
Saved data to 'path/to/directory/sitemap.xml'
```

## Logging

All logs will be saved in a file named `robots_sitemap_log.log` in the script's execution directory. Logs include timestamps, severity levels (DEBUG, INFO, WARNING, and ERROR), and specific messages related to the operations performed.

## Development

### Coding Standards

- Follow PEP 8 guidelines for Python coding.
- Use logging for all output that would typically be printed to the console in production-grade applications.

### Contributions

Contributions are welcome! Feel free to submit issues or pull requests for enhancements and bug fixes.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
