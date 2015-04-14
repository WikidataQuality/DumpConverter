"""Contains dump converter class for xml dumps."""
from lxml import etree


from DumpConverter import DumpConverter


class XmlDumpConverter(DumpConverter):
    """
    Dump converter for dumps in xml format. Is responsible for splitting dump
    into single entities and process them by applying given property mapping.
    """
    def __init__(self, csv_entities_file, csv_meta_file, is_quiet,
                 source_item_id, source_property_id, data_source_language,
                 data_source_license, namespace_map, entities_xpath,
                 entity_id_path, property_mapping):
        """
        Creates new XmlDumpConverter instance.
        :param csv_entities_file: File object for external entities.
        :param csv_meta_file: File object for meta information about the dump.
        :param is_quiet: If set to True, console output will be suppressed.
        :param source_item_id: Id of item of the data source.
        :param source_property_id: Id of property of the identifier of the data source.
        :param data_source_language: Code of the language of the data source.
        :param data_source_license: Id of item of the license of the data source.
        :param namespace_map: Xml namespace mapping.
        :param entities_xpath: XPath to retrieve entities out of the dump.
        :param entity_id_path: XPath to retrieve id of a single entity.
        :param property_mapping: Property mapping from data source to Wikidata.
        """
        super(XmlDumpConverter, self).__init__(
            csv_entities_file,
            csv_meta_file,
            is_quiet,
            source_item_id,
            source_property_id,
            data_source_language,
            data_source_license)

        self.namespace_map = namespace_map
        self.entities_xpath = entities_xpath
        self.entities_path = self.apply_namespace_map(entities_xpath)
        self.entity_id_path = entity_id_path
        self.property_mapping = property_mapping

    def apply_namespace_map(self, node_path):
        """
        Applies namespace map on specified node path.
        Replaces names of namespaces with their url.
        :param node_path: Simple path to a xml node.
        :return: Node path with concrete namespaces.
        """
        nodes = []
        for node in node_path.split("/"):
            for prefix, namespace in self.namespace_map.iteritems():
                node = node.replace("{0}:".format(prefix),
                                    "{{{0}}}".format(namespace))
            nodes.append(node)

        return "/".join(nodes)

    def process_dump(self, dump_file):
        """
        Generator that iterates through xml elements of given file and
        processes the ones that matches entity_path.
        :param dump_file: File object of the dump.
        :return: Triples of entity id, property id and external values
        """
        node_path = []
        for event, element in etree.iterparse(dump_file, events=("start", "end")):
            if event == "start":
                node_path.append(element.tag)
            if event == "end":
                if "/".join(node_path) == self.entities_path:
                    process_entity_generator = self.process_entity(element)
                    if process_entity_generator:
                        for external_value in process_entity_generator:
                            if external_value:
                                yield external_value

                        if not self.is_quiet:
                            self.print_progress(
                                "Process database dump...{0}", dump_file.tell())

                        # Clean up unneeded references
                        # http://www.ibm.com/developerworks/xml/library/x-hiperfparse/
                        element.clear()
                        while element.getprevious() is not None:
                            del element.getparent()[0]
                del node_path[-1]

        # Write new line to console to overwrite progress
        if not self.is_quiet:
            print

    def process_entity(self, entity_element):
        """
        Generator that processes single entity of the dump by applying mapping.
        :param entity_element: Xml element of a single entity.
        :return: Triples of entity id, property id and external values
        """
        # Get entity id
        try:
            entity_id = entity_element.xpath(self.entity_id_path,
                                             namespaces=self.namespace_map)[0]
        except IndexError:
            return

        # Evaluate mapping and extract values
        for property_id, mappings in self.property_mapping.iteritems():
            external_values = []
            for mapping in mappings:
                # Get affected elements
                elements = []
                for node_selector in mapping['nodes']:
                    # Evaluate xpath node selector
                    result = entity_element.xpath(node_selector,
                                                  namespaces=self.namespace_map)

                    # Append result to nodes list in correct format
                    for i in range(0, len(result)):
                        if i >= len(elements):
                            elements.append([])
                        elements[i].append(result[i].encode("utf-8"))

                # Run formatter on nodes if provided
                # Otherwise concat list of affected nodes
                if "formatter" in mapping:
                    for element in elements:
                        formatter = mapping['formatter']
                        formatted_value = self.run_formatter(formatter, element)
                        if formatted_value:
                            external_values.append(formatted_value)
                else:
                    for element in elements:
                        external_values += element

            if external_values:
                yield entity_id, property_id, external_values
