"""
API request and response models
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class ClockInRequest(BaseModel):
    """Request model for clocking in an employee"""
    employee_id: str
    project_id: Optional[str] = None
    task_id: Optional[str] = None
    timestamp: Optional[datetime] = None


class ClockOutRequest(BaseModel):
    """Request model for clocking out an employee"""
    employee_id: str
    timestamp: Optional[datetime] = None 