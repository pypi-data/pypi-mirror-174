from cloudyns.base.constants import PROVIDER_DIGITAL_OCEAN
from cloudyns.base.dataclasses import CloudynsConf
from cloudyns.base.exceptions import BuilderProviderMissing, ProviderDoesNotSupport
from cloudyns.managers.providers import DigitalOceanManager, BaseProviderManager

_VALID_PROVIDERS_MAP = {
    PROVIDER_DIGITAL_OCEAN: DigitalOceanManager,
}


def build_provider_manager(conf: CloudynsConf) -> BaseProviderManager:
    if not conf.provider:
        raise BuilderProviderMissing

    provider_manager_class = _VALID_PROVIDERS_MAP.get(conf.provider)
    if not provider_manager_class:
        raise ProviderDoesNotSupport(provider=conf.provider)

    return provider_manager_class(conf=conf)
