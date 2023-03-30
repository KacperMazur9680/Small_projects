import sqlite3
import sys
import argparse

class Food_Blog:
    def __init__(self) -> None:
        parser = argparse.ArgumentParser(description="Print out available recipes with given info.")
        parser.add_argument("db_name", type=str, help="insert the database name with file extension.")
        parser.add_argument("--ingredients", type=str, help="insert comma separated ingredients.")
        parser.add_argument("--meals", type=str, help="insert comma separated mealtimes.")
        self.args = parser.parse_args()
        self.conn = sqlite3.connect(f"./food_blog_backend/{self.args.db_name}")
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

         self.recipe_id = self.cursor.execute(f'SELECT recipe_id FROM recipes WHERE recipe_name = "{self.recipe_name}"').fetchone()[0]

         for serving in servings:
            self.cursor.execute(f"""
            INSERT INTO serve(recipe_id, meal_id)
            VALUES ({self.recipe_id}, {serving});""")

         self.conn.commit()

    def ask_quantity(self) -> None:
       measures = self.cursor.execute("SELECT measure_name FROM measures").fetchall()
       measures = [msr[0] for msr in measures]

       ingredients = self.cursor.execute("SELECT ingredient_name FROM ingredients").fetchall()
       ingredients = [ingr[0] for ingr in ingredients]

       while True:
         info = input("\nPlease enter info in the following format <quantity measure ingredient>\n" \
                      "Input quantity of ingredient <enter empty string to stop>: ")
         if info == "":
            break
         
         info = info.split()
         if len(info) == 2:
            if info[1] not in ingredients:
               print("The ingredient is not conclusive!")
               continue
            quantity = info[0]
            ingredient = info[1]
            measure = ""

         else:
            if info[1] not in measures:
               print("The measure is not conclusive!")
               continue

            if info[2] not in ingredients:
               print("The ingredient is not conclusive!")
               continue
            
            quantity = info[0]
            measure = info[1]
            ingredient = info[2]
         
         self.cursor.execute(f"""INSERT INTO quantity(measure_id, ingredient_id, quantity, recipe_id)
         VALUES ((select measure_id from measures where measure_name = "{measure}"), \
         (select ingredient_id from ingredients where ingredient_name = "{ingredient}"), {quantity}, \
         {self.recipe_id});""")
         
       self.conn.commit()
    
    def select_recipes(self) -> None:
      try:
         ingredients = tuple(self.args.ingredients.split(","))
         meals = tuple(self.args.meals.split(","))
      except AttributeError:
         print("Both parameters have to be input for the recipe selecting script to work properly.")
         sys.exit(1)
      
      if len(meals) == 1:
         meals = str(meals).replace(",", "")

      if len(ingredients) == 1:
         ingredients = str(ingredients).replace(",", "")
            
      recipes = self.cursor.execute(f"""
        SELECT recipe_name 
        FROM recipes 
        WHERE recipe_id IN 
        (
            SELECT recipe_id 
            FROM quantity 
            WHERE ingredient_id IN 
               (
               SELECT ingredient_id 
               FROM ingredients 
               WHERE ingredient_name IN {ingredients}
               ) 
            GROUP BY recipe_id 
            HAVING COUNT(DISTINCT ingredient_id) = {len(ingredients)}
        )
        
        INTERSECT

         SELECT recipe_name
         FROM recipes 
         WHERE recipe_id IN 
         (
             SELECT recipe_id 
             FROM serve WHERE meal_id IN 
             (
               SELECT meal_id 
               FROM meals 
               WHERE meal_name IN {meals}
             )
         )
      """).fetchall()

      if len(recipes) == 0:
         print("There are no such recipes in the database.")
      else:
         print(f"Recipes selected for you: {', '.join([recipe[0] for recipe in recipes])}")

    def run(self) -> None:
      if len(sys.argv) == 2:
         self.flag = True

         while self.flag:
            self.ask_recipe()

            if self.flag == False:
               break

            self.ask_serving()
            self.ask_quantity()

      else:
         self.select_recipes()

      self.conn.close()


if __name__ == "__main__":
   app = Food_Blog()
   app.run()

