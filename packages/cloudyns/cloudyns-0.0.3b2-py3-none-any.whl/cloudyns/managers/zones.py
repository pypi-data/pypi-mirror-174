import requests

from abc import abstractmethod
from typing import Dict, Any, Optional, Literal

from cloudyns.base import exceptions as cloudyns_exc
from cloudyns.base.constants import (
    VALID_TYPES_RECORDS,
    TYPE_RECORD_A,
    STATUS_CODE_404_NOT_FOUND,
    STATUS_CODE_201_CREATED,
    STATUS_CODE_422_UNPROCESSABLE_ENTITY,
    STATUS_CODE_204_NO_CONTENT,
)
from cloudyns.base.exceptions import ApiUnknownError
from cloudyns.validators import records as records_validators
from cloudyns.validators.response_validators import validate_basic_status_code_response


class BaseDomain(object):
    domain_name: str
    domain_ttl: int = 3600
    zone_file = str
    _zone_url: str
    _headers: Dict[str, str] = None


class BaseRecord(BaseDomain):
    record_id: int
    record_type: Optional[str] = None
    name: Optional[str] = None
    data: Optional[str] = None
    priority: Optional[int] = None
    port: Optional[int] = None
    ttl: Optional[int] = None
    weight: Optional[int] = None
    flags: Optional[str] = None
    tag: Optional[str] = None

    @abstractmethod
    def delete_record(self):
        raise NotImplementedError

    @abstractmethod
    def update_record(self, *args, **kwargs):
        raise NotImplementedError


class BaseZoneDomain(BaseDomain):
    zone_file = str
    _base_url: str
    _url_domain: str
    _headers: Dict[str, str] = None
    _records_map = Dict[str, Any]

    @abstractmethod
    def delete_domain(self):
        raise NotImplementedError

    @abstractmethod
    def _add_record(
        self, record_type: Literal[VALID_TYPES_RECORDS] = TYPE_RECORD_A, *args, **kwargs
    ):
        raise NotImplementedError

    @abstractmethod
    def add_a_record(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def add_aaa_record(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def add_caa_record(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def add_cname_record(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def add_mx_record(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def add_ns_record(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def add_soa_record(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def add_srv_record(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def add_txt_record(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def _validate_record(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def _validate_a_record(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def _validate_aaa_record(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def _validate_caa_record(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def _validate_cname_record(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def _validate_mx_record(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def _validate_ns_record(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def _validate_soa_record(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def _validate_srv_record(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def _validate_txt_record(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def get_records(self):
        raise NotImplementedError

    @abstractmethod
    def get_record(
        self,
        name: str,
        record_type: Literal[VALID_TYPES_RECORDS] = TYPE_RECORD_A,
        data: str = None,
    ):
        raise NotImplementedError

    @abstractmethod
    def _fetch_records(self):
        raise NotImplementedError

    @property
    def quantity_record(self):
        return len(self._records_map)

    @property
    def _remote_quantity_record(self):
        raise NotImplementedError


class DoRecord(BaseRecord):
    _base_url = "https://api.digitalocean.com/v2/domains"

    def __init__(
        self,
        domain_name: str,
        headers: Dict[str, str],
        record_id: int,
        record_type: str,
        name: Optional[str] = None,
        data: Optional[str] = None,
        priority: Optional[int] = None,
        port: Optional[int] = None,
        ttl: Optional[int] = None,
        weight: Optional[int] = None,
        flags: Optional[str] = None,
        tag: Optional[str] = None,
    ):
        self.domain_name = domain_name
        self.record_id = record_id
        self.record_type = record_type
        self.name = name
        self.data = data
        self.priority = priority
        self.port = port
        self.ttl = ttl
        self.weight = weight
        self.flags = flags
        self.tag = tag

        self._zone_url = f"{self._base_url}/{domain_name}"
        self._records_url = f"{self._base_url}/{domain_name}/records"
        self._this_url = f"{self._records_url}/{self.record_id}"
        self._headers = headers

    def __str__(self):
        return f"<DoRecord: domain={self.domain_name} name={self.name} type={self.record_type} data={self.data}>"

    def __repr__(self):
        return self.__str__()

    def delete_record(self):
        response = requests.delete(url=self._this_url, headers=self._headers)
        validate_basic_status_code_response(response)
        if response.status_code == STATUS_CODE_204_NO_CONTENT:
            del self
            return
        raise ApiUnknownError

    def update_record(self, *args, **kwargs):
        data = {
            "type": kwargs.get("record_type", self.record_type),
            "name": kwargs.get("name", self.name),
            "data": kwargs.get("data", self.data),
            "priority": kwargs.get("priority", self.priority),
            "port": kwargs.get("port", self.port),
            "ttl": kwargs.get("ttl", self.ttl),
            "weight": kwargs.get("weight", self.weight),
            "flags": kwargs.get("flags", self.flags),
            "tag": kwargs.get("tag", self.tag),
        }
        response = requests.patch(url=self._this_url, headers=self._headers, json=data)
        validate_basic_status_code_response(response)
        response_json = response.json()
        record = response_json["domain_record"]
        self.record_type = record["type"]
        self.name = record["name"]
        self.data = record["data"]
        self.priority = record["priority"]
        self.port = record["port"]
        self.ttl = record["ttl"]
        self.weight = record["weight"]
        self.flags = record["flags"]
        self.tag = record["tag"]


class DoDomain(BaseZoneDomain):
    _base_url = "https://api.digitalocean.com/v2/domains"

    def __init__(self, domain_name: str, headers: Dict[str, str]):
        self.domain_name = domain_name
        self._headers = headers
        self._url_domain = f"{self._base_url}/{self.domain_name}/records"
        self._fetch_records()

    def __str__(self):
        return f"<DoDomain: {self.domain_name}>"

    def __repr__(self):
        return self.__str__()

    def _fetch_records(self):
        next_url = self._url_domain
        domain_records = {}
        while next_url:
            response = requests.get(url=next_url, headers=self._headers)
            response_json = response.json()
            page_records = response_json.get("domain_records")
            next_url = response_json.get("links", {}).get("pages", {}).get("next")
            domain_records.update(
                {
                    f'{record["name"]}-{record["type"]}-{record["data"]}-{record["id"]}': DoRecord(
                        domain_name=self.domain_name,
                        headers=self._headers,
                        record_id=record["id"],
                        record_type=record["type"],
                        name=record["name"],
                        data=record["data"],
                        priority=record["priority"],
                        port=record["port"],
                        ttl=record["ttl"],
                        weight=record["weight"],
                        flags=record["flags"],
                        tag=record["tag"],
                    )
                    for record in page_records
                }
            )
        self._quantity_cache = len(domain_records)

        self._records_map = domain_records

    def get_records(self):
        if (
            not self._records_map
            or self._quantity_cache != self._remote_quantity_record
        ):
            self._fetch_records()
        return list(self._records_map.values())

    def get_record(
        self,
        name: str,
        type: Literal[VALID_TYPES_RECORDS] = TYPE_RECORD_A,
        data: str = None,
    ):
        record_key_start_with = (
            f"{name}-{type}"
        )
        record_key_start_with += f"-{data}" if data else ""

        record_keys = [
            key
            for key in self._records_map.keys()
            if key.startswith(record_key_start_with)
        ]

        if not record_keys:
            raise cloudyns_exc.RecordNameTypeDoesNotExist(
                record_name=record_name, record_type=record_type
            )
        if len(record_keys) > 1:
            raise cloudyns_exc.MultiplesRecordSameNameType(
                record_name=record_name, record_type=record_type
            )
        record_key = record_keys[0]
        record = self._records_map.get(record_key)
        if not record:
            raise cloudyns_exc.RecordNameTypeDoesNotExist(
                record_name=record_name, record_type=record_type
            )
        return record

    def _add_record(
        self,
        record_type: Literal[VALID_TYPES_RECORDS] = TYPE_RECORD_A,
        name: Optional[str] = None,
        data: Optional[str] = None,
        priority: Optional[int] = None,
        port: Optional[int] = None,
        ttl: Optional[int] = None,
        weight: Optional[int] = None,
        flags: Optional[str] = None,
        tag: Optional[str] = None,
    ):
        values = self._validate_record(
            record_type=record_type,
            name=name,
            data=data,
            priority=priority,
            port=port,
            ttl=ttl,
            weight=weight,
            flags=flags,
            tag=tag,
        )
        if not values:
            raise cloudyns_exc.ProvidesWrongData

        try:
            record = self.get_record(
                name=name, type=record_type
            )
        except Exception:
            pass
        else:
            if record:
                raise cloudyns_exc.RecordAlreadyExist
        response = requests.post(
            url=self._url_domain, json=values, headers=self._headers
        )

        if response.status_code == STATUS_CODE_404_NOT_FOUND:
            raise cloudyns_exc.AddRecordDomainNotFound

        if response.status_code == STATUS_CODE_422_UNPROCESSABLE_ENTITY:
            error_message = response.json().get("message")
            raise cloudyns_exc.AddRecordUnprocessableEntity(message=error_message)

        validate_basic_status_code_response(response)

        if response.status_code == STATUS_CODE_201_CREATED:
            record_data = response.json()["domain_record"]
            record_id = record_data.pop("id")
            record_type = record_data.pop("type")
            current_record = DoRecord(
                domain_name=self.domain_name,
                headers=self._headers,
                record_id=record_id,
                record_type=record_type,
                **record_data,
            )
            self._fetch_records()
            return current_record

        raise cloudyns_exc.ApiUnknownError

    def _validate_record(
        self, record_type: Literal[VALID_TYPES_RECORDS] = TYPE_RECORD_A, *args, **kwargs
    ):
        map_validations = {TYPE_RECORD_A: self._validate_a_record}
        kwargs.update({"map_validations": map_validations})
        values = records_validators.validate_record(
            record_type=record_type, *args, **kwargs
        )
        return values

    def add_a_record(self, name: str, data: str, ttl: int = None):
        return self._add_record(
            record_type=TYPE_RECORD_A,
            name=name,
            data=data,
            ttl=ttl,
        )

    def _validate_a_record(self, *args, **kwargs):
        values = records_validators.validate_a_record(*args, **kwargs)

        return values

    @property
    def _remote_quantity_record(self):
        response = requests.get(url=self._url_domain, headers=self._headers)
        response_json = response.json()
        remote_records = response_json.get("meta", {}).get("total", 0)
        return remote_records
