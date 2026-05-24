# import flet as ft
# # from src.models.name import read_data,save_data
# import random
# from flet_color_pickers import ColorLabelType, ColorPicker, PaletteType
#
# def cards_people(page:ft.Page):
#     # user_data=read_data()
#     # name_first = user_data.get("name_first", "анонімус")
#
#     def change_color(e):
#
#         new_color = e.control.data
#         app1.bgcolor = new_color
#         bottom1.bgcolor = new_color
#         # save_data({
#         #     "name_first": name_first,
#         #     "color": new_color,
#         # })
#
#         page.update()
#         return new_color
#     def on_change(e):
#         color=e.data
#         container.bgcolor=color
#
#
#
#     colors = ["red", "green", "blue", "yellow", "purple"]
#     containers=ft.Column(
#
#     )
#     for color in colors:
#         containers.controls.append(
#             ft.Container(
#                 bgcolor=color,
#                 alignment=ft.Alignment.CENTER,
#                 content=ft.Text(f"{color}", color='black',),
#                 data=color,
#
#                 on_click=change_color,
#                 height=80,
#                 width=200,
#             )
#         )
#
#     picker = ColorPicker(
#         color="#ff0000",
#
#         color_history=[
#             "#ff0000",
#             "#00ff00",
#             "#0000ff",
#             "#ffff00",
#             "#00ffff",
#             "#ff00ff",
#         ], on_color_change=on_change)
#     page_add=ft.SafeArea(
#             expand=True,
#             content=ft.Container(
#                 alignment=ft.Alignment.CENTER,
#                 content=ft.Container(
#                     content=
#                             containers,
#
#                 ),
#             ),
#         )
#
#     def theme_changed(e):
#         if page.theme_mode == ft.ThemeMode.DARK:
#             page.theme_mode = ft.ThemeMode.LIGHT
#             icon.icon = ft.Icons.LIGHT_MODE
#         else:
#             page.theme_mode = ft.ThemeMode.DARK
#             icon.icon = ft.Icons.DARK_MODE
#
#     async def go_login(e):
#         await page.push_route("/")
#
#     async def go_to_choose_cards(e):
#         await page.push_route("/settings")
#
#     return ft.View(
#
#         route="/settings",
#
#         controls=[ft.Column([
#
#             app1:=ft.AppBar(title=ft.Text(f"Вітаємо, Юрій! "),
#                       actions=[
#
#
#                           ft.IconButton(ft.Icons.LOGIN, on_click=go_login),
#                           icon := ft.IconButton(icon=ft.Icons.DARK_MODE, on_click=theme_changed)
#                       ],bgcolor=random.choice(colors) ),
#
#             ft.Divider(),
#             page_add,
#
#             ft.Container(bottom1 := ft.BottomAppBar(
#                 bgcolor=random.choice(colors),
#                 content=ft.Row(
#                     alignment=ft.MainAxisAlignment.SPACE_AROUND,
#                     controls=[
#                         ft.IconButton(ft.Icons.SKIP_PREVIOUS,
#                                       icon_color='black' if icon.icon == ft.Icons.DARK_MODE else 'white',on_click=go_login),
#                         ft.IconButton(ft.Icons.SKIP_NEXT,
#                                       icon_color='black' if icon.icon == ft.Icons.DARK_MODE else 'white',
#                                       on_click=go_to_choose_cards),
#                     ],
#                 ),
#             ),
#                          bgcolor=random.choice(colors),
#                          alignment=ft.Alignment.BOTTOM_CENTER,
#                          padding=0
#
#                          )
#
#         ], expand=True,
#             alignment=ft.MainAxisAlignment.CENTER,
#             horizontal_alignment=ft.CrossAxisAlignment.CENTER,
#
#         )])
#
#
# if __name__ == '__main__':
#     ft.run(cards_people)