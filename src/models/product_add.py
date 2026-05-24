import csv
from .save_data import *

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





def products_csv():
    """Записування продуктів до CSV-таблиці"""
    with open(filename, "w", newline="",encoding="utf-8") as file:
        if not products:
            return print('На даний момент продуктів немає')
        columns = list(products[0].keys())
        writer = csv.DictWriter(file, fieldnames=columns)
        writer.writeheader()
        writer.writerows(products)


def write_csv():
        try:
            with open(filename, "r", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                return reader

        except FileNotFoundError:
             return []

def show_all_products():
    """Читання CSV-таблиці"""
    with open(filename, "r", newline="", encoding="utf-8") as file:
        product_table=list(csv.DictReader(file))
        if not product_table:
            return print()
        return product_table



if __name__ == '__main__':
    load_csv_products()
    products_csv()
    show_all_products()

