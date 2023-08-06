from datetime import datetime
from pydantic import BaseModel, EmailStr


class QuestionSortOrder(BaseModel):
    assessmentQnaId: str
    sortOrder: str


class AssessmentCreation(BaseModel):
    type: str
    title: str
    startDate: datetime
    endDate: datetime
    description: str


class AssessmentStatusChange(BaseModel):
    assessmentId: str
    isActive: bool


class AssessmentUserRequest(BaseModel):
    firstName: str
    lastName: str
    email: EmailStr
    assessmentId: str


class AssessmentUserAddRequest(BaseModel):
    email: EmailStr
    assessmentId: str
    enabled: bool
    score: int
    status: str


class AssessmentUserStatusRequest(BaseModel):
    assessmentUserId: str
    enabled: bool


class UserAssessmentMarkedRequest(BaseModel):
    assessmentUserId: str
    marked: bool


class UserAssessmentQNAMarkedRequest(BaseModel):
    assessmentUserQnaId: str
    isCorrect: bool
    personalNotes: str
