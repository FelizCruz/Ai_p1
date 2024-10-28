import tkinter as tk
from functools import partial
from tkinter import ttk, messagebox
import sqlite3
from icecream import ic
def calculate_bmr(weight, height, age, gender):
    if gender == 'Male':
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    elif gender == 'Female':
        bmr = 10 * weight + 6.25 * height - 5 * age - 161
    else:
        raise ValueError("Gender should be 'Male' or 'Female'")
    return bmr

def calculate_tdee(bmr, activity_level):
    activity_factors = {
        "Sedentary": 1.2,
        "Lightly Active": 1.375,
        "Moderately Active": 1.55,
        "Very Active": 1.725
    }
    tdee = bmr * activity_factors[activity_level]
    return tdee

def calculate_macronutrients(tdee):
    protein_percentage = 0.25
    carb_percentage = 0.50
    fat_percentage = 0.25

    protein_calories = tdee * protein_percentage
    carbs_calories = tdee * carb_percentage
    fats_calories = tdee * fat_percentage

    protein_grams = protein_calories / 4
    carbs_grams = carbs_calories / 4
    fats_grams = fats_calories / 9

    return protein_grams, carbs_grams, fats_grams

def recommend_meals_greedy(db_name, target_calories, target_protein, target_carbs, diet_preference, optimization_goal):
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()

    # Fetch meals based on diet preference and meal type
    if diet_preference and diet_preference != "None":
        cursor.execute("SELECT name, calories, protein, carbs, fats, meal_type FROM meals WHERE type = ?", (diet_preference,))
        print(f"Querying meals with preference: {diet_preference}")
    else:
        cursor.execute("SELECT name, calories, protein, carbs, fats, meal_type FROM meals")
        print("Querying meals with no specific preference")

    meals = cursor.fetchall()
    connection.close()

    # Debug: Check the fetched meals
    if not meals:
        print(f"No meals found for dietary preference: {diet_preference}")
        messagebox.showerror("No Meals Found", f"No meals found for the specified preference: {diet_preference}.")
        return {"Breakfast": [], "Lunch": [], "Dinner": []}, 0, 0, 0, 0
    else:
        print(f"Found {len(meals)} meals for dietary preference: {diet_preference}")
        for meal in meals:
            print(meal)

    # Initialize variables for tracking the meal plan and total nutrition
    meal_plan = {"Breakfast": [], "Lunch": [], "Dinner": []}
    total_calories = 0
    total_protein = 0
    total_carbs = 0
    total_fats = 0

    # Track which meals have already been added to prevent repetition
    added_meals = set()

    # Ensure at least one meal per type, even if repetition is necessary
    for meal_type in meal_plan:
        # Filter meals based on the current meal type
        available_meals = [meal for meal in meals if meal[5] == meal_type]
        ic(meal_type)
        partial_calories=0
        if available_meals:
            # Sort meals based on the optimization goal
            if optimization_goal == "minimize_fat":
                meals_sorted = sorted(available_meals, key=lambda meal: meal[4])  # Sort by fat (meal[4])
            elif optimization_goal == "maximize_protein":
                meals_sorted = sorted(available_meals, key=lambda meal: -meal[2])  # Sort by protein (meal[2]), descending
            else:
                raise ValueError("Unknown optimization goal")
            #ic(meals_sorted)
            # Add the best available meal for this type
            for meal in meals_sorted:
                name, calories, protein, carbs, fats, m_type = meal
                if name not in added_meals and partial_calories + calories <= target_calories * 0.36:
                    meal_plan[meal_type].append(name)
                    total_calories += calories
                    partial_calories+=calories
                    total_protein += protein
                    total_carbs += carbs
                    total_fats += fats
                    added_meals.add(name)
                    ic(added_meals)
                    ic(partial_calories)
                else:
                    ic(total_calories)
                    ic(available_meals)
                    ic(name)
                    ic(partial_calories)
        else:
            break

    return meal_plan, total_calories, total_protein, total_carbs, total_fats





root = tk.Tk()
root.title("Diet Recommender")

def calculate_and_display():
    try:
        age = int(age_entry.get())
        height = float(height_entry.get())
        weight = float(weight_entry.get())
        gender = gender_var.get()
        activity_level = activity_var.get()
        goal = goal_var.get()
        diet_preference = diet_var.get()

        bmr = calculate_bmr(weight, height, age, gender)
        tdee = calculate_tdee(bmr, activity_level)

        # Adjust TDEE based on the user's goal
        if goal == "Weight Loss":
            tdee -= 500
        elif goal == "Muscle Gain":
            tdee += 500

        protein, carbs, fats = calculate_macronutrients(tdee)

        # Set optimization goal for the greedy algorithm (e.g., minimize fat or maximize protein)
        optimization_goal = "minimize_fat"  # Change to "maximize_protein" for the other option
        print("target calories="+str(tdee))
        # Get meal recommendations using the greedy algorithm
        meal_plan, total_cals, total_prot, total_carbs, total_fats = recommend_meals_greedy(
            "Diet_Recom.db", tdee, protein, carbs, diet_preference, optimization_goal)

        result_text = "Recommended Meal Plan:\n"

        # Display meals based on their type
        for meal_type in meal_plan:
            result_text += f"\n{meal_type} Options:\n" + "\n".join(meal_plan[meal_type]) + "\n"

        result_text += (f"\nTotal: {total_cals} cal, Protein: {total_prot}g, "
                        f"Carbs: {total_carbs}g, Fats: {total_fats}g")

        result_label.config(text=result_text, wraplength=350, justify="left", padx=10, pady=10)

    except ValueError as e:
        messagebox.showerror("Input Error", str(e))

# Setup the window and its layout as in your original code

# Get the screen dimensions
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Set a fixed width and maximize the height
window_width = 500  # Fixed window width
window_height = screen_height  # Set window height to the screen height

# Set the window size and position
root.geometry(f"{window_width}x{window_height}+{(screen_width - window_width) // 2}+0")
root.resizable(False, False)  # Disable window resizing

# Create input fields and labels
frame = tk.Frame(root, padx=10, pady=10)
frame.pack()

tk.Label(frame, text="Age:").grid(row=0, column=0, pady=5, sticky="w")
age_entry = tk.Entry(frame, width=15)
age_entry.grid(row=0, column=1, pady=5)

tk.Label(frame, text="Height (cm):").grid(row=1, column=0, pady=5, sticky="w")
height_entry = tk.Entry(frame, width=15)
height_entry.grid(row=1, column=1, pady=5)

tk.Label(frame, text="Weight (kg):").grid(row=2, column=0, pady=5, sticky="w")
weight_entry = tk.Entry(frame, width=15)
weight_entry.grid(row=2, column=1, pady=5)

# Dropdown for gender
tk.Label(frame, text="Gender:").grid(row=3, column=0, pady=5, sticky="w")
gender_var = tk.StringVar(value="Male")
gender_menu = ttk.Combobox(frame, textvariable=gender_var, values=["Male", "Female"], state="readonly", width=13)
gender_menu.grid(row=3, column=1, pady=5)

# Dropdown for activity level
tk.Label(frame, text="Activity Level:").grid(row=4, column=0, pady=5, sticky="w")
activity_var = tk.StringVar(value="Sedentary")
activity_menu = ttk.Combobox(frame, textvariable=activity_var,
                             values=["Sedentary", "Lightly Active", "Moderately Active", "Very Active"],
                             state="readonly", width=13)
activity_menu.grid(row=4, column=1, pady=5)

# Dropdown for goal
tk.Label(frame, text="Goal:").grid(row=5, column=0, pady=5, sticky="w")
goal_var = tk.StringVar(value="Maintenance")
goal_menu = ttk.Combobox(frame, textvariable=goal_var,
                         values=["Weight Loss", "Maintenance", "Muscle Gain"],
                         state="readonly", width=13)
goal_menu.grid(row=5, column=1, pady=5)

# Dropdown for diet preference
tk.Label(frame, text="Diet Preference:").grid(row=6, column=0, pady=5, sticky="w")
diet_var = tk.StringVar(value="None")
diet_menu = ttk.Combobox(frame, textvariable=diet_var,
                         values=["None", "keto", "vegetarian", "protein", "carb"],
                         state="readonly", width=13)
diet_menu.grid(row=6, column=1, pady=5)

# Create a button to calculate
calculate_button = tk.Button(frame, text="Calculate", command=calculate_and_display)
calculate_button.grid(row=7, column=0, columnspan=2, pady=10)

# Create a label to display results
result_label = tk.Label(root, text="", justify="left", padx=10, font=("Arial", 10))
result_label.pack(pady=10)

# Start the main event loop
root.mainloop()
