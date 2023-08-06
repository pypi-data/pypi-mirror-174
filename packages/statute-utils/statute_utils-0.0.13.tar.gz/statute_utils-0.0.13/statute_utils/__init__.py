from .designator import StatuteDesignation, StatuteMatcher
from .formula import (
    IndeterminateStatute,
    ProvisionLabel,
    ProvisionPattern,
    ProvisionSubject,
    StatuteBase,
    StatuteCategory,
    match_provision,
    match_provisions,
)
from .id import StatuteCounted, StatuteID
from .spanner import get_statutory_provision_spans
