MAX_MESSAGES = 40
KEEP_MESSAGES = 20

def trim_history(messages):
    if len(messages) > MAX_MESSAGES:
        messages = messages[-KEEP_MESSAGES:]
        # история должна начинаться с реплики user
        while messages and messages[0]["role"] != "user":
            messages = messages[1:]
    return messages