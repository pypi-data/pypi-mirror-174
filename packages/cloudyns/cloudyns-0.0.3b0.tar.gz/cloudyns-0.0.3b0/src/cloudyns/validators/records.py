from typing import Literal

from cloudyns.base.constants import VALID_TYPES_RECORDS, TYPE_RECORD_A
from cloudyns.base import exceptions as cloudyns_exc


def validate_a_record(*args, **kwargs):
    values = {"type": TYPE_RECORD_A}
    name = kwargs.get("name")
    data = kwargs.get("data")
    ttl = kwargs.get("ttl")

    if not name:
        raise cloudyns_exc.AttrNameRequiredRecordTypeA
    values.update(dict(name=name))

    if not data:
        raise cloudyns_exc.AttrDataRequiredRecordTypeA
    values.update(dict(data=data))

    if ttl:
        values.update(dict(ttl=ttl))

    return values


def validate_record(
    record_type: Literal[VALID_TYPES_RECORDS] = TYPE_RECORD_A, *args, **kwargs
):
    internal_map_validations = kwargs.pop("map_validations", None)
    map_validations = internal_map_validations or {TYPE_RECORD_A: validate_a_record}
    validator = map_validations.get(record_type)

    if not validator:
        raise cloudyns_exc.InvalidRecordType(record_type=record_type)
    values = validator(**kwargs)
    return values
