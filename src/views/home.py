import flet as ft
import datetime

from src.models.load_product import *
from src.models.save_data import *


def home(page):

    page.background = "assets/icon.ico"

    async def handle_drawer_change(e):
        selected = e.control.selected_index
        routes = {
            0: "/list_of_products",
            1: "/table_of_products",
            2: "/analytics",
            3: "/settings",
        }
        route = routes.get(selected)
        if route:
            await page.push_route(route)

    # async def handle_show_drawer(e):
    #     page.open(drawer)
    #
    async def go_work(e):
        await page.push_route('/table_of_products')



    def build_notifications():
        expired_count = sum(1 for p in products if p["end_date"] < datetime.datetime.now().strftime("%d.%m.%Y"))
        soon_count = sum(1 for p in products if (
                datetime.datetime.strptime(p["end_date"], "%d.%m.%Y") - datetime.datetime.now()
        ).days <= 5)


        return ft.Row(
            spacing=16,
            controls=[
                ft.Container(
                    padding=ft.Padding.symmetric(horizontal=16, vertical=10),
                    border_radius=10,
                    bgcolor=ft.Colors.with_opacity(0.2, ft.Colors.RED),
                    border=ft.Border.all(1, ft.Colors.with_opacity(0.5, ft.Colors.RED)),
                    content=ft.Row(
                        spacing=8,
                        controls=[
                            ft.Icon(ft.Icons.WARNING_AMBER_ROUNDED, color=ft.Colors.RED, size=18),
                            ft.Text(f"{expired_count} прострочених", color=ft.Colors.RED, size=13, weight=ft.FontWeight.W_500),
                        ]
                    )
                ),
                ft.Container(
                    padding=ft.Padding.symmetric(horizontal=16, vertical=10),
                    border_radius=10,
                    bgcolor=ft.Colors.with_opacity(0.2, ft.Colors.ORANGE),
                    border=ft.Border.all(1, ft.Colors.with_opacity(0.5, ft.Colors.ORANGE)),
                    content=ft.Row(
                        spacing=8,
                        controls=[
                            ft.Icon(ft.Icons.ACCESS_TIME, color=ft.Colors.ORANGE, size=18),
                            ft.Text(f"{soon_count} закінчуються", color=ft.Colors.ORANGE, size=13, weight=ft.FontWeight.W_500),
                        ]
                    )
                ),
            ]
        )

    items = [
        (ft.Icons.INVENTORY, "Інвентар", "/inventory"),
        (ft.Icons.SHOPPING_BAG_OUTLINED, "Покупки", "/table_of_products"),
        (ft.Icons.BAR_CHART_OUTLINED, "Аналітика", "/analytics"),
        (ft.Icons.SETTINGS_OUTLINED, "Налаштування", "/settings"),
    ]

    buttons = [
        ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.IconButton(
                    icon=icon,
                    icon_color=ft.Colors.CYAN if i == 0 else ft.Colors.WHITE,
                    on_click=lambda e, r=route: page.push_route(r),
                ),
                ft.Text(label, size=11, color=ft.Colors.WHITE, visible=False),
            ]
        )
        for i, (icon, label, route) in enumerate(items)
    ]

    rail = ft.Container(

        width=80,
        bgcolor=ft.Colors.with_opacity(0.15, ft.Colors.BLACK),
        padding=ft.Padding.symmetric(vertical=20),
        content=ft.Column(
            expand=True,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Image(src='assets/icon.ico', height=50, width=50),

                    ]
                ),
                ft.Column(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    expand=True,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=buttons,
                )
            ],
        )
    )

    drawer = ft.NavigationDrawer(
        controls=[
            ft.NavigationDrawerDestination(icon=ft.Icons.INVENTORY_2, label="Інвентар"),
            ft.NavigationDrawerDestination(icon=ft.Icons.SHOPPING_BAG_OUTLINED, label="Покупки"),
            ft.NavigationDrawerDestination(icon=ft.Icons.BAR_CHART_OUTLINED, label="Аналітика"),
            ft.NavigationDrawerDestination(icon=ft.Icons.SETTINGS_OUTLINED, label="Налаштування"),
        ],
        on_change=handle_drawer_change,
    )

    features = [
        (ft.Icons.LIST_ALT, "Список товарів", "Додавай, редагуй та видаляй продукти"),
        (ft.Icons.TIMER_OUTLINED, "Терміни придатності", "Відстежуй дати та отримуй сповіщення"),
        (ft.Icons.SHOPPING_CART_OUTLINED, "Списки покупок", "Автоматичне формування на основі залишків"),
        (ft.Icons.ANALYTICS_OUTLINED, "Облік витрат", "Аналізуй споживання та витрати"),
    ]

    feature_cards = ft.Row(
        spacing=16,
        controls=[
            ft.Container(
                width=180,
                padding=ft.Padding.all(20),
                border_radius=16,
                bgcolor=ft.Colors.with_opacity(0.12, ft.Colors.WHITE),
                border=ft.Border.all(1, ft.Colors.with_opacity(0.2, ft.Colors.WHITE)),
                content=ft.Column(
                    spacing=10,
                    controls=[
                        ft.Icon(icon, color=ft.Colors.CYAN, size=28),
                        ft.Text(title, color=ft.Colors.WHITE, size=14, weight=ft.FontWeight.BOLD),
                        ft.Text(desc, color=ft.Colors.with_opacity(0.7, ft.Colors.WHITE), size=12),
                    ]
                )
            )
            for icon, title, desc in features
        ]
    )

    hero_content = ft.SafeArea(
        expand=True,
        content=ft.Container(
        expand=True,
        content=ft.Stack(
            expand=True,
            controls=[
                ft.Image(
                    src="assets/main_photo.jpg",
                    expand=True,
                    fit=ft.BoxFit.COVER,
                ),

                ft.Container(
                    expand=True,
                    padding=ft.Padding.symmetric(horizontal=60, vertical=40),
                    content=ft.Column(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        expand=True,
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
                                            "Створення програмного забезпечення для керування запасами та інвентарем вдома.\nВідстежуй кількість, терміни придатності та споживання товарів.",
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
                                                bgcolor=ft.Colors.CYAN,
                                                padding=ft.Padding.symmetric(horizontal=40, vertical=18),
                                                shape=ft.RoundedRectangleBorder(radius=12),
                                            ),
                                            on_click=go_work,
                                        ),
                                    ],
                                )
                            ),
                            feature_cards,
                        ],
                    )
                ),
            ]
        )
    ))

    return ft.View(
        route="/home",
        padding=0,
        drawer=drawer,
        controls=[
            ft.Row(
                expand=True,
                spacing=0,
                controls=[
                    rail,
                    ft.VerticalDivider(width=0.1),
                    hero_content,
                ],
            ),
        ],
    )