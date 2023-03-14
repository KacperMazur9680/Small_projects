import sqlite3

class Food_Blog:
    def __init__(self) -> None:
        data = {"meals": ("breakfast", "brunch", "lunch", "supper"),
          "ingredients": ("milk", "cacao", "strawberry", "blueberry", "blackberry", "sugar"),
             "measures": ("ml", "g", "l", "cup", "tbsp", "tsp", "dsp", "")}

        self.conn = sqlite3.connect("./food_blog_backend/food_blog_db.s3db")
        self.cursor = self.conn.cursor()
