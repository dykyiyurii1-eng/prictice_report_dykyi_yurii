import flet as ft

from src.views import *

async def main(page: ft.Page):
    page.bgcolor = ft.Colors.TRANSPARENT
    page.window.icon='assets/icon.ico'
    page.scroll = ft.ScrollMode.AUTO
    page.image='assets/main_photo.jpg'
    page.favicon='assets/icon.ico'


    async def route_change(e=None):
        route = page.route or "/"
        page.views.clear()
        page.views.append(await home(page))

        if page.route == "/table_of_products":
            page.views.append(await table_of_products1(page))
        elif route == "/buy_products":
            page.views.append(await buy_products(page))
        elif route == "/analytics":
            await analytics(page)
        page.update()


    async def view_pop(e):
        if len(page.views) > 1:
            page.views.pop()
            top_view = page.views[-1]
            await page.push_route(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    await route_change()


if __name__ == "__main__":
    ft.run(main, view=ft.AppView.WEB_BROWSER, port=5000, assets_dir="assets")
    # ft.run(main)
