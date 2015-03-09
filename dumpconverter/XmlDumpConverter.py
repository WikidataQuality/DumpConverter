import sys
from lxml import etree


from DumpConverter import DumpConverter


class XmlDumpConverter(DumpConverter):
    def __init__(self, csv_entities_file, csv_meta_file, source_item_id, source_property_id, data_source_language, data_source_license, namespace_map, entities_path, entity_id_path, property_mapping):
        super(XmlDumpConverter, self).__init__(
            csv_entities_file,
            csv_meta_file,
            source_item_id,
            source_property_id,
            data_source_language,
            data_source_license)

        self.namespace_map = namespace_map
        self.entities_path = self.apply_namespace_map(entities_path, namespace_map)
        self.entity_id_path = entity_id_path
        self.property_mapping = property_mapping

    # Applies namespace map on specified node path
    @staticmethod
    def apply_namespace_map(entities_path, namespace_map):
        nodes = []
        for node in entities_path.split("/"):
            for prefix, namespace in namespace_map.iteritems():
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
                    for entity_id, property_id, external_values in self.process_entity(element):
                        yield entity_id, property_id, external_values

                    # Clean up unneeded references
                    # http://www.ibm.com/developerworks/xml/library/x-hiperfparse/
                    element.clear()
                    while element.getprevious() is not None:
                        del element.getparent()[0]
                del node_path[-1]

        # Write new line to console to now overwrite progress
        sys.stdout.write("\n")

    # Processes single entity of the dump
    def process_entity(self, element):
        # Get entity id
        entity_id = element.xpath(self.entity_id_path, namespaces=self.namespace_map)[0]

        # Evaluate mapping and extract values
        for property_id, mapping in self.property_mapping.iteritems():
            # Get affected nodes/texts
            results = element.xpath(mapping["nodeSelector"], namespaces=self.namespace_map)
            if results:
                # If value formatter is provided, apply on each result
                if "valueFormatter" in mapping:
                    external_values = []
                    for result in results:
                        result = result.xpath(mapping["valueFormatter"], namespaces=self.namespace_map)
                        if result:
                            external_values.append(result)
                else:
                    external_values = results

                yield entity_id, property_id, external_values