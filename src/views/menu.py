import flet as ft


APP_BG = "#EEF4F8"
PANEL_BG = "#FFFFFF"
MENU_BG = "#102331"
MENU_ACTIVE = "#1D9BF0"
MENU_TEXT = "#D7E3EC"
TEXT_DARK = "#17212B"


def navigation_menu(page, active_route="/"):
    def nav_click(route):
        async def handler(e):
            await page.push_route(route)

        return handler

    nav_items = [
        (ft.Icons.HOME_OUTLINED, "Головна", "/"),
        (ft.Icons.INVENTORY, "Таблиця продуктів", "/table_of_products"),
        (ft.Icons.SHOPPING_BAG_OUTLINED, "Список покупок", "/buy_products"),
        (ft.Icons.BAR_CHART_OUTLINED, "Аналіз продуктів", "/analytics"),
    ]

    return ft.Container(
        width=104,
        bgcolor=MENU_BG,
        padding=ft.Padding.symmetric(vertical=22, horizontal=10),
        content=ft.Column(
            expand=True,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Container(
                    width=66,
                    height=66,
                    border_radius=8,
                    bgcolor=ft.Colors.WHITE,
                    border=ft.Border.all(1, ft.Colors.with_opacity(0.35, ft.Colors.CYAN_ACCENT)),
                    alignment=ft.Alignment.CENTER,
                    content=ft.Image(src="icon.ico", height=48, width=48),
                ),
                ft.Column(
                    expand=True,
                    spacing=10,
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Container(
                            width=82,
                            height=72,
                            border_radius=8,
                            bgcolor=ft.Colors.with_opacity(0.16, MENU_ACTIVE) if route == active_route else ft.Colors.TRANSPARENT,
                            border=ft.Border.all(1, ft.Colors.with_opacity(0.35, MENU_ACTIVE)) if route == active_route else None,
                            content=ft.Column(
                                spacing=2,
                                alignment=ft.MainAxisAlignment.CENTER,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                controls=[
                                    ft.IconButton(
                                        icon=icon,
                                        tooltip=label,
                                        icon_color=ft.Colors.CYAN_ACCENT if route == active_route else MENU_TEXT,
                                        on_click=nav_click(route),
                                    ),
                                    ft.Text(
                                        label,
                                        size=10,
                                        color=ft.Colors.CYAN_ACCENT if route == active_route else MENU_TEXT,
                                        text_align=ft.TextAlign.CENTER,
                                    ),
                                ],
                            ),
                        )
                        for icon, label, route in nav_items
                    ],
                ),
                ft.Container(height=58),
            ],
        ),
    )
