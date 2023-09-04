# 2022 Dec9 version 0.7  ， From Haydon Ge
# add pop window to select file flow:
# add folder clear function
# add moved function.
# move the event case to mainloop

import tkinter as tk
import os
import time
import logging
import queue
from threading import Thread
import shutil
import watchdog.observers as observers  # 2
import watchdog.events as events  # 2

from configparser import ConfigParser
from tkinter import Toplevel, Label  # messagebox,button, Tk,

cfg = ConfigParser()
cfg.read(r'C:\config\config.ini', encoding="utf-8")
cfg.sections()
source_folder = cfg.get('folder', 'source_folder')
# source_folder2 = cfg.get ('folder','source_folder2') ++MULTIPLE FOLDER MONITOR
backup_folder = cfg.get('folder', 'destination_fold')
error_folder = cfg.get('folder', 'error_folder')

prename = cfg.get('folder', 'prefix_iden')
Prefix_iden = prename.split(",")
serial_pre = ""


logger = logging.getLogger(__name__)
# SENTINEL = None

all_file1 = []


def gci(filepath):
    # 遍历filepath下所有文件，包括子目录
    all_file = []
    files = os.listdir(filepath)
    for fi in files:
        fi_d = os.path.join(filepath, fi)
        if os.path.isdir(fi_d):
            gci(fi_d)
        else:  # 可以在这里加判断，使得满足特定后缀的的文件才能append
            all_file.append(os.path.join(filepath, fi_d))
    return all_file


# all_file1 = gci(source_folder)
# for i in all_file1:
#    os.remove(i)

window = tk.Tk()  # root =tk()
window.title('序列号监控 - 0.7')
window.geometry('550x320')
window.attributes('-topmost', True)
canvas = tk.Canvas(window, height=350, width=550)

"#Status information"
status_x = tk.StringVar()
status_x.set('等待输入条码')
tk.Label(window, textvariable=status_x, font=("黑体", 14)).place(x=60, y=80)

tk.Label(window, text="请输入条码：").place(x=60, y=130)
tk.Label(window, text="使用机器扫条码时，保持输入框为空，点击开始监控").place(x=60, y=180)
tk.Label(window, text="使用外部扫码枪时，扫描条码后，自动开始监控").place(x=60, y=200)
# Observer !
observer = observers.Observer()


def renew_path_name(filepath, serial_number):
    file_break_name = os.path.split(filepath)
    file_temp_name = file_break_name[1]
    p3 = file_temp_name.find("_")
    change_file_name = serial_number + file_temp_name[p3:]
    new_name = file_break_name[0] + "\\" + change_file_name
    # print (new_name)
    return new_name


class MyEventHandler(events.FileSystemEventHandler):
    def on_any_event(self, event):
        super(MyEventHandler, self).on_any_event(event)  # 继承父类
        queue.put(event)

    def __init__(self, queue):
        self.queue = queue


def start_test(event):
    #  print("开始监控")
    global observer
    status_x.set(serial_x.get() + ' 文件监控中')
    pre_serial = ""
    for i in Prefix_iden:
        if serial_x.get().find(i) != -1:
            pre_serial = i
            break
        else:
            pre_serial = ""
    if ((pre_serial != "") and len(serial_x.get()) == 11) or serial_x.get() == "":
        btn_stop.place(x=160, y=230)
        btn_start.place_forget()
        Input_serial.configure(state='readonly')
        # event_handler = MyEventHandler(queue) #初始化事件？
        observer = observers.Observer()
        observer.schedule(event_handler, path=source_folder,
                          recursive=False)  # 实例化监听对象，监控指定路径path，该路径触发任何事件都会调用event_handler来处理
        observer.start()
    else:
        status_x.set("请输入正确序列号")


def stop_test(event):
    btn_stop.place_forget()  # 防止没有开始线程就停止
    if (observer != []):
        observer.stop()
        observer.join()
        btn_start.place(x=60, y=230)
        Input_serial.configure(state="normal")
        serial_x.set("")
        status_x.set("停止监控")
    else:
        pass


def stop_return(observer):
    btn_stop.place_forget()  # 防止没有开始线程就停止
    if (observer != []):
        observer.stop()
        observer.join()
        btn_start.place(x=60, y=230)
        Input_serial.configure(state="normal")
        serial_x.set("")
        status_x.set("停止监控")
    else:
        pass


def clear_folder(event):
    all_files = []
    all_files = gci(source_folder)
    for filelist in all_files:
        chakai = os.path.split(filelist)
        error_file_name = error_folder + "\\" + chakai[1]
        shutil.copyfile(filelist, error_file_name)  # 抛去错误目录
        os.remove(filelist)  # 删除原有文件


def clear_Result_folder(event):
    all_file3 = []
    all_file3 = gci(backup_folder)
    for filelist in all_file3:
        chakai = os.path.split(filelist)
        error_file_name = error_folder + "\\" + chakai[1]
        shutil.copyfile(filelist, error_file_name)  # 抛去错误目录
        os.remove(filelist)  # 删除原有文件


def pop_always_on_top(msg='dd'):  # This will be on top of any other window
    msg_window = Toplevel()
    msg_window.title("选择文件去处")
    msg_window.attributes('-topmost', True)
    msg_window.geometry('300x200')

    Label(msg_window, text=msg).place(x=50, y=50)

    btn_start2 = tk.Button(msg_window, text='再次投递', command=msg_window.destroy)
    # btn_start2.bind('<Button-1>',msg_window.destroy)
    btn_start2.place(x=50, y=130)

    btn_stop2 = tk.Button(msg_window, text='转入不良', command=lambda: stop_return)
    # btn_stop2.bind('<Button-1>',msg_window.destroy)
    btn_stop2.place(x=150, y=130)
    # msg_window.destroy


#


def process(queue):
    while True:
        time.sleep(2)
        event = queue.get()
        s1 = event.event_type
        n1 = event.src_path
        file = r'c:\config\monitor.txt'
        with open(file, 'a+') as f:
            f.write(n1 + ' ' + s1 + '\n')  # 加\n换行显示
            f.close()
        if event.key[0] == "created":  # (event.key)[0] == "created"
            # if tk.messagebox.askyesno('提示', '要把文件进行比较操作吗'):
            with open(event.src_path, mode='rb+') as f:
                while True:
                    try:
                        line = f.readline()  # 逐行读取
                        line_str = line.decode().splitlines()[0]
                        p1 = line_str.find("Barcode")  # 文件是否正确
                        for i in Prefix_iden:
                            p2 = line_str.find(i)
                            if p2 != -1:
                                break
                        # p2 = line_str.find("1M") #是否包括条码
                    except IndexError:  # 超出范围未找到任何内容则退出
                        f.close()
                        chakai = os.path.split(event.src_path)
                        error_file_name = error_folder + "\\" + chakai[1]
                        shutil.copyfile(event.src_path, error_file_name)  # 抛去错误目录
                        os.remove(event.src_path)
                        break
                    else:
                        if p1 != -1:  # 找到#Barcode,文件正确。
                            if p2 != -1:  # 找到1M,JY,CX，且输入不为空。测试完成后，跳出，等输入下一片条码。
                                f.close()
                                chakai = os.path.split(event.src_path)
                                backup_name = backup_folder + "\\" + chakai[1]
                                shutil.copyfile(event.src_path, backup_name)
                                os.remove(event.src_path)
                                # observer.join()
                                # Stop_return(observer)# 只要有输入，就会在处理完文件后退出。
                                break
                            if Input_serial.get() == "" and p2 == -1:  # 输入为空，文件内也没有任何条码，抛去error
                                try:
                                    f.close()
                                    chakai = os.path.split(event.src_path)
                                    error_file_name = error_folder + "\\" + chakai[1]
                                    shutil.copyfile(event.src_path, error_file_name)  # 抛去错误目录
                                    os.remove(event.src_path)  # 删除原有文件
                                    # observer.join()
                                    # 是否要退出？
                                except(FileNotFoundError, FileExistsError):
                                    status_x.set('没有条码烧入')
                                finally:
                                    break  # 文件错误。停止继续
                            else:  # Input_serial 输入框内有合法的序列号开头的序列号，1M JY CX
                                rest = f.read()
                                f.seek(-len(line) - len(rest), 1)  # 光标移动到上一行, 要替换这行。。
                                f.truncate()  # 删除余下内容
                                Barcode_content = "Barcode:" + Input_serial.get() + '\n'
                                f.write(Barcode_content.encode())  # 插入指定内容
                                f.write(rest)  # 还原余下内容
                                f.close()
                                try:
                                    newname_in_test = event.src_path
                                    chakai = os.path.split(event.src_path)
                                    pos = chakai[1].find("_")
                                    new_temp_filename = chakai[0] + "\\" + Input_serial.get() + chakai[1][pos:]
                                    os.rename(newname_in_test, new_temp_filename)
                                    backup_name = backup_folder + "\\" + os.path.split(new_temp_filename)[1]
                                    shutil.copyfile(new_temp_filename, backup_name)
                                except(FileNotFoundError, FileExistsError):
                                    status_x.set('文件重新命名错误，请重新检查')
                                    break
                                else:
                                    os.remove(new_temp_filename)

                                finally:
                                    stop_return(observer)  # 回到初始画面
                                    break
        # else:
        # print("转移到ERROR")
        # chakai = os.path.split(event.src_path)
        # error_file_name = error_folder +"\\"+chakai[1]
        # shutil.copyfile(event.src_path,error_file_name) #抛去错误目录
        # os.remove(event.src_path) #移除原有文件


btn_start = tk.Button(window, text='开始监控文件夹')
btn_start.bind('<Button-1>', start_test)
btn_start.place(x=60, y=230)

btn_stop = tk.Button(window, text='停止监控文件夹')
btn_stop.bind('<Button-1>', stop_test)
btn_stop.place(x=160, y=230)
btn_stop.place_forget()

btn_Clear = tk.Button(window, text='清除监控文件夹')
btn_Clear.bind('<Button-1>', clear_folder)
btn_Clear.place(x=260, y=230)

btn_Clear_result = tk.Button(window, text='清除输出文件夹')
btn_Clear_result.bind('<Button-1>', clear_Result_folder)
btn_Clear_result.place(x=380, y=230)
serial_x = tk.StringVar()
serial_x.set('')  # 初始无条码
Input_serial = tk.Entry(window, textvariable=serial_x)
Input_serial.place(x=160, y=130)
Input_serial.bind("<Return>", start_test)
Input_serial.focus()

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                        format='[%(asctime)s %(threadName)s] %(message)s',
                        datefmt='%H:%M:%S')

    queue = queue.Queue()
    num_workers = 4
    pool = [Thread(target=process, args=(queue,)) for i in range(num_workers)]
    for t in pool:
        t.daemon = True
        t.start()
    event_handler = MyEventHandler(queue)  # 初始化事件？
    time.sleep(0.5)
    window.mainloop()
