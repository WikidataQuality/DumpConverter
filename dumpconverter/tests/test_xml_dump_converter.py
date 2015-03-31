import pytest

from lxml import etree, objectify

import os
from io import BytesIO

from dumpconverter.XmlDumpConverter import XmlDumpConverter


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
def test_apply_namespace_map(entities_path, expected_path):
    dump_converter = create_dump_converter()
    actual_path = dump_converter.apply_namespace_map(entities_path)

    assert expected_path == actual_path


def test_process_dump():
    # Read test dump file
    script_dir = os.path.dirname(__file__)
    dump_file = open(os.path.join(script_dir, "testdata/xml_dump.xml"), "rb")

    # Create mocked dump converter
    dump_converter = create_dump_converter()
    def process_entity_mock(xml_entity):
        yield xml_entity
    dump_converter.process_entity = process_entity_mock

    # Parse test dump file and get expected result
    xml_tree = etree.parse(dump_file)
    expected_result = xml_tree.xpath("../" + dump_converter.entities_xpath, namespaces=dump_converter.namespace_map)
    dump_file.seek(0)

    # Process dump_file
    actual_result = list(dump_converter.process_dump(dump_file))

    # Run assertions
    assert len(expected_result) == len(actual_result)

    deannotate_function = lambda x: objectify.deannotate(x, cleanup_namespaces=True)
    actual_result = map(deannotate_function, actual_result)
    expected_result = map(deannotate_function, expected_result)
    assert expected_result == actual_result


@pytest.mark.parametrize(["entity_file_path", "expected_result"], [
    (
        "testdata/xml_entity_valid.xml",
        [
            ("119033364", 1, ["bar"]),
            ("119033364", 2, ["Answer to the Ultimate Question of Life, the Universe, and Everything=42"]),
            ("119033364", 3, ["bar", "baz"])
        ]
    ),
    (
        "testdata/xml_entity_invalid.xml",
        []
    )
])
def test_process_entity(entity_file_path, expected_result):
    # Parse test entity file
    script_dir = os.path.dirname(__file__)
    entity_file = etree.parse(os.path.join(script_dir, entity_file_path)).getroot()

    # Create converter and process entity_file
    dump_converter = create_dump_converter()
    actual_result = list(dump_converter.process_entity(entity_file))

    # Run assertions
    assert expected_result == actual_result


# Creates dump converter instance for testing
def create_dump_converter():
    property_mapping = {
        1: [
            {
                "nodes": ["foo:foo/text()"]
            }
        ],
        2: [
            {
                "nodes": [
                    "foo:title/text()",
                    "foo:value/text()"
                ],
                "formatter": "nodes[0] + '=' + nodes[1]"
            }
        ],
        3: [
            {
                "nodes": ["foo:foo/text()"]
            },
            {
                "nodes": ["foo:fu/text()"]
            }
        ],
        4: [
            {
                "nodes": ["foo:foobar/text()"]
            }
        ]
    }
    namespace_map = {
        "foo": "http://www.foo.com",
        "bar": "http://www.bar.com"
    }
    entities_path = "foo:element/foo:subelement"
    entity_id_path = "@id"

    dump_converter = XmlDumpConverter(
        BytesIO(),
        BytesIO(),
        True,
        42,
        42,
        "en",
        "CC0",
        namespace_map,
        entities_path,
        entity_id_path,
        property_mapping
    )

    return dump_converter