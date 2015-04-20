"""Contains helper methods for console output."""
import sys
import math


def print_progress(message, current_bytes, total_bytes=None):
    """
    Prints progress of an I/O process.
    :param message: Message that should be shown in front of the progress.
    :param current_bytes: Number of current bytes.
    :param total_bytes: Number of total bytes.
    """
    if total_bytes is not None:
        progress = float(current_bytes) / total_bytes * 100
        message = message.format(str(round(progress, 2)) + "%")
    else:
        message = message.format(format_bytes(current_bytes))

    sys.stdout.write("\r\033[K")
    sys.stdout.write(message)
    sys.stdout.flush()


def format_bytes(bytes_count, precision=2):
    """
    Formats number of bytes to string with suitable unit.
    :param bytes_count: Number of bytes.
    :param precision: Precision of size number.
    :return: Formatted string with suitable unit.
    """
    if bytes_count > 0:
        units = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
        exponent = int(math.floor(math.log(bytes_count, 1024)))
        power = math.pow(1024, exponent)
        converted = round(bytes_count / power, precision)
        if converted > 0:
            return '%s %s' % (converted, units[exponent])

    return '0 B'
