GESTURES = {
    'drag': {'thumb': 0, 'index': 0, 'middle': 0, 'ring': 0, 'pinky': 0},
    # 'open_hand': {'thumb': 1, 'index': 1, 'middle': 1, 'ring': 1, 'pinky': 1},
    'move': {'thumb': 0, 'index': 1, 'middle': 0, 'ring': 0, 'pinky': 0},
    'left_click': {'thumb': 0, 'index': 1, 'middle': 1, 'ring': 0, 'pinky': 0},
    'scroll_up': {'thumb': 0, 'index': 1, 'middle': 1, 'ring': 1, 'pinky': 0},
    'scroll_down': {'thumb': 0, 'index': 1, 'middle': 1, 'ring': 1, 'pinky': 1}
}
# GESTURES = {
#     'fist': {'thumb': 0, 'index': 0, 'middle': 0, 'ring': 0, 'pinky': 0},
#     'open_hand': {'thumb': 1, 'index': 1, 'middle': 1, 'ring': 1, 'pinky': 1},
#     'pointing': {'thumb': 0, 'index': 1, 'middle': 0, 'ring': 0, 'pinky': 0},
#     'victory': {'thumb': 0, 'index': 1, 'middle': 1, 'ring': 0, 'pinky': 0},
#     'scroll_up': {'thumb': 1, 'index': 1, 'middle': 0, 'ring': 0, 'pinky': 0},
#     'scroll_down': {'thumb': 0, 'index': 1, 'middle': 1, 'ring': 1, 'pinky': 1}
# }


def identify_gesture(finger_states):
    for gesture, config in GESTURES.items():
        if all(finger_states[finger] == config[finger] for finger in config):
            return gesture
    return 'none'
