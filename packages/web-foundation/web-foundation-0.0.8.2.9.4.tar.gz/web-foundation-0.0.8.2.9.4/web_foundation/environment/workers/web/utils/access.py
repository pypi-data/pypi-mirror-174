import asyncio
import json as py_json
from typing import List, Type, Coroutine, Callable, Any

from sanic.exceptions import NotFound

from web_foundation.environment.resources.database.model_loader import ModelLoader
from web_foundation.environment.resources.database.models import AbstractDbModel, GenericDbType
from web_foundation.environment.workers.web.ext.request_handler import InputContext

ExternalCallback = Callable[
    [AbstractDbModel | List[AbstractDbModel] | None], Coroutine[Any, Any, None]]


async def exec_access(inc: InputContext,
                      model: Type[AbstractDbModel],
                      fetch_fields: List[str] = None,
                      middleware: Type[ModelLoader] = ModelLoader,
                      external_callback: ExternalCallback = None
                      ):
    """
    Access to models
    """
    match inc.request.method:
        case "GET":
            kwargs = inc.r_kwargs
            entity_id = kwargs.pop("entity_id", None)
            if entity_id is None:
                limit = inc.request.args.get("limit")
                offset = inc.request.args.get("offset")
                limit = int(limit) if limit and limit.isdigit() else 100
                offset = int(offset) if offset and offset.isdigit() else None
                # order_by = inc.request.args.get("order_by")  # for openapi. Variable forwarded to read_all in kwargs
                for ar, val in inc.request.args.items():
                    if ar in ["limit", "offset"]:
                        continue
                    val = val[0]
                    if val.lower() == 'false':
                        val = False
                    elif val.lower() == 'true':
                        val = True
                    elif val.isdigit():
                        val = int(val)
                    elif "." in val and val.replace('.', '').isdigit():
                        val = float(val)
                    elif val.startswith("["):
                        val = py_json.loads(val)
                    kwargs[ar] = val

                retrieved_all, total = await middleware.read_all(model, inc.identity, limit, offset,
                                                                 fetch_fields=fetch_fields, **kwargs)
                if external_callback:
                    asyncio.create_task(external_callback(retrieved_all))
                res = [await model.values_dict() for model in retrieved_all]
                return res, total
            retrieved = await middleware.read(model, entity_id, inc.identity, fetch_fields=fetch_fields, **kwargs)
            if not retrieved:
                raise NotFound()

        case "POST":
            retrieved = await middleware.create(model, inc.identity, inc.dto, **inc.r_kwargs)

        case "PATCH":
            entity_id = inc.r_kwargs.pop("entity_id")
            retrieved = await middleware.update(model, entity_id, inc.identity, inc.dto, **inc.r_kwargs)

        case "DELETE":
            entity_id = inc.r_kwargs.pop("entity_id")
            retrieved = await middleware.delete(model, entity_id, inc.identity, **inc.r_kwargs)

    if external_callback:
        asyncio.create_task(external_callback(retrieved))
    if isinstance(retrieved, list):
        return [await i.values_dict() for i in retrieved]
    return await retrieved.values_dict()


async def exec_access_with_total(inc: InputContext,
                      model: Type[AbstractDbModel],
                      fetch_fields: List[str] = None,
                      middleware: Type[ModelLoader] = ModelLoader,
                      external_callback: ExternalCallback = None):
    """Return from read_all dict with "items" and "total" """
    result = await exec_access(inc=inc, model=model, fetch_fields=fetch_fields,
                               middleware=middleware,
                               external_callback=external_callback)
    if inc.request.method == "GET" and isinstance(result, tuple):
        return {"items": result[0], "total": result[1]}
    return result
