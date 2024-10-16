import tkinter as tk
from tkinter import messagebox
import heapq
import copy
import sqlite3
import matplotlib.pyplot as plt
import networkx as nx

def create_database(db_name="fitness_workouts.db"):
    """Creates the SQLite database and populates it with workouts."""
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()

    # Drop the existing table if it exists
    cursor.execute("DROP TABLE IF EXISTS workouts")

    # Create table for workouts
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS workouts (
        name TEXT PRIMARY KEY,
        calories_burned INTEGER,
        duration INTEGER,
        reps INTEGER,
        intensity TEXT
    );
    """)

    # Insert workout data
    workouts_data = [
        ("Running", 500, 30, 0, "high"),
        ("Weightlifting", 300, 45, 10, "high"),
        ("Yoga", 200, 60, 0, "low"),
        ("HIIT", 600, 20, 15, "high"),
        ("Cycling", 400, 45, 0, "high"),
        ("Swimming", 600, 30, 0, "high"),
        ("Pilates", 250, 40, 0, "low"),
        ("Rock Climbing", 500, 60, 5, "high"),
        ("Dance Class", 300, 60, 0, "low"),
        ("Boxing", 450, 30, 15, "high"),
        ("Walking", 150, 60, 0, "low")
    ]

    # Insert data into the table
    cursor.executemany("INSERT OR IGNORE INTO workouts VALUES (?, ?, ?, ?, ?);", workouts_data)

    # Commit changes and close connection
    connection.commit()
    connection.close()
    print(f"Database '{db_name}' created and populated successfully.")

class AStarWorkoutPlanner:
    def __init__(self, db_name):
        self.workouts = self.load_data(db_name)
        self.expansion_history = []
        self.graph = nx.Graph()

    def load_data(self, db_name):
        """Load workouts from the SQLite database."""
        connection = sqlite3.connect(db_name)
        cursor = connection.cursor()

        cursor.execute("SELECT name, calories_burned, duration, reps, intensity FROM workouts")
        workouts = [{"name": row[0], "calories_burned": row[1], "duration": row[2], "reps": row[3], "intensity": row[4]} for row in cursor.fetchall()]

        connection.close()
        return workouts

    def heuristic(self, state, goal_calories):
        """Estimate remaining calories to burn."""
        remaining = max(0, goal_calories - state["calories"])
        return remaining

    def find_workout_plan(self, goal_calories, intensity):
        """A* search to find the optimal workout plan."""
        if goal_calories <= 0:
            return None

        start_state = {
            "calories": 0,
            "workouts": []
        }
        frontier = []
        visited = set()
        counter = 0

        heapq.heappush(frontier, (self.heuristic(start_state, goal_calories), counter, start_state))
        self.graph.add_node(0, calories=0)

        while frontier:
            _, _, current_state = heapq.heappop(frontier)
            self.expansion_history.append(current_state["calories"])

            # Check if we've reached or exceeded the goal calories
            if current_state["calories"] >= goal_calories:
                return current_state

            state_key = tuple((workout["name"], workout["sets"]) for workout in current_state["workouts"])
            if state_key in visited:
                continue
            visited.add(state_key)

            for workout in self.workouts:
                # Apply intensity filter
                if intensity == "low" and workout["intensity"] == "high":
                    continue
                if intensity == "high" and workout["intensity"] == "low":
                    continue

                new_state = copy.deepcopy(current_state)
                new_state["calories"] += workout["calories_burned"]
                found = False
                for w in new_state["workouts"]:
                    if w["name"] == workout["name"]:
                        w["sets"] += 1
                        found = True
                        break
                if not found:
                    new_state["workouts"].append({
                        "name": workout["name"],
                        "duration": workout["duration"],
                        "reps": workout["reps"],
                        "sets": 1,
                        "calories_burned": workout["calories_burned"]
                    })
                counter += 1
                heapq.heappush(frontier, (self.heuristic(new_state, goal_calories), counter, new_state))
                self.graph.add_node(counter, calories=new_state["calories"])
                self.graph.add_edge(counter - 1, counter)

        return None  # No valid plan found

class FitnessPlannerApp:
    def __init__(self, root, db_name):
        self.root = root
        self.root.title("Fitness Planner")

        self.height_label = tk.Label(root, text="Enter your height (cm):")
        self.height_label.grid(row=0, column=0)
        self.height_entry = tk.Entry(root)
        self.height_entry.grid(row=0, column=1)

        self.weight_label = tk.Label(root, text="Enter your weight (kg):")
        self.weight_label.grid(row=1, column=0)
        self.weight_entry = tk.Entry(root)
        self.weight_entry.grid(row=1, column=1)

        self.caloric_intake_label = tk.Label(root, text="Enter your daily caloric intake:")
        self.caloric_intake_label.grid(row=2, column=0)
        self.caloric_intake_entry = tk.Entry(root)
        self.caloric_intake_entry.grid(row=2, column=1)

        self.intensity_label = tk.Label(root, text="Choose your intensity:")
        self.intensity_label.grid(row=3, column=0)
        self.intensity_var = tk.StringVar(root)
        self.intensity_var.set("low")
        self.low_intensity_radio = tk.Radiobutton(root, text="Low Intensity", variable=self.intensity_var, value="low")
        self.low_intensity_radio.grid(row=3, column=1)
        self.high_intensity_radio = tk.Radiobutton(root, text="High Intensity", variable=self.intensity_var, value="high")
        self.high_intensity_radio.grid(row=3, column=2)

        self.plan_button = tk.Button(root, text="Get Workout Plan", command=self.get_workout_plan)
        self.plan_button.grid(row=4, column=0, columnspan=3)

        self.result_text = tk.Text(root, height=10, width=40)
        self.result_text.grid(row=5, column=0, columnspan=3)

    def get_workout_plan(self):
        try:
            height = int(self.height_entry.get())
            weight = int(self.weight_entry.get())
            caloric_intake = int(self.caloric_intake_entry.get())
            intensity = self.intensity_var.get()

            # Calculate BMR
            bmr = 10 * weight + 6.25 * height - 5 * 25 + 5  # Adding 5 for male BMR calculation
            goal_calories = caloric_intake - bmr

            planner = AStarWorkoutPlanner("fitness_workouts.db")
            workout_plan = planner.find_workout_plan(goal_calories, intensity)

            if workout_plan:
                result_text = "Workout Plan:\n"
                total_calories_burned = 0
                for workout in workout_plan["workouts"]:
                    result_text += f"- {workout['name']} ({workout['duration']} mins, {workout['reps']} reps, {workout['sets']} sets)\n"
                    total_calories_burned += workout["calories_burned"] * workout["sets"]
                result_text += f"\nEstimated Calories Burned: {total_calories_burned} kcal"
                self.result_text.delete(1.0, tk.END)
                self.result_text.insert(tk.END, result_text)

                # Plot the expansion of nodes
                pos = nx.spring_layout(planner.graph)
                nx.draw(planner.graph, pos, with_labels=True, node_size=500, node_color="skyblue", font_size=10, font_weight="bold")
                plt.title(f"A* Search Node Expansion (Total Nodes Expanded: {len(planner.graph.nodes)})")
                plt.show()
            else:
                messagebox.showinfo("Error", "No valid workout plan found.")
        except ValueError:
            messagebox.showinfo("Error", "Invalid input. Please enter valid height, weight, and caloric intake.")

if __name__ == "__main__":
    create_database()
    root = tk.Tk()
    app = FitnessPlannerApp(root, "fitness_workouts.db")
    root.mainloop()