"""Contains tests for DumpConverter class"""
import pytest
from mock import *

from dumpconverter.DumpConverter import DumpConverter
from dumpconverter.writer.ResultWriter import ResultWriter

@patch.object(ResultWriter, "to_archive")
@pytest.mark.parametrize("database", [
    None,
    "foo",
    "bar"
])
def test_execute(to_archive_mock, database):
    converter = DumpConverter(None, database)
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
    assert 1 == to_archive_mock.call_count


@patch.object(ResultWriter, "to_archive")
def test_execute_unknown(to_archive_mock):
    converter = DumpConverter(None, 'crap')
    run_converter_mock = Mock()
    converter.run_converter = run_converter_mock
    converter.DATABASES = {
        "foo": None,
        "bar": None
    }

    assert converter.execute() is False
    assert 0 == to_archive_mock.call_count


def test_run_converter():
    converter_foo, execute_mock_foo = mock_converter()
    converter_bar, execute_mock_bar = mock_converter()

    converter = DumpConverter(None)
    converter.DATABASES = {
        "foo": {
            "converter": converter_foo
        },
        "bar": {
            "converter": converter_bar
        }
    }
    converter.run_converter("foo", "result_writer_mock")

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
