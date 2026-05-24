import flet as ft
import flet_charts as fch
import plotly.express as px
import csv
import asyncio
from src.models.save_data import *
from src.models.load_product import *

async def main(page: ft.Page):
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
        page.update()
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


    page.add(
        chart
    )

ft.run(main, assets_dir="src/assets")
