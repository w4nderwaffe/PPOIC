from xml.dom.minidom import Document
from xml.sax import ContentHandler, parse

from models.student_record import StudentRecord


class StudentRecordSaxHandler(ContentHandler):
    def __init__(self):
        super().__init__()
        self.records = []
        self.current_tag = ""
        self.current_name = ""
        self.current_group = ""
        self.current_semesters = []
        self.buffer = ""

    def startElement(self, name, attrs):
        self.current_tag = name
        self.buffer = ""
        if name == "student":
            self.current_name = ""
            self.current_group = ""
            self.current_semesters = []

    def characters(self, content):
        self.buffer += content

    def endElement(self, name):
        value = self.buffer.strip()

        if name == "full_name":
            self.current_name = value
        elif name == "group":
            self.current_group = value
        elif name == "semester":
            if value:
                self.current_semesters.append(int(value))
        elif name == "student":
            if len(self.current_semesters) == 10:
                record = StudentRecord(
                    full_name=self.current_name,
                    group=self.current_group,
                    social_work=self.current_semesters
                )
                self.records.append(record)

        self.current_tag = ""
        self.buffer = ""


class XmlService:
    ROOT_TAG = "students"

    def save(self, records: list[StudentRecord], file_path: str):
        document = Document()
        root = document.createElement(self.ROOT_TAG)
        document.appendChild(root)

        for record in records:
            student_element = document.createElement("student")

            full_name_element = document.createElement("full_name")
            full_name_element.appendChild(document.createTextNode(record.full_name))
            student_element.appendChild(full_name_element)

            group_element = document.createElement("group")
            group_element.appendChild(document.createTextNode(record.group))
            student_element.appendChild(group_element)

            social_work_element = document.createElement("social_work")
            for value in record.social_work:
                semester_element = document.createElement("semester")
                semester_element.appendChild(document.createTextNode(str(value)))
                social_work_element.appendChild(semester_element)

            student_element.appendChild(social_work_element)
            root.appendChild(student_element)

        with open(file_path, "w", encoding="utf-8") as file:
            file.write(document.toprettyxml(indent="    ", encoding=None))

    def load(self, file_path: str) -> list[StudentRecord]:
        handler = StudentRecordSaxHandler()
        parse(file_path, handler)
        return handler.records