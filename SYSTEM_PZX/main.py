if __name__ == "__main__":
    import os
    from lib.folder_manager import FolderManager
    from lib.hotkey_manager import HotkeyManager

    # Base path ของ system_pzx
    BASE_PATH = os.path.dirname(os.path.abspath(__file__))
    MANAGER = FolderManager(BASE_PATH)
    ########################## CREATE FOLDER  ##########################
    # folder_name = "001_read_hkx"
    # folder_create =  MANAGER.create_structure_ie(folder_name)
    # # # อ่านเนื้อหาในโฟลเดอร์
    # path_import = f"001_read_hkx/import/"
    # param = MANAGER.read_folder_detail(path_import)
    # print(f"Contents of {folder_name}: {param}")

    # fpath = f"001_read_hkx/export/"
    # fname = f"example1"
    # example1 =  MANAGER.create_json(fpath,fname,param)
    

    # ########################## สร้าง Fnis list ##########################
    # folder_name = "002_create_fnis_list"
    # folder_create =  MANAGER.create_structure_ie(folder_name)    


    # file_name = f"002_create_fnis_list/import/example1.json"
    # data = MANAGER.read_json(file_name)
    # print(data)
    # HKEYMANGER = HotkeyManager(data)
    # head = "b -a"  
    # content_list = HKEYMANGER.fnis_list(head)   
    # print(content_list)
    # name_text = f"002_create_fnis_list/export/FNIS_SensualDancer_List.txt"
    # text_write =  MANAGER.create_text(name_text,content_list)


    # ########################## สร้าง DICT อ่านจาก FNIS ##########################  
    # file_name = f"003_dict_by_fnis_list/import/FNIS_SensualDancer_List.txt"
    # data = MANAGER.read_file_txt(file_name)
    
    # selected_data = []
    # for line in data:
    #     # แยกข้อความโดยใช้ช่องว่างเป็นตัวแยก
    #     parts = line.split(' ')
    #     selected_data.append(parts[2])
        
    # print(selected_data)
    # name_text = f"003_dict_by_fnis_list/export/fnis_list.json"
    # MANAGER.create_json(name_text,selected_data)
    # ########################## 006_HotKey ##########################
    folder_name =  f"006_hotkey_create"
    folder_create =  MANAGER.create_structure_ie(folder_name)
    
    path = f"006_hotkey_create\\import\\fnis_list.json"
    param = MANAGER.read_json(path)
    
    # print(param)
    HKM = HotkeyManager(None)
    content_list = HKM.process_pose('Joe','Pose Joe',param,10)
    print(content_list)
    # for i, data in enumerate(param, start=1):
    #     pose_data.append(f'{s_name}{i}|{data.strip()}')   
    #     if len(pose_data) >= data_per_round or i == len(param):
    #         new_pose = f"{s_pose}{current_pose}"
    #         format_pose[new_pose] = pose_data.copy()
    #         pose_data = []
    #         current_pose += 1
        
    # print(format_pose)
    # print(pose_data)
    # ########################## 004_duplicate ##########################
    # folder_name = "004_duplicate_read"
    # folder_create =  MANAGER.create_structure_ie(folder_name)
    # MANAGER.create_structure("004_duplicate/import")
    # sample_target = {
    #         "a.txt": "Hello from Target - 1",
    #         "b.txt": "Hello from Target - 2",
    #         "c.txt": "Hello from Target - 1",
    #         "d.txt": "Hello from Target - 4",
    #         "e.txt": "Hello from Target - 5",
    # }
    
    # MANAGER.create_sample_files("004_duplicate_read/import",sample_target)
    # param = MANAGER.check_duplicates_in_target("004_duplicate_read/import")
    # print(param)
    # fname = f"004_duplicate_read/export/example4.json"
    # example4 =  MANAGER.create_json(fname,param)
    # param = MANAGER.create_structure("004_duplicate_read/Target")

    
    # ########################## 005_duplicate_to ##########################  
    # folder_name = "005_duplicate_move"
    # folder_create =  MANAGER.create_structure_ie(folder_name)

    # file_name = '005_duplicate_move/import/example4.json'
    # param = MANAGER.read_json(file_name)
    # print(param)
    # MANAGER.duplicates_to_folder("005_duplicate_move/export","folder/txt",param, action="copy")
    # print(example4)
    
    


    # ########################## 006_HOTKEY ##########################