import os
import json
# ใน system_pzx/lib/folder_manager.py
class FolderManager:
    def __init__(self, base_path):
        self.base_path = base_path

    def create_structure(self, folder_name):
        main_folder_path = os.path.join(self.base_path, folder_name)
        import_folder = os.path.join(main_folder_path, "import")
        export_folder = os.path.join(main_folder_path, "export")

        try:
            os.makedirs(import_folder, exist_ok=True)
            os.makedirs(export_folder, exist_ok=True)
            print(f"Folders created successfully under: {main_folder_path}")
        except Exception as e:
            print(f"Error creating folders: {e}")


    def read_folder_detail(self, folder_name):
        folder_path = os.path.join(self.base_path, folder_name)
        try:
            if os.path.exists(folder_path):
                return os.listdir(folder_path)
            else:
                print(f"Folder not found: {folder_path}")
                return []
        except Exception as e:
            print(f"Error reading folder: {e}")
            return []

    def read_file_txt(self, file_name):
        file_path = os.path.join(self.base_path, file_name)
        if not os.path.isfile(file_path):
            print(f"Error: File {file_path} does not exist.")
            return None
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                lines = file.readlines()
                # ลบ \n ออกจากแต่ละบรรทัด
                return [line.strip() for line in lines]
        except Exception as e:
            print(f"Error while reading the file: {e}")
            return None

    def create_text(self,path,text_name, content_list):
        file_name = f"{path}{text_name}.txt"
        file_path = os.path.join(self.base_path, file_name)

        try:
            with open(file_path, 'w', encoding='utf-8') as file:
                # เขียนเนื้อหาใน content_list ทีละบรรทัด
                for line in content_list:
                    file.write(f"{line}\n")
            print(f"สร้างไฟล์สำเร็จ: {file_path}")
        except Exception as e:
            print(f"เกิดข้อผิดพลาดในการสร้างไฟล์: {e}")


    def create_json(self,path,text_name, content):
        file_name = f"{path}{text_name}.json"
        file_path = os.path.join(self.base_path, file_name)
        try:
            with open(file_path, 'w', encoding='utf-8') as file:
                json.dump(content, file, ensure_ascii=False, indent=4)
            print(f"สร้างไฟล์สำเร็จ: {file_path}")
        except Exception as e:
            print(f"เกิดข้อผิดพลาดในการสร้างไฟล์: {e}")

    def read_json(self, path, text_name):
        """
        อ่านข้อมูลจากไฟล์ JSON และแปลงกลับเป็น Python object
        """
        file_name = f"{path}{text_name}.json"
        file_path = os.path.join(self.base_path, file_name)
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)  # แปลง JSON กลับเป็น Python object
            print(f"อ่านข้อมูลสำเร็จจาก: {file_path}")
            return data
        except Exception as e:
            print(f"เกิดข้อผิดพลาดในการอ่านไฟล์: {e}")
            return None
