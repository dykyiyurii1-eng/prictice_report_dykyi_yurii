import flet as ft
import flet_lottie as ftl
from src.models.load_product import *
from src.views.menu import navigation_menu


async def buy_products(page: ft.Page):
    page.scroll = "auto"
    picker = ft.DateRangePicker()
    text_from_txt = load_buy_products()
    print(text_from_txt)

    btn1 = ft.Button(
        "Pick date range",
        icon=ft.Icons.DATE_RANGE,
        on_click=lambda _: page.show_dialog(picker),
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

    def handle_update(e: ft.DismissibleUpdateEvent):
        print(e)

    content = ft.SafeArea(
        content=ft.Column(
            controls=[
                ft.Row(
                    [
                        ftl.Lottie(
                            src="https://assets2.lottiefiles.com/packages/lf20_wd1udlcz.json",
                            reverse=False,
                            error_content=ft.Placeholder(ft.Text("Error loading Lottie")),
                            on_error=lambda e: print(f"Error loading Lottie: {e.data}"),
                        )
                    ],
                    width=200,
                    height=200,
                    expand=True,
                    vertical_alignment=ft.CrossAxisAlignment.END,
                ),
                ft.ListView(
                    expand=True,
                    controls=[
                        ft.Dismissible(
                            dismiss_direction=ft.DismissDirection.HORIZONTAL,
                            background=ft.Container(bgcolor=ft.Colors.GREEN),
                            secondary_background=ft.Container(bgcolor=ft.Colors.RED),
                            on_dismiss=handle_dismiss,
                            on_update=handle_update,
                            on_confirm_dismiss=handle_confirm_dismiss,
                            dismiss_thresholds={
                                ft.DismissDirection.END_TO_START: 0.2,
                                ft.DismissDirection.START_TO_END: 0.2,
                            },
                            content=ft.ListTile(title=ft.Text(f"Item {i}")),
                        )
                        for i in range(10)
                    ],
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
                    ft.VerticalDivider(width=0.1),
                    content,
                ],
            )
        ],
    )


async def main(page: ft.Page):
    page.views.append(await buy_products(page))
    page.update()


if __name__ == "__main__":
    ft.run(main)
