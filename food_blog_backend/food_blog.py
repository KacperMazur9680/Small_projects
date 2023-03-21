import sqlite3
import sys

class Food_Blog:
    def __init__(self) -> None:
        db_name = sys.argv[1]
        self.conn = sqlite3.connect(f"./food_blog_backend/{db_name}")
        self.cursor = self.conn.cursor()


        self.cursor.execute("""PRAGMA foreign_keys = ON;""")

        def create_table(table_name: str, name: str, not_null: str="NOT NULL") -> None:
          self.cursor.execute(f"""
          CREATE TABLE IF NOT EXISTS {table_name} (
          {name}_id INTEGER PRIMARY KEY,
          {name}_name TEXT UNIQUE {not_null}
          );
          """)

        create_table("meals", "meal")
        create_table("ingredients", "ingredient")
        create_table("measures", "measure", not_null="")

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS recipes(
        recipe_id INTEGER PRIMARY KEY,
        recipe_name TEXT NOT NULL,
        recipe_description TEXT
        );""")

        self.data = {
                "meals": ("breakfast", "brunch", "lunch", "supper"),
          "ingredients": ("milk", "cacao", "strawberry", "blueberry", "blackberry", "sugar"),
             "measures": ("ml", "g", "l", "cup", "tbsp", "tsp", "dsp", "")
             }
  
        try:
          for key, vals in self.data.items():
            for val in vals:
                self.cursor.execute(f"""
                INSERT INTO {key}({key[:-1]}_name)
                VALUES ('{val}');""")
        except sqlite3.IntegrityError:
          pass        
      
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS serve(
        serve_id INTEGER PRIMARY KEY,
        recipe_id INTEGER NOT NULL,
        meal_id INTEGER NOT NULL,
        FOREIGN KEY(recipe_id) REFERENCES recipes(recipe_id),
        FOREIGN KEY(meal_id) REFERENCES meals(meal_id)
        );""")
       
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS quantity(
        quantity_id INTEGER PRIMARY KEY,
        measure_id INTEGER NOT NULL,
        ingredient_id INTEGER NOT NULL,
        quantity INTEGER NOT NULL,
        recipe_id INTEGER NOT NULL,
        FOREIGN KEY(measure_id) REFERENCES measures(measure_id),
        FOREIGN KEY(ingredient_id) REFERENCES ingredients(ingredient_id),
        FOREIGN KEY(recipe_id) REFERENCES recipes(recipe_id)
        );""")

        self.conn.commit()
        print("Data added.\n")

    def ask_recipe(self) -> None:
      print("Pass empty string to exit.")
      while True:
         recipe_name = input("Recipe name: ")
         if recipe_name == "":
            break
         recipe_desc = input("Recipe description: ")
         
         self.cursor.execute(f"""
         INSERT INTO recipes(recipe_name, recipe_description)
         VALUES ('{recipe_name}', '{recipe_desc}');""")

         meals = self.cursor.execute("""SELECT * FROM meals;""").fetchall()
         for meal in meals:
            id_, name = meal
            print(f"{id_}) {name}", end=" ")

         servings = input("\nWhen the dish can be served (space separetad answer): ").split()

         recipe_id = self.cursor.execute(f'SELECT recipe_id FROM recipes WHERE recipe_name = "{recipe_name}"').fetchone()[0]

         for serving in servings:
            self.cursor.execute(f"""
            INSERT INTO serve(recipe_id, meal_id)
            VALUES ({recipe_id}, {serving});""")

         self.conn.commit()

    def run(self):
      self.ask_recipe()
      self.conn.close()

if __name__ == "__main__":
   app = Food_Blog()
   app.run()

