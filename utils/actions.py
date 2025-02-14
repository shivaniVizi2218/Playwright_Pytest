def execute_step(test, element, action, description, data=None):
    def click_action():
        element.click()

    def dblclick_action():
        element.dblclick()

    def fill_action():
        element.fill(data[0])

    def navigate_action():
        element.goto(data[0])

    def type_action():
        element.type(data[0])

    def check_action():
        element.check(force=True)

    def uncheck_action():
        element.uncheck(force=True)

    def tap_action():
        element.tap()

    def hover_action():
        element.hover()

    # Dictionary as a switch-case equivalent
    actions = {
        'click': click_action,
        'dblclick': dblclick_action,
        'fill': fill_action,
        'navigate': navigate_action,
        'type': type_action,
        'check': check_action,
        'uncheck': uncheck_action,
        'tap': tap_action,
        'hover': hover_action,
    }

    # Executing the action
    test.step(description, lambda: actions.get(action, lambda: None)())
