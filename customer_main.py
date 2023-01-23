import kivy.uix.screenmanager
import numpy as np
from kivy.properties import StringProperty
from kivymd.app import MDApp
from kivymd.uix.list import (
    IRightBodyTouch,
    OneLineAvatarIconListItem,
    OneLineIconListItem,
)
from kivymd.uix.selectioncontrol import MDCheckbox
from kivy.core.window import Window
from kivymd.uix.list import OneLineAvatarIconListItem

from customer.customer_functions import load, ranking
import back.ahp as ahp

Window.size = (375, 750)


class CriteriaQuestionsState:
    def __init__(self, criteria: list[str], actual_criteria: list[int]):
        self.criteria = criteria
        self.curr_nr = -1
        self.questions = ahp.generate_customer_questions(actual_criteria)
        self.criteria_matrix = np.ones((len(actual_criteria), len(actual_criteria)))

    def get_left_cat(self):
        return self.criteria[self.questions[self.curr_nr][0][0]]

    def get_right_cat(self):
        return self.criteria[self.questions[self.curr_nr][1][0]]

    def save_value(self, c):
        if self.curr_nr == -1:
            return
        c = float(c)
        q = self.questions[self.curr_nr]
        self.criteria_matrix[q[0][1], q[1][1]] = c
        self.criteria_matrix[q[1][1], q[0][1]] = 1 / c

    def check_next_question(self):
        self.curr_nr += 1
        if self.curr_nr + 1 >= len(self.questions):
            return True
        return False


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
        self.right = -min(-1, value - 1)
        s = str(self.left) + " : " + str(self.right)
        self.ids.compare_label.text = s

    def switch_next_save_buttons(self):
        value = self.ids.next_button.disabled
        opacity = self.ids.next_button.opacity
        self.ids.next_button.disabled = not value
        self.ids.next_button.opacity = abs(1 - self.ids.next_button.opacity)
        self.ids.save_button.opacity = opacity
        self.ids.save_button.disabled = value

    def reset_values(self, cqs: CriteriaQuestionsState):
        self.ids.question_label.text = "Compare categories:\n"
        self.ids.left_label.text = cqs.get_left_cat()
        self.ids.right_label.text = cqs.get_right_cat()
        self.left = self.right = 1
        s = str(self.left) + " : " + str(self.right)
        self.ids.slider.value = 0
        self.ids.compare_label.text = s


class ChooseCategoriesScreen(kivy.uix.screenmanager.Screen):
    def add_items_to_list(self, criteria):
        for i, crit in enumerate(criteria):
            item = ListItemWithCheckbox(text=f"{crit}", icon="ice-cream", id=str(i))
            item.ids.checkbox.set_things(i)
            self.ids.scroll.add_widget(item)


class CustomerApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cqs: CriteriaQuestionsState | None = None
        self.questions = None
        self.actual_criteria = []
        self.criteria = None
        self.propositions = None
        self.method = "EVM"

    def on_start(self):
        self.theme_cls.primary_palette = "Pink"
        self.theme_cls.primary_hue = "500"
        # self.theme_cls.theme_style = "Dark"
        self.criteria, self.propositions = load()
        self.root.ids.choosecategories_screen.add_items_to_list(self.criteria)

    def change_screen(self, screen_name, direction="down", mode="push"):
        screen_manager = self.root.ids.screen_manager

        if direction == "None":
            screen_manager.transition = kivy.uix.screenmanager.NoTransition()
            screen_manager.current = screen_name
        else:
            screen_manager.transition = kivy.uix.screenmanager.CardTransition(
                direction=direction, mode=mode
            )
            screen_manager.current = screen_name

        if screen_name == "result_screen":
            self.results()

    def results(self):
        self.root.ids.result_screen.ids.rv.data = []
        _, final_indexes = ranking(
            self.criteria,
            self.propositions,
            self.actual_criteria,
            self.cqs.criteria_matrix,
            self.method
        )
        for i in final_indexes:
            self.root.ids.result_screen.ids.rv.data.append(
                {
                    "viewclass": "CustomOneLineIconListItem",
                    "icon": "ice-cream",
                    "text": self.propositions[i],
                    "callback": lambda x: x,
                }
            )

    def check(self, id, value):
        if value:
            self.actual_criteria.append(id)
        else:
            self.actual_criteria.remove(id)

    def choose_metchod(self, id, value):
        if value:
            self.method = id
            print(id)

    def save_categories(self):
        if len(self.actual_criteria) < 1:
            self.root.ids.choosecategories_screen.ids.red_label.text = (
                "You have to select something"
            )
            return
        self.cqs = CriteriaQuestionsState(self.criteria, self.actual_criteria)
        if len(self.actual_criteria) == 1:
            self.change_screen("result_screen")
        else:
            self.change_screen("rankcategories_screen")
            self.next()

    def next(self):
        left = self.root.ids.rankcategories_screen.left
        right = self.root.ids.rankcategories_screen.right
        self.cqs.save_value((left / right))
        if self.cqs.check_next_question():
            self.root.ids.rankcategories_screen.switch_next_save_buttons()
        self.root.ids.rankcategories_screen.reset_values(self.cqs)

    def save_ranking(self):
        left = self.root.ids.rankcategories_screen.left
        right = self.root.ids.rankcategories_screen.right
        self.cqs.save_value((left / right))
        self.change_screen("result_screen", "None")


if __name__ == "__main__":
    CustomerApp().run()
