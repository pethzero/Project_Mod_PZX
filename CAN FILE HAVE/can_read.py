import json
import os

def process_files(import_folder, json_file_path, output_file):
    # อ่าน JSON จากไฟล์
    with open(json_file_path, 'r') as json_file:
        data = json.load(json_file)

    # ดึงข้อมูลจาก stringList
    string_list = data.get('stringList', {})
    
    # สร้างเซ็ตของชื่อที่พบใน JSON (เอาชื่อหลัง '|')
    json_names = set()
    for group, items in string_list.items():
        for entry in items:
            parts = entry.split('|')
            if len(parts) > 1:  # ตรวจสอบว่ามีตัวแบ่ง '|'
                name = parts[1]  # เอาชื่อที่อยู่หลัง '|'
                json_names.add(name)

    # สร้างรายการสำหรับไฟล์ที่มีและไม่มีข้อมูล
    have_data = []
    not_have_data = []

    # ตรวจสอบไฟล์ในโฟลเดอร์ import
    for file_name in os.listdir(import_folder):
        if file_name.endswith('.hkx'):
            base_name = file_name.split('.')[0]
            if base_name in json_names:
                have_data.append(base_name)
            else:
                not_have_data.append(base_name)

    # สร้างผลลัพธ์
    result = {
        "have_data": have_data,
        "not_have_data": not_have_data
    }

    # บันทึกผลลัพธ์ลงในไฟล์ data.json
    with open(output_file, 'w') as output_json_file:
        json.dump(result, output_json_file, indent=4)

# กำหนดพาธของโฟลเดอร์และไฟล์
import_folder = 'import'
json_file_path = 'read.json'
output_file = 'data.json'

# เรียกใช้งานฟังก์ชัน
process_files(import_folder, json_file_path, output_file)
