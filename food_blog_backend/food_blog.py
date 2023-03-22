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
      self.recipe_name = input("Recipe name <pass empty string to exit>: ")
      if self.recipe_name == "":
         self.flag = False
         return 0
      recipe_desc = input("Recipe description: ")
         
      self.cursor.execute(f"""
      INSERT INTO recipes(recipe_name, recipe_description)
      VALUES ('{self.recipe_name}', '{recipe_desc}');""")

      self.conn.commit()

    def ask_serving(self) -> None:
         meals = self.cursor.execute("""SELECT * FROM meals;""").fetchall()
         for meal in meals:
            id_, name = meal
            print(f"{id_}) {name}", end=" ")

         servings = input("\nWhen the dish can be served (space separated answer): ").split()

         recipe_id = self.cursor.execute(f'SELECT recipe_id FROM recipes WHERE recipe_name = "{self.recipe_name}"').fetchone()[0]

         for serving in servings:
            self.cursor.execute(f"""
            INSERT INTO serve(recipe_id, meal_id)
            VALUES ({recipe_id}, {serving});""")

         self.conn.commit()

    def ask_quantity(self) -> None:
       measures = self.cursor.execute("SELECT measure_name FROM measures").fetchall()
       measures = [msr[0] for msr in measures]
       print(measures)

       ingredients = self.cursor.execute("SELECT ingredient_name FROM ingredients").fetchall()
       ingredients = [ingr[0] for ingr in ingredients]

       while True:
         info = input("\nPlease enter info in the following format <quantity measure ingredient>\n" \
                      "Input quantity of ingredient <enter empty string to stop>: ")
         if info == "":
            break
         
         info = info.split()
         if info[1] not in measures:
            print("The measure is not conclusive!")
            continue

         if info[2] not in ingredients:
            print("The ingredient is not conclusive!")
            continue

         self.conn.commit()




    def run(self):
      self.flag = True
      while self.flag:
         self.ask_recipe()
         if self.flag == False:
            break
         self.ask_serving()
         self.ask_quantity()

      self.conn.close()

if __name__ == "__main__":
   app = Food_Blog()
   app.run()

