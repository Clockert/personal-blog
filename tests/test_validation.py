"""
Tests for input validation functions
"""
import pytest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from validation import (
    validate_post_data,
    validate_comment_data,
    validate_image_url,
    validate_pagination_params,
    sanitize_tags
)


class TestValidatePostData:
    """Tests for post data validation"""

    def test_valid_post_data(self):
        """Test that valid post data passes validation"""
        is_valid, error = validate_post_data(
            "Valid Title",
            "This is valid content",
            "This is a valid excerpt",
            "python, flask"
        )
        assert is_valid is True
        assert error is None

    def test_empty_title(self):
        """Test that empty title fails validation"""
        is_valid, error = validate_post_data("", "Content", "Excerpt")
        assert is_valid is False
        assert "Title is required" in error

    def test_whitespace_only_title(self):
        """Test that whitespace-only title fails validation"""
        is_valid, error = validate_post_data("   ", "Content", "Excerpt")
        assert is_valid is False
        assert "Title is required" in error

    def test_title_too_long(self):
        """Test that title over 200 characters fails"""
        long_title = "x" * 201
        is_valid, error = validate_post_data(long_title, "Content", "Excerpt")
        assert is_valid is False
        assert "200 characters" in error

    def test_empty_content(self):
        """Test that empty content fails validation"""
        is_valid, error = validate_post_data("Title", "", "Excerpt")
        assert is_valid is False
        assert "Content is required" in error

    def test_content_too_long(self):
        """Test that content over 50,000 characters fails"""
        long_content = "x" * 50001
        is_valid, error = validate_post_data("Title", long_content, "Excerpt")
        assert is_valid is False
        assert "50,000 characters" in error

    def test_empty_excerpt(self):
        """Test that empty excerpt fails validation"""
        is_valid, error = validate_post_data("Title", "Content", "")
        assert is_valid is False
        assert "Excerpt is required" in error

    def test_excerpt_too_long(self):
        """Test that excerpt over 500 characters fails"""
        long_excerpt = "x" * 501
        is_valid, error = validate_post_data("Title", "Content", long_excerpt)
        assert is_valid is False
        assert "500 characters" in error

    def test_tags_too_long(self):
        """Test that tags over 200 characters fails"""
        long_tags = "x" * 201
        is_valid, error = validate_post_data("Title", "Content", "Excerpt", long_tags)
        assert is_valid is False
        assert "Tags" in error

    def test_optional_tags(self):
        """Test that tags are optional"""
        is_valid, error = validate_post_data("Title", "Content", "Excerpt", None)
        assert is_valid is True

    def test_multiple_errors(self):
        """Test that multiple errors are reported together"""
        is_valid, error = validate_post_data("", "", "")
        assert is_valid is False
        assert "Title" in error
        assert "Content" in error
        assert "Excerpt" in error


class TestValidateCommentData:
    """Tests for comment data validation"""

    def test_valid_comment(self):
        """Test that valid comment data passes"""
        is_valid, error = validate_comment_data("This is a great post!", "John")
        assert is_valid is True
        assert error is None

    def test_empty_comment(self):
        """Test that empty comment fails"""
        is_valid, error = validate_comment_data("", "John")
        assert is_valid is False
        assert "Comment cannot be empty" in error

    def test_whitespace_only_comment(self):
        """Test that whitespace-only comment fails"""
        is_valid, error = validate_comment_data("   ", "John")
        assert is_valid is False
        assert "empty" in error

    def test_comment_too_long(self):
        """Test that comment over 5,000 characters fails"""
        long_comment = "x" * 5001
        is_valid, error = validate_comment_data(long_comment, "John")
        assert is_valid is False
        assert "5,000 characters" in error

    def test_author_too_long(self):
        """Test that author name over 100 characters fails"""
        long_author = "x" * 101
        is_valid, error = validate_comment_data("Comment", long_author)
        assert is_valid is False
        assert "Author name" in error

    def test_optional_author(self):
        """Test that author is optional"""
        is_valid, error = validate_comment_data("Valid comment", None)
        assert is_valid is True


class TestValidateImageUrl:
    """Tests for image URL validation"""

    def test_valid_http_url(self):
        """Test that valid HTTP URL passes"""
        is_valid, error = validate_image_url("http://example.com/image.jpg")
        assert is_valid is True
        assert error is None

    def test_valid_https_url(self):
        """Test that valid HTTPS URL passes"""
        is_valid, error = validate_image_url("https://example.com/image.jpg")
        assert is_valid is True
        assert error is None

    def test_empty_url_is_valid(self):
        """Test that empty URL is valid (optional field)"""
        is_valid, error = validate_image_url("")
        assert is_valid is True

    def test_none_url_is_valid(self):
        """Test that None URL is valid (optional field)"""
        is_valid, error = validate_image_url(None)
        assert is_valid is True

    def test_url_without_protocol(self):
        """Test that URL without http/https fails"""
        is_valid, error = validate_image_url("example.com/image.jpg")
        assert is_valid is False
        assert "http://" in error or "https://" in error

    def test_ftp_protocol_fails(self):
        """Test that FTP protocol fails"""
        is_valid, error = validate_image_url("ftp://example.com/image.jpg")
        assert is_valid is False
        assert "http" in error

    def test_url_too_long(self):
        """Test that URL over 2000 characters fails"""
        long_url = "https://example.com/" + "x" * 2000
        is_valid, error = validate_image_url(long_url)
        assert is_valid is False
        assert "too long" in error


class TestValidatePaginationParams:
    """Tests for pagination parameter validation"""

    def test_valid_page_number(self):
        """Test that valid page number passes"""
        is_valid, error, page = validate_pagination_params(5)
        assert is_valid is True
        assert error is None
        assert page == 5

    def test_page_one(self):
        """Test that page 1 is valid"""
        is_valid, error, page = validate_pagination_params(1)
        assert is_valid is True
        assert page == 1

    def test_negative_page_number(self):
        """Test that negative page fails"""
        is_valid, error, page = validate_pagination_params(-1)
        assert is_valid is False
        assert page == 1  # Should default to 1

    def test_zero_page_number(self):
        """Test that page 0 fails"""
        is_valid, error, page = validate_pagination_params(0)
        assert is_valid is False
        assert page == 1  # Should default to 1

    def test_extremely_large_page(self):
        """Test that extremely large page number fails"""
        is_valid, error, page = validate_pagination_params(99999)
        assert is_valid is False
        assert "too large" in error
        assert page == 1

    def test_string_page_number(self):
        """Test that string page parameter is converted"""
        is_valid, error, page = validate_pagination_params("5")
        assert is_valid is True
        assert page == 5

    def test_invalid_string_page(self):
        """Test that non-numeric string fails"""
        is_valid, error, page = validate_pagination_params("abc")
        assert is_valid is False
        assert page == 1


class TestSanitizeTags:
    """Tests for tag sanitization"""

    def test_basic_tags(self):
        """Test that basic tags are preserved"""
        result = sanitize_tags("python, flask, web")
        assert result == "python, flask, web"

    def test_extra_whitespace_removed(self):
        """Test that extra whitespace is removed"""
        result = sanitize_tags("python,  flask  ,   web")
        assert result == "python, flask, web"

    def test_empty_tags_removed(self):
        """Test that empty tags are removed"""
        result = sanitize_tags("python, , flask, , web")
        assert result == "python, flask, web"

    def test_duplicate_tags_removed(self):
        """Test that duplicate tags are removed (case insensitive)"""
        result = sanitize_tags("python, Python, PYTHON, flask")
        assert result == "python, flask"

    def test_empty_string(self):
        """Test that empty string returns empty string"""
        result = sanitize_tags("")
        assert result == ""

    def test_none_input(self):
        """Test that None returns empty string"""
        result = sanitize_tags(None)
        assert result == ""

    def test_max_20_tags(self):
        """Test that only first 20 tags are kept"""
        many_tags = ", ".join([f"tag{i}" for i in range(25)])
        result = sanitize_tags(many_tags)
        tag_list = result.split(", ")
        assert len(tag_list) == 20

    def test_preserves_first_occurrence_case(self):
        """Test that first occurrence's case is preserved"""
        result = sanitize_tags("Python, python, PYTHON")
        assert result == "Python"
