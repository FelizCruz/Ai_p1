import sqlite3

def create_database(db_name):
    # Connect to the SQLite database
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()

    # Drop existing tables if they exist (optional, for development)
    cursor.execute("DROP TABLE IF EXISTS meals")
    cursor.execute("DROP TABLE IF EXISTS workouts")

    # Create meals table with detailed nutritional information
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS meals (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        calories INTEGER NOT NULL,
        protein REAL NOT NULL,
        carbs REAL NOT NULL,
        fats REAL NOT NULL,
        type TEXT NOT NULL,
        meal_type TEXT NOT NULL
    )
    ''')

    # Meal data with detailed nutritional values (calories, protein, carbs, fats)
    meals_data = [
        ("Keto Omelette", 400, 25, 5, 30, "keto","Breakfast"),
        ("Keto Omelette", 400, 25, 5, 30, "keto", "Lunch"),
        ("Orange Juice",200,2,25,0,"vegetarian","Breakfast"),
        ("Lentils with Rice",200,4,45,0.5,"carb","Lunch"),
        ("Lentils with Rice", 200, 4, 45, 0.5, "carb", "Dinner"),
        ("Eggplant Curry",150,1.5,8,12,"vegetarian","Lunch"),
        ("Eggplant Curry", 150, 1.5, 8, 12, "vegetarian", "Dinner"),
        ("Sauteed Cauliflower",150,3,5,15,"keto","Lunch"),
        ("Sauteed Cauliflower", 150, 3, 5, 15, "keto", "Dinner"),
        ("Tomato and Spinach Pasta",350,14,70,3,"carb","Lunch"),
        ("Tomato and Spinach Pasta", 350, 14, 70, 3, "carb", "Dinner"),
        ("Greek Yogurt with Nuts", 300, 15, 20, 10, "protein","Breakfast"),
        ("Vegetable Stir Fry", 200, 5, 30, 5, "vegetarian","Lunch"),
        ("Vegetable Stir Fry", 200, 5, 30, 5, "vegetarian", "Dinner"),
        ("Chicken Breast", 220, 45, 0, 5, "protein","Lunch"),
        ("Chicken Breast", 220, 45, 0, 5, "protein", "Dinner"),
        ("Quinoa Salad", 280, 8, 40, 8, "carb","Breakfast"),
        ("Quinoa Salad", 280, 8, 40, 8, "carb", "Lunch"),
        ("Quinoa Salad", 280, 8, 40, 8, "carb", "Dinner"),
        ("Grilled Chicken Salad", 350, 30, 10, 18, "keto","Lunch"),
        ("Avocado Salad", 250, 3, 12, 22, "keto","Breakfast"),
        ("Avocado Salad", 250, 3, 12, 22, "keto", "Lunch"),
        ("Avocado Salad", 250, 3, 12, 22, "keto", "Dinner"),
        ("Paneer Tikka", 300, 18, 8, 20, "vegetarian","Lunch"),
        ("Paneer Tikka", 300, 18, 8, 20, "vegetarian", "Dinner"),
        ("Protein Smoothie", 220, 25, 18, 5, "protein", "Breakfast"),
        ("Protein Smoothie", 220, 25, 18, 5, "protein","Lunch"),
        ("Grilled Salmon", 450, 40, 0, 30, "protein","Lunch"),
        ("Grilled Salmon", 450, 40, 0, 30, "protein", "Dinner"),
        ("Egg White Omelette", 150, 20, 3, 4, "protein","Breakfast"),
        ("Almond Butter Shake", 400, 10, 15, 35, "keto","Breakfast"),
        ("Almond Butter Shake", 400, 10, 15, 35, "keto", "Lunch"),
        ("Almond Butter Shake", 400, 10, 15, 35, "keto", "Dinner"),
        ["Grilled Chicken Caesar Salad", 350, 35, 12, 20, "protein", "Lunch"],
        ["Blueberry Almond Oatmeal", 300, 8, 45, 10, "carb", "Breakfast"],
        ["Roasted Sweet Potato with Black Beans", 350, 8, 50, 6, "carb", "Lunch"],
         ["Grilled Ribeye with Garlic Butter", 550, 40, 0, 45, "protein", "Dinner"],
         ["Hummus and Veggie Wrap", 300, 10, 35, 12, "vegetarian", "Lunch"],
         ["Spinach and Quinoa Salad with Feta", 250, 10, 30, 8, "vegetarian", "Dinner"],
         ["Cottage Cheese with Pineapple", 180, 14, 20, 4, "protein", "Breakfast"],
         ["Chia Pudding with Coconut Milk", 350, 10, 30, 20, "keto", "Breakfast"],
         ["Mixed Nuts and Cheese Platter", 450, 15, 20, 35, "keto", "Lunch"],
         ["Tofu Curry with Rice", 400, 20, 50, 15, "vegetarian", "Dinner"],
         ["Cheese and Tomato Omelet", 300, 18, 5, 25, "protein", "Breakfast"],
         ["Beef Stir-Fry with Broccoli", 500, 35, 30, 20, "protein", "Dinner"],
         ["Avocado Smoothie with Spinach", 350, 8, 30, 22, "keto", "Lunch"],
         ["Chicken Tikka Masala with Basmati Rice", 550, 35, 60, 18, "protein", "Dinner"],
         ["Cauliflower Rice with Grilled Shrimp", 350, 30, 10, 18, "keto", "Dinner"],
         ["Falafel Wrap with Tzatziki", 450, 15, 60, 18, "vegetarian", "Lunch"],
         ["Eggplant Parmesan", 400, 15, 45, 15, "vegetarian", "Dinner"],
         ["Zucchini Noodles with Pesto and Cherry Tomatoes", 275, 10, 12, 20, "keto", "Lunch"],
          ["Lentil and Kale Stew", 300, 15, 50, 6, "vegetarian", "Dinner"],
          ["Grilled Salmon with Roasted Brussels Sprouts", 400, 35, 10, 22, "protein", "Dinner"],
          ["Stuffed Bell Peppers with Quinoa and Black Beans", 350, 12, 55, 8, "vegetarian", "Dinner"]
          ]

    cursor.executemany('INSERT INTO meals (name, calories, protein, carbs, fats, type, meal_type) VALUES (?, ?, ?, ?, ?, ?, ?)', meals_data)
    # Commit changes and close the connection
    connection.commit()
    connection.close()

if __name__ == "__main__":
    create_database("Diet_Recom.db")
    print("Database created successfully!")


