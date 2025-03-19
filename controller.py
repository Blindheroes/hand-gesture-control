import pyautogui


class MouseController:
    def __init__(self):
        self.dragging = False
        self.click_threshold = 0.2  # 20ms

    def execute_action(self, gesture, x=None, y=None):
        if gesture == 'move' and x and y:
            self.move_cursor(x, y)
        elif gesture == 'left_click':
            pyautogui.click()
        elif gesture == 'right_click':
            pyautogui.rightClick()
        elif gesture == 'drag':
            if not self.dragging:
                pyautogui.mouseDown()
                self.dragging = True
            else:
                pyautogui.mouseUp()
                self.dragging = False
        elif gesture == 'scroll_up':
            pyautogui.scroll(10)
        elif gesture == 'scroll_down':
            pyautogui.scroll(-10)

    def move_cursor(self, x, y):
        pyautogui.moveTo(x, y, duration=0.1)

# click
# drag
# move
# scroll up
# croll down
#
