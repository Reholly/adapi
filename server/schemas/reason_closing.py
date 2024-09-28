from .common import APIModel


class ReasonClosingBase(APIModel):
    id: int
    reason_name: str


class ReasonClosingOut(ReasonClosingBase):
    pass
