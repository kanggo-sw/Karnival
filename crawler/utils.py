import re


def strip_text(text: str) -> str:
    text = text.replace("​", "")
    st = text.strip()
    remove_emoji = re.compile("[\U00010000-\U0010ffff]", flags=re.UNICODE)
    return remove_emoji.sub(r"", st)
