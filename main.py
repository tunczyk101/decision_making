from kivy.uix.screenmanager import Screen, NoTransition, CardTransition
from back.AHP import AHP
from kivymd.app import MDApp
from kivy.core.window import Window
from expert.main import load_questions


Window.size = (375, 750)

class AddExpertiseScreen(Screen):
    left = 1
    right = 1
    AHP = load_questions()

    def reset_values(self):
        self.left = 1
        self.right = 1

    def get_new_left_right_values(self, value):
        # print(value)
        self.left = - min(-1, value - 1)
        self.right = max(1, value + 1)
        print(self.left, ":", self.right)
        s = str(self.left) + " : " + str(self.right)
        self.ids.compare_label.text = s
    def left_right(self):
        return self.left, ":", self.right


class HomeScreen(Screen):
    pass

class MainApp(MDApp):

    def on_start(self):
        # https://kivymd.readthedocs.io/en/latest/themes/theming/
        self.theme_cls.primary_palette = 'Purple'
        self.theme_cls.primary_hue = "500"
        self.theme_cls.theme_style = "Dark"

    def printsth(self):
        print("sth")

    def change_screen(self, screen_name, direction='down', mode="pop"):
        # Get the screen manager from the kv file.
        screen_manager = self.root.ids.screen_manager

        if direction == "None":
            screen_manager.transition = NoTransition()
            screen_manager.current = screen_name
            return

        screen_manager.transition = CardTransition(direction=direction, mode=mode)
        screen_manager.current = screen_name



MainApp().run()

# # criteria = ["jakosc lodow", "cena", "jakosc sorbetow"]
#
# if __name__ == "__main__":
#     ahp = AHP(criteria, propositions)
#     ahp.start()
