from allure import step

from components.elements import Elements
from constants.application import VISIBLE, COMBO_BOX, EDIT, EDIT_FORM, OK, BUTTON


class EditPage(Elements):
    def __init__(self, app):
        self.app = app

    @step('Авторизация пользователя')
    def user_login(self, user):
        self.app.wait(VISIBLE)
        self.app.window(class_name=COMBO_BOX).click_input()
        self.app.window(class_name=COMBO_BOX).select(user)
        self.app.window(class_name=COMBO_BOX).click()
        self.app.child_window(class_name=EDIT).wrapper_object()

    @step('Редактирование формы')
    def edit_form(self, text):
        form = self.app.child_window(title=EDIT_FORM, class_name=EDIT).wrapper_object()
        form.type_keys(text)

    @step('Клик по кнопке')
    def click_btn(self):
        self.app.child_window(title=OK, class_name=BUTTON).click()
