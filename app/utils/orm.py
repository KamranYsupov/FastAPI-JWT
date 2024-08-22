from typing import Coroutine

from fastapi import HTTPException
from pydantic import BaseModel
from starlette import status

from .exceptions import AlreadyExistsError 

async def validate_object_insertion(
    insert_service_method: Coroutine,
    insert_schema: BaseModel,
    exception_status_code: int = status.HTTP_400_BAD_REQUEST,
    exception_detail: str | None = None,
):
    try:
        obj = await insert_service_method(insert_schema)
    except AlreadyExistsError as e:
        if not exception_detail:
            exception_detail = str(e)
        raise HTTPException(
                status_code=exception_status_code,
                detail=exception_detail
            )
    
    return obj