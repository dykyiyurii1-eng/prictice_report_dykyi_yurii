import asyncio
import csv
import os
from .save_data import *
async def load_products():
    """Асинхронне завантаження продуктів з CSV"""
    await asyncio.sleep(0)
    products = []
    try:
        with open(filename, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                row["quantity"] = int(row["quantity"])
                row["price"] = float(row["price"])
                products.append(row)
    except FileNotFoundError:
        return []
    return products


def load_buy_products():
    """Записування в змінну те, що в файлі-txt"""
    list_products.clear()
    try:
        with open(filename_txt, "r", encoding="utf-8") as file:
            for i in file:
                if i.strip():
                    list_products.append(i.strip())
        return list_products
    except FileNotFoundError:
        print("Файл ще не створений")
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        return []