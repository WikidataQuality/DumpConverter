"""Contains exceptions appearing while downloading files."""


class DownloadError(Exception):
    """Exception that is raised, when the download of a file fails."""
    def __init__(self, status_code=None, message=None):
        super(DownloadError, self).__init__(message)
        self.status_code = status_code
