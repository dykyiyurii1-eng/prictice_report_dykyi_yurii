import flet as ft
import flet_lottie as ftl
from src.models.load_product import *
from src.views.menu import APP_BG, PANEL_BG, TEXT_DARK, navigation_menu
from src.models.save_data import *
from src.models.product_add import products_add_to_txt

async def buy_products(page: ft.Page):
    page.scroll = "auto"
    picker = ft.DateRangePicker()
    load_buy_products()

    btn1 = ft.Button(
        "Pick date range",
        icon=ft.Icons.DATE_RANGE,
        on_click=lambda _: page.show_dialog(picker),
        style=ft.ButtonStyle(bgcolor=ft.Colors.CYAN_600, color=ft.Colors.WHITE),
    )

    async def handle_dialog_action_click(e: ft.Event[ft.TextButton]):
        page.pop_dialog()
        await dialog.data.confirm_dismiss(e.control.data)

    dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Please confirm"),
        content=ft.Text("Do you really want to delete this item?"),
        actions=[
            ft.TextButton("Yes", data=True, on_click=handle_dialog_action_click),
            ft.TextButton("No", data=False, on_click=handle_dialog_action_click),
        ],
        actions_alignment=ft.MainAxisAlignment.CENTER,
    )

    async def handle_confirm_dismiss(e: ft.DismissibleDismissEvent):
        if e.direction == ft.DismissDirection.END_TO_START:
            dialog.data = e.control
            page.show_dialog(dialog)
        else:
            await e.control.confirm_dismiss(True)

    def handle_dismiss(e: ft.Event[ft.Dismissible]):
        e.control.parent.controls.remove(e.control)
        e.control.parent.update()



    def make_dismissible(text: str):
        return ft.Dismissible(
            dismiss_direction=ft.DismissDirection.HORIZONTAL,
            background=ft.Container(bgcolor=ft.Colors.GREEN),
            secondary_background=ft.Container(bgcolor=ft.Colors.RED),
            on_dismiss=handle_dismiss,

            on_confirm_dismiss=handle_confirm_dismiss,
            dismiss_thresholds={
                ft.DismissDirection.END_TO_START: 0.2,
                ft.DismissDirection.START_TO_END: 0.2,
            },
            content=ft.ListTile(title=ft.Text(text)),
        )

    list_view = ft.ListView(
        expand=True,
        controls=[make_dismissible(f"{i}") for i in list_products],
    )

    name_input = ft.TextField(
        label="Введіть назву продукту",
        expand=True,
        border_color=ft.Colors.BLUE_GREY_300,
    )

    def add_new_item(e):
        if name_input.value.strip():
            list_view.controls.append(make_dismissible(name_input.value.strip()))
            products_add_to_txt(name_input.value.strip())
            name_input.value = ""
            list_view.update()

            # name_input.update()

    content = ft.Container(
        expand=True,
        bgcolor=APP_BG,
        padding=24,
        content=ft.Column(
            expand=True,
            spacing=18,
            controls=[
                ft.Text("Список покупок", size=28, weight=ft.FontWeight.BOLD, color=TEXT_DARK),
                ft.Row(
                    controls=[
                        name_input,
                        ft.IconButton(
                            icon=ft.Icons.ADD_CIRCLE,
                            icon_color=ft.Colors.CYAN_600,
                            icon_size=32,
                            tooltip="Додати продукт",
                            on_click=add_new_item,
                        ),
                    ],
                ),
                ft.Container(
                    height=170,
                    bgcolor=PANEL_BG,
                    border_radius=8,
                    border=ft.Border.all(1, ft.Colors.BLUE_GREY_100),
                    alignment=ft.Alignment.CENTER_LEFT,
                    padding=16,
                    content=ft.Row(
                        [
                            ftl.Lottie(
                                src="https://assets2.lottiefiles.com/packages/lf20_wd1udlcz.json",
                                reverse=False,
                                error_content=ft.Placeholder(ft.Text("Error loading Lottie")),
                                on_error=lambda e: print(f"Error loading Lottie: {e.data}"),
                            ),
                            ft.Text("Shopping list", size=24, weight=ft.FontWeight.BOLD, color=TEXT_DARK),
                        ],
                        spacing=20,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                ),
                ft.Container(
                    expand=True,
                    bgcolor=PANEL_BG,
                    border_radius=8,
                    border=ft.Border.all(1, ft.Colors.BLUE_GREY_100),
                    padding=10,
                    content=list_view,
                ),
                btn1,
            ],
        ),
    )

    return ft.View(
        route="/buy_products",
        controls=[
            ft.Row(
                expand=True,
                spacing=0,
                controls=[
                    navigation_menu(page, "/buy_products"),
                    content,
                ],
            )
        ],
    )