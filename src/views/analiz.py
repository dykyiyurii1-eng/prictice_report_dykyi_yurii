import flet as ft
import flet_charts as fch
import plotly.express as px
from src.models.load_product import load_products


async def analytics(page):
    loading = ft.Column(
        controls=[
            ft.ProgressRing(width=60, height=60, stroke_width=6, color=ft.Colors.CYAN),
            ft.Text("Завантаження даних...", size=16, color=ft.Colors.WHITE),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        expand=True,
    )

    products = await load_products()

    if not products:
        return ft.View(
            route="/analytics",
            controls=[
                ft.Column(
                    [ft.Text("❌ Немає продуктів для аналізу", size=20, color=ft.Colors.WHITE)],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    expand=True,
                )
            ],
        )

    names = [p["name"] for p in products]
    costs = [p["quantity"] * p["price"] for p in products]

    fig = px.bar(
        x=names,
        y=costs,
        labels={"x": "Продукти", "y": "Витрати (грн)"},
        title="Аналіз витрат по продуктах",
        color=names,
    )
    chart = fch.PlotlyChart(figure=fig, expand=True)

    total = sum(costs)
    avg = total / len(costs)

    stats = ft.Column(
        spacing=8,
        controls=[
            ft.Text(f"Загальні витрати: {total:.2f} грн", size=16, color=ft.Colors.WHITE),
            ft.Text(f"Середні витрати: {avg:.2f} грн", size=16, color=ft.Colors.WHITE),
            ft.Text(f"Максимальні витрати: {max(costs):.2f} грн", size=16, color=ft.Colors.WHITE),
            ft.Text(f"Мінімальні витрати: {min(costs):.2f} грн", size=16, color=ft.Colors.WHITE),
        ],
    )

    loading.visible = False

    return ft.View(
        route="/analytics",
        scroll=ft.ScrollMode.AUTO,
        padding=0,
        controls=[
            ft.Column(
                expand=True,
                controls=[loading, chart, stats],
            )
        ],
    )