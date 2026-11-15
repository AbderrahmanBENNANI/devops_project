from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

class CVData(BaseModel):
    model_config = ConfigDict(extra="forbid")
    full_name: str = Field(min_length=2, max_length=100)
    email: str = Field(max_length=254)
    phone: str = Field(default="", max_length=40)
    city: str = Field(default="", max_length=100)
    title: str = Field(default="", max_length=120)
    summary: str = Field(default="", max_length=2000)
    skills: list[str] = Field(default_factory=list, max_length=30)
    experience: list[dict] = Field(default_factory=list, max_length=15)
    education: list[dict] = Field(default_factory=list, max_length=15)

class LetterData(BaseModel):
    model_config = ConfigDict(extra="forbid")
    full_name: str = Field(min_length=2, max_length=100)
    recipient: str = Field(default="Madame, Monsieur", max_length=150)
    company: str = Field(default="", max_length=150)
    role: str = Field(min_length=2, max_length=120)
    paragraphs: list[str] = Field(min_length=1, max_length=6)
