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


    # path_import = f"002_create_fnis_list/import/"
    # file_name = 'example1'
    # data = MANAGER.read_json(path_import,file_name)
    # print(data)
    # HKEYMANGER = HotkeyManager(data)
    # head = "b -a"  
    # content_list = HKEYMANGER.fnis_list(head)   
    # print(content_list)
    # path_export = f"002_create_fnis_list/export/"
    # name_text = f"FNIS_SensualDancer_List"
    # text_write =  MANAGER.create_text(path_export,name_text,content_list)


    # ########################## สร้าง DICT อ่านจาก FNIS ##########################  
        # path_import = f"003_dict_by_fnis_list/import/FNIS_SensualDancer_List.txt"
    # data = MANAGER.read_file_txt(path_import)
    
    # selected_data = []
    # for line in data:
    #     # แยกข้อความโดยใช้ช่องว่างเป็นตัวแยก
    #     parts = line.split(' ')
    #     selected_data.append(parts[2])
        
    # print(selected_data)
    
    
    
    # ########################## 004_duplicate ##########################
    folder_name = "004_duplicate"
    folder_create =  MANAGER.create_structure_ie(folder_name)
    
    # folder_name = "004_duplicate/Target"
    MANAGER.create_structure("004_duplicate/Target")
    MANAGER.create_structure("004_duplicate/Source")
    
    
    sample_target = {
            "a.txt": "Hello from Target - 1",
            "b.txt": "Hello from Target - 2",
            "c.txt": "Hello from Target - 1",
            "d.txt": "Hello from Target - 4",
            "e.txt": "Hello from Target - 5",
    }
    
    MANAGER.create_sample_files("004_duplicate/Source",sample_target)
    
    param = MANAGER.check_duplicates_in_target("004_duplicate/Source")
    fpath = f"004_duplicate/export/"
    fname = f"example1"
    example4 =  MANAGER.create_json(fpath,fname,param)
    print(example4)
    
    

