from urllib.parse import urlparse

# This function checks if the given URL is valid and well-formed
def is_valid_url(url):
    try:
        # Parse the URL into parts (scheme, netloc, path, etc.)
        result = urlparse(url)

        # Return True only if the URL has both scheme (like http/https) and a network location
        return all([result.scheme, result.netloc])

    except ValueError:
        # If urlparse fails, it's not a valid URL
        return False

