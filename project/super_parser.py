"""Parse string to remove stop words"""

from .models import StopWord


def remove_stop_words(text: str) -> str:
    """Remove stop words"""

    # remove first and last spaces and replace ' by <space> char
    first_pass = text.strip().replace("'", " ")
    # remove non alphabetic's chars
    clean = []
    for word in first_pass.split(" "):
        clean.append("".join(c for c in word
                             if (c.isalpha()
                                 or c == "-")))
    # remove isolated chars
    clean = [x for x in clean if len(x) > 1]
    # remove stop words
    no_stop_words = []
    for word in clean:
        c = StopWord.query.filter_by(word=word).first()
        if not c:
            no_stop_words.append(word)
    return " ".join(no_stop_words)


def extract_principal_verb(text: str) -> str:
    """Extract principal verb"""

    pass


def extract_searching_words(text: str) -> str:
    """Keep principal words only"""

    pass