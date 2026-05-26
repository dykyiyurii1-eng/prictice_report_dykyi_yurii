import flet as ft


def navigation_menu(page, active_route="/"):
    def nav_click(route):
        async def handler(e):
            await page.push_route(route)

        return handler

    nav_items = [
        (ft.Icons.HOME_OUTLINED, "Home", "/"),
        (ft.Icons.INVENTORY, "Products", "/table_of_products"),
        (ft.Icons.SHOPPING_BAG_OUTLINED, "Purchases", "/buy_products"),
        (ft.Icons.BAR_CHART_OUTLINED, "Analytics", "/analytics"),
    ]

    return ft.Container(
        width=80,
        bgcolor=ft.Colors.with_opacity(0.2, ft.Colors.BLACK),
        padding=ft.Padding.symmetric(vertical=20),
        content=ft.Column(
            expand=True,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Image(src="icon.ico", height=50, width=50),
                ft.Column(
                    expand=True,
                    alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.IconButton(
                            icon=icon,
                            tooltip=label,
                            icon_color=ft.Colors.CYAN if route == active_route else ft.Colors.WHITE,
                            on_click=nav_click(route),
                        )
                        for icon, label, route in nav_items
                    ],
                ),
            ],
        ),
    )
