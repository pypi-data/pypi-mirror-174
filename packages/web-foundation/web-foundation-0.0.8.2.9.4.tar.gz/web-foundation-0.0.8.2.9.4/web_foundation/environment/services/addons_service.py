from web_foundation.environment.services.service import Service


class ApiAddonsService(Service):

    async def add_new_middleware(self, filename: str):
        await self._worker.mdw_manager.add_new_middleware(filename)

    async def delete_middleware(self, filename: str):
        await self._worker.mdw_manager.delete_middleware(filename)
