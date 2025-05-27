def get_next_prompt(history, riddle=False, insight=False):
    step = len([msg for msg in history if msg['role'] == 'assistant'])
    last_user_input = history[-1]['content'] if history else ""

    if step == 0:
        return "What’s something you want to talk about today?"
    elif step == 1:
        return "What’s motivating you to pursue that goal?"
    elif step == 2:
        return "What joy does the other option bring?"
    elif step == 3:
        return "What do you usually do when this comes up?"
    elif step == 4:
        return "What do you feel you should do instead, and why?"
    elif step == 5 and insight:
        return "Could it be that you're torn between two values that matter deeply to you?"
    elif step == 6 and riddle:
        return "Here’s a riddle: What holds you back but is made by your own thoughts?"
    else:
        return "Thanks for sharing all of that. Does anything feel clearer now, or is something still unclear?"
