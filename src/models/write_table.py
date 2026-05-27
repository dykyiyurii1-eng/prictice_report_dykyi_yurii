from .save_data import *
import csv
from pathlib import Path
def write_table(products,  filename):
    Path(history_file).parent.mkdir(parents=True, exist_ok=True)
    with open(filename, "w", newline="", encoding="utf-8") as file:
        if products:
            writer = csv.DictWriter(file, fieldnames=list(products[0].keys()))
            writer.writeheader()
            writer.writerows(products)