# -*- coding: utf-8 -*-
"""Contains test for XmlDumpConverter class"""
import os
import pytest
from lxml import etree, objectify

from dumpconverter.dataformatconverters.XmlDumpConverter import XmlDumpConverter


@pytest.mark.parametrize(["entities_path", "expected_path"], [
    (
        "foo:element",
        "{http://www.foo.com}element"
    ),
    (
        "foo:element/bar:subelement",
        "{http://www.foo.com}element/{http://www.bar.com}subelement"
    ),
    (
        "element",
        "element"
    ),
    (
        "element/subelement",
        "element/subelement"
    ),

])
def test_apply_namespaces(entities_path, expected_path):
    xml_converter = create_dump_converter()
    actual_path = xml_converter.apply_namespaces(entities_path)

    assert expected_path == actual_path


def test_process_dump():
    with open_test_file("testdata/xml_dump.xml") as dump_file:
        xml_converter = create_dump_converter()
        def process_entity_mock(xml_entity):
            yield xml_entity
        xml_converter.process_entity = process_entity_mock

        xml_tree = etree.parse(dump_file)
        expected_result = xml_tree.xpath("../foo:element/foo:subelement",
                                         namespaces=xml_converter.namespaces)
        dump_file.seek(0)

        actual_result = list(xml_converter.process_dump(dump_file))

        assert len(expected_result) == len(actual_result)
        deannotate = lambda x: objectify.deannotate(x, cleanup_namespaces=True)
        actual_result = map(deannotate, actual_result)
        expected_result = map(deannotate, expected_result)
        assert expected_result == actual_result


@pytest.mark.parametrize(["entity_file_path", "expected_values"], [
    (
        "testdata/xml_entity_valid.xml",
        [
            ("119033364", "P1", ["foobar"]),
            ("119033364", "P2", ["Answer to the Ultimate Question of Life, the Universe, and Everything=42"]),
            ("119033364", "P3", ["foobar", "42"]),
            ("119033364", "P4", ["fubar"])
        ]
    ),
    (
        "testdata/xml_entity_invalid.xml",
        []
    )
])
def test_process_entity(entity_file_path, expected_values):
    with open_test_file(entity_file_path) as dump_file:
        entity_element = etree.parse(dump_file)
        xml_converter = create_dump_converter()
        actual_values = list(xml_converter.process_entity(entity_element))

        assert len(expected_values) == len(actual_values)
        for expected_value in expected_values:
            assert expected_value in actual_values


@pytest.mark.parametrize(["entity_file_path", "expected_entity_id"], [
    (
        "testdata/xml_entity_valid.xml",
        "119033364"
    ),
    (
        "testdata/xml_entity_invalid.xml",
        None
    )
])
def test_extract_entity_id(entity_file_path, expected_entity_id):
    with open_test_file(entity_file_path) as dump_file:
        entity_element = etree.parse(dump_file)
        xml_converter = create_dump_converter()
        actual_entity_id = xml_converter.extract_entity_id(entity_element)

        assert expected_entity_id == actual_entity_id


@pytest.mark.parametrize(["entity_file_path", "value_paths", "expected_values"], [
    (
        "testdata/xml_entity_valid.xml",
        ["foo:fubar"],
        [["42"]]
    ),
    (
        "testdata/xml_entity_valid.xml",
        ["foo:fubar/text()"],
        [["42"]]
    ),
    (
        "testdata/xml_entity_valid.xml",
        [
            "foo:foo",
            "foo:fubar"
        ],
        [
            ["foobar", "42"]
        ]
    ),
    (
        "testdata/xml_entity_valid.xml",
        [
            "foo:foobar/foo:foo",
            "foo:foobar/foo:bar"
        ],
        [
            ["foo", "bar"],
            ["fu", "bar"]
        ]
    )
])
def test_get_affected_values(entity_file_path, value_paths, expected_values):
    with open_test_file(entity_file_path) as dump_file:
        entity_element = etree.parse(dump_file)
        xml_converter = create_dump_converter()
        actual_values = xml_converter.get_affected_values(entity_element,
                                                           value_paths)

        assert expected_values == actual_values


@pytest.mark.parametrize(["value", "expected_value"], [
    (
        u"foobar",
        u"foobar"
    ),
    (
        unichr(152) + u"foobar" + unichr(156),
        u"foobar"
    ),
    (
        u"füübar",
        u"füübar"
    )
])
def test_remove_control_characters(value, expected_value):
    xml_converter = create_dump_converter()
    actual_value = xml_converter.remove_unprintable_characters(value)

    assert expected_value == actual_value


@pytest.mark.parametrize(["formatter", "values", "expected_values"], [
    (
        lambda x, y: x+y,
        [
            ["foo", "bar"],
            ["fu", "bar"]
        ],
        ["foobar", "fubar"]
    ),
    (
        lambda x, y: x+y,
        [
            ["foo"],
            ["fu"]
        ],
        []
    )
])
def test_run_formatter(formatter, values, expected_values):
    actual_values = XmlDumpConverter.run_formatter(formatter, values)

    assert expected_values == actual_values


@pytest.mark.parametrize(["formatter", "values", "expected_value"], [
    (
        lambda x: x,
        ["foo"],
        "foo"
    ),
    (
        lambda x, y: x+y,
        ["foo", "bar"],
        "foobar"
    )
])
def test_formatter_wrapper(formatter, values, expected_value):
    actual_value = XmlDumpConverter.formatter_wrapper(
        formatter,
        values
    )

    assert actual_value == expected_value


def create_dump_converter():
    """
    Creates xml dump converter instance for testing.
    :return: Instance of XmlDumpConverter.
    """
    property_mapping = {
        "P1": [
            {
                "value_paths": ["foo:foo"]
            }
        ],
        "P2": [
            {
                "value_paths": [
                    "foo:title",
                    "foo:fubar"
                ],
                "formatter": lambda x, y: x + "=" + y
            }
        ],
        "P3": [
            {
                "value_paths": ["foo:foo"]
            },
            {
                "value_paths": ["foo:fubar"]
            }
        ],
        "P4": [
            {
                "value_paths": ["foo:bar"]
            }
        ],
        "P5": [
            {
                "value_paths": [ "foo:baz" ]
            }
        ]
    }
    namespaces = {
        "foo": "http://www.foo.com",
        "bar": "http://www.bar.com"
    }
    entities_path = "foo:element/foo:subelement"
    entity_id_path = "@id"

    xml_converter = XmlDumpConverter(
        entities_path,
        entity_id_path,
        property_mapping,
        namespaces
    )

    return xml_converter


def open_test_file(file_path, mode="rb"):
    """
    Opens a file containing test data by specifying a relative file path.
    :param file_path: Relative file path.
    :param mode: Mode in which file should be opened.
    :return: Opened file object.
    """
    script_dir = os.path.dirname(__file__)
    entity_file_path = os.path.join(script_dir, file_path)
    fileobj = open(entity_file_path, mode)

    return fileobj