import re


def url_slug(title):
    title = re.sub(r"[^\w\s-]", "", title)
    title = title.strip().replace(" ", "-")
    title = re.sub(r"-+", "-", title)
    return title.lower()
