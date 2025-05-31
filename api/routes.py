from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from api.db import get_async_session
from api.dtos import SecretMessageCreate, SecretMessagePublic
from api.services import SecretMessageService

router = APIRouter(prefix="/api/secret")

@router.get("/{token}", response_model=SecretMessagePublic)
async def get_secret(token: str, session: Session = Depends(get_async_session)):
    try:
        service = SecretMessageService(session)
        secret = await service.get_secret(token)
        if not secret:
            raise HTTPException(status_code=404, detail="Secret not found or expired")
        # Delete the secret after retrieval to prevent reuse
        await service.delete_secret(token)
        response = SecretMessagePublic(token=token, encrypted_message=secret)
        return response
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("", response_model=SecretMessagePublic)
async def create_secret(dto: SecretMessageCreate, session: Session = Depends(get_async_session)):
    try:
        service = SecretMessageService(session)
        token = await service.save_secret(dto.encrypted_message)
        response = SecretMessagePublic(token=token, encrypted_message=dto.encrypted_message)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
