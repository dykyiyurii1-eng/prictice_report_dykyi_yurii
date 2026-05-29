import random
import string
import re

def new_id(products):
    existing = [p["id"] for p in products]
    while True:
        num = str(random.randint(1, 100))
        chars = "".join(random.choices(string.ascii_lowercase, k=5))
        new_id = num + chars
        if new_id not in existing:
            return new_id

def validate_product(data):
    required = ["name", "category", "quantity", "place", "price", "end_date"]
    for field in required:
        if not data.get(field, "").strip():
            return False, "Заповніть усі поля та оберіть дату завершення"

    if not re.match(r"^\d+$", data["quantity"].strip()):
        return False, "Кількість має бути цілим числом"
    if int(data["quantity"].strip()) <= 0:
        return False, "Кількість має бути більше 0"

    if not re.match(r"^\d+(\.\d+)?$", data["price"].strip()):
        return False, "Ціна має бути числом"
    if float(data["price"].strip()) <= 0:
        return False, "Ціна має бути більше 0"

    if not re.match(r"^\d{2}\.\d{2}\.\d{4}$", data["end_date"].strip()):
        return False, "Дата має бути у форматі дд.мм.рррр"

    return True, ""