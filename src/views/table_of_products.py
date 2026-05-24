import flet as ft
import datetime

from src.models.load_product import load_products
from src.models.write_table import *
from src.models.logic_id_valid_name import *



def table_of_products1(page):
    page.favicon = "icon.ico"


    style_field = dict(
        border_color=ft.Colors.BLUE_400,
        border_radius=8,
        bgcolor=ft.Colors.BLUE_50,
        focused_border_color=ft.Colors.BLUE_600,
        cursor_color=ft.Colors.RED,
        text_style=ft.TextStyle(size=14, weight=ft.FontWeight.BOLD),
        label_style=ft.TextStyle(color=ft.Colors.BLUE_800),
        hint_style=ft.TextStyle(color=ft.Colors.GREY_500, italic=True),
    )

    async def go_city(e):
        await page.push_route("/")

    async def go_user_add(e):
        await page.push_route("/add_user")

    def edit_row(e):
        item = e.control.data
        id_input.value = item["id"]
        name_input.value = item["name"]
        category_input.value = item["category"]
        quantity_input.value = str(item["quantity"])
        place_input.value = item["place"]
        price_input.value = str(item["price"])
        end_date_input.value = item["end_date"]
        input_rows.visible = True
        add_btn_agree.visible = True
        btn_for_cancle.visible = True
        page.update()

    def delete_row(e):
        global products
        item = e.control.data
        table.rows = [row for row in table.rows if row.data != item]
        products = [p for p in products if p["id"] != item["id"]]
        write_table()
        table.visible = bool(products)
        page.update()

    columns = [
        ft.DataColumn(ft.Text("ID")),
        ft.DataColumn(ft.Text("Назва")),
        ft.DataColumn(ft.Text("Категорія")),
        ft.DataColumn(ft.Text("Кількість")),
        ft.DataColumn(ft.Text("Місце")),
        ft.DataColumn(ft.Text("Ціна")),
        ft.DataColumn(ft.Text("Дата початку")),
        ft.DataColumn(ft.Text("Дата завершення")),
        ft.DataColumn(ft.Text("Дії")),
    ]

    table = ft.DataTable(
        border=ft.Border.all(1, ft.Colors.BLUE_400),
        border_radius=10,
        heading_row_color=ft.Colors.BLUE_100,
        heading_row_height=40,
        data_row_color=ft.Colors.WHITE,
        data_row_min_height=35,
        divider_thickness=1,
        column_spacing=20,
        horizontal_lines=ft.BorderSide(1, ft.Colors.GREY_300),
        vertical_lines=ft.BorderSide(1, ft.Colors.GREY_300),
        columns=columns,
        rows=[],
        visible=bool(products),
    )

    def create_row(item):
        return ft.DataRow(
            cells=[
                ft.DataCell(ft.Text(item["id"])),
                ft.DataCell(ft.Text(item["name"])),
                ft.DataCell(ft.Text(item["category"])),
                ft.DataCell(ft.Text(str(item["quantity"]))),
                ft.DataCell(ft.Text(item["place"])),
                ft.DataCell(ft.Text(str(item["price"]))),
                ft.DataCell(ft.Text(item["start_date"])),
                ft.DataCell(ft.Text(item["end_date"])),
                ft.DataCell(
                    ft.Row([
                        ft.IconButton(icon=ft.Icons.DELETE, data=item, on_click=delete_row),
                        ft.IconButton(icon=ft.Icons.EDIT_NOTE, data=item, on_click=edit_row),
                    ])
                ),
            ],
            data=item,
        )

    for item in products:
        table.rows.append(create_row(item))

    def handle_change(e):
        if e.control.value:
            local_date = e.control.value.astimezone()
            end_date_input.value = local_date.strftime("%d.%m.%Y")
            page.update()

    today = datetime.datetime.now()
    picker = ft.DatePicker(
        first_date=datetime.datetime(year=today.year, month=today.month, day=today.day),
        last_date=datetime.datetime(year=today.year + 1, month=12, day=31),
        current_date=today,
        on_change=handle_change,
    )

    id_input = ft.TextField(value=new_id(products), label="ID", read_only=True, **style_field)
    name_input = ft.TextField(label="Назва", **style_field)
    category_input = ft.TextField(label="Категорія", **style_field)
    quantity_input = ft.TextField(label="Кількість", **style_field)
    place_input = ft.TextField(label="Місце", **style_field)
    price_input = ft.TextField(label="Ціна", **style_field)
    end_date_input = ft.TextField(
        label="Дата завершення",
        read_only=True,
        prefix_icon=ft.Icons.CALENDAR_MONTH,
        on_click=lambda e: page.show_dialog(picker),
        **style_field,
    )
    start_date_input = ft.TextField(
        label="Дата початку",
        helper=f'Дата буде записана так {datetime.datetime.now().strftime("%d.%m.%Y %H:%M")}',
        read_only=True,
        prefix_icon=ft.Icons.CALENDAR_MONTH,
        **style_field,
    )

    input_rows = ft.Column([
        ft.Row([id_input, name_input, category_input, quantity_input]),
        ft.Row([place_input, price_input, start_date_input, end_date_input]),
    ], visible=False)

    def agree(e):
        data = {
            "name": name_input.value,
            "category": category_input.value,
            "quantity": quantity_input.value,
            "place": place_input.value,
            "price": price_input.value,
            "end_date": end_date_input.value,
        }
        ok, msg = validate_product(data)
        if not ok:
            page.show_dialog(
                ft.AlertDialog(
                    title=ft.Text("Помилка"),
                    content=ft.Text(msg),
                    actions=[ft.TextButton("Ок", on_click=lambda e: page.pop_dialog())],
                    open=True,
                )
            )
            return

        quantity_val = int(quantity_input.value.strip())
        price_val = float(price_input.value.strip())

        product = next((p for p in products if p["id"] == id_input.value), None)
        if product:
            product.update({
                "name": name_input.value.strip(),
                "category": category_input.value.strip(),
                "quantity": quantity_val,
                "place": place_input.value.strip(),
                "price": price_val,
                "end_date": end_date_input.value.strip(),
            })
            for row in table.rows:
                if row.data["id"] == product["id"]:
                    row.data = product
                    row.cells[1].content.value = product["name"]
                    row.cells[2].content.value = product["category"]
                    row.cells[3].content.value = str(product["quantity"])
                    row.cells[4].content.value = product["place"]
                    row.cells[5].content.value = str(product["price"])
                    row.cells[7].content.value = product["end_date"]
                    break
        else:
            start_date_val = datetime.datetime.now().strftime("%d.%m.%Y %H:%M")
            new_item = {
                "id": id_input.value.strip(),
                "name": name_input.value.strip(),
                "category": category_input.value.strip(),
                "quantity": quantity_val,
                "place": place_input.value.strip(),
                "price": price_val,
                "start_date": start_date_val,
                "end_date": end_date_input.value.strip(),
            }
            products.append(new_item)
            table.rows.append(create_row(new_item))
            table.visible = True

        write_table()
        input_rows.visible = False
        add_btn_agree.visible = False
        btn_for_cancle.visible = False
        page.update()

    def cancle(e):
        input_rows.visible = False
        add_btn_agree.visible = False
        btn_for_cancle.visible = False
        page.update()

    def fields_see(e):
        id_input.value = new_id(products)
        input_rows.visible = True
        add_btn_agree.visible = True
        btn_for_cancle.visible = True
        page.update()

    btn_for_cancle = ft.Button("Скасувати", on_click=cancle, visible=False)
    add_btn_agree = ft.Button("Підтвердити", on_click=agree, visible=False)
    add_product = ft.Row(
        [ft.Button("Додати продукт", on_click=fields_see)],
        alignment=ft.MainAxisAlignment.END,
    )

    def search_products(e):
        query = e.control.value.strip().lower()
        table.rows.clear()
        for item in products:
            if query in item["name"].lower():
                table.rows.append(create_row(item))
        table.visible = bool(table.rows)
        page.update()

    anchor = ft.SearchBar(
        view_elevation=4,
        divider_color=ft.Colors.AMBER,
        bar_hint_text="Пошук продуктів...",
        view_hint_text="Введіть назву продукту...",
        on_change=search_products,
    )

    page_add = ft.SafeArea(
        expand=True,
        content=ft.Container(
            content=ft.Column([
                input_rows,
                table,
                add_btn_agree,
                add_product,
                btn_for_cancle,
                ft.NavigationDrawer(
                    controls=[
                        ft.Container(
                            padding=ft.Padding.only(left=28, top=20, bottom=12),
                            content=ft.Text("🚀 HomeStock", size=18, weight=ft.FontWeight.BOLD, color="#FF00FF"),
                        ),
                        ft.NavigationDrawerDestination(
                            icon=ft.Icons.INVENTORY_2,
                            selected_icon=ft.Icons.INVENTORY,
                            label="Інвентар",
                        ),
                        ft.NavigationDrawerDestination(
                            icon=ft.Icons.SHOPPING_BAG_OUTLINED,
                            selected_icon=ft.Icons.SHOPPING_BAG,
                            label="Покупки",
                        ),
                        ft.NavigationDrawerDestination(
                            icon=ft.Icons.BAR_CHART_OUTLINED,
                            selected_icon=ft.Icons.BAR_CHART,
                            label="Аналітика",
                        ),
                        ft.NavigationDrawerDestination(
                            icon=ft.Icons.SETTINGS_OUTLINED,
                            selected_icon=ft.Icons.SETTINGS,
                            label="Налаштування",
                        ),
                    ],
                )
            ], spacing=20),
        ),
    )

    return ft.View(
        route="/table_of_products",
        controls=[ft.Column([
            ft.AppBar(
                title=ft.Text("Flet app"),
                actions=[
                    anchor,
                    ft.IconButton(ft.Icons.HOUSE, on_click=go_city),
                    ft.IconButton(ft.Icons.LOCATION_CITY_ROUNDED),
                ]
            ),
            page_add,
        ], expand=True)]
    )