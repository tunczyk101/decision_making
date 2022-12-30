import kivy.uix.screenmanager
from kivy.properties import StringProperty
from kivymd.app import MDApp
from kivymd.uix.list import IRightBodyTouch, OneLineAvatarIconListItem
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.icon_definitions import md_icons
from kivy.core.window import Window
from kivymd.uix.list import OneLineAvatarIconListItem

from customer.customer_functions import load

Window.size = (375, 750)


class ListItemWithCheckbox(OneLineAvatarIconListItem):
    icon = StringProperty("android")


class RightCheckbox(IRightBodyTouch, MDCheckbox):
    pass


class StartScreen(kivy.uix.screenmanager.Screen):
    pass


class ChooseCategoriesScreen(kivy.uix.screenmanager.Screen):
    ahp = None

    def add_items_to_list(self, ahp):
        self.ahp = ahp

        for i in range(len(ahp.criteria)):
            self.ids.scroll.add_widget(ListItemWithCheckbox(text=f"{ahp.criteria[i]}", icon="ice-cream"))


class CustomerApp(MDApp):
    ahp = None

    def on_start(self):
        self.theme_cls.primary_palette = 'Pink'
        self.theme_cls.primary_hue = "500"
        self.theme_cls.theme_style = "Dark"
        self.ahp = load()
        self.root.ids.choosecategories_screen.add_items_to_list(self.ahp)

    def change_screen(self, screen_name, direction='down', mode="push"):
        # Get the screen manager from the kv_expert file.
        screen_manager = self.root.ids.screen_manager

        if direction == "None":
            screen_manager.transition = kivy.uix.screenmanager.NoTransition()
            screen_manager.current = screen_name
        else:
            screen_manager.transition = kivy.uix.screenmanager.CardTransition(direction=direction, mode=mode)
            screen_manager.current = screen_name

        if screen_name == "add_expertise_screen":
            self.root.ids.add_expertise_screen.reset_values()


CustomerApp().run()
