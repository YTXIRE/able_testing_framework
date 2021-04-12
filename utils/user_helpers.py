def user_application_auth(app, username, password):
    app.wait("visible")
    app.window(class_name="ComboBox").click_input()
    app.window(class_name="ComboBox").select("PROGNOZ_TEST")
    app.window(class_name="ComboBox").click()
    app.child_window(class_name="Edit").wrapper_object()
