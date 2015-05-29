"""Contains dump converter class for processing xml dumps."""
import unicodedata
from lxml import etree

from dumpconverter.utils import consoleutils


class XmlDumpConverter():
    """
    Dump converter for dumps in xml format. Is responsible for splitting dump
    into single entities and process them by applying given property mapping.
    """
    def __init__(self, entities_path, entity_id_path, property_mapping,
                 namespaces=None, is_quiet=False):
        """
        Creates new XmlDumpConverter instance
        :param entities_path: XPath to retrieve entities out of the dump.
        :param entity_id_path: XPath to retrieve id of a single entity.
        :param property_mapping: Property mapping from data source to Wikidata.
        :param namespaces: XML namespace mapping.
        :param is_quiet: If set to True, console output will be suppressed.
        """
        self.entity_id_path = entity_id_path
        self.property_mapping = property_mapping
        self.namespaces = namespaces or {}
        self.is_quiet = is_quiet
        self.entities_path = self.apply_namespaces(entities_path)

    def apply_namespaces(self, element_path):
        """
        Applies namespace map on specified node path.
        Replaces names of namespaces with corresponding url.
        :param element_path: Simple path to a xml node.
        :return: Node path with concrete namespaces.
        """
        if self.namespaces:
            nodes = []
            for node in element_path.split("/"):
                for prefix, namespace in self.namespaces.iteritems():
                    node = node.replace("{0}:".format(prefix),
                                        "{{{0}}}".format(namespace))
                nodes.append(node)

            return "/".join(nodes)
        else:
            return element_path

    def process_dump(self, dump_file):
        """
        Generator that iterates through xml elements of given file and
        extracts values from the ones that matches entity_path.
        :param dump_file: File object of the dump.
        :return: Triples of entity id, property id and external values
        """
        node_path = []
        for event, element in etree.iterparse(dump_file, events=("start", "end")):
            if event == "start":
                node_path.append(element.tag)
            if event == "end":
                if "/".join(node_path) == self.entities_path:
                    for external_value in self.process_entity(element):
                        if external_value:
                            yield external_value

                    # Clean up unneeded references
                    # http://www.ibm.com/developerworks/xml/library/x-hiperfparse/
                    element.clear()
                    while element.getprevious() is not None:
                        del element.getparent()[0]

                    if not self.is_quiet:
                        message = "Processing database dump...{0}"
                        consoleutils.print_progress(message, dump_file.tell())
                del node_path[-1]

        # Write new line to console to overwrite progress
        if not self.is_quiet:
            print

    def process_entity(self, entity_element):
        """
        Generator that extracts values from given entity by applying mapping.
        :param entity_element: Xml element of a single entity.
        :return: Triples of entity id, property id and external values
        """
        entity_id = self.extract_entity_id(entity_element)
        if entity_id is not None:
            for property_id, mappings in self.property_mapping.iteritems():
                external_values = []
                for mapping in mappings:
                    value_paths = mapping['value_paths']
                    values = self.get_affected_values(entity_element, value_paths)

                    if "formatter" in mapping:
                        formatter = mapping['formatter']
                        external_values += self.run_formatter(formatter, values)
                    else:
                        for value in values:
                            external_values += value

                if external_values:
                    yield entity_id, property_id, list(set(external_values))

    def extract_entity_id(self, entity_element):
        """
        Extracts the id of a given entity.
        :param entity_element: Xml element of a single entity.
        :return: Id of the given entity.
        """
        entity_id = entity_element.xpath(self.entity_id_path,
                                         namespaces=self.namespaces)

        if isinstance(entity_id, basestring):
            return entity_id
        elif isinstance(entity_id, list):
            try:
                return entity_id[0]
            except IndexError:
                pass

    def get_affected_values(self, entity_element, value_paths):
        """
        Extracts values affected by xpaths from given entity.
        :param entity_element: Xml element of a single entity.
        :param value_paths: List of XPaths to extract values from xml element.
        :return: Values that are affected by given mapping.
        """
        elements = []
        for value_path in value_paths:
            result = entity_element.xpath(value_path,
                                          namespaces=self.namespaces)

            for i in range(0, len(result)):
                value = result[i]
                if isinstance(value, unicode):
                    value = self.remove_control_characters(value)
                elif not isinstance(value, str):
                    value = value.text
                value = value.encode("utf-8")

                if i >= len(elements):
                    elements.append([])
                elements[i].append(value)

        return elements

    @staticmethod
    def remove_control_characters(value):
        """
        Removes all unicode control characters from a given string.
        :param value: String value
        :return: String without unicode control characters.
        """
        return "".join(ch for ch in value if unicodedata.category(ch)[0] != "C")

    @staticmethod
    def run_formatter(formatter, values):
        """
        Runs specified formatter on given values.
        :param formatter: Formatter function
        :param values: List of values from dump.
        :return: List of formatted values.
        """
        formatted_values = []
        for value in values:
            formatted_value = XmlDumpConverter.formatter_wrapper(formatter, value)
            if formatted_value:
                formatted_values.append(formatted_value)

        return formatted_values

    @staticmethod
    def formatter_wrapper(formatter, values):
        """
        Wrapper for formatters that takes list of arguments and passes them
        to specified formatter function.
        :param formatter: Formatter function.
        :param values: List of arguments for formatter.
        :return: Result of formatter execution.
        """
        try:
            return formatter(*values)
        except:
            pass
