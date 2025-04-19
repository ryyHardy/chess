import flet as ft

from src.config import ASSETS_DIR


def main(page: ft.Page):
    page.window.width = page.window.height = 800
    page.window.resizable = False
    page.add(ft.Text("Hello World!", size=50))


if __name__ == "__main__":
    ft.app(target=main, assets_dir=ASSETS_DIR)
