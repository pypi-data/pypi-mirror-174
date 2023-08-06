from typing import Optional


class Response:
    def __init__(self, content=None, status_code=None, headers: Optional[dict[str, str]] = None, media_type=None):
        """
        content - A str or bytes.
        status_code - An int HTTP status code.
        headers - A dict of strings.
        media_type - A str giving the media type. E.g. "text/html".
        """
        self.content = content
        self.status_code = status_code
        self.headers = headers
        self.media_type = media_type


class GpkgFileResponse(Response):
    def __init__(
        self,
        content,
        file_name=None,
    ):
        """
        content - A str or bytes.
        status_code - An int HTTP status code.
        headers - A dict of strings.
        media_type - A str giving the media type. E.g. "text/html".
        """
        super().__init__(
            content=content,
            headers={"Content-Type": "application/xml", "Content-Disposition": f'attachment; filename="{file_name}"'},
        )
