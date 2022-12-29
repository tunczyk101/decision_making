from kivy.uix.screenmanager import Screen, NoTransition, CardTransition
from back.AHP import AHP
from kivymd.app import MDApp
from kivy.core.window import Window
from expert.main import load_questions, save_expert
from back.functions import without_whitespace


Window.size = (375, 750)

class SaveScreen(Screen):
    pass

class AddExpertiseScreen(Screen):
    left = 1
    right = 1
    AHP = load_questions()

    def reset_values(self):
        text = self.AHP.get_next_expert_question()
        if not text:
            self.ids.question_label.text = "Time to save questions"
            self.ids.next_button.disabled = True
            self.ids.next_button.opacity = 0
            self.ids.save_button.opacity = 1
            return
        self.ids.question_label.text = text
        self.left = 1
        self.right = 1
        s = str(self.left) + " : " + str(self.right)
        self.ids.compare_label.text = s

    def get_new_left_right_values(self, value):
        # print(value)
        self.left = - min(-1, value - 1)
        self.right = max(1, value + 1)
        s = str(self.left) + " : " + str(self.right)
        self.ids.compare_label.text = s
    def next(self):
        self.AHP.save_expert_value((self.left / self.right))
        self.reset_values()

    def save(self, expert_name, label, function):
        if without_whitespace(expert_name):
            print("save")
            save_expert(self.AHP, expert_name)
            function("home_screen")
        else:
            label.text = "Get rid of whitespaces"


class HomeScreen(Screen):
    pass

class MainApp(MDApp):

    def on_start(self):
        # https://kivymd.readthedocs.io/en/latest/themes/theming/
        self.theme_cls.primary_palette = 'Purple'
        self.theme_cls.primary_hue = "500"
        self.theme_cls.theme_style = "Dark"

    def change_screen(self, screen_name, direction='down', mode="pop"):
        # Get the screen manager from the kv file.
        screen_manager = self.root.ids.screen_manager

        if direction == "None":
            screen_manager.transition = NoTransition()
            screen_manager.current = screen_name
            return

        screen_manager.transition = CardTransition(direction=direction, mode=mode)
        screen_manager.current = screen_name

        if screen_name == "add_expertise_screen":
            self.root.ids.add_expertise_screen.reset_values()



MainApp().run()

# # criteria = ["jakosc lodow", "cena", "jakosc sorbetow"]
#
# if __name__ == "__main__":
#     ahp = AHP(criteria, propositions)
#     ahp.start()
