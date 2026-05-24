from .save_data import *
import csv
def write_table():
    global products
    # os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w", newline="", encoding="utf-8") as file:
        if products:
            writer = csv.DictWriter(file, fieldnames=list(products[0].keys()))
            writer.writeheader()
            writer.writerows(products)