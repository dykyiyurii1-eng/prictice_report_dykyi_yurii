import flet as ft
import flet_charts as fch
import plotly.express as px
import csv
import asyncio
from src.models.save_data import *
from src.models.load_product import *

async def analytics(page):
    page.title = "Аналіз витрат"
    page.scroll = "auto"


    loading_ring = ft.ProgressRing(height=500, width=500, stroke_width=8, color=ft.Colors.BLUE,
                                   )
    loading_text = ft.Text("⏳ Завантаження даних...", size=20)
    loading_view = ft.Column(
        [loading_ring, loading_text],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        expand=True
    )
    page.add(loading_view)
    page.update()


    products = await load_products()

    if not products:
        loading_text.value = "❌ Немає продуктів для аналізу"
        loading_ring.visible=False
        return


    names = [p["name"] for p in products]
    costs = [p["quantity"] * p["price"] for p in products]

    fig = px.bar(
        x=names,
        y=costs,
        labels={"x": "Продукти", "y": "Витрати (грн)"},
        title="Аналіз витрат по продуктах",
        color=names
    )
    chart = fch.PlotlyChart(figure=fig, expand=True)

    total = sum(costs)
    avg = total / len(costs)

    stats = ft.Column([
        ft.Text(f"Загальні витрати: {total:.2f} грн"),
        ft.Text(f"Середні витрати: {avg:.2f} грн"),
        ft.Text(f"Максимальні витрати: {max(costs):.2f} грн"),
        ft.Text(f"Мінімальні витрати: {min(costs):.2f} грн"),
    ])


    page.controls.clear()


    page_add= ft.SafeArea(
        expand=True,
        content=ft.Container(ft.Column([
            chart,stats]
        )))
    return ft.View(
        route="/analytics",
        padding=0,
        controls=[
            ft.Row(
                expand=True,
                spacing=0,
                controls=[
                   page_add
                ],
            ),
        ],
    )



if __name__ == '__main__':
    analytics()
