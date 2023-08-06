from dataclasses import dataclass
from typing import Optional, Literal

from cloudyns.base.constants import PROVIDER_DIGITAL_OCEAN, AVAILABLE_PROVIDERS


@dataclass
class CloudynsConf:
    provider: Literal[AVAILABLE_PROVIDERS] = PROVIDER_DIGITAL_OCEAN
    username: Optional[str] = None
    password: Optional[str] = None
    token: Optional[str] = None
