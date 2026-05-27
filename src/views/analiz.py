import flet as ft
import flet_charts as fch
import plotly.graph_objects as go
from src.models.load_product import load_products
from src.views.menu import APP_BG, PANEL_BG, TEXT_DARK, navigation_menu


async def analytics(page):
    loading_view = ft.View(
        route="/analytics",
        controls=[
            ft.Row(
                expand=True,
                spacing=0,
                controls=[
                    navigation_menu(page, "/analytics"),
                    ft.Container(
                        expand=True,
                        bgcolor=APP_BG,
                        alignment=ft.Alignment.CENTER,
                        content=ft.Column(
                            spacing=14,
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            controls=[
                                ft.ProgressRing(width=54, height=54, stroke_width=6, color=ft.Colors.CYAN_700),
                                ft.Text("Готуємо аналітику...", size=18, weight=ft.FontWeight.BOLD, color=TEXT_DARK),
                                ft.Text("Завантажуємо товари та формуємо графік.", size=13, color=ft.Colors.BLUE_GREY_600),
                            ],
                        ),
                    ),
                ],
            )
        ],
    )
    page.views.append(loading_view)
    page.update()

    products = await load_products()

    if loading_view in page.views:
        page.views.remove(loading_view)

    if not products:
        content = ft.Container(
            expand=True,
            bgcolor=APP_BG,
            padding=24,
            content=ft.Column(
                [
                    ft.Icon(ft.Icons.BAR_CHART_OUTLINED, size=56, color=ft.Colors.CYAN_700),
                    ft.Text("Поки немає даних для аналізу", size=22, weight=ft.FontWeight.BOLD, color=TEXT_DARK),
                    ft.Text(
                        "Додайте товари в таблиці, і тут з'явиться короткий аналіз витрат.",
                        size=14,
                        color=ft.Colors.BLUE_GREY_600,
                        text_align=ft.TextAlign.CENTER,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                expand=True,
            ),
        )
        return ft.View(
            route="/analytics",
            controls=[
                ft.Row(
                    expand=True,
                    spacing=0,
                    controls=[
                        navigation_menu(page, "/analytics"),
                        content,
                    ],
                )
            ],
        )

    names = [p["name"] for p in products]
    costs = [p["quantity"] * p["price"] for p in products]

    fig = go.Figure(data=[go.Bar(x=names, y=costs, marker_color="#1D9BF0")])
    fig.update_layout(
        title="Аналіз витрат по продуктах",
        xaxis_title="Продукти",
        yaxis_title="Витрати (грн)",
        height=330,
        margin=dict(l=36, r=20, t=54, b=48),
        showlegend=False,
        template="plotly_white",
    )
    chart = fch.PlotlyChart(figure=fig, expand=True)

    total = sum(costs)
    avg = total / len(costs)

    stats = ft.Row(
        wrap=True,
        spacing=10,
        controls=[
            ft.Container(width=220, padding=12, border_radius=8, bgcolor="#102331", content=ft.Text(f"Загальні витрати: {total:.2f} грн", size=14, color=ft.Colors.WHITE)),
            ft.Container(width=220, padding=12, border_radius=8, bgcolor="#18364A", content=ft.Text(f"Середні витрати: {avg:.2f} грн", size=14, color=ft.Colors.WHITE)),
            ft.Container(width=220, padding=12, border_radius=8, bgcolor="#1D4D63", content=ft.Text(f"Максимальні витрати: {max(costs):.2f} грн", size=14, color=ft.Colors.WHITE)),
            ft.Container(width=220, padding=12, border_radius=8, bgcolor="#245D72", content=ft.Text(f"Мінімальні витрати: {min(costs):.2f} грн", size=14, color=ft.Colors.WHITE)),
        ],
    )

    content = ft.Container(
        expand=True,
        bgcolor=APP_BG,
        padding=20,
        content=ft.Column(
            expand=True,
            spacing=14,
            controls=[
                ft.Text("Analytics", size=24, weight=ft.FontWeight.BOLD, color=TEXT_DARK),
                ft.Container(
                    height=380,
                    padding=14,
                    bgcolor=PANEL_BG,
                    border_radius=8,
                    border=ft.Border.all(1, ft.Colors.BLUE_GREY_100),
                    content=chart,
                ),
                stats,
            ],
        ),
    )

    return ft.View(
        route="/analytics",
        scroll=ft.ScrollMode.AUTO,
        padding=0,
        controls=[
            ft.Row(
                expand=True,
                spacing=0,
                controls=[
                    navigation_menu(page, "/analytics"),
                    content,
                ],
            )
        ],
    )
