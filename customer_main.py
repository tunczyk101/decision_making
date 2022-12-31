import kivy.uix.screenmanager
from kivy.properties import StringProperty
from kivymd.app import MDApp
from kivymd.uix.list import IRightBodyTouch, OneLineAvatarIconListItem, OneLineIconListItem
from kivymd.uix.selectioncontrol import MDCheckbox
from kivy.core.window import Window
from kivymd.uix.list import OneLineAvatarIconListItem

from customer.customer_functions import load, ranking

Window.size = (375, 750)


class CustomOneLineIconListItem(OneLineIconListItem):
    icon = StringProperty()

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
    left = right = 1

    def get_new_left_right_values(self, value):
        self.left = max(1, value + 1)
        self.right = - min(-1, value - 1)
        s = str(self.left) + " : " + str(self.right)
        self.ids.compare_label.text = s

    def switch_next_save_buttons(self):
        value = self.ids.next_button.disabled
        opacity = self.ids.next_button.opacity
        self.ids.next_button.disabled = not value
        self.ids.next_button.opacity = abs(1 - self.ids.next_button.opacity)
        self.ids.save_button.opacity = opacity
        self.ids.save_button.disabled = value

    def reset_values(self, ahp):
        self.ids.question_label.text = "Compare categories:\n"
        self.ids.left_label.text = ahp.get_left_cat()
        self.ids.right_label.text = ahp.get_right_cat()
        self.left = self.right = 1
        s = str(self.left) + " : " + str(self.right)
        self.ids.slider.value = 0
        self.ids.compare_label.text = s


class ChooseCategoriesScreen(kivy.uix.screenmanager.Screen):
    ahp = None

    def add_items_to_list(self, ahp):
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
        self.root.ids.choosecategories_screen.add_items_to_list(self.ahp)

    def change_screen(self, screen_name, direction='down', mode="push"):
        screen_manager = self.root.ids.screen_manager

        if direction == "None":
            screen_manager.transition = kivy.uix.screenmanager.NoTransition()
            screen_manager.current = screen_name
        else:
            screen_manager.transition = kivy.uix.screenmanager.CardTransition(direction=direction, mode=mode)
            screen_manager.current = screen_name

        if screen_name == "result_screen":
            self.results()

    def results(self):
        ranking(self.ahp)
        propositions = self.ahp.propositions
        self.root.ids.result_screen.ids.rv.data = []
        for i, w in self.ahp.final_ranking:
            self.root.ids.result_screen.ids.rv.data.append({
                "viewclass": "CustomOneLineIconListItem",
                "icon": "ice-cream",
                "text": propositions[i],
                "callback": lambda x: x,
            })

    def check(self, id, value):
        if value:
            self.ahp.actual_criteria.append(id)
        else:
            self.ahp.actual_criteria.remove(id)

    def save_categories(self):

        if len(self.ahp.actual_criteria) < 1:
            self.root.ids.choosecategories_screen.ids.red_label.text = "You have to select something"
            return
        self.ahp.generate_customer_questions()
        if len(self.ahp.actual_criteria) == 1:
            self.change_screen("result_screen")
        else:
            self.change_screen("rankcategories_screen")
            self.next()

    def next(self):
        left = self.root.ids.rankcategories_screen.left
        right = self.root.ids.rankcategories_screen.right
        self.ahp.save_customer_value((left / right))
        if self.ahp.check_next_customer_question():
            self.root.ids.rankcategories_screen.switch_next_save_buttons()
        self.root.ids.rankcategories_screen.reset_values(self.ahp)


CustomerApp().run()
