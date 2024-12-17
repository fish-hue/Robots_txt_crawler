# basic.py README

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
