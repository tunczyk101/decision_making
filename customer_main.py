import kivy.uix.screenmanager
from kivy.properties import StringProperty
from kivymd.app import MDApp
from kivymd.uix.list import IRightBodyTouch, OneLineAvatarIconListItem
from kivymd.uix.selectioncontrol import MDCheckbox
from kivy.core.window import Window
from kivymd.uix.list import OneLineAvatarIconListItem

from customer.customer_functions import load

Window.size = (375, 750)


class ListItemWithCheckbox(OneLineAvatarIconListItem):
    icon = StringProperty("android")


class RightCheckbox(IRightBodyTouch, MDCheckbox):
    name = None

    def set_things(self, id):
        self.name = id


class StartScreen(kivy.uix.screenmanager.Screen):
    pass


class ResultScreen(kivy.uix.screenmanager.Screen):
    pass


class RankCategoriesScreen(kivy.uix.screenmanager.Screen):
    pass


class ChooseCategoriesScreen(kivy.uix.screenmanager.Screen):
    ahp = None

    def add_items_to_list(self, ahp, func):
        self.ahp = ahp

        for i in range(len(ahp.criteria)):
            item = ListItemWithCheckbox(text=f"{ahp.criteria[i]}", icon="ice-cream", id=str(i))
            item.ids.checkbox.set_things(i)
            self.ids.scroll.add_widget(item)


class CustomerApp(MDApp):
    ahp = None

    def on_start(self):
        self.theme_cls.primary_palette = 'Pink'
        self.theme_cls.primary_hue = "500"
        self.theme_cls.theme_style = "Dark"
        self.ahp = load()
        self.root.ids.choosecategories_screen.add_items_to_list(self.ahp, self.check)

    def change_screen(self, screen_name, direction='down', mode="push"):
        screen_manager = self.root.ids.screen_manager

        if direction == "None":
            screen_manager.transition = kivy.uix.screenmanager.NoTransition()
            screen_manager.current = screen_name
        else:
            screen_manager.transition = kivy.uix.screenmanager.CardTransition(direction=direction, mode=mode)
            screen_manager.current = screen_name

        if screen_name == "add_expertise_screen":
            self.root.ids.add_expertise_screen.reset_values()

    def check(self, id, value):
        if value:
            self.ahp.actual_criteria.append(id)
        else:
            self.ahp.actual_criteria.remove(id)

    def save_categories(self):
        if len(self.ahp.actual_criteria) < 1:
            self.root.ids.choosecategories_screen.ids.red_label.text = "You have to select something"
            return
        if len(self.ahp.actual_criteria) == 1:
            self.change_screen("result_screen")
        else:
            self.ask_questions()

    def ask_questions(self):
        self.change_screen("rankcategories_screen")



CustomerApp().run()
