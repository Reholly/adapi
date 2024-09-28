from server.schemas.common import APIModel


class CategoryBase(APIModel):
    id: int
    category_name: str = ''


class CategoryOut(CategoryBase):
    pass
