import xml.etree.ElementTree as ET
import json

class ClassModelParser:
    def __init__(self, input_file):
        self.tree = ET.parse(input_file)
        self.root = self.tree.getroot()
        self.class_elements = {class_elem.get("name"): class_elem for class_elem in self.root.findall("Class")}
        
    def get_class_elements(self):
        return self.class_elements

    def get_root_class_name(self):
        for name, class_elem in self.class_elements.items():
            if class_elem.get("isRoot", "false").lower() == "true":
                return name
        return None

    def process_attributes(self, class_elem):
        attributes = []
        for attribute in class_elem.findall("Attribute"):
            attributes.append({
                "name": attribute.get("name"),
                "type": attribute.get("type")
            })
        return attributes

    def process_aggregations(self, class_name):
        aggregations = []
        for aggregation in self.root.findall(f"Aggregation[@target='{class_name}']"):
            child_class_name = aggregation.get("source")
            source_multiplicity = aggregation.get("sourceMultiplicity")
            if '..' in source_multiplicity:
                min_val, max_val = map(int, source_multiplicity.split(".."))
            else:
                min_val = max_val = int(source_multiplicity)
            aggregations.append((child_class_name, min_val, max_val))
        return aggregations

class ArtifactGenerator:
    def __init__(self, class_model_parser):
        self.class_model_parser = class_model_parser
        self.class_elements = class_model_parser.get_class_elements()

    def add_class():
        raise NotImplementedError("This method should be overridden in subclasses.")

    def generate_file():
        raise NotImplementedError("This method should be overridden in subclasses.")

class MetaJsonGenerator(ArtifactGenerator):
    def add_class(self, meta_info, class_name, min_val=None, max_val=None):
        class_elem = self.class_elements[class_name]
        class_info = {
            "class": class_elem.get("name"),
            "documentation": class_elem.get("documentation", ""),
            "isRoot": class_elem.get("isRoot", "false").lower() == "true",
            "parameters": self.class_model_parser.process_attributes(class_elem),
        }
        if min_val is not None and max_val is not None:
            class_info["min"]=str(min_val)
            class_info["max"]=str(max_val)
        aggregations = self.class_model_parser.process_aggregations(class_name)
        for child_class_name, min_val, max_val in aggregations:
            self.add_class(meta_info, child_class_name, min_val, max_val)
            class_info["parameters"].append({
                'name':child_class_name,
                'type':'class'
            })


        meta_info.append(dict(sorted(class_info.items())))

    def generate_file(self):
        meta_info = []
        root_class_name = self.class_model_parser.get_root_class_name()
        if root_class_name:
            self.add_class(meta_info, root_class_name)

        with open('out/meta.json', 'w', encoding='utf-8') as f:
            json.dump(meta_info, f, indent=4, ensure_ascii=False)

class ConfigXmlGenerator(ArtifactGenerator):
    def add_class(self, parent_elem, class_name):
        class_elem = self.class_elements[class_name]
        for attribute in class_elem.findall("Attribute"):
            attr_elem = ET.SubElement(parent_elem, attribute.get("name"))
            attr_elem.text = attribute.get("type")

        aggregations = self.class_model_parser.process_aggregations(class_name)
        for child_class_name, min_val, _ in aggregations:
            child_elem = ET.SubElement(parent_elem, child_class_name)
            self.add_class(child_elem, child_class_name)

    def indent_xml(self, elem, level=0):
        i = "\n" + level*"    "
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = i + "    "
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
            for elem in elem:
                self.indent_xml(elem, level+1)
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = i

    def generate_file(self):
        root_class_name = self.class_model_parser.get_root_class_name()
        if not root_class_name:
            raise ValueError("Root element not found in the XML")

        config = ET.Element(root_class_name)
        self.add_class(config, root_class_name)

        self.indent_xml(config)

        tree = ET.ElementTree(config)
        tree.write("out/config.xml", encoding="utf-8", xml_declaration=False)

def main():
    input_file = 'input/impulse_test_input.xml'
    class_model_parser = ClassModelParser(input_file)
    
    meta_json_generator = MetaJsonGenerator(class_model_parser)
    meta_json_generator.generate_file()
    
    config_xml_generator = ConfigXmlGenerator(class_model_parser)
    config_xml_generator.generate_file()

if __name__ == "__main__":
    main()
