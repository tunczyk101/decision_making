import kivy.uix.screenmanager
import numpy as np
from kivymd.app import MDApp
from kivy.core.window import Window
from expert.expert_functions import load, save_expert
from back.functions import without_whitespace, get_image
import certifi
import os
import back.ahp as ahp

os.environ["SSL_CERT_FILE"] = certifi.where()

Window.size = (375, 750)


class PropositionQuestonsState:
    def __init__(self, criteria: list[str], propositions: list[str]):
        self.propositions_matrices = np.ones(
            (len(criteria), len(propositions), len(propositions)), dtype=float
        )
        self.propositions = propositions
        self.criteria = criteria
        self.questions = None
        self.curr_nr = -1
        self.generate_expert_questions()

    def check_next_question(self):
        self.curr_nr += 1
        if self.curr_nr + 1 >= len(self.questions):
            return True
        return False

    def last_question_check(self):
        if self.curr_nr + 1 >= len(self.questions):
            return True
        return False

    def get_category(self):
        return self.criteria[self.questions[self.curr_nr][0]]

    def get_left(self):
        return self.propositions[self.questions[self.curr_nr][1][0]]

    def get_right(self):
        return self.propositions[self.questions[self.curr_nr][1][1]]

    def save_expert_value(self, c):
        if self.curr_nr == -1:
            return
        c = float(c)
        q = self.questions[self.curr_nr]
        self.propositions_matrices[q[0], q[1][0], q[1][1]] = c
        if c != 0:
            c = 1 / c

        self.propositions_matrices[q[0], q[1][1], q[1][0]] = c

    def generate_expert_questions(self):
        self.questions = ahp.generate_expert_questions(
            len(self.criteria), len(self.propositions)
        )

    def get_max_satty_index(self):
        return max(
            (
                ahp.index(self.propositions_matrices[i, :, :], "EVM")
                for i in range(len(self.criteria))
            ),
            default=0,
        )


class SaveScreen(kivy.uix.screenmanager.Screen):
    pass


class AddExpertiseScreen(kivy.uix.screenmanager.Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.v_left = 1
        self.v_right = 1
        self.criteria, self.propositions = load()
        self.pqs = PropositionQuestonsState(self.criteria, self.propositions)

    def reset_values(self):
        if self.pqs.check_next_question():
            # self.ids.question_label.text = "Time to save questions"
            self.ids.next_button.disabled = True
            self.ids.next_button.opacity = 0
            self.ids.save_button.opacity = 1
            self.ids.save_button.disabled = False

        self.ids.question_label.text = "Category:\n" + self.pqs.get_category()
        self.ids.left_label.text = self.pqs.get_left()
        self.ids.left_photo.source = get_image(self.pqs.get_left())
        self.ids.right_label.text = self.pqs.get_right()
        self.ids.right_photo.source = get_image(self.pqs.get_right())
        self.ids.slider.value = 0
        self.v_left = 1
        self.v_right = 1
        self.ids.compare_label.text = "1 : 1"

    def get_new_left_right_values(self, value):
        self.v_left = max(1, value + 1)
        self.v_right = -min(-1, value - 1)
        s = str(self.v_left) + " : " + str(self.v_right)
        self.ids.compare_label.text = s

    def next(self, skip):
        if not skip:
            self.pqs.save_expert_value((self.v_left / self.v_right))
        else:
            self.pqs.save_expert_value(0)

        if not self.pqs.last_question_check():
            self.reset_values()

    def save(self, expert_name, label, function):
        if without_whitespace(expert_name):
            save_expert(
                self.criteria,
                self.propositions,
                self.pqs.propositions_matrices,
                expert_name,
            )
            function("home_screen")
            self.pqs.generate_expert_questions()
            self.ids.next_button.disabled = False
            self.ids.next_button.opacity = 1
            self.ids.save_button.opacity = 0
            self.ids.save_button.disabled = True
        else:
            label.text = "Get rid of whitespaces"

    def func(self):
        return f"SATTY index: {self.pqs.get_max_satty_index()}"


class HomeScreen(kivy.uix.screenmanager.Screen):
    pass


class ExpertApp(MDApp):
    def on_start(self):
        # https://kivymd.readthedocs.io/en/latest/themes/theming/
        self.theme_cls.primary_palette = "Purple"
        self.theme_cls.primary_hue = "500"
        self.theme_cls.theme_style = "Dark"

    def change_screen(self, screen_name, direction="down", mode="push"):
        # Get the screen manager from the kv_expert file.
        screen_manager = self.root.ids.screen_manager

        if screen_name == "save_screen":
            if not self.root.ids.add_expertise_screen.pqs.last_question_check():
                return
            self.root.ids.save_screen.ids.info_label.text = (
                self.root.ids.add_expertise_screen.func()
            )

        if direction == "None":
            screen_manager.transition = kivy.uix.screenmanager.NoTransition()
            screen_manager.current = screen_name
        else:
            screen_manager.transition = kivy.uix.screenmanager.CardTransition(
                direction=direction, mode=mode
            )
            screen_manager.current = screen_name

        if screen_name == "add_expertise_screen":
            self.root.ids.add_expertise_screen.reset_values()


if __name__ == "__main__":
    ExpertApp().run()
