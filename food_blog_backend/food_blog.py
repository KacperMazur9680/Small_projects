import sqlite3
import sys

class Food_Blog:
    def __init__(self) -> None:
        self.data = {
                "meals": ("breakfast", "brunch", "lunch", "supper"),
          "ingredients": ("milk", "cacao", "strawberry", "blueberry", "blackberry", "sugar"),
             "measures": ("ml", "g", "l", "cup", "tbsp", "tsp", "dsp", "")
             }

        db_name = sys.argv[1]
        self.conn = sqlite3.connect(f"./food_blog_backend/{db_name}")
        self.cursor = self.conn.cursor()

        def create_table(table_name, name, not_null="NOT NULL"):
          self.cursor.execute(f"""
          CREATE TABLE IF NOT EXISTS {table_name} (
          {name}_id INTEGER PRIMARY KEY,
          {name}_name TEXT UNIQUE {not_null}
          );
          """)

        create_table("meals", "meal")
        create_table("ingredients", "ingredient")
        create_table("measures", "measure", not_null="")

    def populate(self):
      for key, vals in self.data.items():
         for val in vals:
            self.cursor.execute(f"""
            INSERT INTO {key}({key[:-1]}_name)
            VALUES ('{val}');""")
            
      self.conn.commit()
      print("Data added.")

    def run(self):
      self.populate()
      self.conn.close()

if __name__ == "__main__":
   app = Food_Blog()
   app.run()

