import datetime

import flet as ft

from src.models.load_product import load_products
from src.views.menu import MENU_ACTIVE, navigation_menu


async def home(page):
    products = await load_products()

    async def go_products(e):
        await page.push_route("/table_of_products")

    async def go_buy_products(e):
        await page.push_route("/buy_products")

    async def go_analytics(e):
        await page.push_route("/analytics")

    def nav_click(route):
        async def handler(e):
            await page.push_route(route)

        return handler

    async def handle_drawer_change(e):
        routes = {
            0: "/table_of_products",
            1: "/buy_products",
            2: "/analytics",
            3: "/",
        }
        route = routes.get(e.control.selected_index)
        if route:
            await page.push_route(route)

    def product_end_dates():
        dates = []
        for product in products:
            try:
                dates.append(datetime.datetime.strptime(product["end_date"], "%d.%m.%Y"))
            except (KeyError, TypeError, ValueError):
                continue
        return dates

    def build_notifications():
        today = datetime.datetime.now().date()
        dates = product_end_dates()
        expired_count = sum(1 for end_date in dates if end_date.date() < today)
        soon_count = sum(1 for end_date in dates if 0 <= (end_date.date() - today).days <= 3)

        return ft.Row(
            spacing=16,
            wrap=True,
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                ft.Container(
                    padding=ft.Padding.symmetric(horizontal=16, vertical=10),
                    border_radius=8,
                    bgcolor=ft.Colors.with_opacity(0.16, ft.Colors.RED),
                    border=ft.Border.all(1, ft.Colors.with_opacity(0.42, ft.Colors.RED)),
                    content=ft.Row(
                        spacing=8,
                        tight=True,
                        controls=[
                            ft.Icon(ft.Icons.WARNING_AMBER_ROUNDED, color=ft.Colors.RED, size=18),
                            ft.Text(f"{expired_count} вже вийшли із вжитку", color=ft.Colors.RED, size=13,
                                    weight=ft.FontWeight.W_500),
                        ],
                    ),
                ),
                ft.Container(
                    padding=ft.Padding.symmetric(horizontal=16, vertical=10),
                    border_radius=8,
                    bgcolor=ft.Colors.with_opacity(0.16, ft.Colors.ORANGE),
                    border=ft.Border.all(1, ft.Colors.with_opacity(0.42, ft.Colors.ORANGE)),
                    content=ft.Row(
                        spacing=8,
                        tight=True,
                        controls=[
                            ft.Icon(ft.Icons.ACCESS_TIME, color=ft.Colors.ORANGE, size=18),
                            ft.Text(f"{soon_count} скоро вийдуть із вжитку", color=ft.Colors.ORANGE, size=13,
                                    weight=ft.FontWeight.W_500),
                        ],
                    ),
                ),
            ],
        )

    nav_items = [
        (ft.Icons.INVENTORY, "Products", "/table_of_products"),
        (ft.Icons.SHOPPING_BAG_OUTLINED, "Purchases", "/buy_products"),
        (ft.Icons.BAR_CHART_OUTLINED, "Analytics", "/analytics"),
        (ft.Icons.HOME_OUTLINED, "Home", "/"),
    ]

    rail = ft.Container(
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
                        ft.Column(
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            controls=[
                                ft.IconButton(
                                    icon=icon,
                                    tooltip=label,
                                    icon_color=ft.Colors.CYAN if route == "/table_of_products" else ft.Colors.WHITE,
                                    on_click=nav_click(route),
                                )
                            ],
                        )
                        for icon, label, route in nav_items
                    ],
                ),
            ],
        ),
    )

    drawer = ft.NavigationDrawer(
        controls=[
            ft.NavigationDrawerDestination(icon=ft.Icons.INVENTORY_2, label="Products"),
            ft.NavigationDrawerDestination(icon=ft.Icons.SHOPPING_BAG_OUTLINED, label="Purchases"),
            ft.NavigationDrawerDestination(icon=ft.Icons.BAR_CHART_OUTLINED, label="Analytics"),
            ft.NavigationDrawerDestination(icon=ft.Icons.HOME_OUTLINED, label="Home"),
        ],
        on_change=handle_drawer_change,
    )

    features = [
        (ft.Icons.LIST_ALT, "Таблиця продуктів", "Додавай, редагуй, шукай та видаляй продукти"),
        (ft.Icons.TIMER_OUTLINED, "Терміни придатності", "Відстежуй дати та отримуй швидкі попередження"),
        (ft.Icons.SHOPPING_CART_OUTLINED, "Список покупок", "Створюй список покупок із збережених продуктів"),
        (ft.Icons.ANALYTICS_OUTLINED, "Аналітика витрат", "Переглядай підсумки та витрати на продукти"),
    ]

    feature_cards = ft.Row(
        spacing=16,
        wrap=True,
        controls=[
            ft.Container(
                width=190,
                padding=ft.Padding.all(20),
                border_radius=8,
                bgcolor=ft.Colors.with_opacity(0.12, ft.Colors.WHITE),
                border=ft.Border.all(1, ft.Colors.with_opacity(0.22, ft.Colors.WHITE)),
                content=ft.Column(
                    spacing=10,
                    controls=[
                        ft.Icon(icon, color=ft.Colors.CYAN, size=28),
                        ft.Text(title, color=ft.Colors.WHITE, size=14, weight=ft.FontWeight.BOLD),
                        ft.Text(desc, color=ft.Colors.with_opacity(0.76, ft.Colors.WHITE), size=12),
                    ],
                ),
            )
            for icon, title, desc in features
        ],
    )

    hero_content = ft.Container(
        expand=True,
        clip_behavior=ft.ClipBehavior.HARD_EDGE,
        content=ft.Stack(
        width=float("inf"),
            expand=True,
            controls=[
                ft.Image(src="main_photo.jpg", fit=ft.BoxFit.COVER, expand=True,width=float("inf")),
                ft.Container(bgcolor="#B0102331", expand=True),
                ft.Container(
                    padding=ft.Padding.symmetric(horizontal=58, vertical=42),
                    alignment=ft.Alignment.CENTER,
                    content=ft.Column(
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        expand=True,
                        spacing=28,
                        controls=[
                            ft.Container(
                                alignment=ft.Alignment.CENTER,
                                content=ft.Column(
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                    spacing=16,
                                    controls=[
                                        ft.Text(
                                            "Керуй домашнім\nінвентарем розумно",
                                            size=48,
                                            weight=ft.FontWeight.BOLD,
                                            color=ft.Colors.WHITE,
                                            text_align=ft.TextAlign.CENTER,
                                        ),
                                        ft.Text(
                                           "Відстежуй кількість, терміни придатності та споживання товарів",
                                            size=15,
                                            color= ft.Colors.WHITE,
                                            text_align=ft.TextAlign.CENTER,
                                        ),
                                        build_notifications(),
                                        ft.Button(
                                            content=ft.Row(
                                                controls=[
                                                    ft.Icon(ft.Icons.ROCKET_LAUNCH, color=ft.Colors.BLACK),
                                                    ft.Text("Почати роботу", size=16, weight=ft.FontWeight.BOLD,
                                                            color=ft.Colors.BLACK),
                                                ],
                                                tight=True,
                                                alignment=ft.MainAxisAlignment.CENTER,
                                            ),
                                            style=ft.ButtonStyle(
                                                bgcolor=MENU_ACTIVE,
                                                padding=ft.Padding.symmetric(horizontal=40, vertical=18),
                                                shape=ft.RoundedRectangleBorder(radius=8),
                                            ),
                                            on_click=go_products,
                                        ),
                                        ft.Row(
                                            spacing=12,
                                            wrap=True,
                                            alignment=ft.MainAxisAlignment.CENTER,
                                            controls=[
                                                ft.Button(
                                                    "Покупки",
                                                    icon=ft.Icons.SHOPPING_BAG_OUTLINED,
                                                    style=ft.ButtonStyle(color=ft.Colors.WHITE),
                                                    on_click=go_buy_products,
                                                ),
                                                ft.Button(
                                                    "Аналітика",
                                                    icon=ft.Icons.INSIGHTS,
                                                    style=ft.ButtonStyle(color=ft.Colors.WHITE),
                                                    on_click=go_analytics,
                                                ),
                                            ],
                                        ),
                                        ft.Container(
                                            width=720,
                                            alignment=ft.Alignment.CENTER,
                                            content=ft.Text(
                                                "Швидкий доступ до таблиці товарів, покупок і аналізу витрат з одного місця.",
                                                size=13,
                                                color=ft.Colors.with_opacity(0.78, ft.Colors.WHITE),
                                                text_align=ft.TextAlign.CENTER,
                                            ),
                                        ),
                                    ],
                                )
                            ),
                            feature_cards,
                        ],
                    ),
                ),
            ],
        ),
    )

    return ft.View(
        route="/",
        padding=0,
        drawer=drawer,
        controls=[
            ft.Row(
                expand=True,
                controls=[
                    navigation_menu(page, "/"),
                    hero_content,
                ],
            ),
        ],
    )
