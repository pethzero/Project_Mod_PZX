import os
import json
from collections import defaultdict

def extract_json(json_file_path):
    data_json = []  # ใช้ set เพื่อป้องกันการซ้ำ
    try:
        # เปิดไฟล์ JSON
        with open(json_file_path, 'r') as file:
            data = json.load(file)
        
        # ตรวจสอบว่าข้อมูลที่อ่านมาเป็น list หรือไม่
        if not isinstance(data, list):
            raise ValueError("JSON data should be a list of objects.")
        
        # ดึงชื่อไฟล์จาก field 'texture'
        for item in data:
            data_json.append(item)
    
    except FileNotFoundError:
        print(f"Error: The file at {json_file_path} was not found.")
    except json.JSONDecodeError:
        print(f"Error: The file at {json_file_path} is not a valid JSON.")
    except ValueError as e:
        print(f"Error: {e}")
    
    return data_json

def extract_texture_names(json_file_path):
    texture_names = set()  # ใช้ set เพื่อป้องกันการซ้ำ
    try:
        # เปิดไฟล์ JSON
        with open(json_file_path, 'r') as file:
            data = json.load(file)
        
        # ตรวจสอบว่าข้อมูลที่อ่านมาเป็น list หรือไม่
        if not isinstance(data, list):
            raise ValueError("JSON data should be a list of objects.")
        
        # ดึงชื่อไฟล์จาก field 'texture'
        for item in data:
            if 'texture' in item:
                texture_path = item['texture']
                file_name = os.path.basename(texture_path)  # ดึงชื่อไฟล์จาก path
                texture_names.add(file_name)
    
    except FileNotFoundError:
        print(f"Error: The file at {json_file_path} was not found.")
    except json.JSONDecodeError:
        print(f"Error: The file at {json_file_path} is not a valid JSON.")
    except ValueError as e:
        print(f"Error: {e}")
    
    return texture_names

def save_to_export_folder(export_folder_path, texture_names):
    try:
        # สร้างโฟลเดอร์ export ถ้ายังไม่มี
        if not os.path.exists(export_folder_path):
            os.makedirs(export_folder_path)
        
        # บันทึกข้อมูลลงในไฟล์ JSON
        export_file_path = os.path.join(export_folder_path, 'export_data.json')
        with open(export_file_path, 'w') as file:
            json.dump(list(texture_names), file, indent=4)
        
        print(f"Data saved to {export_file_path}")
    
    except IOError as e:
        print(f"Error: {e}")

def process_directory(import_directory_path, export_directory_path):
    all_texture_names = set()
    
    try:
        # ตรวจสอบว่าไดเรกทอรีมีอยู่
        if not os.path.isdir(import_directory_path):
            raise ValueError(f"The directory {import_directory_path} does not exist.")
        
        # อ่านรายชื่อไฟล์ในไดเรกทอรี
        files = os.listdir(import_directory_path)
        
        # กรองเฉพาะไฟล์ JSON
        json_files = [f for f in files if f.endswith('.json')]
        
        for json_file in json_files:
            json_file_path = os.path.join(import_directory_path, json_file)
            
            # ดึงชื่อไฟล์และบันทึกลงใน set
            texture_names = extract_texture_names(json_file_path)
            all_texture_names.update(texture_names)
        
        # บันทึกข้อมูลทั้งหมดลงในโฟลเดอร์ export
        save_to_export_folder(export_directory_path, all_texture_names)
    
    except ValueError as e:
        print(f"Error: {e}")

def process_find_overlay(overlay_directory_path, textures_json_path, export_directory_path):
    try:
        # อ่าน textures.json เพื่อดึงรายชื่อไฟล์ที่มีอยู่แล้ว
        existing_json_names = extract_json(textures_json_path)
        overlay_files = []

        print(existing_json_names)
        # อ่านไฟล์ในโฟลเดอร์ overlay ที่กำหนด
        for root, _, files in os.walk(overlay_directory_path):
            for file in files:
                if file.endswith('.dds') or file.endswith('.png'):  # กรองตามประเภทไฟล์ที่ต้องการ
                    if file not in existing_json_names:  # ถ้าไฟล์ไม่ซ้ำ (เปรียบเทียบแบบ lower case)
                        print(file)
                        overlay_files.append(file)  # เพิ่มแค่ชื่อไฟล์ ไม่รวมเส้นทาง
        
        # บันทึกไฟล์ที่ไม่ซ้ำลงใน output_path
        export_file_path = os.path.join(export_directory_path, 'overlay_non_duplicate.json')
        with open(export_file_path, 'w') as file:
            json.dump(overlay_files, file, indent=4)
        
        print(f"Overlay textures saved to {export_file_path}")
    
    except Exception as e:
        print(f"Error: {e}")


def find_section_and_area(file_name, lookup_data):
    # ค้นหาค่าที่ตรงกับชื่อไฟล์
    for entry in lookup_data:
        if entry['value'] in file_name:
            return entry['section'], entry['area']
    # ถ้าไม่พบ ให้ใช้ค่าเริ่มต้น
    return 'ILoveBBC', 'Body'

def create_overlay_json(overlay_non_duplicate_path, export_file_path, lookup_data):
    try:
        # อ่านข้อมูลจาก overlay_non_duplicate.json
        with open(overlay_non_duplicate_path, 'r') as file:
            overlay_files = json.load(file)

        overlay_data = []

        for file in overlay_files:
            name, ext = os.path.splitext(file)
            name_text = f'BBC_{name}'  # เพิ่ม prefix 'pzx_' ให้กับชื่อไฟล์

            # ค้นหา section และ area ตามค่าใน lookup_data
            section_text, area_text = find_section_and_area(file.lower(), lookup_data)

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


def find_remove(overlay_non_duplicate_path, export_directory_path):
    try:
        # อ่านข้อมูลจาก overlay_non_duplicate.json
        with open(overlay_non_duplicate_path, 'r') as file:
            data = json.load(file)

        texture_count = defaultdict(int)
        duplicates = []
        unique_textures = []
        
        # นับจำนวนการปรากฏของแต่ละ texture
        for item in data:
            texture = item['texture']
            texture_count[texture] += 1
            if texture_count[texture] == 2:  # เจอครั้งที่ 2 แปลว่ามันซ้ำ
                duplicates.append(item)
            if texture_count[texture] == 1:  # เจอครั้งแรก
                unique_textures.append(item)
        
        # บันทึกตัวซ้ำไปยัง remove_duplicate.json
        remove_duplicate_path = os.path.join(export_directory_path, 'remove_duplicate.json')
        with open(remove_duplicate_path, 'w') as file:
            json.dump(duplicates, file, indent=4)
        print(f"Duplicates saved to {remove_duplicate_path}")
        
        # บันทึกตัวไม่ซ้ำไปยัง z_export_tattoo.json
        z_export_tattoo_path = os.path.join(export_directory_path, 'z_export_tattoo.json')
        with open(z_export_tattoo_path, 'w') as file:
            json.dump(unique_textures, file, indent=4)
        print(f"Unique textures saved to {z_export_tattoo_path}")

    except FileNotFoundError:
        print(f"Error: The file at {overlay_non_duplicate_path} was not found.")
    except json.JSONDecodeError:
        print(f"Error: The file at {overlay_non_duplicate_path} is not a valid JSON.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # Path to the import and export directories
    import_directory_path = os.path.join(os.getcwd(), 'import')
    export_directory_path = os.path.join(os.getcwd(), 'export')

    overlay_directory_path = r"E:\SKYRIM MAKE MOD\TATTOO\CaptiveTattoos_BBC_RMO\Textures\Actors\Character\slavetats\CaptiveTattoos\JB"
    textures_json_path = os.path.join(export_directory_path, 'export_data.json')

    overlay_non_duplicate_path = os.path.join(export_directory_path, 'overlay_non_duplicate.json')
    export_overlay_path = os.path.join(export_directory_path, 'export_overlay.json')

    import_data_overlay_path = os.path.join(import_directory_path, "CaptiveTattoos.json")
    
    # # Export
    # process_directory(import_directory_path, export_directory_path)

    # # # FIND JOSN
    # process_find_overlay(overlay_directory_path, textures_json_path, export_directory_path)

    # # # Define lookup data
    # lookup_data = [
    #     {'section': 'BBC Belly', 'value': 'belly', 'area': 'Body'},
    #     {'section': 'BBC Womb', 'value': 'womb', 'area': 'Body'},
    #     {'section': 'BBC CapTats (Hands)', 'value': 'hands', 'area': 'Hands'}, 
    #     {'section': 'BBC Face', 'value': 'face', 'area': 'Face'}, 
    #     {'section': 'BBC CapTats (Front)', 'value': 'front', 'area': 'Body'} ,
    #     {'section': 'BBC CapTats (Back) ', 'value': 'back', 'area': 'Body'} ,
    #     {'section': 'BBC CapTats (Butt) ', 'value': 'butt', 'area': 'Body'} ,
    #     {'section': 'BBC CapTats (Breast) ', 'value': 'breast', 'area': 'Body'} ,
    #     {'section': 'BBC CapTats (Arm) ', 'value': 'arm', 'area': 'Body'} ,
    #     {'section': 'BBC CapTats (Leg) ', 'value': 'leg', 'area': 'Body'} ,
    #     {'section': 'BBC CapTats (Ankle) ', 'value': 'ankle', 'area': 'Body'} ,
    #     {'section': 'BBC CapTats (Ass) ', 'value': 'ass', 'area': 'Body'} , 
    # ]
    # # Create the overlay JSON
    # create_overlay_json(overlay_non_duplicate_path, export_overlay_path, lookup_data)
   
    # เรียกใช้ฟังก์ชัน find_remove
    find_remove(import_data_overlay_path, export_directory_path)