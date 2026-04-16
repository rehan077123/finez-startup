import importlib
import inspect
import pkgutil
from typing import Dict, List

import providers
from providers.base import AffiliateProvider


_PROVIDERS: Dict[str, AffiliateProvider] = {}


def _ensure_registered() -> None:
    if _PROVIDERS:
        return
    for module_info in pkgutil.iter_modules(providers.__path__):
        name = module_info.name
        if name in ("base", "registry") or name.startswith("_"):
            continue
        module = importlib.import_module(f"providers.{name}")
        for _, obj in inspect.getmembers(module, inspect.isclass):
            if obj is AffiliateProvider or not issubclass(obj, AffiliateProvider):
                continue
            instance = obj()
            if getattr(instance, "id", None):
                _PROVIDERS[instance.id] = instance


def list_providers() -> List[dict]:
    _ensure_registered()
    return [{"id": p.id, "name": p.name} for p in _PROVIDERS.values()]


def get_provider(provider_id: str) -> AffiliateProvider:
    _ensure_registered()
    if provider_id not in _PROVIDERS:
        raise KeyError(provider_id)
    return _PROVIDERS[provider_id]
