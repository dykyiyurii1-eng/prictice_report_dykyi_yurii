import flet as ft
import flet_lottie as ftl
from src.models.load_product import *
from src.views.menu import APP_BG, PANEL_BG, TEXT_DARK, navigation_menu
from src.models.save_data import *
from src.models.product_add import products_add_to_txt, products_remove_from_txt
from src.models.history_buy import load_history, save_to_history, clear_history


async def buy_products(page: ft.Page):
    page.scroll = "auto"
    load_buy_products()

    edit_input = ft.TextField(label="Редагувати назву", expand=True)

    async def handle_dialog_action_click(e: ft.Event[ft.TextButton]):
        page.pop_dialog()
        await dialog.data.confirm_dismiss(e.control.data)

    dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Підтвердіть дію"),
        content=ft.Text("Ви дійсно хочете видалити цей елемент?"),
        actions=[
            ft.TextButton("Так", data=True, on_click=handle_dialog_action_click),
            ft.TextButton("Ні", data=False, on_click=handle_dialog_action_click),
        ],
        actions_alignment=ft.MainAxisAlignment.CENTER,
    )

    async def handle_confirm_dismiss(e: ft.DismissibleDismissEvent):
        if e.direction == ft.DismissDirection.START_TO_END:
            dialog.data = e.control
            page.show_dialog(dialog)
        else:
            dismissible = e.control
            edit_input.value = dismissible.content.content.title.value

            async def save(ev):
                old_name = dismissible.content.content.title.value
                dismissible.content.content.title.value = edit_input.value
                dismissible.content.content.update()
                save_to_history("Відредаговано", f"{old_name} → {edit_input.value}")
                page.pop_dialog()
                await dismissible.confirm_dismiss(False)

            async def cancel(ev):
                page.pop_dialog()
                await dismissible.confirm_dismiss(False)

            page.show_dialog(ft.AlertDialog(
                modal=True,
                title=ft.Text("Редагувати продукт"),
                content=edit_input,
                actions=[
                    ft.TextButton("Зберегти", on_click=save),
                    ft.TextButton("Скасувати", on_click=cancel),
                ],
                actions_alignment=ft.MainAxisAlignment.CENTER,
            ))

    def handle_dismiss(e: ft.Event[ft.Dismissible]):
        name = e.control.content.content.title.value
        products_remove_from_txt(name)
        save_to_history("Видалено", name)
        e.control.parent.controls.remove(e.control)
        empty_state.visible = len(list_view.controls) == 0
        e.control.parent.update()
        empty_state.update()

    def make_dismissible(text: str):
        return ft.Dismissible(
            dismiss_direction=ft.DismissDirection.HORIZONTAL,
            background=ft.Container(
                bgcolor=ft.Colors.RED,
                padding=ft.Padding.only(left=20),
                alignment=ft.Alignment.CENTER_LEFT,
                content=ft.Row(
                    controls=[
                        ft.Icon(ft.Icons.DELETE, color=ft.Colors.WHITE),
                        ft.Text("Видалити", color=ft.Colors.WHITE, weight=ft.FontWeight.W_500),
                    ],
                ),
            ),
            secondary_background=ft.Container(
                bgcolor=ft.Colors.BLUE,
                padding=ft.Padding.only(right=20),
                alignment=ft.Alignment.CENTER_RIGHT,
                content=ft.Row(
                    alignment=ft.MainAxisAlignment.END,
                    controls=[
                        ft.Icon(ft.Icons.EDIT, color=ft.Colors.WHITE),
                        ft.Text("Редагувати", color=ft.Colors.WHITE, weight=ft.FontWeight.W_500),
                    ],
                ),
            ),
            on_dismiss=handle_dismiss,
            on_confirm_dismiss=handle_confirm_dismiss,
            dismiss_thresholds={
                ft.DismissDirection.END_TO_START: 0.2,
                ft.DismissDirection.START_TO_END: 0.2,
            },
            content=ft.Container(
                margin=ft.Margin.only(bottom=8),
                border_radius=8,
                bgcolor=PANEL_BG,
                border=ft.Border.all(1, ft.Colors.BLUE_GREY_100),
                content=ft.ListTile(
                    leading=ft.Icon(ft.Icons.SHOPPING_CART_OUTLINED, color=ft.Colors.CYAN_700),
                    title=ft.Text(text, color=TEXT_DARK, weight=ft.FontWeight.W_500),
                    trailing=ft.Icon(ft.Icons.SWIPE, color=ft.Colors.BLUE_GREY_300),
                ),
            ),
        )

    list_view = ft.ListView(
        expand=True,
        controls=[make_dismissible(i) for i in list_products],
    )

    def show_history(e):
        history = load_history()

        action_colors = {
            "Видалено": ft.Colors.RED_400,
            "Відредаговано": ft.Colors.BLUE_400,
            "Додано": ft.Colors.CYAN_400,
        }

        def on_clear(ev):
            clear_history()
            page.pop_dialog()

        page.show_dialog(ft.AlertDialog(
            modal=True,
            title=ft.Text("Історія дій"),
            content=ft.Container(
                width=340,
                height=340,
                content=ft.ListView(
                    expand=True,
                    controls=[
                        ft.Container(
                            margin=ft.Margin.only(bottom=6),
                            padding=ft.Padding.symmetric(horizontal=12, vertical=8),
                            border_radius=8,
                            bgcolor=ft.Colors.with_opacity(0.15, action_colors.get(item["action"], ft.Colors.GREY)),
                            border=ft.Border.all(1, ft.Colors.with_opacity(0.4, action_colors.get(item["action"], ft.Colors.GREY))),
                            content=ft.Row(
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                controls=[
                                    ft.Column(
                                        spacing=2,
                                        controls=[
                                            ft.Text(
                                                item["action"],
                                                size=11,
                                                color=action_colors.get(item["action"], ft.Colors.GREY),
                                                weight=ft.FontWeight.BOLD,
                                            ),
                                            ft.Text(
                                                item["name"],
                                                size=13,
                                                color=TEXT_DARK,
                                                weight=ft.FontWeight.W_500,
                                            ),
                                        ],
                                    ),
                                    ft.Text(
                                        item["time"],
                                        size=11,
                                        color=ft.Colors.BLUE_GREY_400,
                                    ),
                                ],
                            ),
                        )
                        for item in reversed(history)
                    ] if history else [
                        ft.Container(
                            alignment=ft.Alignment.CENTER,
                            padding=24,
                            content=ft.Text("Історія порожня", color=ft.Colors.BLUE_GREY_400),
                        )
                    ],
                ),
            ),
            actions=[
                ft.TextButton("Очистити", on_click=on_clear),
                ft.TextButton("Закрити", on_click=lambda e: page.pop_dialog()),
            ],
            actions_alignment=ft.MainAxisAlignment.CENTER,
        ))

    empty_state = ft.Container(
        visible=len(list_products) == 0,
        expand=True,
        alignment=ft.Alignment.CENTER,
        padding=24,
        content=ft.Column(
            spacing=12,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ftl.Lottie(
                    src="https://assets2.lottiefiles.com/packages/lf20_wd1udlcz.json",
                    reverse=False,
                    width=180,
                    height=130,
                    error_content=ft.Placeholder(ft.Text("Помилка завантаження")),
                    on_error=lambda e: print(f"Error loading Lottie: {e.data}"),
                ),
                ft.Text("Список покупок порожній", size=22, weight=ft.FontWeight.BOLD, color=TEXT_DARK),
                ft.Text(
                    "Додайте продукт у полі вище, і він з'явиться тут.",
                    size=14,
                    color=ft.Colors.BLUE_GREY_600,
                    text_align=ft.TextAlign.CENTER,
                ),
            ],
        ),
    )

    name_input = ft.TextField(
        label="Введіть назву продукту",
        expand=True,
        border_color=ft.Colors.BLUE_GREY_300,
    )

    def add_new_item(e):
        if name_input.value.strip():
            name = name_input.value.strip()
            list_view.controls.append(make_dismissible(name))
            products_add_to_txt(name)
            save_to_history("Додано", name)
            name_input.value = ""
            empty_state.visible = False
            list_view.update()
            name_input.update()
            empty_state.update()

    content = ft.Container(
        expand=True,
        bgcolor=APP_BG,
        padding=24,
        content=ft.Column(
            expand=True,
            spacing=18,
            controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Text("Список покупок", size=28, weight=ft.FontWeight.BOLD, color=TEXT_DARK),
                        ft.IconButton(
                            icon=ft.Icons.HISTORY,
                            icon_color=ft.Colors.CYAN_700,
                            tooltip="Історія дій",
                            on_click=show_history,
                        ),
                    ],
                ),
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
                        spacing=20,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ftl.Lottie(
                                src="https://assets2.lottiefiles.com/packages/lf20_wd1udlcz.json",
                                reverse=False,
                                error_content=ft.Placeholder(ft.Text("Помилка завантаження")),
                                on_error=lambda e: print(f"Error loading Lottie: {e.data}"),
                            ),
                            ft.Text("Список покупок", size=24, weight=ft.FontWeight.BOLD, color=TEXT_DARK),
                        ],
                    ),
                ),
                ft.Container(
                    expand=True,
                    bgcolor=PANEL_BG,
                    border_radius=8,
                    border=ft.Border.all(1, ft.Colors.BLUE_GREY_100),
                    padding=10,
                    content=ft.Stack(
                        expand=True,
                        controls=[
                            list_view,
                            empty_state,
                        ],
                    ),
                ),
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