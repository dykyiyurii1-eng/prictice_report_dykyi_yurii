import flet as ft

from src.views import *

def main(page: ft.Page):
    # page.title = "дз"
    page.window.icon='assets/icon.ico'
    def route_change():
        page.views.clear()
        page.views.append(home(page))

        if page.route == "/table_of_products":
            page.views.append(table_of_products1(page))
        # if page.route == "/settings":
        #     page.views.append(cards_people(page))
        page.update()

    async def view_pop(e):
        if len(page.views) > 1:
            page.views.pop()
            top_view = page.views[-1]
            await page.push_route(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    route_change()


if __name__ == "__main__":
    # ft.run(main, view=ft.AppView.WEB_BROWSER, port=9201)
    ft.run(main)