from models.student_record import StudentRecord
from services.xml_service import XmlService


def test_xml_service_save_and_load(tmp_path):
    service = XmlService()
    records = [
        StudentRecord("Иванов Иван Иванович", "ПИ-21", [1, 2, 0, 3, 1, 4, 2, 0, 1, 2]),
        StudentRecord("Петров Петр Петрович", "ПИ-22", [2, 2, 2, 2, 2, 2, 2, 2, 2, 2]),
    ]

    file_path = tmp_path / "students.xml"

    service.save(records, str(file_path))
    loaded_records = service.load(str(file_path))

    assert len(loaded_records) == 2
    assert loaded_records[0].full_name == "Иванов Иван Иванович"
    assert loaded_records[0].group == "ПИ-21"
    assert loaded_records[0].social_work == [1, 2, 0, 3, 1, 4, 2, 0, 1, 2]
    assert loaded_records[1].total_social_work == 20


def test_xml_service_save_creates_xml_file(tmp_path):
    service = XmlService()
    records = [
        StudentRecord("Иванов Иван Иванович", "ПИ-21", [1] * 10),
    ]

    file_path = tmp_path / "students.xml"
    service.save(records, str(file_path))

    content = file_path.read_text(encoding="utf-8")
    assert "<students>" in content
    assert "<student>" in content
    assert "<full_name>Иванов Иван Иванович</full_name>" in content


def test_xml_service_load_skips_student_with_incorrect_semesters(tmp_path):
    content = """<?xml version="1.0" encoding="utf-8"?>
<students>
    <student>
        <full_name>Иванов Иван Иванович</full_name>
        <group>ПИ-21</group>
        <social_work>
            <semester>1</semester>
            <semester>1</semester>
            <semester>1</semester>
        </social_work>
    </student>
</students>
"""
    file_path = tmp_path / "bad_students.xml"
    file_path.write_text(content, encoding="utf-8")

    service = XmlService()
    loaded_records = service.load(str(file_path))

    assert loaded_records == []