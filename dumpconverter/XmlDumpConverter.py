from lxml import etree


from DumpConverter import DumpConverter


class XmlDumpConverter(DumpConverter):
    def __init__(self, csv_entities_file, csv_meta_file, is_quiet, source_item_id, source_property_id, data_source_language, data_source_license, namespace_map, entities_xpath, entity_id_path, property_mapping):
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

    # Applies namespace map on specified node path
    def apply_namespace_map(self, entities_xpath):
        nodes = []
        for node in entities_xpath.split("/"):
            for prefix, namespace in self.namespace_map.iteritems():
                node = node.replace("{0}:".format(prefix), "{{{0}}}".format(namespace))
            nodes.append(node)

        return "/".join(nodes)

    # Iterates through xml elements of given file and processes the ones that matches entity_path
    def process_dump(self, dump_file):
        node_path = []
        for event, element in etree.iterparse(dump_file, events=("start", "end")):
            # Build current node path to get all the entities specified by entity_path
            if event == "start":
                node_path.append(element.tag)
            if event == "end":
                if "/".join(node_path) == self.entities_path:
                    # Process entity
                    for external_value in self.process_entity(element):
                        yield external_value

                    # Print progress
                    if not self.is_quiet:
                        self.print_progress("Process database dump...{0}", dump_file.tell())

                    # Clean up unneeded references
                    # http://www.ibm.com/developerworks/xml/library/x-hiperfparse/
                    element.clear()
                    while element.getprevious() is not None:
                        del element.getparent()[0]
                del node_path[-1]

        # Write new line to console to now overwrite progress
        if not self.is_quiet:
            print

        return
        yield

    # Processes single entity of the dump
    def process_entity(self, entity):
        # Get entity id
        try:
            entity_id = entity.xpath(self.entity_id_path, namespaces=self.namespace_map)[0]
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
                    result = entity.xpath(node_selector, namespaces=self.namespace_map)

                    # Append result to nodes list in correct format
                    for i in range(0, len(result)):
                        if i >= len(elements):
                            elements.append([])
                        elements[i].append(result[i].encode("utf-8"))

                # Run formatter on nodes if provided
                # Otherwise concat list of affected nodes
                if "formatter" in mapping:
                    for element in elements:
                        formatted_value = self.run_formatter(mapping['formatter'], element)
                        if formatted_value:
                            external_values.append(formatted_value)
                else:
                    for element in elements:
                        external_values += element

            if external_values:
                yield entity_id, property_id, external_values

        return
        yield