from pydantic import BaseModel, EmailStr, Field


class UserSchemaMixin(BaseModel):
    username: str = Field(title='Имя пользователя', max_length=50, min_length=8)
    email: EmailStr = Field(title='E-mail')
    
  
class SellerSchemaMixin(BaseModel):
    name: str = Field(title='Имя продавца', max_length=32)
    bio: str | None = Field(title='Информация о продавце', default=None)
    is_verified: bool = Field(title='Подтверждён', default=False)
    
      
class ProductSchemaMixin(BaseModel):
    name: str = Field(title='Название продукта')
    description: str = Field(title='Описание')
    price: float = Field(title='Цена', default=0)
    rating: float = Field(title='Оценка', le=5.0, gt=1.0)
    
    
