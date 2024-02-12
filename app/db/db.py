import copy

from gotrue import AsyncMemoryStorage

from supabase.client import ClientOptions
from supabase._async.client import AsyncClient, create_client

from ..core.settings import settings


class Repository:
    """Supabase repository to administrate connections to DB"""
    admin: AsyncClient = None
    client_options = ClientOptions(
        auto_refresh_token=False,
        postgrest_client_timeout=10,
        storage=AsyncMemoryStorage()
    )

    @classmethod
    async def init_admin(cls):
        cls.admin = await create_client(
            settings.SUPABASE_URL.unicode_string(),
            settings.SERVICE_KEY.get_secret_value(),
            options=ClientOptions(
                schema='auth',
                storage=AsyncMemoryStorage()
            )
        )

    @classmethod
    async def close_admin(cls):
        if cls.admin is None:
            return
        await cls.admin.auth.close()
        await cls.admin.postgrest.aclose()
        await cls.admin.storage.aclose()

    @classmethod
    async def get_client(cls,) -> AsyncClient | None:
        client: AsyncClient = await create_client(
            settings.SUPABASE_URL.unicode_string(),
            settings.ANON_KEY.get_secret_value(),
            options=copy.deepcopy(cls.client_options)
        )
        return client
