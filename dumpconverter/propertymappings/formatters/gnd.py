"""Contains several formatters for GND data source."""
# coding: utf8


def gender_formatter(gender):
    """
    Converts gender values from GND to Wikidata format.
    :param gender: Gender value in GND format.
    :return: Gender value in Wikidata format.
    """
    if gender == "0":
        return "weiblich"
    elif gender == "1":
        return "männlich"


def basic_name_formatter(basic_name):
    """
    Converts basic names from GND to Wikidata format.
    :param basic_name: Name following the schema "Surname, Forename".
    :return: Name in Wikidata format.
    """
    name_split = basic_name.split(", ")
    if len(name_split) >= 2:
        return "%s %s" % (name_split[1], name_split[0])
    else:
        return name_split[0]


def personal_name_formatter(basic_name, count=None):
    """
    Converts personal name from GND to Wikidata format.
    :param basic_name: Personal name in GND format.
    :param count: Count of the name.
    :return: Name in Wikidata format.
    """
    if count:
        return "%s %s" % (basic_name, count)
    else:
        return basic_name


def date_formatter(date):
    """
    Converts date from GND to Wikidata format.
    :param date: Date in GND format.
    :return: Date in Wikidata format.
    """
    return date.replace("XX.", "")


def start_date_formatter(timespan):
    """
    Extracts start date from GND timespan and converts it to Wikidata format.
    :param timespan: Timespan in GND format.
    :return: Start date in Wikidata format.
    """
    return date_formatter(timespan.split("-")[0])


def end_date_formatter(timespan):
    """
    Extracts end date from GND timespan and converts it to Wikidata format.
    :param timespan: Timespan in GND format.
    :return: End date in Wikidata format.
    """
    timespan_split = timespan.split("-")
    if len(timespan_split) >= 2:
        return date_formatter(timespan_split[1])


def geo_coordinate_formatter(latitude, longitude):
    """
    Formats geo coordinates from GND to Wikidata format.
    :param latitude: Latitude in GND format.
    :param longitude: Longitude in GND format.
    :return: Geo coordinate in Wikidata format.
    """
    return "%s,%s" % (latitude, longitude)
