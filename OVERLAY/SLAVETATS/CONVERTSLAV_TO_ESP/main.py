import os
import json

# Function to read JSON data
def read_json(path):
    try:
        with open(path, 'r') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print(f"Error: The file at {path} was not found.")
        return None
    except json.JSONDecodeError:
        print(f"Error: The file at {path} is not valid JSON.")
        return None

# Function to write JSON data
def write_json(path, data):
    try:
        with open(path, 'w') as file:
            json.dump(data, file, indent=4)
    except IOError as e:
        print(f"Error writing to file {path}: {e}")


def format_area(area):
    area_mapping = {
        "Body": "Body",
        "Face": "Face",
        "Hands": "Hands",
        "Feet": "Feet"
    }
    return area_mapping.get(area.title(), area)

def generate_text(entry):
    name = entry.get("name")
    texture = entry.get("texture").replace('\\', '\\\\')  # แทนที่ \ ด้วย \\
    # ใช้ escape \\\\ เพื่อให้เขียนออกมาเป็น \\ ในไฟล์
    return f'AddBodypaint("{name}","Actors\\\\Character\\\\Slavetats\\\\{texture}")\n'

def export_by_area(final_directory, data):
    # เก็บข้อมูลที่จะแปลงจากแต่ละ entry ลงใน dict ตามพื้นที่
    data_by_area = {}
    
    for entry in data:
        area = format_area(entry.get("area", "Body"))
        filename = f'export_{area.lower()}.txt'  # ตั้งชื่อไฟล์ตาม area และแปลงเป็น lowercase
        text = generate_text(entry)
        
        # เก็บข้อมูลไว้ใน dict โดยใช้ area เป็น key
        if filename not in data_by_area:
            data_by_area[filename] = []
        data_by_area[filename].append(text)
    
    # เขียนข้อมูลลงไฟล์ทั้งหมด
    for filename, texts in data_by_area.items():
        new_path = os.path.join(final_directory, filename)
        
        # เขียนข้อมูลลงไฟล์ (สร้างใหม่และเขียนข้อมูลทั้งหมดในครั้งเดียว)
        with open(new_path, 'w') as file:
            file.writelines(texts)


if __name__ == "__main__":
    target_directory = r"E:\SKYRIM MAKE MOD\TATTOO\CaptiveTattoos_BBC_RMO_PZX\Textures\Actors\Character\slavetats\CaptiveTattoos.json"
    export_directory = os.path.join(os.getcwd(), 'export')
    import_directory = os.path.join(os.getcwd(), 'import')
    final_directory = os.path.join(os.getcwd(), 'final')

    # Create directories if they don't exist
    for directory in [import_directory, export_directory, final_directory]:
        os.makedirs(directory, exist_ok=True)
        
    # Read the JSON data
    data = read_json(target_directory)

    if data is not None:
        print("Original Data:", data)

        # data_struct = {'data_body':[],'data_':[]}
        export_by_area(final_directory,data)
        # for entry in data:
        #     print()

