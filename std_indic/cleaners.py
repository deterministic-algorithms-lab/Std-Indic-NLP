import re

BYTE_ORDER_MARK = "\uFEFF"
BYTE_ORDER_MARK_2 = "\uFFFE"
WORD_JOINER = "\u2060"
SOFT_HYPHEN = "\u00AD"

ZERO_WIDTH_SPACE = "\u200B"
NO_BREAK_SPACE = "\u00A0"

ZERO_WIDTH_NON_JOINER = "\u200C"
ZERO_WIDTH_JOINER = "\u200D"


def clean_text(text):
    text = text.lower()
    text = text.replace(BYTE_ORDER_MARK, "")
    text = text.replace(BYTE_ORDER_MARK_2, "")
    text = text.replace(WORD_JOINER, "")
    text = text.replace(SOFT_HYPHEN, "")

    text = text.replace(ZERO_WIDTH_SPACE, " ")  # ??
    text = text.replace(NO_BREAK_SPACE, " ")

    text = text.replace(ZERO_WIDTH_NON_JOINER, "")
    text = text.replace(ZERO_WIDTH_JOINER, "")

    text = re.sub(r"[-()\"#/@;:<>{}-=~|.?,]", "", text)
    return text


def str_to_unicode(str):
    return chr(int(str[2:], 16))


class resolve_cotractions(object):
    def __init__(self, lang):
        super().__init__()
        self.lang = lang
        self.contractions = []
        with open("./std_indic/contractions/" + lang + ".txt", "r") as f:
            for line in f.readlines():
                text = line.rstrip()
                text = re.sub(r"\s+", r" ", text)
                self.contractions.append(text.split(" ", 1))

    def resolve_contractions(self, text):
        for contraction in self.contractions:
            text = text.replace(contraction[0], contraction[1])
        return text


class resolve_chars(object):
    def __init__(self, lang):
        super().__init__()
        self.lang = lang
        self.normalizations = []
        with open("./std_indic/unicode_normalization/" + lang + ".txt", "r") as f:
            content = f.read()
            replacements = re.findall(r"\[.+\]", content)
            for elem in replacements:
                elem = elem.strip("[]")
                elems = elem.split(" , ")
                self.normalizations.append(
                    [str_to_unicode(elems[0]), str_to_unicode(elems[1])]
                )

    def normalize(self, text):
        for norm in self.normalizations:
            text = text.replace(norm[0], norm[1])
        return text


class resolve_group_chars(object):
    def __init__(self, lang):
        super().__init__()
        self.lang = lang
        self.replaces = []
        with open(
            "./std_indic/unicode_normalization/groups/" + lang + ".txt", "r"
        ) as f:
            for line in f.readlines():
                line = re.sub(r"\s+", r" ", line.rstrip())
                line = line.split("#")[0].rstrip()
                # print(line)
                original, replacement = line.split(" ")
                match_str = self.make_pattern(original)
                repl_str = self.make_pattern(replacement, True)
                print(match_str, repl_str)
                self.replaces.append((match_str, repl_str))

    def make_pattern(self, original, is_replacement=False):
        original_parts = original.split(",")
        match_str = ""
        # print(original_parts)
        for part in original_parts:
            if is_replacement:
                if not part.startswith("0x"):
                    match_str += "\\g<" + part + ">"
                else:
                    match_str += str_to_unicode(part)
            else:
                if "-" not in part:
                    match_str += "(" + str_to_unicode(part) + ")"
                else:
                    match_str += (
                        "(["
                        + str_to_unicode(part.split("-")[0])
                        + "-"
                        + str_to_unicode(part.split("-")[1])
                        + "])"
                    )
        return match_str

    def normalize(self, text):
        for norm in self.replaces:
            print(norm[0], norm[1])
            text = re.sub(norm[0], norm[1], text)
        return text
