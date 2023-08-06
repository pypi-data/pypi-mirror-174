import re
from enum import Enum
from pathlib import Path
from typing import Iterator, NamedTuple, Pattern

from loguru import logger
from pydantic import BaseModel, Field, constr, validator

separator_pattern: Pattern = re.compile("|".join([r",", r"\s+", r"(\sand\s)"]))


def split_separator(text: str):
    for a in separator_pattern.split(text):
        if a and a != "and":  # removes None, ''
            yield a


class IndeterminateStatute(NamedTuple):
    """When unable to determine the serialized state of the statute, e.g. Constitution could mean 1987 Constitution, 1973 Constitution, etc."""

    text: str


class StatuteCategory(str, Enum):
    RA = "ra"
    CA = "ca"
    ACT = "act"
    CONST = "const"
    SPAIN = "spain"
    BP = "bp"
    PD = "pd"
    EO = "eo"
    LOI = "loi"
    VETO = "veto"
    ROC = "roc"
    RULE_BM = "rule_bm"
    RULE_AM = "rule_am"
    RULE_RESO = "rule_reso"
    OCA_CIR = "oca_cir"
    SC_CIR = "sc_cir"


class StatuteBase(BaseModel):
    """Used to identify the statute based on a category and identifier. The col and index fields are populated in anticipation of future use via the `sqlpyd` library."""

    statute_category: StatuteCategory = Field(
        description="This should match the enumeration in StatuteID.",
        col=str,
        index=True,
    )
    statute_serial_id: constr(to_lower=True) = Field(  # type: ignore
        ...,
        regex="[a-z0-9-]+",
        col=str,
        index=True,
    )

    @validator("statute_category", pre=True)
    def category_in_lower_case(cls, v):
        return StatuteCategory(v.lower())

    @validator("statute_serial_id", pre=True)
    def serial_id_lower(cls, v):
        return v.lower()

    class Config:
        use_enum_values = True

    @classmethod
    def extract_initial(cls, serial_title: str) -> "StatuteBase":
        """Get the first matching statute and convert to category and serial_id; note that `StatuteBase` is a Named Tuple with different keys from the `StatuteBase`; and the latter is always lower-cased."""
        from statute_utils.id import StatuteID

        if base := StatuteID.get_statute_matches(serial_title):
            first_statute = base[0]
            if isinstance(first_statute, StatuteBase):
                return first_statute
        raise Exception(f"No statute base created from {serial_title=}")

    @property
    def serial_title(self) -> str:
        """Generate a serialized version, e.g. with category RA and serial_id 386, this becomes Republic Act No. 386."""
        from statute_utils.id import StatuteID

        member = StatuteID.get_member(self.statute_category)
        if not member:
            raise Exception(f"Bad member {self.statute_category=}")
        return member.make_title(self.statute_serial_id.upper())

    def get_path(self, path: Path) -> Path | None:
        target = path / self.statute_category / self.statute_serial_id
        if target.exists():
            return target
        return None

    def get_paths(self, path: Path) -> list[Path]:
        """The serial id isn't enough since the variant of a `StatuteRow.id` includes a `-<digit>` where the digit is the variant."""
        targets = []
        target = path / self.statute_category
        paths = target.glob(f"{self.statute_serial_id}-*/details.yaml")
        for variant_path in paths:
            if variant_path.exists():
                targets.append(variant_path.parent)
        return targets

    def extract_folders(self, statute_path: Path) -> Iterator[Path]:
        """Using the `category` and `id` of the object, get the possible folder paths."""
        if folder := self.get_path(statute_path):
            yield folder
        else:
            if folders := self.get_paths(statute_path):
                yield from folders
            else:
                logger.error(f"No statute path/s detected for {self=}")

    def units_path(self, folder: Path) -> Path | None:
        """There are two kinds of unit files: the preferred / customized
        variant and the one scraped (the default in the absence of a preferred
        variant)."""
        text = f"{self.statute_category}{self.statute_serial_id}.yaml"
        preferred = folder / text
        if preferred.exists():
            return preferred

        default = folder / "units.yaml"
        if default.exists():
            return default

        return None

    @property
    def deconstructed_identifiers(self) -> list[str]:
        """Extracts compound identifiers, e.g. "EO 1, 2, 14 and 14-A."""
        return list(split_separator(self.statute_serial_id))

    @property
    def is_single(self) -> bool:
        """Determine if only a single identifier contained in the field."""
        return len(self.deconstructed_identifiers) == 1

    @property
    def separate_identifiers(self) -> list["StatuteBase"] | None:
        """If there multiple identifiers, produce multiple instances."""

        if self.is_single:
            return None

        base = []
        min_length = 1  # see doubtful base
        for i in self.deconstructed_identifiers:
            item_length = len(i)
            if item_length >= min_length:
                min_length = item_length
                base.append(
                    StatuteBase(
                        statute_category=self.statute_category,
                        statute_serial_id=i,
                    )
                )
            else:
                # Deals with cases where the second part is doubtful base are doubtful e.g.:
                # RA 8493, 12 (12 is doubtful)
                # RA 8042,35 (35 is doubtful)
                # RULE_BM 793, 30
                # RA 9136, 08
                # RA 7695, and 64
                continue

        return base
