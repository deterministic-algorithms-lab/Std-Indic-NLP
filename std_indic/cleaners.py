import re


def clean_text(text):
    text = text.lower()
    # foction de replacement
    text = re.sub(r"i'm", "i am", text)
    text = re.sub(r"she's", "she is", text)
    text = re.sub(r"can't", "can not", text)
    text = re.sub(r"[-()\"#/@;:<>{}-=~|.?,]", "", text)
    return text
