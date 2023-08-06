from typing import Match

from .base import StatutePatternsMethods
from .statute_base import StatuteBase, StatuteCategory


def cull_suffix(text: str) -> str:
    """Remove `the`, `of`, `,`, ` ` from the text's suffix, when existing text is passed"""
    for i in ["the", "of", ","]:
        text = text.removesuffix(i).strip()
    return text


class RepublicAct(StatutePatternsMethods):
    group_name = "republic_act"
    digit_group_name = "RA_digit"

    def __init__(self) -> None:
        base_text = self.statute_base_pattern(
            group_name=self.group_name,
            first_word=r"Rep(.|ublic)?",
            second_word=r"Act?\s?",
            first_letter="R",
            second_letter="A",
            optional_number_keyword=self.optional_number_keyword,
        )

        digit = rf"(?P<{self.digit_group_name}>{self.digit_format})"

        self.formula = rf"""
        ( # e.g. Republic Act (RA) No. 242
            \b{base_text}
            \s*{digit}
        )
        """

    @classmethod
    def matcher(cls, m: Match) -> StatuteBase | None:
        if m.group(cls.group_name):
            return StatuteBase(
                statute_category=StatuteCategory.RA,
                statute_serial_id=cull_suffix(m.group(cls.digit_group_name)),
            )
        return None


class ExecutiveOrder(StatutePatternsMethods):
    group_name = "executive_order"
    digit_group_name = "EO_digit"

    def __init__(self) -> None:
        base_text = self.statute_base_pattern(
            group_name=self.group_name,
            first_word=r"Exec(.|utive)?",
            second_word=r"Order?\s?",
            first_letter="E",
            second_letter="O",
            optional_number_keyword=self.optional_number_keyword,
        )

        digit = rf"(?P<{self.digit_group_name}>{self.digit_format})"

        self.formula = rf"""
        (
            \b{base_text}
            \s*{digit}
        )
        """

    @classmethod
    def matcher(cls, m: Match) -> StatuteBase | None:
        if m.group(cls.group_name):
            return StatuteBase(
                statute_category=StatuteCategory.EO,
                statute_serial_id=cull_suffix(m.group(cls.digit_group_name)),
            )
        return None


class PresidentialDecree(StatutePatternsMethods):
    group_name = "presidential_decree"
    digit_group_name = "PD_digit"

    def __init__(self) -> None:
        base_text = self.statute_base_pattern(
            group_name=self.group_name,
            first_word=r"Pres(.|idential)?",
            second_word=r"Dec(.|ree)?\s?",
            first_letter="P",
            second_letter="D",
            optional_number_keyword=self.optional_number_keyword,
        )

        digit = rf"(?P<{self.digit_group_name}>{self.digit_format})"

        self.formula = rf"""
        (
            \b{base_text}
            \s*{digit}
        )
        """

    @classmethod
    def matcher(cls, m: Match) -> StatuteBase | None:
        if m.group(cls.group_name):
            return StatuteBase(
                statute_category=StatuteCategory.PD,
                statute_serial_id=cull_suffix(m.group(cls.digit_group_name)),
            )
        return None


class BatasPambansa(StatutePatternsMethods):
    group_name = "batas_pambansa"
    digit_group_name = "BP_digit"

    def __init__(self) -> None:
        base_text = self.statute_base_pattern(
            group_name=self.group_name,
            first_word=r"Batas",
            second_word=r"Pambansa",
            first_letter="B",
            second_letter="P",
            optional_number_keyword=self.optional_bilang_keyword,
        )  # * number keyword replaced with bilang

        digit = rf"(?P<{self.digit_group_name}>{self.digit_format})"

        self.formula = rf"""
        (
            \b{base_text}
            \s*{digit}
        )
        """

    @classmethod
    def matcher(cls, m: Match) -> StatuteBase | None:
        if m.group(cls.group_name):
            return StatuteBase(
                statute_category=StatuteCategory.BP,
                statute_serial_id=cull_suffix(m.group(cls.digit_group_name)),
            )
        return None


class CommonwealthAct(StatutePatternsMethods):
    group_name = "commonwealth_act"
    digit_group_name = "CA_digit"

    def __init__(self) -> None:
        base_text = self.statute_base_pattern(
            group_name="commonwealth_act",
            first_word=r"Com(.|monwealth)?",
            second_word=r"Act\s?",
            first_letter="C",
            second_letter="A",
            optional_number_keyword=self.optional_number_keyword,
        )

        # * digits are limited to 3
        digit = (
            rf"(?P<{self.digit_group_name}>{self.simple_commonwealth_digits})"
        )

        self.formula = rf"""
        (
            \b{base_text}
            \s*{digit}
        )
        """

    @classmethod
    def matcher(cls, m: Match) -> StatuteBase | None:
        if m.group(cls.group_name):
            return StatuteBase(
                statute_category=StatuteCategory.CA,
                statute_serial_id=cull_suffix(m.group(cls.digit_group_name)),
            )
        return None


class LegacyAct(StatutePatternsMethods):
    group_name = "legacy_act"
    digit_group_name = "ACT_digit"

    def __init__(self) -> None:

        # join a list of negative lookbehinds
        non_match = "".join(
            rf"(?<!{i}\s)"
            for i in [
                r"An",
                r"AN",
                r"Republic",
                r"Rep",
                r"Rep\.",
                r"REPUBLIC",
                r"Commonwealth",
                r"COMMONWEALTH",
            ]
        )

        # * negative lookbehinds with words: "Act/Acts"
        base_text = rf"(?P<legacy_act>{non_match}Acts?)"

        digit = rf"(?P<{self.digit_group_name}>{self.digit_format})"

        self.formula = rf"""
        (
            \b{base_text}
            \s+{self.optional_number_keyword}
            \s*{digit}
        )
        """

    @classmethod
    def matcher(cls, m: Match) -> StatuteBase | None:
        if m.group(cls.group_name):
            return StatuteBase(
                statute_category=StatuteCategory.ACT,
                statute_serial_id=cull_suffix(m.group(cls.digit_group_name)),
            )
        return None


class AdministrativeMatter(StatutePatternsMethods):
    group_name = "rule_am"
    digit_group_name = "AM_digit"

    def __init__(self) -> None:
        base_text = self.statute_base_pattern(
            group_name=self.group_name,
            first_word=r"""Adm(
                \.|
                in\.|
                inistrative
            )""",
            second_word=r"Matter",
            first_letter="A",
            second_letter="M",
            optional_number_keyword=self.optional_number_keyword,
        )

        digit = rf"""
            (?P<{self.digit_group_name}>
                (
                    [\w-]+
                    -sc # must end with SC
                )|
                (
                    99-10-05-0 # not ending in SC
                )

            )"""

        self.formula = rf"""
        ( # e.g. Administrative Matter (AM) No. 242
            \b{base_text}
            \s*{digit}
        )
        """

    @classmethod
    def matcher(cls, m: Match) -> StatuteBase | None:
        if m.group(cls.group_name):
            return StatuteBase(
                statute_category=StatuteCategory.RULE_AM,
                statute_serial_id=cull_suffix(m.group(cls.digit_group_name)),
            )
        return None


class BarMatter(StatutePatternsMethods):
    group_name = "rule_bm"
    digit_group_name = "BM_digit"

    def __init__(self) -> None:
        base_text = self.statute_base_pattern(
            group_name=self.group_name,
            first_word=r"Bar",
            second_word=r"Matter",
            first_letter="B",
            second_letter="M",
            optional_number_keyword=self.optional_number_keyword,
        )

        digit = rf"""
            (?P<{self.digit_group_name}>
                803|
                1922|
                1645|
                850|
                287|
                1132|
                1755|
                1960|
                1153|
                209
            )"""

        self.formula = rf"""
        (
            \b{base_text}
            \s*{digit}
        )
        """

    @classmethod
    def matcher(cls, m: Match) -> StatuteBase | None:
        if m.group(cls.group_name):
            return StatuteBase(
                statute_category=StatuteCategory.RULE_BM,
                statute_serial_id=cull_suffix(m.group(cls.digit_group_name)),
            )
        return None


class ResolutionEnBanc(StatutePatternsMethods):
    group_name = "rule_reso"
    digit_group_name = "RESO_digit"

    def __init__(self) -> None:
        version_one = rf"""
        (
            Court
            \s+
            En
            \s+
            Banc
            \s+
            Resolution
        )
        """

        version_two = rf"""
        (
            Resolution
            \s+
            [o|O]f
            \s+
            [t|T]he
            \s+
            Court
            \s+
            En
            \s+
            Banc
        )
        """

        digit = rf"(?P<{self.digit_group_name}>[\w-]+)"  # TODO: fix, need to include date and means of converting the date to serialized form

        self.formula = rf"""
        ( # e.g. Court En Banc Resolution dated 10-15-1991
            \b
            (?P<{self.group_name}>{version_one}|{version_two}
            )
            \s+
            [D|d]ated
            \s*{digit}
        )
        """

    @classmethod
    def matcher(cls, m: Match) -> StatuteBase | None:
        if m.group(cls.group_name):
            return StatuteBase(
                statute_category=StatuteCategory.RULE_RESO,
                statute_serial_id=cull_suffix(m.group(cls.digit_group_name)),
            )
        return None


class VetoMessage(StatutePatternsMethods):
    group_name = "veto_msg"
    digit_group_name = "veto_digit"

    def __init__(self) -> None:
        veto = rf"""
        (
            Veto
            \s+
            Message
        )
        """

        digit = rf"(?P<{self.digit_group_name}>[\w]{5,})"  # TODO: need more samples

        self.formula = rf"""
        ( # e.g. Veto Message - 11534
            \b
            (?P<{self.group_name}>{veto})
            [\s\-\–]+
            \s*{digit}
        )
        """

    @classmethod
    def matcher(cls, m: Match) -> StatuteBase | None:
        if m.group(cls.group_name):
            return StatuteBase(
                statute_category=StatuteCategory.VETO,
                statute_serial_id=m.group(cls.digit_group_name),
            )
        return None


class CircularOCA(
    StatutePatternsMethods
):  # TODO: need more samples, matches 0
    group_name = "rule_oca_cir"
    digit_group_name = "OCA_CIR_digit"

    def __init__(self) -> None:
        base = rf"""
        (
            OCA
            \s+
            Cir(\.|cular)
        )
        """

        digit = rf"(?P<{self.digit_group_name}>[\w-]+)"

        self.formula = rf"""
        ( # OCA Cir. No. 39-02
            \b
            (?P<{self.group_name}>{base})
            \s+
            (No\.\s*)?
            {digit}
        )
        """

    @classmethod
    def matcher(cls, m: Match) -> StatuteBase | None:
        if m.group(cls.group_name):
            return StatuteBase(
                statute_category=StatuteCategory.OCA_CIR,
                statute_serial_id=cull_suffix(m.group(cls.digit_group_name)),
            )
        return None


class CircularSC(StatutePatternsMethods):  # TODO: need more samples, matches 0
    group_name = "rule_sc_cir"
    digit_group_name = "SC_CIR_digit"

    def __init__(self) -> None:
        base = rf"""
        (
            SC
            \s+
            Cir(\.|cular)
        )
        """

        digit = rf"(?P<{self.digit_group_name}>[\w-]+)"

        self.formula = rf"""
        ( # SC Cir. No. 19
            \b
            (?P<{self.group_name}>{base})
            \s+
            (No\.\s*)?
            {digit}
        )
        """

    @classmethod
    def matcher(cls, m: Match) -> StatuteBase | None:
        if m.group(cls.group_name):
            return StatuteBase(
                statute_category=StatuteCategory.SC_CIR,
                statute_serial_id=cull_suffix(m.group(cls.digit_group_name)),
            )
        return None


class LetterInstruction(StatutePatternsMethods):
    group_name = "letter_of_instruction"
    digit_group_name = "LOI_digit"

    def __init__(self) -> None:
        base = rf"""
        (
            Letter
            \s+
            of
            \s+
            Instruction(s)?
        )|
        (
            LOI
        )
        """

        digit = rf"""
            (?P<{self.digit_group_name}>
                474|
                729|
                97|
                270|
                926|
                1295|
                19|
                174|
                273|
                767|
                1416|
                713|
                968
            )\b"""

        self.formula = rf"""
        ( # Letter of Instructions No. 1223
            \b
            (?P<{self.group_name}>{base})
            \s+
            (No\.\s*)?
            {digit}
        )
        """

    @classmethod
    def matcher(cls, m: Match) -> StatuteBase | None:
        if m.group(cls.group_name):
            return StatuteBase(
                statute_category=StatuteCategory.LOI,
                statute_serial_id=cull_suffix(m.group(cls.digit_group_name)),
            )
        return None
