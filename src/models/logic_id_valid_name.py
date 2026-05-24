import random
import string

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
    try:
        q = int(data["quantity"].strip())
        if q <= 0:
            raise ValueError
    except ValueError:
        return False, "Кількість має бути цілим числом > 0"
    try:
        p = float(data["price"].strip())
        if p <= 0:
            raise ValueError
    except ValueError:
        return False, "Ціна має бути числом > 0"
    return True, ""