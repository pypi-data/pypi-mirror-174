from typing import Optional, List

from pydantic import BaseModel


class QuestionSearch(BaseModel):
    questionTitle: Optional[str] = None
    skillId: Optional[str] = None
    levelId: Optional[str] = None
    subSkill1Id: Optional[str] = None
    subSkill2Id: Optional[str] = None
    subSkill3Id: Optional[str] = None
    roleId: Optional[str] = None
