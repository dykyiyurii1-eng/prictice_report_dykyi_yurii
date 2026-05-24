import asyncio
import csv
from .save_data import *
async def load_products():
    """Асинхронне завантаження продуктів з CSV"""
    await asyncio.sleep(0)  # дає можливість UI оновлюватися
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
                product = i.strip()
                if product:
                    list_products.append(product)
    except FileNotFoundError:
        print("Файл ще не створений")