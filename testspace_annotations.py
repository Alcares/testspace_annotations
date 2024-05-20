from pathlib import Path
from lxml import etree as ET


def pytest_addoption(parser):
    parser.addoption("--dirpath", action="store", default=None,
                     help="Path to the directory containing the XML file and attachments")


def pytest_sessionfinish(session, exitstatus):
    dir_path = session.config.getoption("--dirpath")
    if dir_path:
        xml_file_path = Path(dir_path / "test.xml")
        attachment_path = Path(dir_path / "annotations")
        modify_xml_report(xml_file_path, attachment_path)


def modify_xml_report(xml_file, attachment_path):
    parser = ET.XMLParser(strip_cdata=False)
    tree = ET.parse(xml_file, parser)
    root = tree.getroot()

    for testcase in root.iter('testcase'):
        test_name = testcase.get('name')
        class_name = testcase.get('classname').split(".")[-1]
        final_name = class_name + test_name + ".html"
        attachment_file = attachment_path / final_name
        if attachment_file.is_file():
            system_out = testcase.find('system-out')
            attachment_string = f"[[ATTACHMENT|{attachment_file}]]\n"
            system_out.text += attachment_string

    tree.write(xml_file, encoding='utf-8', xml_declaration=True)
