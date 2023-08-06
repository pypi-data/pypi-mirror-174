from typing import Optional

import attr
from pydantic import Field, SecretStr

from .. import types


class RestoreManifest(types.Manifest):
    stanza: str = Field(
        description="pgBackRest stanza of the primary instance to restore from."
    )


@attr.s(auto_attribs=True, frozen=True, slots=True)
class Service:
    """A pgbackrest service bound to a PostgreSQL instance."""

    stanza: str
    """Name of the stanza"""


class ServiceManifest(types.ServiceManifest, service_name="pgbackrest"):

    stanza: Optional[str] = Field(
        default=None,
        description=(
            "Name of pgBackRest stanza. "
            "Something describing the actual function of the instance, such as 'app'."
        ),
        readonly=True,
    )
    password: Optional[SecretStr] = Field(
        default=None,
        description="Password of PostgreSQL role for pgBackRest.",
        exclude=True,
    )
    restore: Optional[RestoreManifest] = Field(
        default=None, readOnly=True, writeOnly=True, exclude=True
    )
