from typing import Optional, List

from pydantic import BaseModel


class QuestionAnswer(BaseModel):
    id: str
    jobId: str
    question: str
    answer: str
    skillId: Optional[str]
    levelId: Optional[str]
    subSkill1Id: Optional[str]
    subSkill2Id: Optional[str]
    subSkill3Id: Optional[str]
    questionType: str
    questionTheme: Optional[str]
    time: int
    points: int
    mediaQuestion: Optional[bool]
    mediaExtension: Optional[str]
    fileEncoded: Optional[str]
    roles: Optional[List[str]]
