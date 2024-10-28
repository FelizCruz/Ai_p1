import tkinter as tk
from tkinter import messagebox, PhotoImage
import subprocess

# Function to run Python scripts
def run_code1():
    try:
        result1 = subprocess.run(["python", "betadays.py"], check=True)
        print(f"betadays.py exited with code: {result1.returncode}")
    # Run the second script
        result2 = subprocess.run(["python", "crushednuts.py"], check=True)
        print(f"crushednuts.py exited with code: {result2.returncode}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to run Code 1:\n{str(e)}")

def run_code2():
    try:
        subprocess.run(["python", "fp.py"]) 
    except Exception as e:     
        messagebox.showerror("Error", f"Failed to run Code 2:\n{str(e)}")

# Create the main window
window = tk.Tk()
window.title("Select Your Program")
window.geometry("400x300")
window.config(bg="#282a36")  # Set background color to a dark shade

# Add an optional icon (if you have an image, save it as 'icon.png')
# window.iconphoto(False, PhotoImage(file="icon.png"))

# Create a vibrant header label
header = tk.Label(
    window, 
    text="Choose a Mode to Run", 
    font=("Helvetica", 24, "bold"), 
    fg="#f8f8f2", 
    bg="#44475a", 
    pady=10
)
header.pack(fill=tk.X)

# Define button styles
button_style = {
    "font": ("Helvetica", 14, "bold"),
    "width": 15,
    "height": 2,
    "relief": "raised",
    "bd": 3,
    "cursor": "hand2",
    "activebackground": "#50fa7b",  # Vibrant green
    "activeforeground": "#282a36",
}

# Create buttons to run the two codes
button1 = tk.Button(
    window, 
    text="Meal Planner", 
    bg="#ff5555",  # Red button
    fg="#f8f8f2", 
    command=run_code1, 
    **button_style
)
button1.pack(pady=15)

button2 = tk.Button(
    window, 
    text="Fitness Planner", 
    bg="#8be9fd",  # Cyan button
    fg="#282a36", 
    command=run_code2, 
    **button_style
)
button2.pack(pady=15)

# Footer label
footer = tk.Label(
    window, 
    text="Powered by Python & Tkinter", 
    font=("Helvetica", 10), 
    fg="#6272a4", 
    bg="#282a36"
)
footer.pack(side=tk.BOTTOM, pady=10)

# Start the GUI event loop
window.mainloop()
