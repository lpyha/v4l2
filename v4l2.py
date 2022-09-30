import re
import subprocess
import cv2

class MyV4l2():
    
    def __init__(self) -> None:
        self.camera_list = []
        self.camera_settings_list = []


    def get_camera_list(self) -> list:
        out = subprocess.getoutput("v4l2-ctl --list-devices")
        splitOut = out.splitlines()
        for i in range(len(splitOut)):
            if (splitOut[i][-1:] == ':'):
                cap = cv2.VideoCapture(int(splitOut[i+1][11:]))
                if (cap.isOpened() == True):
                    self.camera_list.append([splitOut[i], splitOut[i+1][11:]])
        return self.camera_list


    def get_camera_settings(self, camera_id: int) -> list:
        cmd_out = subprocess.getoutput(f"v4l2-ctl -d /dev/video{camera_id} -L")
        cmd_array = cmd_out.splitlines()
        for i in range(len(cmd_array)):
            tmp = cmd_array[i].split()
            for j in range(len(tmp)):
                res = re.match("value=", tmp[j])
                if res:
                    self.camera_settings_list.append(tmp)
        return self.camera_settings_list


    def set_default_settings(self, camera_id: int, setting_list: list) -> None:
        for i in range(len(setting_list)):
            for j in range(len(setting_list[i])):
                res = re.match("default=", setting_list[i][j])
                if res:
                    default_value = re.sub(r'[^0-9]', '', setting_list[i][j])
                    subprocess.run(["v4l2-ctl", "-d", f"/dev/video{camera_id}", "-c", f"{setting_list[i][0]}={default_value}"])

    
if __name__ == "__main__":
    v4l2 = MyV4l2()
    camera_list = v4l2.get_camera_list()
    print("*********************************************")
    print("<YOU CAN OPEN CAMERA BY INDEX>")
    for i in range(len(camera_list)):
        print(f"\n{camera_list[i]}\n")
        print("*********************************************")
    camera_id = int(input("camera_id>>>"))
    camera_settings_list = v4l2.get_camera_settings(camera_id)
    for i in range(len(camera_settings_list)):
        print(camera_settings_list[i])
    print("*********************************************")
    flag = ord(input("Initialize the camera settings?[y/n]\n>>"))
    if flag == ord('y'):
        v4l2.set_default_settings(camera_id, camera_settings_list)
        print("success")
    else:
        print("exit")