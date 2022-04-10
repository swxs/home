from typing import Optional, List, Dict

from pydantic import BaseModel


class PasswordLockSchema(BaseModel):
    name: Optional[str] = None
    key: Optional[str] = None
    website: Optional[str] = None
    user_id: Optional[str] = None
    used: Optional[int] = 0
    ttype: Optional[int] = 0
    custom: Optional[Dict] = None
