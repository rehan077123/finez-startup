from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional


class AffiliateProvider(ABC):
    id: str
    name: str

    @abstractmethod
    async def fetch_trending(
        self,
        *,
        category: str,
        subcategory: Optional[str] = None,
        limit: int = 10,
    ) -> List[Dict[str, Any]]:
        raise NotImplementedError()

