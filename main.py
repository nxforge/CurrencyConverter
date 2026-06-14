import flet as ft
import money
import json
import os


def main(page: ft.Page):
    file = f"{os.path.expanduser("~")}/money.json"

    firstMoney = ""
    history = []
    lastMoney = ""
    columnHistory = None


    # Json Format

    def load_history():
        nonlocal history
        if os.path.exists(file):
            try:
                with open(file, "r", encoding="utf-8") as f:
                    history = json.load(f)
            except Exception as e:
                print("Error load JSON:", e)
                history = []

    def save_history():
        try:
            with open(file, "w", encoding="utf-8") as f:
                json.dump(history, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print("Error save JSON:", e)


    # Mini Functions

    def get_options(options):
        widget = []

        for option in options:
            widget.append(
                ft.DropdownOption(
                    key=option,
                    content=ft.Text(
                        value=option,
                    ),
                )
            )
        return widget
    

    def money_update(*args):
        try:
            lastMoneyObj.value = str(money.Money().money_input(firstMoney))
            page.update()
        except:
            pass


    def history_update(*args):
        widget = []

        if len(history) > 0:

            for i, text in enumerate(history):
                widget.append(
                    ft.Row(
                        controls=[
                            ft.Text(text, size=18),
                            
                            ft.IconButton(
                                icon=ft.Icons.DELETE_OUTLINE,
                                tooltip="Delete",
                                data=i,
                                on_click=delete_from_history,
                                icon_color=ft.Colors.GREEN_900
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                    )
                )

        else:
            widget.append(ft.Text("No Favorites!", size=18))
        
        columnHistory.controls = widget

        page.update()
        save_history()
    

    # Events

    def delete_from_history(e: ft.ControlEvent):
        idx = e.control.data
        if 0 <= idx < len(history):
            history.pop(idx)
            history_update()

    def add_to_history(e: ft.ControlEvent):
        item = f"{firstMoney} RUB = {lastMoneyObj.value} EURO"
        history.insert(0, item)
        history_update()

    def on_change_firstMoneyInput(e: ft.ControlEvent):
        nonlocal firstMoney

        e.control.value = e.control.value.replace(',', '.').replace(' ', '')
        try:
            firstMoney = float(e.control.value)
        except:
            if e.control.value != "":
                e.control.value = firstMoney
        print("First:", firstMoney)
        money_update()

    def on_change_pickDate(e: ft.ControlEvent):
        money.Money().date_input(e.control.value.strftime('%Y-%m-%d'))
        print("First:", e.control.value.strftime('%Y-%m-%d'))
        money_update()
    
    def on_focus(e: ft.ControlEvent):
        e.control.label_style = ft.TextStyle(color=ft.Colors.GREEN_900)
        e.control.update()

    def on_blur(e: ft.ControlEvent):
        e.control.label_style = ft.TextStyle(color=ft.Colors.GREY_700)
        e.control.update()
    

    # Big Objects

    def money_card(app):
        cardUnit = ft.Card()

        rowUnit = ft.Row(controls=[
            ft.TextField(label="First Currency", on_change=on_change_firstMoneyInput, focused_border_color=ft.Colors.GREEN_900, cursor_color=ft.Colors.GREEN_900, selection_color=ft.Colors.GREEN_100, on_focus=on_focus, on_blur=on_blur, width=180,),

            ft.Text("RUB to", size=18),

            lastMoneyObj,

            ft.Text("EURO", size=18),

            ft.VerticalDivider(
                thickness=1.8,
            ),

            ft.FloatingActionButton(
                icon=ft.Icons.CALENDAR_MONTH_OUTLINED,
                tooltip="Pick Date",
                on_click=lambda e: page.open(
                    ft.DatePicker(
                        on_change=on_change_pickDate
                    )
                ),
                bgcolor=ft.Colors.GREEN_300
            ),

            ft.FloatingActionButton(
                icon=ft.Icons.ADD,
                tooltip="To Favorite",
                on_click=add_to_history,
                bgcolor=ft.Colors.GREEN_300
            )
        ], height=60, expand=True, tight=True)

        cardUnit.content = ft.Container(
            content=rowUnit, 
            padding=20,
            alignment=ft.alignment.center,
        )

        centered_card = ft.Row(
            controls=[cardUnit],
            alignment=ft.MainAxisAlignment.CENTER,
        )

        app.controls.append(centered_card)


    def history_card(app):
        nonlocal columnHistory
        cardHistory = ft.Card(expand=True,)

        columnHistory = ft.Column(controls=[], expand=True)

        cardHistory.content = ft.Container(
            content=columnHistory, 
            padding=20,
            alignment=ft.alignment.center,
        )

        app.controls.append(cardHistory)


    lastMoneyObj = ft.TextField(label="Last Currency", on_change=money_update, focused_border_color=ft.Colors.GREEN_900, cursor_color=ft.Colors.GREEN_900, selection_color=ft.Colors.GREEN_100, on_focus=on_focus, on_blur=on_blur, width=180,)

    page.title = "Currency Converter"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.scroll = ft.ScrollMode.AUTO

    app = ft.Column()
    page.controls.append(app)

    money_card(app)

    history_card(app)
    load_history()
    history_update()

    page.update()

ft.app(main)
