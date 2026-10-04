import io
import unittest
import urllib.error
from email.message import Message
from unittest.mock import patch

from lovstudio_skill_helper import api, auth


def http_error(status, body, content_type="application/json", ray=None):
    headers = Message()
    headers["content-type"] = content_type
    if ray:
        headers["cf-ray"] = ray
    return urllib.error.HTTPError(
        "https://lovstudio.ai/api/example", status, "Denied", headers,
        io.BytesIO(body.encode()),
    )


class ApiErrorTests(unittest.TestCase):
    def test_html_proxy_error_is_not_an_entitlement_denial(self):
        error = api.ApiError.from_http(http_error(403, "<html>private upstream detail</html>", "text/html"))
        self.assertEqual(error.code, "unexpected_http_response")
        self.assertNotIn("private upstream", error.message)

    def test_cloudflare_html_keeps_ray(self):
        error = api.ApiError.from_http(http_error(
            403, "<html>Cloudflare Error 1010</html>", "text/html", "test-ray-SJC",
        ))
        self.assertEqual(error.code, "website_protection_blocked")
        self.assertIn("test-ray-SJC", error.message)

    def test_json_error_code_is_separate_from_ray_diagnostic(self):
        error = api.ApiError.from_http(http_error(
            403, '{"error":"skill_not_owned"}', ray="test-ray-SJC",
        ))
        self.assertEqual(error.code, "skill_not_owned")
        self.assertIn("test-ray-SJC", error.message)

    def test_all_request_paths_identify_the_official_client(self):
        def respond(request, **kwargs):
            self.assertTrue(request.get_header("User-agent").startswith("lovstudio-skill-helper/"))
            return io.BytesIO(b"{}")

        with patch("urllib.request.urlopen", side_effect=respond):
            api.call("heartbeat", {})
            api.list_catalog()
            auth._post("https://lovstudio.ai/test", {})


if __name__ == "__main__":
    unittest.main()
