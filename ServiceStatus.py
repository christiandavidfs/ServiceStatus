import tkinter as tk
import requests
import json
from tkinter import simpledialog
import time
from tkinter import messagebox
import os

def check_api_status(api_url, status_label, response_label):
    try:
        start_time = time.time()
        response = requests.get(api_url)
        end_time = time.time()

        if response.status_code == 200:
            status_label.config(bg='green', text=f'Status: {response.status_code}')
        else:
            status_label.config(bg='red', text=f'Error: {response.status_code}')

        response_time = round((end_time - start_time) * 1000, 2)  # Convert to milliseconds and round to 2 decimal places
        response_label.config(text=f'Response: {response_time} ms')

    except:
        status_label.config(bg='red', text='Error: Connection Failed')

    # Call the check_api_status() function again after 5 seconds
    root.after(5000, check_api_status, api_url, status_label, response_label)

def add_url():
    name = simpledialog.askstring('Add URL', 'Enter API name:')
    if not name:
        show_message('Error', 'API name cannot be empty')
        return

    url = simpledialog.askstring('Add URL', 'Enter API URL:')
    if not url:
        show_message('Error', 'API URL cannot be empty')
        return

    api_list.append({'name': name, 'url': url})
    with open('api_list.json', 'w') as f:
        json.dump(api_list, f)
    refresh_api_list()

def modify_url(name):
    for api in api_list:
        if api['name'] == name:
            new_name = simpledialog.askstring('Modify URL', 'Enter new API name:')
            if not new_name:
                show_message('Error', 'API name cannot be empty')
                return

            new_url = simpledialog.askstring('Modify URL', 'Enter new API URL:')
            if not new_url:
                show_message('Error', 'API URL cannot be empty')
                return

            api['name'] = new_name
            api['url'] = new_url
            with open('api_list.json', 'w') as f:
                json.dump(api_list, f)
            refresh_api_list()
            break

def delete_url(name):
    api_list[:] = [api for api in api_list if api['name'] != name]
    with open('api_list.json', 'w') as f:
        json.dump(api_list, f)
    refresh_api_list()

def submit_new_entry(name_entry, url_entry, window):
    name = name_entry.get()
    if not name:
        show_message('Error', 'API name cannot be empty')
        return

    url = url_entry.get()
    if not url:
        show_message('Error', 'API URL cannot be empty')
        return

    api_list.append({'name': name, 'url': url})
    with open('api_list.json', 'w') as f:
        json.dump(api_list, f)
    window.destroy()
    refresh_api_list()

def show_message(title, message):
    messagebox.showinfo(title, message)

def add_new_entry(event):
    if event.type == '4':  # Right button click event
        new_entry_window = tk.Toplevel(root)
        new_entry_window.title('Add New Entry')

        name_label = tk.Label(new_entry_window, text='Name:')
        name_label.grid(row=0, column=0, padx=5, pady=5)

        name_entry = tk.Entry(new_entry_window)
        name_entry.grid(row=0, column=1, padx=5, pady=5)

        url_label = tk.Label(new_entry_window, text='URL:')
        url_label.grid(row=1, column=0, padx=5, pady=5)

        url_entry = tk.Entry(new_entry_window)
        url_entry.grid(row=1, column=1, padx=5, pady=5)

        submit_button = tk.Button(new_entry_window, text='Submit',
                                  command=lambda: submit_new_entry(name_entry, url_entry, new_entry_window))
        submit_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

def refresh_api_list():
    for widget in root.winfo_children():
        widget.destroy()

    if os.path.exists('api_list.json'):
        with open('api_list.json', 'r') as f:
            api_list = json.load(f)
    else:
        api_list = [{'name': 'Google', 'url': 'https://www.google.com'}]
        with open('api_list.json', 'w') as f:
            json.dump(api_list, f)

    api_list = [api for api in api_list if api['name'] and api['url']]  # Exclude entries with empty or null values

    for api in api_list:
        api_frame = tk.Frame(root)
        api_frame.pack(pady=5)

        api_name_label = tk.Label(api_frame, text=api['name'], width=10)
        api_name_label.pack(side=tk.LEFT)

        api_status_label = tk.Label(api_frame, width=50)
        api_status_label.pack(side=tk.LEFT, padx=5)

        api_response_label = tk.Label(api_frame, width=15)
        api_response_label.pack(side=tk.LEFT)

        # Create a dropdown menu for each API entry
        menu = tk.Menu(api_frame, tearoff=0)
        menu.add_command(label='Modify', command=lambda name=api['name']: modify_url(name))
        menu.add_command(label='Delete', command=lambda name=api['name']: delete_url(name))
        api_name_label.bind('<Button-3>', lambda event, menu=menu: menu.post(event.x_root, event.y_root))

        # Remove the check button and call the check_api_status() function directly
        check_api_status(api['url'], api_status_label, api_response_label)

root = tk.Tk()
root.title('API Status')

# Load the api_list from the JSON file
if os.path.exists('api_list.json'):
    with open('api_list.json', 'r') as f:
        api_list = json.load(f)
else:
    api_list = [{'name': 'Google', 'url': 'https://www.google.com'}]
    with open('api_list.json', 'w') as f:
        json.dump(api_list, f)

# Bind the root window to the add_new_entry() function
root.bind('<Button-3>', add_new_entry)

refresh_api_list()

# Set the alpha channel of the window to 0.5 to make it partially transparent
root.attributes('-alpha', 0.9)

root.mainloop()
