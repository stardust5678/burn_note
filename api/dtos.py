from sqlmodel import SQLModel

class SecretMessageCreate(SQLModel):
    encrypted_message: str

class SecretMessagePublic(SQLModel):
    token: str
    encrypted_message: str