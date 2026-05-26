import csv
from .save_data import *
import os
def load_csv_products():
    """Записування в змінну те, що в таблиці"""
    products.clear()
    try:
        with open(filename,"r",encoding="utf-8") as file:
            save_product=csv.DictReader(file)
            for i in save_product:
                products.append({
                    "id": i["id"],
                    "name": i["name"],
                    "category": i["category"],
                    "quantity": int(i["quantity"]),
                    "place": i["place"],
                    "price": float(i["price"]),
                    "start_date": i["start_date"],
                    "end_date": i["end_date"]
                })
    except FileNotFoundError:
        pass

def products_add_to_txt(text):
    try:
        with open(filename_txt,"a",encoding="utf-8") as file:
            file.write(f'{text}\n')
    except FileNotFoundError:
        os.makedirs(os.path.dirname(filename), exist_ok=True)



def write_csv():
        try:
            with open(filename, "r", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                return reader

        except FileNotFoundError:
             return []




if __name__ == '__main__':
    load_csv_products()


