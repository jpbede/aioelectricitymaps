"""Module contains classes for de-/serialisation with marshmallow."""
from dataclasses import dataclass, field

from dataclasses_json import DataClassJsonMixin, config
from marshmallow import fields

from .models import Zone


@dataclass(slots=True, frozen=True)
class ZoneList(dict[str, Zone], DataClassJsonMixin):
    """List of zones"""

    zones: dict[str, Zone] = field(
        metadata=config(
            mm_field=fields.Dict(
                keys=fields.String(),
                values=fields.Nested(Zone.schema()),
            )
        )
    )
