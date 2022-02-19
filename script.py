# Made by pressfguillaume
# Created because I have an OCD when it comes to messy folders

import tkinter as tk
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
from datetime import datetime
from subprocess import call
import json

# Add the full path of the json file if you decide to compile
with open('data.json', 'r') as data_file:
    data = json.load(data_file)
directory = []
extension = []
config_data = []
for i in data["outputFolders"]:
    directory.append(i['directory'])
    extension.append(i['extension'])
    config_data = dict(zip(extension, directory))


def disable_input():
    window.configure(state='disabled')


class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        for file_name in os.listdir(data["trackingFolder"]):
            file_source = data["trackingFolder"] + "/" + file_name
            split_tup = os.path.splitext(file_name)
            file_extension = split_tup[1]
            for config_data_ext, config_data_path in config_data.items():
                if file_extension == config_data_ext:
                    new_destination = config_data_path + "/" + file_name
                    os.rename(file_source, new_destination)
                    hour_and_minute = datetime.now().strftime("%H:%M:%S")
                    message = f'  [{hour_and_minute}] - {file_name} was moved to {config_data_path}\n'
                    print(f'\033[4m{datetime.now().strftime("%H:%M:%S")}\033[0m - [{file_extension.upper()}] \033[95m{file_name}\033[0m was moved to \033[92m{config_data_path}\033[0m')
                    file_path = config_data_path
                    folder_button = tk.Button(window, text='Open in finder',
                                              width=9,
                                              padx=2,
                                              pady=2,
                                              cursor="hand",
                                              bd=1, highlightthickness=0,
                                              command=lambda: call(["open", file_path]))
                    open_file_button = tk.Button(window, text=f'Open file [{file_extension.upper()}]',
                                                 width=8,
                                                 padx=4,
                                                 pady=2,
                                                 anchor='w',
                                                 cursor="hand",
                                                 bd=1, highlightthickness=0,
                                                 command=lambda: call(["open", new_destination]))

                    window.window_create(tk.END, window=open_file_button)
                    window.window_create(tk.END, window=folder_button)
                    window.configure(state='normal')
                    window.insert(tk.END, message)
                    window.configure(state='disabled')
                else:
                    pass


event_handler = MyHandler()
observer = Observer()
observer.schedule(event_handler, data["trackingFolder"], recursive=True)
observer.start()
root = tk.Tk()
root.geometry("950x300")
root.title('Logs: Download folder file movement automation')
#Add some transparency
#root.attributes('-alpha', 0.95)
window = tk.Text(
    root,
    font=('Helvetica', 13),
    padx=10,
    pady=10,
    cursor='arrow'
)
window.pack(
    fill="both",
    expand=True,
    padx=0,
    pady=0
)
window.config(
    highlightthickness=0,
    borderwidth=0
)
disable_input()
root.mainloop()
