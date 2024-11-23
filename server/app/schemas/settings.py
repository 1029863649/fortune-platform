from pydantic import BaseModel

class Settings(BaseModel):
    email_notification: bool = True
    browser_notification: bool = False
    public_history: bool = False
    public_favorites: bool = False
    theme: str = 'light'

    class Config:
        from_attributes = True 