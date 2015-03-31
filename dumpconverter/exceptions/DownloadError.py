class DownloadError(Exception):
    def __init__(self, message=None):
        super(DownloadError, self).__init__(message)
