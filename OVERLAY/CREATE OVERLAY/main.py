import os
import json

# ค้นหา section และ area ตาม lookup_data
def find_section_and_area(file_name, lookup_data):
    for entry in lookup_data:
        if entry['value'] in file_name:
            return entry['section'], entry['area']
    return 'BBC', 'Body'  # ค่าเริ่มต้นถ้าไม่พบ

# สร้าง JSON สำหรับ overlay files
def create_overlay_json(overlay_files, export_file_path, lookup_data):
    try:
        overlay_data = []

        for file in overlay_files:
            name, ext = os.path.splitext(file)
            name_text = f'BBC {name}'  # เพิ่ม prefix 'BBC' ให้กับชื่อไฟล์

            # ค้นหา section และ area ตาม lookup_data
            section_text, area_text = find_section_and_area(file, lookup_data)

            texture_text = f"CaptiveTattoos\\JB\\{file}"

            # โครงสร้าง JSON สำหรับแต่ละไฟล์
            overlay_entry = {
                "name": name_text,
                "section": section_text,
                "area": area_text,
                "texture": texture_text
            }
            overlay_data.append(overlay_entry)

        # บันทึก JSON ลงไฟล์ export_overlay.json
        with open(export_file_path, 'w') as file:
            json.dump(overlay_data, file, indent=4)

        print(f"Overlay JSON created and saved to {export_file_path}")

    except Exception as e:
        print(f"Error: {e}")

# ฟังก์ชันหลักในการรันโปรแกรม
def main(target_directory, export_directory, lookup_data):
    # สร้างโฟลเดอร์ถ้าไม่มี
    if not os.path.exists(export_directory):
        os.makedirs(export_directory)

    # ค้นหาไฟล์ใน target directory
    overlay_files = []
    for root, _, files in os.walk(target_directory):
        for file in files:
            if file.endswith('.dds') or file.endswith('.png'):  # กรองตามประเภทไฟล์ที่ต้องการ
                overlay_files.append(file)

    # กำหนด path สำหรับไฟล์ export
    export_file_path = os.path.join(export_directory, 'export_overlay.json')

    # สร้าง JSON สำหรับ overlay files
    create_overlay_json(overlay_files, export_file_path, lookup_data)

if __name__ == "__main__":
    # ตัวอย่างการใช้งาน
    target_directory = r"E:\SKYRIM MAKE MOD\TATTOO\CaptiveTattoos_BBC_RMO\Textures\Actors\Character\slavetats\CaptiveTattoos\JB"
    export_directory = os.path.join(os.getcwd(), 'export')

    # Define lookup data
    lookup_data = [
        {'section': 'BBC Belly', 'value': 'belly', 'area': 'Body'},
        {'section': 'BBC Womb', 'value': 'womb', 'area': 'Body'},
        {'section': 'BBC CapTats (Hands)', 'value': 'hands', 'area': 'Hands'}, 
        {'section': 'BBC Face', 'value': 'face', 'area': 'Face'}, 
        {'section': 'BBC CapTats (Front)', 'value': 'front', 'area': 'Body'} ,
        {'section': 'BBC CapTats (Back) ', 'value': 'back', 'area': 'Body'} ,
        {'section': 'BBC CapTats (Butt) ', 'value': 'butt', 'area': 'Body'} ,
        {'section': 'BBC CapTats (Breast) ', 'value': 'breast', 'area': 'Body'} ,
        {'section': 'BBC CapTats (Arm) ', 'value': 'arm', 'area': 'Body'} ,
        {'section': 'BBC CapTats (Leg) ', 'value': 'leg', 'area': 'Body'} ,
        {'section': 'BBC CapTats (Ankle) ', 'value': 'ankle', 'area': 'Body'} ,
        {'section': 'BBC CapTats (Ass) ', 'value': 'ass', 'area': 'Body'} , 
    ]

    # รันโปรแกรม
    main(target_directory, export_directory, lookup_data)
