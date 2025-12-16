"""
Input validation functions for blog application
Validates all user inputs before database operations
"""

def validate_post_data(title, content, excerpt, tags=None):
    """
    Validate blog post data

    Returns:
        tuple: (is_valid, error_message)
    """
    errors = []

    # Title validation
    if not title or not title.strip():
        errors.append("Title is required")
    elif len(title) > 200:
        errors.append("Title must be 200 characters or less")

    # Content validation
    if not content or not content.strip():
        errors.append("Content is required")
    elif len(content) > 50000:
        errors.append("Content must be 50,000 characters or less")

    # Excerpt validation
    if not excerpt or not excerpt.strip():
        errors.append("Excerpt is required")
    elif len(excerpt) > 500:
        errors.append("Excerpt must be 500 characters or less")

    # Tags validation (optional field)
    if tags and len(tags) > 200:
        errors.append("Tags must be 200 characters or less")

    if errors:
        return False, "; ".join(errors)

    return True, None


def validate_comment_data(comment_text, author=None):
    """
    Validate comment data

    Returns:
        tuple: (is_valid, error_message)
    """
    errors = []

    # Comment text validation
    if not comment_text or not comment_text.strip():
        errors.append("Comment cannot be empty")
    elif len(comment_text) > 5000:
        errors.append("Comment must be 5,000 characters or less")

    # Author validation (optional field)
    if author and len(author) > 100:
        errors.append("Author name must be 100 characters or less")

    if errors:
        return False, "; ".join(errors)

    return True, None


def validate_image_url(image_url):
    """
    Validate image URL format

    Returns:
        tuple: (is_valid, error_message)
    """
    if not image_url or not image_url.strip():
        # Empty URL is valid (optional field)
        return True, None

    # Check for valid HTTP/HTTPS protocol
    if not (image_url.startswith('http://') or image_url.startswith('https://')):
        return False, "Image URL must start with http:// or https://"

    # Check reasonable length
    if len(image_url) > 2000:
        return False, "Image URL is too long"

    return True, None


def validate_pagination_params(page, per_page=6):
    """
    Validate pagination parameters

    Returns:
        tuple: (is_valid, error_message, sanitized_page)
    """
    try:
        page_num = int(page)

        # Ensure positive page number
        if page_num < 1:
            return False, "Invalid page number", 1

        # Prevent extremely large page numbers (potential DoS)
        if page_num > 10000:
            return False, "Page number too large", 1

        return True, None, page_num

    except (ValueError, TypeError):
        return False, "Invalid page parameter", 1


def sanitize_tags(tags):
    """
    Sanitize and normalize tag input

    Returns:
        str: Cleaned tag string
    """
    if not tags:
        return ""

    # Split by comma, strip whitespace, remove empty strings
    tag_list = [tag.strip() for tag in tags.split(',') if tag.strip()]

    # Remove duplicates while preserving order
    seen = set()
    unique_tags = []
    for tag in tag_list:
        tag_lower = tag.lower()
        if tag_lower not in seen:
            seen.add(tag_lower)
            unique_tags.append(tag)

    # Limit to 20 tags maximum
    unique_tags = unique_tags[:20]

    # Join back with consistent formatting
    return ", ".join(unique_tags)
