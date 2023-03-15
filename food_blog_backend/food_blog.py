import sqlite3
import sys

class Food_Blog:
    def __init__(self) -> None:
        db_name = sys.argv[1]
        self.conn = sqlite3.connect(f"./food_blog_backend/{db_name}")
        self.cursor = self.conn.cursor()

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
      
        self.conn.commit()
        print("Data added.")

    def ask_recipe(self) -> None:
      print("Pass the empty recipe name to exit.")
      while True:
         recipe_name = input("Recipe name: ")
         if recipe_name == "":
            break
         recipe_desc = input("Recipe description: ")

         self.cursor.execute(f"""
         INSERT INTO recipes(recipe_name, recipe_description)
         VALUES ('{recipe_name}', '{recipe_desc}');""")
         self.conn.commit()


    def run(self):
      self.ask_recipe()
      self.conn.close()

if __name__ == "__main__":
   app = Food_Blog()
   app.run()

