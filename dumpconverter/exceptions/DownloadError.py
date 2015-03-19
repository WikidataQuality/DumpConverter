class DownloadError(Exception):
    def __init__(self, message):
        super(DownloadError, self).__init__(message)
