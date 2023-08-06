from abc import abstractmethod
from typing import Dict, List, Type

import requests

from cloudyns.base import exceptions as cloudyns_exc
from cloudyns.base.constants import STATUS_CODE_401_UNAUTHORIZED
from cloudyns.base.dataclasses import CloudynsConf
from cloudyns.managers.zones import DoDomain, BaseZoneDomain


class BaseProviderManager:
    conf: CloudynsConf
    headers: Dict[str, str] = None
    _zones: List[str] = None
    _api_url: str = "api.example.com"

    @abstractmethod
    def __init__(self, conf: CloudynsConf):
        raise NotImplementedError

    @abstractmethod
    def get_zones(self):
        raise NotImplementedError

    @abstractmethod
    def get_domain(self, domain_name: str) -> Type[BaseZoneDomain]:
        raise NotImplementedError

    @abstractmethod
    def create_domain(self, domain_name: str, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def update_domain(self, domain_name: str, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def delete_domain(self, domain_name: str, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def _set_headers(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def _fetch_domains(self):
        raise NotImplementedError


class DigitalOceanManager(BaseProviderManager):
    _api_url = "https://api.digitalocean.com/v2/"

    def __init__(self, conf: CloudynsConf):
        if not conf.token:
            raise cloudyns_exc.ProviderTokenAuthenticationMissing

        self.conf = conf
        self.headers = self._set_headers(token=self.conf.token)
        self._fetch_domains()

    def _fetch_domains(self):
        response = requests.get(url=f"{self._api_url}domains/", headers=self.headers)
        if response.status_code == STATUS_CODE_401_UNAUTHORIZED:
            raise cloudyns_exc.ApiUnauthorized
        response_json = response.json()
        page_domains = response_json.get("domains")
        self._zones = [domain["name"] for domain in page_domains]

    def _set_headers(self, *args, **kwargs):
        headers = {
            "content-type": "application/json",
            "Authorization": f"Bearer {kwargs['token']}",
        }
        return headers

    def get_zones(self):
        if not self._zones:
            self._fetch_domains()
        return self._zones

    def get_domain(self, domain_name: str) -> DoDomain:
        if domain_name not in self.get_zones():
            raise cloudyns_exc.ProviderManagerMissingDomain(domain_name=domain_name)
        return DoDomain(domain_name=domain_name, headers=self.headers)

    def create_domain(self, domain_name: str, *args, **kwargs):
        pass

    def update_domain(self, domain_name: str, *args, **kwargs):
        pass

    def delete_domain(self, domain_name: str, *args, **kwargs):
        pass
