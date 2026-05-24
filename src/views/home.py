import flet as ft
import flet as ft
import datetime
import csv
import os
import random
import string

from src .models.load_product import *
from src .models.save_data import *
def home(page):
    async def handle_drawer_change(e):
        selected = e.control.selected_index
        routes = {
            0: "/inventory",
            1: "/table_of_products",
            2: "/analytics",
            3: "/settings",
        }
        route = routes.get(selected)
        if route:
            await page.push_route(route)

    async def handle_show_drawer(e):
        page.open(drawer)
    def build_notifications():
        expired_count = sum(1 for p in products if p["end_date"] < datetime.datetime.now().strftime("%d.%m.%Y"))
        soon_count = sum(1 for p in products if (
                datetime.datetime.strptime(p["end_date"], "%d.%m.%Y") - datetime.datetime.now()
        ).days <= 5)

        return ft.Column([
            ft.Text(f"{expired_count} товарів прострочені", color=ft.Colors.RED, weight=ft.FontWeight.BOLD),
            ft.Text(f"{soon_count} товарів мають бути доставлені протягом наступних 5 днів", color=ft.Colors.ORANGE),
        ])

    rail = ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        min_width=100,
        min_extended_width=400,
        group_alignment=-0.9,
        on_change=handle_drawer_change,
        leading=ft.Image(
            src='assets/icon.ico',
            height=50,
            width=50,
        ),
        destinations=[
            ft.NavigationRailDestination(

                icon=ft.Icons.INVENTORY, label="Інвентар",
                expand=True,

            ),
            ft.NavigationRailDestination(
                expand=True,
                icon=ft.Icons.SHOPPING_BAG_OUTLINED,
                label="Покупки"

            ),
            ft.NavigationRailDestination(
                expand=True,
                icon=ft.Icons.BAR_CHART_OUTLINED, label="Аналітика"


            ),  ft.NavigationRailDestination(

                icon=ft.Icons.SETTINGS_OUTLINED, label="Налаштування"
            )
        ],

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

    slogan = ft.Text("СТВОРЕННЯ ПРОГРАМНОГО ЗАБЕЗПЕЧЕННЯ...", size=22, weight=ft.FontWeight.BOLD, color="#00FFFF")
    description = ft.Text("Включає створення списку товарів...", size=14, color="#FFFFFF")

    start_button = ft.TextButton(
        content=ft.Text("🚀 Почати роботу", size=16, weight=ft.FontWeight.BOLD),
        width=200,
        height=50,
        on_click=handle_show_drawer,
    )

    return ft.View(
        route="/home",
        drawer=drawer,
        controls=[
            ft.Row(
                expand=True,
                controls=[
                    ft.SelectionArea(content=rail),
                    ft.VerticalDivider(width=0.1),
                    # ft.Column(
                    #     alignment=ft.MainAxisAlignment.START,
                    #     expand=True,
                    #     controls=[ft.Text("Body!")],
                    # ),
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            slogan,
            description,
            start_button,
            build_notifications(),

        ],
    )
if __name__ == '__main__':
    home()