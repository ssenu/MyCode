import tkinter as tk
from tkinter import filedialog, messagebox
import sys
import threading
import cv2
import numpy as np
import mss
import pyautogui
import keyboard
import time
import json
import os

CONFIG_FILE = "메크로 설정파일.json"
image_path = None
scroll_value = 5
running = False
stop = False
loopNum = 1

def save_config():
    data = {
        "image_path": image_path,
        "scroll_value": scroll_value
    }

    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
def load_config():
    global image_path, scroll_value

    if not os.path.exists(CONFIG_FILE):
        return

    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    image_path = data.get("image_path", None)
    scroll_value = data.get("scroll_value", 5)

# print를 GUI 창으로 보내는 클래스
class RedirectText:
    def __init__(self, text_widget):
        self.output = text_widget

    def write(self, string):
        self.output.insert(tk.END, string)
        self.output.see(tk.END)

    def flush(self):
        pass

def upload_photo():
    global image_path
    filepath = filedialog.askopenfilename(
        title="사진 선택",
        filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp")]
    )

    if filepath:
        image_path = filepath
        file_label.config(text=filepath, fg="black")
        print("선택된 파일:", filepath)

        save_config()
    else:
        file_label.config(text="선택 안됨", fg="gray")
def stop_program():
    global stop
    global running
    global loopNum
    print("프로그램을 종료합니다.")
    stop = True
    running = False
    loopNum = 1
def run_program():
    global running
    global stop
    global scroll_value
    stop = False
    scroll_value = int(scroll_spin.get())  
    save_config()              
    if running:
        print("이미 실행 중입니다.")
        return
    else:
        print("프로그램을 실행합니다.")
        print("...")
    running = True
    thread = threading.Thread(target=clickLoop)
    thread.start()
def clickLoop():
    global stop
    global loopNum
    template = cv2.imread(image_path, 0)
    if image_path is None:
        print("이미지를 먼저 업로드")
        stop_program()
        return
    if template is None:
        print("이미지 로드 실패")
        stop_program()
        return
    w, h = template.shape[::-1]
    

    scroll = scroll_value
    scrollCount = 0

    with mss.mss() as sct:
        print("메크로 싸이클 횟수 : ", loopNum)
        
        monitor = sct.monitors[0]

        while not stop:
            img = np.array(sct.grab(monitor))
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            result = cv2.matchTemplate(gray, template, cv2.TM_CCOEFF_NORMED)
            threshold = 0.8
            loc = np.where(result >= threshold)

            points = list(zip(*loc[::-1]))

            if not points:
                print("화면에서 이미지를 찾을 수 없습니다")
                stop_program()
                return

            if points:
                points.sort(key=lambda x: x[1])

                for pt in points:

                    if stop:
                        return

                    
                    x = pt[0] + w // 2
                    y = pt[1] + h // 2

                    pyautogui.click(x, y)
                    time.sleep(0.05)

            pyautogui.press("space")
            
            if scrollCount == scroll:
                pyautogui.hotkey("ctrl", "home")
                loopNum += 1
                print("메크로 싸이클 횟수 : ", loopNum)
                scrollCount = 0
            else:
                scrollCount += 1
            

            time.sleep(0.05)


def show_manual():
    manual_text = """
==================================================

사용방법

1. 누르고자 하는 버튼 캡쳐후 저장
(ex. 수강신청 과목 새로고침)

2. [사진 업로드] 버튼을 통해 해당 이미지 선택
(이후 생성되는 "메크로 설정파일.json" 삭제 X)

3. [스크롤 설정] 버튼을 통해 클릭하고자 하는 페이지
스크롤 횟수 설정 
(맨 위에서부터 맨 아래까지 스페이스바 횟수)

4. [실행]을 누르면 자동으로 스크롤을 내리며 실행됨

5. 멈추고자 할 땐, 키보드에서 [F8] 클릭 

==================================================
"""
    print(manual_text)
def set_scroll():
    global scroll_value
    scroll_value = int(scroll_spin.get())
    save_config()



# GUI 생성
root = tk.Tk()
keyboard.add_hotkey("F8", stop_program)
load_config()

root.title("수강신청 메크로")
root.geometry("700x400")



# 왼쪽 프레임
left_frame = tk.Frame(root, width=400)
left_frame.pack(side="left", fill="y", padx=10, pady=10)

# 버튼 중앙 정렬용 프레임
button_frame = tk.Frame(left_frame)
button_frame.pack(expand=True)

# 오른쪽 프레임
right_frame = tk.Frame(root)
right_frame.pack(side="right", expand=True, fill="both", padx=10, pady=10)



# 버튼들
btn_manual = tk.Button(button_frame, text="설명서", height=2, width=30, command=show_manual)
btn_manual.pack(pady=5)

btn_upload = tk.Button(button_frame, text="사진 업로드", height=2, width=30, command=upload_photo)
btn_upload.pack(pady=5)

# 사진 경로 표시 라벨
file_label = tk.Label(button_frame, text="선택 안됨", fg="gray")
if image_path:
    file_label.config(text=image_path, fg="black")
file_label.pack(fill="x", pady=3)


label = tk.Label(button_frame, text='스크롤 횟수')
label.pack()
scroll_spin = tk.Spinbox(button_frame, from_=1, to=50, width=10)
scroll_spin.pack()
scroll_spin.delete(0, tk.END)
scroll_spin.insert(0, scroll_value)

btn_run = tk.Button(button_frame, text="실행", height=5, width=35, command=run_program)
btn_run.pack(pady=5)


# 로그 출력창
log_text = tk.Text(right_frame)
log_text.pack(expand=True, fill="both")

# print 리디렉트
sys.stdout = RedirectText(log_text)
print("Code by ssenu")
print("수강신청 새로고침 메크로입니다.\n"
"[설명서]를 먼저 눌러주세요.\n")
root.mainloop()