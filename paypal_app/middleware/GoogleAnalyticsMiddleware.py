# middleware.py
import random
from django.conf import settings


class GoogleAnalyticsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if settings.DEBUG and "text/html" in response.get("Content-Type", ""):
            analytics_code = """
                <!-- Google tag (gtag.js) -->
                    <script async src="https://www.googletagmanager.com/gtag/js?id=G-M14P19YSS8"></script>
                    <script>
                    window.dataLayer = window.dataLayer || [];
                    function gtag(){dataLayer.push(arguments);}
                    gtag('js', new Date());
                    gtag('create', 'UA-297840826-1', 'auto');
                    gtag('config', 'G-M14P19YSS8');
                </script>
            """
            # Insert the simulated Google Analytics code just before the </body> tag
            response.content = response.content.replace(
                b"</body>", analytics_code.encode("utf-8") + b"</body>", 1
            )

        return response
