import json
import os

# สร้างตัวแปรเก็บข้อมูล
selected_data = []

# อ่านไฟล์ input.txt
with open('pose_input.txt', 'r') as file:
    # อ่านข้อมูลทีละบรรทัด
    for line in file:
        # แยกข้อความโดยใช้ช่องว่างเป็นตัวแยก
        parts = line.split(' ')
        selected_data.append(parts[2])

s_pose = 'fuwa'
s_name = 'Pose Fuwa'
output_file = 'pose_output.txt'
data_per_round = 81

# สร้าง format_pose โดยแบ่งข้อมูลลงในรอบตาม data_per_round
format_pose = {}
current_pose = 1
pose_data = []
for i, data in enumerate(selected_data, start=1):
    # เพิ่มข้อมูลในรอบนี้
    # OLD
    # pose_data.append(f'"{s_name}{i}|{data.strip()}"')
    #JSON
    pose_data.append(f'{s_name}{i}|{data.strip()}')   
    # ถ้าข้อมูลใน pose_data มีมากกว่าหรือเท่ากับ data_per_round หรือเป็นข้อมูลสุดท้าย
    if len(pose_data) >= data_per_round or i == len(selected_data):
        # สร้าง key ใหม่โดยใช้ชื่อ "collygonpose" ตามจำนวนรอบ
        new_pose = f"{s_pose}{current_pose}"
        # เพิ่มข้อมูลใน format_pose
        format_pose[new_pose] = pose_data.copy()

        # รีเซ็ตรายการข้อมูลในรอบ
        pose_data = []
        # เพิ่มรอบ
        current_pose += 1

# # พิมพ์ผลลัพธ์หลังการจัดรูปแบบ
# OLD
# with open(output_file, 'w') as file:
#     # สร้างรายการใหม่
#     for pose, data in format_pose.items():
#         file.write(f'"{pose}": [{", ".join(data)}],\n')
    # print(f"'{pose}': {data}")

json_pose = 'fuwa'
selectedpose = []
packnames = []
stringList_dict = {}

for pose, data in format_pose.items():
    selectedpose.append(0)
    packnames.append(pose)
    stringList_dict[pose] = data

# สร้างข้อมูลตามโครงสร้างที่ต้องการ
structured = {
    "int": {
        "selectedpack": 0
    },
    "intList": {
        "selectedpose": selectedpose
    },
    "string": {
        "name": json_pose
    },
    "stringList": {
        **stringList_dict,
        "packnames": packnames
    }
}

# แปลงข้อมูลเป็น JSON
json_data = json.dumps(structured, indent=4)

# เส้นทางที่ต้องการเขียนไฟล์
# ตั้งชื่อไฟล์ output
output_filename = f'{json_pose}.json'

output_directory = os.path.join('SKSE', 'Plugins', 'PoserHotKeys', 'PoserData')
os.makedirs(output_directory, exist_ok=True)  # สร้างไดเรกทอรีหากยังไม่มี

# เส้นทางไฟล์เต็ม
output_file = os.path.join(output_directory, output_filename)

# เขียน JSON ลงในไฟล์
with open(output_file, 'w') as file:
    file.write(json_data)

# แสดงผล JSON
# print(json_data)