#leaving the following line in as pennance.  Feel free to remove it.
#yes, I'm an idiot and I don't pay attention sometimes when coding. That's what QA is for, lol!
################################################################################################
#Interactive Automate--a simple tool to assist round trip coding with ChatGPT-4o
#Copyright (C) 2024 Matthew Zeits
#This program is free software: you can redistribute it and/or modify it under the terms of the 
#GNU General Public License as published by the Free Software Foundation, either version 3 of 
#the License, or (at your option) any later version.
#This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; 
#without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. 
#See the GNU General Public License for more details.
#You should have received a copy of the GNU General Public License along with this program. 
#If not, see http://www.gnu.org/licenses/.
################################################################################################
import tkinter as tk
from tkinter import scrolledtext, messagebox
import subprocess
import os
import platform
import tempfile

def get_clipboard_tool():
    system = platform.system()
    if system == 'Linux':
        return 'xclip'
    elif system == 'Darwin':
        return 'pbcopy'
    elif system == 'Windows':
        return 'clip'
    else:
        raise Exception('Unsupported OS')

def run_code(code, lang):
    temp_dir = tempfile.gettempdir()
    clipboard_tool = get_clipboard_tool()

    file_exts = {
        "python": "py",
        "c": "c",
        "rust": "rs",
        "go": "go",
        "java": "java",
        "kotlin": "kt",
        "swift": "swift"
    }

    run_cmds = {
        "python": f"python3 {temp_dir}/code_snippet.py",
        "c": f"gcc {temp_dir}/code_snippet.c -o {temp_dir}/code_snippet && {temp_dir}/code_snippet",
        "rust": f"rustc {temp_dir}/code_snippet.rs -o {temp_dir}/code_snippet && {temp_dir}/code_snippet",
        "go": f"go run {temp_dir}/code_snippet.go",
        "java": f"javac {temp_dir}/code_snippet.java && java -cp {temp_dir} code_snippet",
        "kotlin": f"kotlinc {temp_dir}/code_snippet.kt -include-runtime -d {temp_dir}/code_snippet.jar && java -jar {temp_dir}/code_snippet.jar",
        "swift": f"swift {temp_dir}/code_snippet.swift"
    }

    if lang not in file_exts or lang not in run_cmds:
        raise Exception('Unsupported language')

    file_ext = file_exts[lang]
    run_cmd = run_cmds[lang]
    code_file = os.path.join(temp_dir, f"code_snippet.{file_ext}")

    with open(code_file, 'w') as f:
        f.write(code)

    process = subprocess.Popen(run_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    if stderr:
        if clipboard_tool == 'xclip':
            subprocess.run(f"echo '{stderr.decode()}' | {clipboard_tool} -selection clipboard", shell=True)
        else:
            subprocess.run(f"echo '{stderr.decode()}' | {clipboard_tool}", shell=True)
        return f"Errors: {stderr.decode()} (copied to clipboard)"
    else:
        return stdout.decode()

def execute_code():
    code = code_text.get("1.0", tk.END)
    lang = lang_var.get()

    if not code.strip():
        messagebox.showwarning("Input Error", "Please enter some code.")
        return

    try:
        output = run_code(code, lang)
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, output)
    except Exception as e:
        messagebox.showerror("Execution Error", str(e))

# Setup the main window
root = tk.Tk()
root.title("Interactive Code Executor")

# Language selection
lang_var = tk.StringVar(value="python")
languages = ["python", "c", "rust", "go", "java", "kotlin", "swift"]
lang_menu = tk.OptionMenu(root, lang_var, *languages)
lang_menu.pack(pady=10)

# Code input text box
code_text = scrolledtext.ScrolledText(root, width=80, height=20)
code_text.pack(pady=10)

# Execute button
execute_button = tk.Button(root, text="Execute", command=execute_code)
execute_button.pack(pady=10)

# Output text box
output_text = scrolledtext.ScrolledText(root, width=80, height=10)
output_text.pack(pady=10)

# Start the main event loop
root.mainloop()
