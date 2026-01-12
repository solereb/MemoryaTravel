from pydantic import BaseModel

class CountryResponse(BaseModel):
    id: int
    code: str
    name_en: str
    name_ru: str
    
    class Config:
        from_attributes = True
        
class RegionResponse(BaseModel):
    id: int
    name_ru: str
    
    class Config:
        from_attributes = True