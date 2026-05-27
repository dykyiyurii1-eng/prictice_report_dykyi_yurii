from .save_data import *
import os


def products_add_to_txt(text):
    try:
        with open(filename_txt,"a",encoding="utf-8") as file:
            file.write(f'{text}\n')
    except FileNotFoundError:
        os.makedirs(os.path.dirname(filename), exist_ok=True)


def products_remove_from_txt(name: str):
    lines = []
    with open(filename_txt, "r", encoding="utf-8") as f:
        lines = f.readlines()
    with open(filename_txt, "w", encoding="utf-8") as f:
        for line in lines:
            if line.strip() != name.strip():
                f.write(line)






