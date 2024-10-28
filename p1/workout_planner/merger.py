import tkinter as tk
import subprocess

def run_code1():
    subprocess.run(["python", "fp.py"])  # Replace with the actual name

def run_code2():
    subprocess.run(["python", "crushednuts.py"])  # Replace with the actual name

# Main Window
window = tk.Tk()
window.title("Select a Code to Run")
window.geometry("300x150")

button1 = tk.Button(window, text="Run Fitness Planner", command=run_code1)
button1.pack(pady=10)

button2 = tk.Button(window, text="Run Meal Planner", command=run_code2)
button2.pack(pady=10)

window.mainloop()
