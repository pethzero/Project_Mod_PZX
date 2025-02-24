import os

class HotkeyManager:
    def __init__(self, base_list):
        self.base_list = base_list 

    def fnis_list(self, head):
        return [f"{head} {item.replace('.hkx', '').lower()} {item}" for item in self.base_list]
    
    
    def process_pose(self, package_name, pose_name,param, round=81):
        data = {}
        dt_list = []
        current_pose = 1
        
        for i, entry in enumerate(param, start=1):
            dt_list.append(f'{pose_name}{i}|{entry.strip()}')
            
            # เช็คว่าถึงจำนวนข้อมูลต่อรอบหรือข้อมูลหมดแล้ว
            if len(dt_list) >= round or i == len(param):
                new_pose = f"{package_name}{current_pose}"
                data[new_pose] = dt_list.copy()
                dt_list = []
                current_pose += 1
        return data