"""Contains tests for DumpConverter class"""
import pytest
from mock import *
from StringIO import StringIO

from dumpconverter.DumpConverter import DumpConverter

@pytest.mark.parametrize("database", [
    None,
    "foo",
    "bar"
])
def test_execute(database):
    converter = DumpConverter(StringIO(), StringIO(), database)
    run_converter_mock = Mock()
    converter.run_converter = run_converter_mock
    converter.DATABASES = {
        "foo": None,
        "bar": None
    }

    assert converter.execute() is True
    expected = converter.DATABASES.keys() if database is None else [database]
    actual = [args[0] for args, kwargs in run_converter_mock.call_args_list]
    assert expected == actual


def test_execute_unknown():
    converter = DumpConverter(StringIO(), StringIO(), 'crap')
    run_converter_mock = Mock()
    converter.run_converter = run_converter_mock
    converter.DATABASES = {
        "foo": None,
        "bar": None
    }

    assert converter.execute() is False


def test_run_converter():
    converter_foo, execute_mock_foo = mock_converter()
    converter_bar, execute_mock_bar = mock_converter()

    converter = DumpConverter(StringIO(), StringIO())
    converter.DATABASES = {
        "foo": {
            "converter": converter_foo
        },
        "bar": {
            "converter": converter_bar
        }
    }
    converter.run_converter("foo")

    assert converter_foo.call_count == 1
    assert execute_mock_foo.call_count == 1
    assert converter_bar.called is False
    assert execute_mock_bar.called is False


@pytest.mark.parametrize(["databases", "expected_result"], [
    (
        {},
        []
    ),
    (
        {
            "foo": {
                "description": "foobar"
            },
            "fu": {
                "description": "fubar"
            }
        },
        [
            ("foo", "foobar"),
            ("fu", "fubar")
        ]
    ),
    (
        {
            "foo": {
                "description": "foobar",
                "crap": "nonsense"
            }
        },
        [("foo", "foobar")]
    )
])
def test_get_available_databases(databases, expected_result):
    DumpConverter.DATABASES = databases
    assert expected_result == DumpConverter.get_available_databases()

def mock_converter():
    converter_mock = Mock()
    execute_mock = Mock()
    converter_mock.attach_mock(execute_mock, "execute")

    converter_wrapper = Mock()
    converter_wrapper.return_value = converter_mock

    return converter_wrapper, execute_mock
