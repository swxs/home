import datetime
from typing import Optional

import pydantic

from web.custom_types import objectId


class BaseSchema(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(from_attributes=True)

    id: Optional[objectId] = None
    create_by: Optional[objectId] = None
    create_at: Optional[datetime.datetime] = None
    update_by: Optional[objectId] = None
    update_at: Optional[datetime.datetime] = None
    delete_at: Optional[datetime.datetime] = None
