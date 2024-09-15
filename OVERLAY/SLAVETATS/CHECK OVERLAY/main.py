import os
import json
from collections import defaultdict

def find_overlay_data_all(target_directory, export_directory, save_file):
    # สร้างโฟลเดอร์ถ้าไม่มี
    if not os.path.exists(export_directory):
        os.makedirs(export_directory)

    save_path = os.path.join(export_directory, save_file)
    
    # สร้าง dictionary เก็บข้อมูลไฟล์
    file_dict = {}

    # ค้นหาไฟล์ใน target directory
    for root, _, files in os.walk(target_directory):
        for file in files:
            # กรองเฉพาะไฟล์ที่เป็น .dds หรือ .png
            if file.endswith('.dds') or file.endswith('.png'):
                # แยกชื่อไฟล์และส่วนขยาย
                base_name, ext = os.path.splitext(file)

                # ถ้าไฟล์ลงท้ายด้วย _n, _s ให้ข้ามไปเลย
                if base_name.endswith(('_n', '_s')):
                    continue
                
                # ตรวจสอบชื่อหลักโดยไม่สนใจ suffix (_d)
                base_without_suffix = base_name
                if base_name.endswith('_d'):
                    base_without_suffix = base_name[:-2]  # ตัด '_d' ออก

                # ถ้าไฟล์หลักยังไม่มีใน dict ให้ใช้ไฟล์นี้ก่อน
                if base_without_suffix not in file_dict:
                    # ถ้าเป็นไฟล์ปกติ (ไม่ลงท้ายด้วย _d), ให้ใช้ทันที
                    if not base_name.endswith('_d'):
                        file_dict[base_without_suffix] = file
                    # ถ้าเป็นไฟล์ _d ให้ใช้กรณีไม่มีไฟล์หลัก
                    elif base_without_suffix not in file_dict:
                        file_dict[base_without_suffix] = file
    
    # บันทึก JSON ลงไฟล์
    with open(save_path, 'w') as json_file:
        json.dump(list(file_dict.values()), json_file, indent=4)

    print(f"Overlay JSON created and saved to {save_path}")

####################################################################################################################################################################
def prepare_overlay_json(import_directory, export_directory, read_file,export_file):
    data_json = set()  # ใช้ set เพื่อป้องกันการซ้ำ
    try:
        # เปิดไฟล์ JSON
        import_path = os.path.join(import_directory, read_file)
        export_path = os.path.join(export_directory, export_file)

        with open(import_path, 'r') as file:
            data = json.load(file)
        
        # ตรวจสอบว่าข้อมูลที่อ่านมาเป็น list หรือไม่
        if not isinstance(data, list):
            raise ValueError("JSON data should be a list of objects.")
        
        # ดึงชื่อไฟล์จาก field 'texture'
        for item in data:
            if 'texture' in item:
                texture_path = item['texture']
                file_name = os.path.basename(texture_path)  # ดึงชื่อไฟล์จาก path
                data_json.add(file_name)
        print(data_json)

        with open(export_path, 'w') as json_file:
            json.dump(list(data_json), json_file, indent=4)


    except FileNotFoundError:
        print(f"Error: The file at {import_path} was not found.")
    except json.JSONDecodeError:
        print(f"Error: The file at {import_path} is not a valid JSON.")
    except ValueError as e:
        print(f"Error: {e}")
    return data_json

# ฟังก์ชันเพื่อเทียบข้อมูลและหาข้อมูลที่ไม่ซ้ำกัน
def prepare_non_duplicate(export_directory, data_all_file, data_read_file, data_target_file):
    data_all_path = os.path.join(export_directory, data_all_file)
    data_read_path = os.path.join(export_directory, data_read_file)
    data_target_path = os.path.join(export_directory, data_target_file)

    try:
        # อ่านข้อมูลจากไฟล์ data_all.json
        with open(data_all_path, 'r') as file:
            data_all = json.load(file)

        # อ่านข้อมูลจากไฟล์ data_read.json
        with open(data_read_path, 'r') as file:
            data_read = json.load(file)

        # เปลี่ยนข้อมูลทั้งสองให้เป็น set เพื่อความสะดวกในการเทียบและหาค่าที่ไม่ซ้ำกัน
        set_all = set(data_all)
        set_read = set(data_read)

        # หาข้อมูลที่อยู่ใน data_all แต่ไม่อยู่ใน data_read
        unique_data = list(set_all - set_read)

        # เขียนข้อมูลที่ไม่ซ้ำกันลงในไฟล์ data_target.json
        with open(data_target_path, 'w') as output_file:
            json.dump(unique_data, output_file, indent=4)

        print(f"Data saved successfully to {data_target_path}")
    
    except FileNotFoundError as e:
        print(f"Error: {e}")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")


#################################################################################################################################
def find_section_and_area(file_name, lookup_data):
    # ค้นหาค่าที่ตรงกับชื่อไฟล์
    for entry in lookup_data:
        if entry['value'] in file_name:
            return entry['section'], entry['area']
    # ถ้าไม่พบ ให้ใช้ค่าเริ่มต้น
    return 'ILoveBBC', 'Body'

def create_overlay_json(final_directory,final_data,export_directory,export_data, lookup_data):
    try:
        # อ่านข้อมูลจาก overlay_non_duplicate.json
        final_path = os.path.join(final_directory, final_data)
        export_path = os.path.join(export_directory, export_data)

        with open(export_path, 'r') as file:
            data_json = json.load(file)

        final_data = []

        print(data_json)

        for file in data_json:
            name, ext = os.path.splitext(file)
            name_text = f'BBC_{name}'  # เพิ่ม prefix 'pzx_' ให้กับชื่อไฟล์

            # ค้นหา section และ area ตามค่าใน lookup_data
            section_text, area_text = find_section_and_area(file.lower(), lookup_data)

            texture_text = f"CaptiveTattoos\\JB\\{file}"

            # โครงสร้าง JSON สำหรับแต่ละไฟล์
            entry = {
                "name": name_text,
                "section": section_text,
                "area": area_text,
                "texture": texture_text
            }
            final_data.append(entry)

        # บันทึก JSON ลงไฟล์ export_overlay.json
        with open(final_path, 'w') as file:
            json.dump(final_data, file, indent=4)

        print(f"Overlay JSON created and saved to {export_path}")

    except Exception as e:
        print(f"Error: {e}")

def merge_data(import_directory, final_directory, old_file,new_file,final_file):
    try:
        old_path = os.path.join(import_directory, old_file)
        new_path = os.path.join(final_directory, new_file)


        with open(old_path, 'r') as file:
            old_json = json.load(file)

        with open(new_path, 'r') as file:
            new_json = json.load(file)

        old_json.extend(new_json)

        final_path = os.path.join(final_directory, final_file)
        with open(final_path, 'w') as file:
            json.dump(old_json, file, indent=4)




    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # ########################################### ESP
    # # # # FIND TEXT
    # ปรับใหม่
    target_directory = r"E:\SKYRIM MAKE MOD\TATTOO\CaptiveTattoos_BBC_RMO\Textures\Actors\Character\slavetats\CaptiveTattoos\JB"
    export_directory = os.path.join(os.getcwd(), 'export')
    import_directory = os.path.join(os.getcwd(), 'import')
    final_directory = os.path.join(os.getcwd(), 'final')

    if not os.path.exists(import_directory):
        os.makedirs(import_directory)
    if not os.path.exists(export_directory):
        os.makedirs(export_directory)
    if not os.path.exists(final_directory):
        os.makedirs(final_directory)

    # # # อ่าน Data ทั้งหมดก่อน มีการ คัด _n.dds _d.dds _s.dds
    # find_overlay_data_all(target_directory, export_directory, 'data_all.json')

    # # # อ่าน ใน Import 
    # prepare_overlay_json(import_directory, export_directory, 'CaptiveTattoos_Orignal.json', 'data_read.json')

    # # # นำข้อมูลทั้งหมด ที่คัดออก มาแล้ว ลบ กับ ที่่เหลืออยู่
    # prepare_non_duplicate(export_directory,'data_all.json','data_read.json','data_target.json')

    # # # Create the overlay JSON
    # # # # # Define lookup data
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

    # create_overlay_json(final_directory, 'export_data.json',export_directory,'data_target.json', lookup_data)
    
    merge_data(import_directory, final_directory,'CaptiveTattoos_Orignal.json','export_data.json','CaptiveTattoos.json')
    