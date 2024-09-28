from server.schemas.common import APIModel


class StatusBase(APIModel):
    id: int
    status_name: str


class StatusOut(StatusBase):
    pass
