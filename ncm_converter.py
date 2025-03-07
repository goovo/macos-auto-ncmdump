import os
import sys
import json
import fnmatch
from ncmdump import dump
import tkinter as tk
from tkinter import filedialog, ttk
from threading import Thread
import queue

class NCMConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("NCM转换器")
        self.root.geometry("600x400")
        
        # 配置文件路径
        self.config_dir = os.path.expanduser("~/Library/Application Support/NCM转换器")
        self.config_file = os.path.join(self.config_dir, "config.json")
        
        # 加载上次使用的目录
        self.last_directory = self.load_last_directory()
        
        # 设置队列用于线程间通信
        self.queue = queue.Queue()
        
        self.setup_ui()
        self.conversion_running = False
        
        # 定期检查队列更新
        self.root.after(100, self.check_queue)
        
        # 设置关闭窗口时的处理
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def load_last_directory(self):
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    return config.get('last_directory', '')
        except Exception:
            pass
        return os.path.expanduser("~")

    def save_last_directory(self, directory):
        try:
            os.makedirs(self.config_dir, exist_ok=True)
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump({'last_directory': directory}, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存配置失败: {e}")

    def setup_ui(self):
        # 主框架
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # 当前目录显示
        path_frame = ttk.Frame(main_frame)
        path_frame.pack(fill=tk.X, pady=(0, 5))
        ttk.Label(path_frame, text="当前目录：").pack(side=tk.LEFT)
        self.path_label = ttk.Label(path_frame, text=self.last_directory)
        self.path_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # 文件列表框架
        list_frame = ttk.Frame(main_frame)
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        # 创建文件列表
        self.file_listbox = tk.Listbox(list_frame, selectmode=tk.MULTIPLE)
        self.file_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # 添加滚动条
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.file_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.file_listbox.configure(yscrollcommand=scrollbar.set)
        
        # 按钮框架
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=5)
        
        # 添加按钮
        ttk.Button(button_frame, text="选择文件", command=self.choose_files).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="选择文件夹", command=self.choose_directory).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="开始转换", command=self.start_conversion).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="清除列表", command=self.clear_list).pack(side=tk.LEFT, padx=5)
        
        # 进度和状态框架
        status_frame = ttk.Frame(main_frame)
        status_frame.pack(fill=tk.X, pady=5)
        
        # 进度显示
        self.progress_var = tk.StringVar()
        self.progress_label = ttk.Label(status_frame, textvariable=self.progress_var)
        self.progress_label.pack(fill=tk.X)
        
        # 状态显示
        self.status_var = tk.StringVar()
        self.status_label = ttk.Label(status_frame, textvariable=self.status_var)
        self.status_label.pack(fill=tk.X)

    def choose_files(self):
        files = filedialog.askopenfilenames(
            title="选择NCM文件",
            initialdir=self.last_directory,
            filetypes=[("NCM文件", "*.ncm"), ("所有文件", "*.*")]
        )
        if files:
            self.last_directory = os.path.dirname(files[0])
            self.save_last_directory(self.last_directory)
            self.path_label.config(text=self.last_directory)
            self.add_files(files)

    def choose_directory(self):
        directory = filedialog.askdirectory(
            title="选择包含NCM文件的文件夹",
            initialdir=self.last_directory
        )
        if directory:
            self.last_directory = directory
            self.save_last_directory(directory)
            self.path_label.config(text=directory)
            for root, _, files in os.walk(directory):
                for file in files:
                    if file.endswith('.ncm'):
                        self.add_files([os.path.join(root, file)])

    def add_files(self, files):
        for file in files:
            if file not in self.file_listbox.get(0, tk.END):
                self.file_listbox.insert(tk.END, file)

    def clear_list(self):
        self.file_listbox.delete(0, tk.END)

    def start_conversion(self):
        if self.conversion_running:
            return
            
        files = list(self.file_listbox.get(0, tk.END))
        if not files:
            self.status_var.set("请先选择要转换的文件")
            return
            
        self.conversion_running = True
        self.progress_var.set("开始转换...")
        conversion_thread = Thread(target=self.convert_files, args=(files,))
        conversion_thread.daemon = True
        conversion_thread.start()

    def convert_files(self, files):
        total = len(files)
        for i, file in enumerate(files, 1):
            try:
                self.queue.put(("progress", f"正在转换 ({i}/{total}): {os.path.basename(file)}"))
                dump(file)
                os.remove(file)  # 转换成功后删除原文件
                self.queue.put(("status", f"已转换: {os.path.basename(file)}"))
            except Exception as e:
                self.queue.put(("status", f"转换失败 {os.path.basename(file)}: {str(e)}"))
        
        self.queue.put(("complete", "转换完成"))
        self.conversion_running = False

    def check_queue(self):
        try:
            while True:
                msg_type, msg = self.queue.get_nowait()
                if msg_type == "progress":
                    self.progress_var.set(msg)
                elif msg_type == "status":
                    self.status_var.set(msg)
                elif msg_type == "complete":
                    self.progress_var.set(msg)
                    self.file_listbox.delete(0, tk.END)
                self.queue.task_done()
        except queue.Empty:
            pass
        finally:
            self.root.after(100, self.check_queue)

    def on_closing(self):
        if self.conversion_running:
            if tk.messagebox.askokcancel("确认", "正在转换中，确定要退出吗？"):
                self.root.destroy()
        else:
            self.root.destroy()

def main():
    root = tk.Tk()
    app = NCMConverter(root)
    root.mainloop()

if __name__ == "__main__":
    main()