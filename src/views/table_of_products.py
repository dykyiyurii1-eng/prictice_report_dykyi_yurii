import flet as ft
import datetime

from src.models.load_product import *
from src.models.write_table import *
from src.models.logic_id_valid_name import *
from src.views.menu import APP_BG, PANEL_BG, TEXT_DARK, navigation_menu


async def table_of_products1(page):
    page.favicon = "icon.ico"
    products = await load_products()

    style_field = dict(
        border_color=ft.Colors.BLUE_GREY_100,
        border_radius=8,
        bgcolor=ft.Colors.WHITE,
        focused_border_color=ft.Colors.CYAN_600,
        cursor_color=ft.Colors.CYAN_700,
        text_style=ft.TextStyle(size=14, weight=ft.FontWeight.W_500, color=TEXT_DARK),
        label_style=ft.TextStyle(color=ft.Colors.BLUE_GREY_700),
        hint_style=ft.TextStyle(color=ft.Colors.GREY_500, italic=True),
    )

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
        item = e.control.data
        table.rows[:] = [row for row in table.rows if row.data != item]
        products[:] = [p for p in products if p["id"] != item["id"]]
        write_table(products, filename)
        table.visible = bool(products)
        empty_state.visible = not bool(products)
        add_product.visible = bool(products)
        page.update()

    columns = [
        ft.DataColumn(ft.Text("ID", weight=ft.FontWeight.BOLD, color=TEXT_DARK)),
        ft.DataColumn(ft.Text("Назва", weight=ft.FontWeight.BOLD, color=TEXT_DARK)),
        ft.DataColumn(ft.Text("Категорія", weight=ft.FontWeight.BOLD, color=TEXT_DARK)),
        ft.DataColumn(ft.Text("Кількість", weight=ft.FontWeight.BOLD, color=TEXT_DARK)),
        ft.DataColumn(ft.Text("Місце", weight=ft.FontWeight.BOLD, color=TEXT_DARK)),
        ft.DataColumn(ft.Text("Ціна", weight=ft.FontWeight.BOLD, color=TEXT_DARK)),
        ft.DataColumn(ft.Text("Початок", weight=ft.FontWeight.BOLD, color=TEXT_DARK)),
        ft.DataColumn(ft.Text("Завершення", weight=ft.FontWeight.BOLD, color=TEXT_DARK)),
        ft.DataColumn(ft.Text("Дії", weight=ft.FontWeight.BOLD, color=TEXT_DARK)),
    ]

    table = ft.DataTable(
        border=ft.Border.all(1, ft.Colors.BLUE_GREY_100),
        border_radius=8,
        heading_row_color=ft.Colors.BLUE_GREY_50,
        heading_row_height=46,
        data_row_color=ft.Colors.WHITE,
        data_row_min_height=42,
        divider_thickness=1,
        column_spacing=16,
        horizontal_lines=ft.BorderSide(1, ft.Colors.BLUE_GREY_50),
        vertical_lines=ft.BorderSide(1, ft.Colors.BLUE_GREY_50),
        columns=columns,
        rows=[],
        visible=bool(products),
    )

    def cell_text(value, width=None):
        return ft.Text(
            str(value),
            size=13,
            color=TEXT_DARK,
            max_lines=2,
            overflow=ft.TextOverflow.ELLIPSIS,
            width=width,
        )

    def create_row(item):
        return ft.DataRow(
            cells=[
                ft.DataCell(cell_text(item["id"], 74)),
                ft.DataCell(cell_text(item["name"], 140)),
                ft.DataCell(cell_text(item["category"], 120)),
                ft.DataCell(cell_text(item["quantity"], 72)),
                ft.DataCell(cell_text(item["place"], 110)),
                ft.DataCell(cell_text(item["price"], 74)),
                ft.DataCell(cell_text(item["start_date"], 128)),
                ft.DataCell(cell_text(item["end_date"], 110)),
                ft.DataCell(
                    ft.Row(
                        spacing=4,
                        controls=[
                            ft.IconButton(
                                icon=ft.Icons.DELETE,
                                icon_color=ft.Colors.RED_600,
                                bgcolor=ft.Colors.RED_50,
                                tooltip="Видалити",
                                data=item,
                                on_click=delete_row,
                            ),
                            ft.IconButton(
                                icon=ft.Icons.EDIT_NOTE,
                                icon_color=ft.Colors.CYAN_700,
                                bgcolor=ft.Colors.CYAN_50,
                                tooltip="Редагувати",
                                data=item,
                                on_click=edit_row,
                            ),
                        ],
                    )
                ),
            ],
            data=item,
        )

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
        locale=ft.Locale("uk", "UA"),
        on_change=handle_change,
    )

    id_input = ft.TextField(
        value=new_id(products),
        label="ID",
        read_only=True,
        **style_field,
    )

    name_input = ft.TextField(
        label="Назва",
        prefix_icon=ft.Icons.LABEL_OUTLINE,
        **style_field,
    )

    category_input = ft.Dropdown(
        label="Категорія",
        border_color=ft.Colors.BLUE_GREY_100,
        border_radius=8,
        bgcolor=ft.Colors.WHITE,
        focused_border_color=ft.Colors.CYAN_600,
        text_style=ft.TextStyle(color=TEXT_DARK, size=14, weight=ft.FontWeight.W_500),
        label_style=ft.TextStyle(color=ft.Colors.BLUE_GREY_700),
        options=[
            ft.dropdown.Option(key="Молочне", content=ft.Row(controls=[ft.Icon(ft.Icons.WATER_DROP, color=ft.Colors.BLUE_400, size=18), ft.Text("Молочне", color=TEXT_DARK)])),
            ft.dropdown.Option(key="М'ясне", content=ft.Row(controls=[ft.Icon(ft.Icons.SET_MEAL, color=ft.Colors.RED_400, size=18), ft.Text("М'ясне", color=TEXT_DARK)])),
            ft.dropdown.Option(key="Овочі", content=ft.Row(controls=[ft.Icon(ft.Icons.ECO, color=ft.Colors.GREEN_500, size=18), ft.Text("Овочі", color=TEXT_DARK)])),
            ft.dropdown.Option(key="Фрукти", content=ft.Row(controls=[ft.Icon(ft.Icons.SPA, color=ft.Colors.ORANGE_400, size=18), ft.Text("Фрукти", color=TEXT_DARK)])),
            ft.dropdown.Option(key="Напої", content=ft.Row(controls=[ft.Icon(ft.Icons.LOCAL_DRINK, color=ft.Colors.CYAN_500, size=18), ft.Text("Напої", color=TEXT_DARK)])),
            ft.dropdown.Option(key="Заморожене", content=ft.Row(controls=[ft.Icon(ft.Icons.AC_UNIT, color=ft.Colors.LIGHT_BLUE_300, size=18), ft.Text("Заморожене", color=TEXT_DARK)])),
            ft.dropdown.Option(key="Бакалія", content=ft.Row(controls=[ft.Icon(ft.Icons.GRAIN, color=ft.Colors.BROWN_400, size=18), ft.Text("Бакалія", color=TEXT_DARK)])),
            ft.dropdown.Option(key="Інше", content=ft.Row(controls=[ft.Icon(ft.Icons.MORE_HORIZ, color=ft.Colors.BLUE_GREY_400, size=18), ft.Text("Інше", color=TEXT_DARK)])),
        ],
    )


    quantity_input = ft.TextField(
        label="Кількість",
        value="1",
        text_align=ft.TextAlign.CENTER,
        keyboard_type=ft.KeyboardType.NUMBER,
        **style_field,
    )

    def increment(e):
        try:
            quantity_input.value = str(int(quantity_input.value or 0) + 1)
        except ValueError:
            quantity_input.value = "1"
        quantity_input.update()

    def decrement(e):
        try:
            val = int(quantity_input.value or 0)
            if val > 1:
                quantity_input.value = str(val - 1)
        except ValueError:
            quantity_input.value = "1"
        quantity_input.update()

    quantity_row = ft.Row(
        controls=[
            ft.IconButton(
                icon=ft.Icons.REMOVE_CIRCLE_OUTLINE,
                icon_color=ft.Colors.CYAN_700,
                tooltip="Зменшити",
                on_click=decrement,
            ),
            quantity_input,
            ft.IconButton(
                icon=ft.Icons.ADD_CIRCLE_OUTLINE,
                icon_color=ft.Colors.CYAN_700,
                tooltip="Збільшити",
                on_click=increment,
            ),
        ],
        spacing=4,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )

    place_input = ft.Dropdown(
        label="Місце зберігання",
        text_style=ft.TextStyle(color=TEXT_DARK, size=14, weight=ft.FontWeight.W_500),
        label_style=ft.TextStyle(color=ft.Colors.BLUE_GREY_700),
        border_color=ft.Colors.BLUE_GREY_100,
        border_radius=8,
        bgcolor=ft.Colors.WHITE,
        focused_border_color=ft.Colors.CYAN_600,
        options=[
            ft.dropdown.Option(key="Холодильник", content=ft.Row(controls=[ft.Icon(ft.Icons.KITCHEN, color=ft.Colors.BLUE_400, size=18), ft.Text("Холодильник", color=TEXT_DARK)])),
            ft.dropdown.Option(key="Морозилка", content=ft.Row(controls=[ft.Icon(ft.Icons.AC_UNIT, color=ft.Colors.LIGHT_BLUE_300, size=18), ft.Text("Морозилка", color=TEXT_DARK)])),
            ft.dropdown.Option(key="Комора", content=ft.Row(controls=[ft.Icon(ft.Icons.STORAGE, color=ft.Colors.BROWN_400, size=18), ft.Text("Комора", color=TEXT_DARK)])),
            ft.dropdown.Option(key="Полиця", content=ft.Row(controls=[ft.Icon(ft.Icons.SHELVES, color=ft.Colors.ORANGE_400, size=18), ft.Text("Полиця", color=TEXT_DARK)])),
            ft.dropdown.Option(key="Інше", content=ft.Row(controls=[ft.Icon(ft.Icons.MORE_HORIZ, color=ft.Colors.BLUE_GREY_400, size=18), ft.Text("Інше", color=TEXT_DARK)])),
        ],
    )

    price_input = ft.TextField(
        label="Ціна",
        prefix_icon=ft.Icons.ATTACH_MONEY,
        keyboard_type=ft.KeyboardType.NUMBER,
        **style_field,
    )

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
        ft.Row([id_input, name_input, category_input, quantity_row]),
        ft.Row([place_input, price_input, start_date_input, end_date_input]),
    ], visible=False)

    def agree(e):
        data = {
            "name": name_input.value or "",
            "category": category_input.value or "",
            "quantity": quantity_input.value or "",
            "place": place_input.value or "",
            "price": price_input.value or "",
            "end_date": end_date_input.value or "",
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
            empty_state.visible = False

        write_table(products, filename)
        input_rows.visible = False
        add_btn_agree.visible = False
        btn_for_cancle.visible = False
        add_product.visible = bool(products)
        page.update()

    def cancle(e):
        add_product.visible = bool(products)
        input_rows.visible = False
        add_btn_agree.visible = False
        btn_for_cancle.visible = False
        empty_state.visible = not bool(products)
        page.update()

    def fields_see(e):
        if not input_rows.visible:
            id_input.value = new_id(products)
            quantity_input.value = "1"
        input_rows.visible = True
        add_btn_agree.visible = True
        btn_for_cancle.visible = True
        empty_state.visible = False
        page.update()

    btn_for_cancle = ft.Button(
        "Скасувати",
        icon=ft.Icons.CLOSE,
        on_click=cancle,
        visible=False,
        style=ft.ButtonStyle(
            bgcolor=ft.Colors.BLUE_GREY_50,
            color=ft.Colors.BLUE_GREY_800,
            shape=ft.RoundedRectangleBorder(radius=8),
        ),
    )
    add_btn_agree = ft.Button(
        "Підтвердити",
        on_click=agree,
        visible=False,
        style=ft.ButtonStyle(bgcolor=ft.Colors.CYAN_600, color=ft.Colors.WHITE),
    )
    add_product = ft.Row(
        [
            ft.Button(
                "Додати продукт",
                icon=ft.Icons.ADD,
                on_click=fields_see,
                style=ft.ButtonStyle(bgcolor=ft.Colors.CYAN_600, color=ft.Colors.WHITE),
            )
        ],
        alignment=ft.MainAxisAlignment.END,
        visible=bool(products),
    )

    def search_products(e):
        query = e.control.value.strip().lower()
        table.rows.clear()
        for item in products:
            if query in item["name"].lower():
                table.rows.append(create_row(item))
        table.visible = bool(table.rows)
        empty_state.visible = not bool(products)
        page.update()

    anchor = ft.SearchBar(
        view_elevation=100,
        divider_color=ft.Colors.AMBER,
        bar_hint_text="Пошук продуктів...",
        view_hint_text="Введіть назву продукту...",
        on_change=search_products,
    )

    table.rows = [create_row(item) for item in products]

    empty_state = ft.Container(
        visible=not bool(products),
        expand=True,
        alignment=ft.Alignment.CENTER,
        padding=32,
        content=ft.Column(
            spacing=14,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Icon(ft.Icons.INVENTORY_2_OUTLINED, size=56, color=ft.Colors.CYAN_700),
                ft.Text("Поки товарів немає", size=24, weight=ft.FontWeight.BOLD, color=TEXT_DARK),
                ft.Text(
                    "Ви можете додати перший продукт і одразу побачити його в таблиці.",
                    size=14,
                    color=ft.Colors.BLUE_GREY_600,
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Icon(ft.Icons.KEYBOARD_DOUBLE_ARROW_DOWN, size=32, color=ft.Colors.CYAN_700),
                ft.Button(
                    "Додати продукт",
                    icon=ft.Icons.ADD,
                    on_click=fields_see,
                    style=ft.ButtonStyle(bgcolor=ft.Colors.CYAN_600, color=ft.Colors.WHITE),
                ),
            ],
        ),
    )

    table_area = ft.Row(
        controls=[table],
        scroll=ft.ScrollMode.AUTO,
    )

    page_add = ft.SafeArea(
        expand=True,
        content=ft.Container(
            expand=True,
            padding=20,
            bgcolor=PANEL_BG,
            border_radius=8,
            content=ft.Column([
                input_rows,
                empty_state,
                table_area,
                ft.Row(
                    spacing=10,
                    controls=[
                        add_btn_agree,
                        btn_for_cancle,
                    ],
                ),
                add_product,
            ], scroll=ft.ScrollMode.AUTO,)
        ),
    )

    content = ft.Container(
        expand=True,
        bgcolor=APP_BG,
        padding=20,
        content=ft.Column([
            ft.AppBar(
                title=ft.Text("Продукти", color=TEXT_DARK, weight=ft.FontWeight.BOLD),
                bgcolor=APP_BG,
                elevation=0,
                actions=[anchor],
            ),
            page_add,
        ], expand=True),
    )

    return ft.View(
        route="/table_of_products",
        controls=[
            ft.Row(
                expand=True,
                spacing=0,
                controls=[
                    navigation_menu(page, "/table_of_products"),
                    content,
                ],
            )
        ],
    )