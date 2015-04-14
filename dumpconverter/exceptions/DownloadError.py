"""Contains exceptions appearing while downloading dumps."""


class DownloadError(Exception):
    """Exception that is raised, when the download of a dump fails."""
    def __init__(self, message=None):
        super(DownloadError, self).__init__(message)
