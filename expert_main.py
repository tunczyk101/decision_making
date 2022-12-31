import kivy.uix.screenmanager
from kivymd.app import MDApp
from kivy.core.window import Window
from expert.expert_functions import load_questions, save_expert
from back.functions import without_whitespace, get_image
import certifi
import os

os.environ['SSL_CERT_FILE'] = certifi.where()


Window.size = (375, 750)


class SaveScreen(kivy.uix.screenmanager.Screen):
    pass


class AddExpertiseScreen(kivy.uix.screenmanager.Screen):
    left = 1
    right = 1
    AHP = load_questions()

    def reset_values(self):
        if self.AHP.check_next_expert_question():
            # self.ids.question_label.text = "Time to save questions"
            self.ids.next_button.disabled = True
            self.ids.next_button.opacity = 0
            self.ids.save_button.opacity = 1
            self.ids.save_button.disabled = False

        self.ids.question_label.text = "Category:\n" + self.AHP.get_category()
        self.ids.left_label.text = self.AHP.get_left()
        self.ids.left_photo.source = get_image(self.AHP.get_left())
        self.ids.right_label.text = self.AHP.get_right()
        self.ids.right_photo.source = get_image(self.AHP.get_right())
        self.left = self.right = 1
        s = str(self.left) + " : " + str(self.right)
        self.ids.slider.value = 0
        self.ids.compare_label.text = s

    def get_new_left_right_values(self, value):
        self.left = max(1, value + 1)
        self.right = - min(-1, value - 1)
        s = str(self.left) + " : " + str(self.right)
        self.ids.compare_label.text = s

    def next(self):
        self.AHP.save_expert_value((self.left / self.right))

        self.reset_values()

    def save(self, expert_name, label, function):
        if without_whitespace(expert_name):
            self.AHP.fill_expert_diagonals()
            save_expert(self.AHP, expert_name)
            function("home_screen")
            self.AHP.generate_expert_questions()
            self.ids.next_button.disabled = False
            self.ids.next_button.opacity = 1
            self.ids.save_button.opacity = 0
            self.ids.save_button.disabled = True
        else:
            label.text = "Get rid of whitespaces"


class HomeScreen(kivy.uix.screenmanager.Screen):
    pass


class ExpertApp(MDApp):

    def on_start(self):
        # https://kivymd.readthedocs.io/en/latest/themes/theming/
        self.theme_cls.primary_palette = 'Purple'
        self.theme_cls.primary_hue = "500"
        self.theme_cls.theme_style = "Dark"

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


ExpertApp().run()
