# API Service Status Application

This is a simple Python application built with tkinter that allows you to monitor the status and response time of APIs.

## Installation

Before running the application, make sure you have the following dependencies installed:

```shell
pip install tkinter
pip install requests
```

## Usage

1. Clone the repository or download the `main.py` file.
2. Open a terminal and navigate to the project directory.
3. Run the following command to start the application:

   ```shell
   python main.py
   ```

4. The application window will open, displaying the status and response time of the predefined APIs (e.g., Google).
5. Right-click on the window to add a new API entry. Enter the name and URL of the API, then click "Submit".
6. Each API entry has a dropdown menu with options to modify or delete the entry.
7. The application will automatically check the status and response time of the APIs every 5 seconds.

## Code

```python
import tkinter as tk
import requests
import json
from tkinter import simpledialog
import time
from tkinter import messagebox
import os

# Define functions for API status monitoring and management (add, modify, delete)
# ...

# Create the main application window
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

# Set the alpha channel of the window to 0.9 to make it partially transparent
root.attributes('-alpha', 0.9)

root.mainloop()
```

## Contributing

Contributions are welcome! If you have any suggestions, improvements, or bug fixes, please create a pull request.

## License

This project is licensed under the [MIT License](LICENSE).
