import os
import json
import re

# ฟังก์ชันหลักในการรันโปรแกรม
# def find_overlay_data_all(target_directory, export_directory, save_file):
#     # สร้างโฟลเดอร์ถ้าไม่มี
#     if not os.path.exists(export_directory):
#         os.makedirs(export_directory)

#     save_path = os.path.join(export_directory, save_file)
    
#     # ค้นหาไฟล์ใน target directory
#     overlay_files = []
#     for root, _, files in os.walk(target_directory):
#         for file in files:
#             if file.endswith('.dds') or file.endswith('.png'):  # กรองตามประเภทไฟล์ที่ต้องการ
#                 overlay_files.append(file)
    
#     # บันทึก JSON ลงไฟล์
#     with open(save_path, 'w') as file:
#         json.dump(overlay_files, file, indent=4)

#     print(f"Overlay JSON created and saved to {save_path}")
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

# ฟังก์ชันเพื่อเตรียมข้อมูล overlay และจัดการกับไฟล์ input/output
def prepare_overlay(import_directory, export_directory, input_file, output_file):
    input_path = os.path.join(import_directory, input_file)
    output_path = os.path.join(export_directory, output_file)

    # ตรวจสอบว่ามีโฟลเดอร์ export หรือไม่ ถ้าไม่มีให้สร้าง
    if not os.path.exists(export_directory):
        os.makedirs(export_directory)

    # สร้าง set เพื่อเก็บค่าไฟล์ .dds ที่ไม่ซ้ำกัน
    unique_textures = set()

    try:
        # อ่านข้อมูลจาก input file
        with open(input_path, 'r') as file:
            lines = file.readlines()

            # วนลูปแต่ละบรรทัดของไฟล์ input
            for line in lines:
                # ใช้ regex เพื่อค้นหาไฟล์ที่ลงท้ายด้วย .dds
                match = re.search(r'\\([\w_]+\.dds)', line)
                if match:
                    # ดึงชื่อไฟล์ที่ตรงกับ pattern .dds
                    file_name = match.group(1)
                    # เพิ่มชื่อไฟล์เข้า set เพื่อตรวจสอบว่าไม่ซ้ำกัน
                    unique_textures.add(file_name)

        # แปลง set เป็น list เพื่อบันทึกเป็นไฟล์ JSON
        unique_textures_list = list(unique_textures)

        # เขียนข้อมูลลงในไฟล์ JSON
        with open(output_path, 'w') as output_file:
            json.dump(unique_textures_list, output_file, indent=4)
        
        print(f"Data saved successfully to {output_path}")
    
    except FileNotFoundError:
        print(f"Error: {input_file} not found in {import_directory}")
    except Exception as e:
        print(f"An error occurred: {e}")

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

# ฟังก์ชันเพื่อจัดการและสร้าง JSON ตามที่ต้องการ
def create_custom_json(export_directory, data_target_file, data_final_file, text_head):
    # เตรียมผลลัพธ์ในรูปแบบของลิสต์ที่มีหลาย 'title'
    result = [
        {
            'title': 'Body',
            'details': []
        },
        {
            'title': 'Face',
            'details': []
        },
        {
            'title': 'Hand',
            'details': []
        },
        {
            'title': 'Feet',
            'details': []
        }
    ]

    # สร้างดิกชันนารีเพื่อจัดเก็บ 'details' ตาม 'title'
    title_map = {item['title'].lower(): item['details'] for item in result}

    try:
        # อ่านข้อมูลจากไฟล์ data_target.json
        data_target_path = os.path.join(export_directory, data_target_file)
        with open(data_target_path, 'r') as file:
            data_target = json.load(file)

        # ตรวจสอบว่า data_target เป็นลิสต์ของไฟล์ .dds
        if not isinstance(data_target, list):
            raise ValueError("data_target JSON file should be a list.")

        # ตรวจสอบและจัดกลุ่มไฟล์ตาม 'title'
        for item in data_target:
            # ดึงชื่อไฟล์และทำให้เป็น lowercase เพื่อการค้นหาที่ไม่ case-sensitive
            file_name = item.split('.')[0].lower()

            # ค้นหาว่าชื่อไฟล์มีคำหลักจาก title หรือไม่
            matched = False
            for title in title_map:
                if title in file_name:
                    title_map[title].append({
                        'head': title.capitalize(),
                        'text': item
                    })
                    matched = True
                    break

            # ถ้าไม่ตรงกับ title_map ให้เป็น 'Body'
            if not matched:
                new_head = f'{text_head}{file_name}'
                title_map['body'].append({
                    'head': new_head,
                    'text': item
                })

        # แปลง title_map เป็นลิสต์ของดิกชันนารี
        final_result = [item for item in result if item['details']]

        # เขียนข้อมูลที่ไม่ซ้ำกันลงในไฟล์ data_final.json
        data_final_path = os.path.join(export_directory, data_final_file)
        with open(data_final_path, 'w') as output_file:
            json.dump(final_result, output_file, indent=4)

        print(f"Data saved successfully to {data_final_path}")

    except FileNotFoundError as e:
        print(f"Error: {e}")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    
# ฟังก์ชันเพื่อสร้างไฟล์ export_body.txt จาก data_final.json
def create_export_txt(export_directory, final_directory, input_file, output_prefix):
    export_path = os.path.join(export_directory, input_file)
    
    # ตรวจสอบว่า final_directory มีอยู่แล้วหรือไม่ ถ้ายังไม่มี ให้สร้างมันขึ้นมา
    if not os.path.exists(final_directory):
        os.makedirs(final_directory)

    try:
        # อ่านข้อมูลจากไฟล์ data_final.json
        with open(export_path, 'r') as file:
            data_final = json.load(file)

        # ตรวจสอบว่า data_final เป็นลิสต์ของดิกชันนารี
        if not isinstance(data_final, list):
            raise ValueError("data_final JSON file should be a list.")

        # สร้างไฟล์ output สำหรับแต่ละ title
        for item in data_final:
            title = item['title'].lower()
            output_file = f'{output_prefix}{title}.txt'  # สร้างชื่อไฟล์ตาม title
            final_path = os.path.join(final_directory, output_file)

            # เขียนข้อมูลลงในไฟล์ที่สร้าง
            with open(final_path, 'w') as txt_file:
                location = "Actors\\Character\\Slavetats\\CaptiveTattoos\\JB\\"
                for detail in item['details']:
                    head = detail['head']
                    text = detail['text']
                    line = f'AddBodypaint("{head}","{location}{text}")\n'
                    txt_file.write(line)
        
            print(f"Export file created successfully at {final_path}")

    except FileNotFoundError as e:
        print(f"Error: {e}")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # ตัวอย่างการใช้งาน
    target_directory = r"E:\SKYRIM MAKE MOD\TATTOO\CaptiveTattoos_BBC_RMO\Textures\Actors\Character\slavetats\CaptiveTattoos\JB"
    export_directory = os.path.join(os.getcwd(), 'export')
    import_directory = os.path.join(os.getcwd(), 'import')
    final_directory = os.path.join(os.getcwd(), 'final')

    # รันโปรแกรม
    find_overlay_data_all(target_directory, export_directory, 'data_all.json')

    prepare_overlay(import_directory, export_directory, 'data_input.txt', 'data_read.json')

    prepare_non_duplicate(export_directory,'data_all.json','data_read.json','data_target.json')


    # สร้าง JSON และแสดงผล
    custom_json = create_custom_json(export_directory,'data_target.json','data_final.json','BBC_')

    # ตัวอย่างการเรียกใช้ฟังก์ชัน
    final_directory = os.path.join(os.getcwd(), 'final')
    create_export_txt(export_directory,final_directory, 'data_final.json', 'export_')
