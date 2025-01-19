import tkinter as tk
from tkinter import filedialog
import os
import time
import csv



# --------------------------- Variables --------------------------- #
version: str = "2.0.0"
seperator: str = ";"
placeholder: str = "$"
amount_of_variables: int = 0
amount_of_lines: int = 0
variable_filename: str = "variablefile.csv"
static_filename: str = "staticfile.txt"
settings_filename: str = "settings.conf"
global program_dir  # Global variable for the program directory
program_dir = os.path.dirname(os.path.abspath(__file__))  # Start directory for the file dialog

# --------------------------- Functions --------------------------- #
def write_to_log(text):
    text_log['state'] = 'normal'  # Enable the text field
    current_time = time.strftime("%H:%M:%S")    # Get the current time
    text_log.insert(tk.END, current_time + " " + text + "\n")    # Write the time and text to the text field
    text_log['state'] = 'disabled'  # Disable the text field again
    pass

def generate_configfiles():
    global seperator
    global placeholder
    global variable_filename
    global static_filename
    
    with open(variable_filename, newline='') as variable_file:
        csvreader = csv.reader(variable_file, delimiter=seperator)
        
        for row in csvreader:
            # Read the static file content
            with open(static_filename, 'r') as staticfile:
                static_content = staticfile.read()
            
            # Replace placeholders with values from the row
            for i, value in enumerate(row[1:], start=1):  # Start from 1 to skip the filename
                start_index = static_content.find(placeholder)
                if start_index != -1:
                    end_index = start_index + len(placeholder)
                    static_content = static_content[:start_index] + value + static_content[end_index:]
                    start_index = static_content.find(placeholder, start_index + len(value))
                    
                #print(f"Replacing {placeholder} with {value}")  # Debug print
                #print(static_content)  # Debug print
                
            # Write the modified content to a new file
            output_filename = f"{row[0]}.txt"
            with open(output_filename, 'w') as outputfile:
                outputfile.write(static_content)
                
            print(static_content)  # Debug print
            
            write_to_log(f"Generated file {output_filename} with values {row[1:]}")
    pass

def save_settings():
    with open(settings_filename, "w") as file:
        file.write(f"version={version}\n")
        file.write(f"seperator={text_variable_seperator.get()}\n")
        file.write(f"placeholder={text_variable_placeholder.get()}\n")
        file.write(f"variable_filename={variable_filename}\n")
        file.write(f"static_filename={static_filename}\n")
        file.close()
    write_to_log(f"Settings saved to {settings_filename}.")

def load_settings():
    if os.path.isfile(settings_filename):
        with open(settings_filename, "r") as file:
            lines = file.readlines()
            for line in lines:
                if line.startswith("seperator="):
                    seperator = line.strip().split("=")[1]
                    text_variable_seperator.set(seperator)
                elif line.startswith("placeholder="):
                    placeholder = line.strip().split("=")[1]
                    text_variable_placeholder.set(placeholder)
        file.close() 
        write_to_log(f"Settings loaded from {settings_filename}\nSeperator: {seperator}\nPlaceholder: {placeholder}\nVariablefile: {variable_filename}\nStatictextfile: {static_filename}")
    else:
        write_to_log(f"Writing {settings_filename} initially.")
        save_settings()
    pass

def load_variable_file():
    filename = filedialog.askopenfilename(
        title="Select a file",
        initialdir=program_dir,
        filetypes=(("Comma separated values", "*.csv"),("All files", "*.*"))
    )
    if filename:
        global variable_filename
        variable_filename = filename
        write_to_log(f"Variable file {variable_filename} selected.")
    else:
        write_to_log("No file selected.")
    pass

def load_static_file():
    filename = filedialog.askopenfilename(
        title="Select a file",
        initialdir=program_dir,
        filetypes=(("Text file", "*.txt"),("All files", "*.*"))
    )
    if filename:
        global static_filename
        static_filename = filename
        write_to_log(f"Static file {static_filename} selected.")
        text_static.delete('1.0', tk.END)   # Delete the content of the text field
        text_static.insert(tk.END, open(static_filename).read())   # Insert the content of the file into the text field
        write_to_log(f"Static file {static_filename} loaded.")
    else:
        write_to_log("No file selected.")
    pass

def default_settings():
    text_variable_seperator.set(";")   # Set the default value of the seperator
    text_variable_placeholder.set("$")    # Set the default value of the text field.
    static_filename = "staticfile.txt"   # Set the default value of the static filename
    variable_filename = "variablefile.csv"    # Set the default value of the variable filename  
    write_to_log("Settings set to default values.")
    pass


def get_file_name():
    filename = filedialog.askopenfilename(
        title="Select a file",
        filetypes=(("Text files", "*.txt"),("Comma separated values", "*.csv"),("All files", "*.*"))
    )
    if filename:
        return filename
    else:
        write_to_log("No file selected.")

def help_window():
    # Create help window
    help_window = tk.Toplevel(root)  # Create a window
    help_window.title("Help")   # Title of the window
    help_window.geometry("1000x500")   # Size of the window (Width x Height)
    help_window.resizable(True, True)   # Enable resizing of the window
    help_window.configure(bg="antique white")   # Background color of the window

    # Create a text field
    text_help_window = tk.Text(help_window, bg="antique white")   # Create a text field with the same background color
    text_help_window.pack(expand=True, fill='both')  # Make the text field expandable and stick to all sides
    
    # Write the help text to the text field
    text_help_window.insert(tk.END, """
This program is used to generate configfiles from a variable file and a static text file.
The variable file contains the variables that should be inserted into the static text file.
The static text file contains the text that should be used as a template for the configfiles.
The variables in the variable file are seperated by a seperator character.
 The placeholder character is used to mark the position in the static text file where the variables should be inserted.
The seperator and placeholder character can be changed in the settings.
The settings can be saved and loaded from a file.
The settings can be reset to the default values.
The program can generate the configfiles from the variable file and the static text file.
The program can write a log of the generation process.
The program can be closed by clicking the close button.

Made by Luca Moser and Jascha Bucher in 2025. 
""")
    text_help_window.pack()
    pass

def static_text_changed(event):
    open(static_filename, "w").write(text_static.get("1.0", tk.END))
    write_to_log("Static text changed.")
    print("Static text changed.")
    pass
    

# --------------------------- GUI --------------------------- #
# -------- Main Window -------- #
# Create a main window
root = tk.Tk()  # Create a window
root.title("Dynamic Configfile Builder")   # Title of the window
root.resizable(True, True)   # Enable resizing of the window

# Create a main frame with padding
main_frame = tk.Frame(root, padx=10, pady=10)
main_frame.grid(row=0, column=0, sticky="nsew")

# Make the main frame expandable
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

# Add padding to every widget
widget_padx = 5
widget_pady = 5

# Button configuration variables
button_width = 20
button_height = 2
button_color = "pale green"
button_text_size = 11

# Entry field configuration variables
entry_text_size = 15


# -------- Buttons -------- #
# Create a generate files button
btn_generate_files = tk.Button(main_frame, text="Generate files", command=generate_configfiles, width=button_width, height=button_height, bg=button_color, font=("Arial", button_text_size))
btn_generate_files.grid(row=0, column=0, padx=widget_padx, pady=widget_pady)
btn_generate_files.config(default=tk.DISABLED)

# Create a choose variable file button
btn_choose_variable_file = tk.Button(main_frame, text="Choose variable file", command=load_variable_file, width=button_width, height=button_height, bg=button_color, font=("Arial", button_text_size))
btn_choose_variable_file.grid(row=1, column=0, padx=widget_padx, pady=widget_pady)
btn_choose_variable_file.config(default=tk.DISABLED)

# Create a load static text file button
btn_load_static_file = tk.Button(main_frame, text="Load static text file", command=load_static_file, width=button_width, height=button_height, bg=button_color, font=("Arial", button_text_size))
btn_load_static_file.grid(row=2, column=0, padx=widget_padx, pady=widget_pady)
btn_load_static_file.config(default=tk.DISABLED)

# Create a help button
btn_help = tk.Button(main_frame, text="Help", command=help_window, width=button_width, height=button_height, bg=button_color, font=("Arial", button_text_size))
btn_help.grid(row=0, column=5, padx=widget_padx, pady=widget_pady)

# Create a save settings button
btn_save_settings = tk.Button(main_frame, text="Save settings", command=save_settings, width=button_width, height=button_height, bg=button_color, font=("Arial", button_text_size))
btn_save_settings.grid(row=1, column=5, padx=widget_padx, pady=widget_pady)
btn_save_settings.config(default=tk.DISABLED)

# Create a default settings button 
btn_default_settings = tk.Button(main_frame, text="Default settings", command=default_settings, width=button_width, height=button_height, bg=button_color, font=("Arial", button_text_size))
btn_default_settings.grid(row=2, column=5, padx=widget_padx, pady=widget_pady)
btn_default_settings.config(default=tk.DISABLED)


# -------- Text Fields -------- #
# Create a text field for the static text
text_static = tk.Text(main_frame, height=25, width=100)  
text_static.grid(row=5, column=0, columnspan=3, padx=widget_padx, pady=widget_pady, sticky="nsew") 
main_frame.grid_rowconfigure(5, weight=1)   # Make the text field expandable
text_static['state'] = 'normal' # Enable the text field
text_static.bind("<KeyRelease>", static_text_changed)  # Bind the text field to the function

# Create a text field for the log
text_log = tk.Text(main_frame, height=25, width=100)
text_log.grid(row=5, column=4, columnspan=2, padx=widget_padx, pady=widget_pady, sticky="nsew")
main_frame.grid_rowconfigure(5, weight=1)   # Make the text field expandable
text_log['state'] = 'disabled'  # Disable the text field
text_log.config(bg="LightYellow2")  # Set the background color of the text field


# -------- Entry Fields -------- #
# Create an entry field for the seperator
text_variable_seperator = tk.StringVar()
text_variable_seperator.set(";")
char_variable_seperator = tk.Entry(main_frame, textvariable=text_variable_seperator, width=2, justify='center', font=("Arial", entry_text_size))
char_variable_seperator.grid(row=1, column=1, padx=widget_padx, pady=widget_pady)

# Create an entry field for the placeholder
text_variable_placeholder = tk.StringVar()
text_variable_placeholder.set("$")
char_variable_placeholder = tk.Entry(main_frame, textvariable=text_variable_placeholder, width=2, justify='center', font=("Arial", entry_text_size))
char_variable_placeholder.grid(row=2, column=1, padx=widget_padx, pady=widget_pady)


# --------------------------- init --------------------------- #
# -------- create files and folders -------- #
load_settings() # Load the settings from the settings file

# Check if the variable file exists
if os.path.isfile(variable_filename):
    write_to_log(f"The file {variable_filename} exist.")
else:
    write_to_log(f"The file {variable_filename} didn't exist and will be created.")
    with open(variable_filename, "w") as file:
        file.write("Filename1;Variable1;Variable2;Variable3;Variable4;Variable5;Variable6;Variable7;Variable8;Variable9\n")
        file.write("Filename2;Variable1;Variable2;Variable3;Variable4;Variable5;Variable6;Variable7;Variable8;Variable9\n")
        file.write("Filename3;Variable1;Variable2;Variable3;Variable4;Variable5;Variable6;Variable7;Variable8;Variable9\n")

# Check if the variable file exists
if os.path.isfile(static_filename):
    write_to_log(f"The file {static_filename} exist.")
else:
    write_to_log(f"The file {static_filename} didn't exist and will be created.")
    with open(static_filename, "w") as file:
        file.write(
"""Static1 $
Static2 $
Static3 $
Static4 $
Static5 $
Static6 $
Static7 $
Static8 $
Static9 $""")
        
text_static.delete('1.0', tk.END)   # Delete the content of the text field
text_static.insert(tk.END, open(static_filename).read())   # Insert the content of the file into the text field
write_to_log(f"Static file {static_filename} loaded.")

# --------------------------- Main --------------------------- #
root.mainloop()
{    
}