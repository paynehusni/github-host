import tkinter as tk
from tkinter import ttk
import requests
import os
import sys
import ctypes
import threading
import subprocess
import locale
from datetime import datetime

# Define multilingual text
LANGUAGES = {
    'en': {
        'success': "Hosts file successfully updated!",
        'error': "An error occurred while updating hosts file: {error}",
        'update_hosts_button': "Update Hosts File",
        'update_hosts_button_jsdelivr': "Update Hosts File from jsDelivr",
        'downloading_content': "Downloading new hosts content...",
        'reading_hosts': "Reading current hosts file...",
        'writing_hosts': "Writing updated hosts file...",
        'flushing_dns': "Flushing DNS cache..."
    },
    'zh': {
        'success': "Hosts文件已成功更新！",
        'error': "更新hosts文件时发生错误：{error}",
        'update_hosts_button': "更新Hosts文件",
        'update_hosts_button_jsdelivr': "从jsDelivr更新Hosts文件",
        'downloading_content': "正在下载新的hosts内容...",
        'reading_hosts': "正在读取当前的hosts文件...",
        'writing_hosts': "正在写入更新后的hosts文件...",
        'flushing_dns': "正在刷新DNS缓存..."
    },
    'fa': {
        'success': "پرونده hosts با موفقیت به روز رسانی شد!",
        'error': "خطایی در هنگام به روز رسانی پرونده hosts رخ داده است: {error}",
        'update_hosts_button': "به روز رسانی پرونده Hosts",
        'update_hosts_button_jsdelivr': "به روز رسانی پرونده Hosts از jsDelivr",
        'downloading_content': "در حال دریافت محتوای جدید hosts...",
        'reading_hosts': "در حال خواندن فایل hosts فعلی...",
        'writing_hosts': "در حال نوشتن فایل hosts به روز شده...",
        'flushing_dns': "در حال پاکسازی حافظه نهان DNS..."
    },
    'ar': {
        'success': "تم تحديث ملف الـ hosts بنجاح!",
        'error': "حدث خطأ أثناء تحديث ملف الـ hosts: {error}",
        'update_hosts_button': "تحديث ملف Hosts",
        'update_hosts_button_jsdelivr': "تحديث ملف Hosts من jsDelivr",
        'downloading_content': "تحميل محتوى ملف hosts الجديد...",
        'reading_hosts': "قراءة ملف hosts الحالي...",
        'writing_hosts': "كتابة ملف hosts المحدث...",
        'flushing_dns': "مسح ذاكرة التخزين المؤقت لـ DNS..."
    }
}

# Get system language settings
def get_system_language():
    lang, _ = locale.getdefaultlocale()
    return lang.split('_')[0] if lang else 'en'

# Get current system language
CURRENT_LANGUAGE = get_system_language()

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)

def update_hosts(progress_var, console_text, url):
    hosts_path = r'C:\Windows\System32\drivers\etc\hosts'

    try:
        # Update progress
        progress_var.set(10)
        root.update_idletasks()

        # Download new hosts content
        console_text.config(state=tk.NORMAL)  # Allow editing to insert new content
        console_text.insert(tk.END, f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {LANGUAGES[CURRENT_LANGUAGE]['downloading_content']}\n")
        console_text.see(tk.END)  # Scroll to the last line
        console_text.config(state=tk.DISABLED)  # Disable editing

        response = requests.get(url)
        new_content = response.text.encode('utf-8').decode('utf-8')

        # Update progress
        progress_var.set(30)
        root.update_idletasks()

        # Read current hosts file
        console_text.config(state=tk.NORMAL)  # Allow editing to insert new content
        console_text.insert(tk.END, f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {LANGUAGES[CURRENT_LANGUAGE]['reading_hosts']}\n")
        console_text.see(tk.END)  # Scroll to the last line
        console_text.config(state=tk.DISABLED)  # Disable editing

        with open(hosts_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        # Update progress
        progress_var.set(50)
        root.update_idletasks()

        start_index = -1
        end_index = -1

        # Find the first start marker and the last end marker
        for i, line in enumerate(lines):
            if '# github-hosts start' in line and start_index == -1:
                start_index = i
            if '# github-hosts end' in line:
                end_index = i

        # Update progress
        progress_var.set(70)
        root.update_idletasks()

        if start_index != -1 and end_index != -1 and start_index < end_index:
            # If valid markers are found, delete those lines and insert new content
            del lines[start_index:end_index+1]
            lines.insert(start_index, new_content)
        else:
            # If no valid markers are found, add new content at the end of the file
            if lines and not lines[-1].endswith('\n'):
                lines.append('\n')  # Ensure the last line ends with a newline character
            lines.append(new_content)

        # Update progress
        progress_var.set(90)
        root.update_idletasks()

        # Write to hosts file
        console_text.config(state=tk.NORMAL)  # Allow editing to insert new content
        console_text.insert(tk.END, f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {LANGUAGES[CURRENT_LANGUAGE]['writing_hosts']}\n")
        console_text.see(tk.END)  # Scroll to the last line
        console_text.config(state=tk.DISABLED)  # Disable editing

        with open(hosts_path, 'w', encoding='utf-8') as file:
            file.writelines(lines)

        # Flush DNS cache
        console_text.config(state=tk.NORMAL)  # Allow editing to insert new content
        console_text.insert(tk.END, f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {LANGUAGES[CURRENT_LANGUAGE]['flushing_dns']}\n")
        console_text.see(tk.END)  # Scroll to the last line
        console_text.config(state=tk.DISABLED)  # Disable editing

        subprocess.run(["ipconfig", "/flushdns"])

        # Output success message
        console_text.config(state=tk.NORMAL)  # Allow editing to insert new content
        console_text.insert(tk.END, f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {LANGUAGES[CURRENT_LANGUAGE]['success']}\n")
        console_text.see(tk.END)  # Scroll to the last line
        console_text.config(state=tk.DISABLED)  # Disable editing

    except Exception as e:
        # Output error message
        console_text.config(state=tk.NORMAL)  # Allow editing to insert new content
        console_text.insert(tk.END, f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {LANGUAGES[CURRENT_LANGUAGE]['error'].format(error=str(e))}\n")
        console_text.see(tk.END)  # Scroll to the last line
        console_text.config(state=tk.DISABLED)  # Disable editing

    finally:
        # Reset progress bar and update button state
        progress_var.set(0)
        update_button.config(state=tk.NORMAL)
        update_button_jsdelivr.config(state=tk.NORMAL)

def start_update(source):
    # Disable update buttons and start update thread
    update_button.config(state=tk.DISABLED)
    update_button_jsdelivr.config(state=tk.DISABLED)
    if source == "github":
        url = 'https://raw.githubusercontent.com/paynehusni/github-host/master/hosts'
    elif source == "jsdelivr":
        url = 'https://cdn.jsdelivr.net/gh/paynehusni/github-host/hosts'
    threading.Thread(target=update_hosts, args=(progress_var, console_text, url), daemon=True).start()

# Create main window
root = tk.Tk()
root.title("Update Hosts File")
# root.geometry("500x400")
# Set window to be non-resizable
root.resizable(False, False)
# Create progress bar
progress_var = tk.DoubleVar()
progress_bar = ttk.Progressbar(root, variable=progress_var, maximum=100)
progress_bar.pack(pady=20, padx=10, fill=tk.X)

# Create a Frame to hold Text and Scrollbar
frame = tk.Frame(root)
frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Create text box and scrollbar
console_text = tk.Text(frame, wrap=tk.WORD)
console_text.grid(row=0, column=0, sticky="nsew")

scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=console_text.yview)
scrollbar.grid(row=0, column=1, sticky="ns")

# Bind text box and scrollbar
console_text.config(yscrollcommand=scrollbar.set, state=tk.DISABLED)  # Disable editing initially

# Create and place buttons
update_button = tk.Button(root, text=LANGUAGES[CURRENT_LANGUAGE]['update_hosts_button'], command=lambda: start_update("github"))
update_button.pack(pady=10)

update_button_jsdelivr = tk.Button(root, text=LANGUAGES[CURRENT_LANGUAGE]['update_hosts_button_jsdelivr'], command=lambda: start_update("jsdelivr"))
update_button_jsdelivr.pack(pady=10)

# Check if running with admin privileges
if not is_admin():
    # If not running as admin, restart with admin privileges
    run_as_admin()
    sys.exit()

# Run main loop
root.mainloop()