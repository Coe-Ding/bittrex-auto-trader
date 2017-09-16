from appJar import gui


def create_gui():
    app = gui("Login Window", "400x200")

    # STYLES
    app.setBg("blue")
    app.setFont(18)

    # LABELS
    app.addLabel("title", "Welcome to appJar")
    app.setLabelBg("title", "red")

    # INPUTS
    app.addLabelEntry("Username")
    app.addLabelSecretEntry("Password")


    # FUNCTIONS
    def press(button):
        if button == "Cancel":
            app.stop()
        elif button == "Submit":
            usr = app.getEntry("Username")
            pwd = app.getEntry("Password")
            print("User:", usr, "Pass:", pwd)


    # BUTTONS
    app.addButtons(["Submit", "Cancel"], press)

    # ACTIONS
    app.setFocus("Username")

    app.go()