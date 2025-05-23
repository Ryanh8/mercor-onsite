"""Time tracking model schema for the application."""

from dataclasses import dataclass
from typing import Optional, Dict, Any
from datetime import datetime, timezone
import uuid


@dataclass
class TimeTracking:
    """
    Simple time tracking model for employee work sessions.
    
    Attributes:
        start: Start timestamp (Unix timestamp in milliseconds) - required
        end: End timestamp (Unix timestamp in milliseconds) - required (0 for active sessions)
        timezone: Timezone string - optional
        employeeId: Employee ID - optional
        teamId: Team ID - optional  
        projectId: Project ID - optional
        taskId: Task ID - optional
        shiftId: Shift ID - optional
    """
    
    start: int
    end: int = 0  # 0 for active sessions
    timezone: Optional[str] = None
    employeeId: Optional[str] = None
    teamId: Optional[str] = None
    projectId: Optional[str] = None
    taskId: Optional[str] = None
    shiftId: Optional[str] = None

    def __post_init__(self) -> None:
        """Basic validation after initialization."""
        if self.start <= 0:
            raise ValueError("Start timestamp must be positive")
        
        # Only validate end > start if end is not 0 (active session)
        if self.end != 0 and self.start >= self.end:
            raise ValueError("Start time must be before end time")

    @property
    def is_active_session(self) -> bool:
        """Check if this is an active time tracking session (end = 0)."""
        return self.end == 0

    @property
    def duration_milliseconds(self) -> int:
        """Get the duration in milliseconds. Returns 0 for active sessions."""
        if self.is_active_session:
            return 0
        return self.end - self.start

    @property
    def current_duration_milliseconds(self) -> int:
        """Get current duration including active sessions."""
        if self.is_active_session:
            current_time = int(datetime.now().timestamp() * 1000)
            return current_time - self.start
        return self.end - self.start

    def clock_out(self, end_timestamp: int) -> None:
        """Clock out by setting the end timestamp."""
        if not self.is_active_session:
            raise ValueError("Cannot clock out - session is already completed")
        
        if end_timestamp <= self.start:
            raise ValueError("End time must be after start time")
            
        self.end = end_timestamp

    @classmethod
    def create_active_session(cls, start: int, employeeId: Optional[str] = None,
                             projectId: Optional[str] = None, taskId: Optional[str] = None,
                             teamId: Optional[str] = None, shiftId: Optional[str] = None,
                             timezone: Optional[str] = None) -> "TimeTracking":
        """
        Create an active time tracking session (end = 0).
        
        Args:
            start: Start timestamp in milliseconds
            employeeId: Employee ID
            projectId: Project ID
            taskId: Task ID
            teamId: Team ID
            shiftId: Shift ID
            timezone: Timezone string
            
        Returns:
            TimeTracking instance for active session
        """
        return cls(
            start=start,
            end=0,  # Active session
            employeeId=employeeId,
            projectId=projectId,
            taskId=taskId,
            teamId=teamId,
            shiftId=shiftId,
            timezone=timezone
        )

    @classmethod
    def from_dict(cls, data: dict) -> "TimeTracking":
        """
        Create a TimeTracking instance from a dictionary.
        
        Args:
            data: Dictionary containing time tracking data
            
        Returns:
            TimeTracking instance
        """
        return cls(
            start=data.get("start"),
            end=data.get("end", 0),
            timezone=data.get("timezone"),
            employeeId=data.get("employeeId"),
            teamId=data.get("teamId"),
            projectId=data.get("projectId"),
            taskId=data.get("taskId"),
            shiftId=data.get("shiftId")
        )

    def to_dict(self) -> dict:
        """
        Convert TimeTracking instance to dictionary.
        
        Returns:
            Dictionary representation of the time tracking entry
        """
        result = {
            "start": self.start,
            "end": self.end
        }
        
        # Only include optional fields if they have values
        if self.timezone is not None:
            result["timezone"] = self.timezone
        if self.employeeId is not None:
            result["employeeId"] = self.employeeId
        if self.teamId is not None:
            result["teamId"] = self.teamId
        if self.projectId is not None:
            result["projectId"] = self.projectId
        if self.taskId is not None:
            result["taskId"] = self.taskId
        if self.shiftId is not None:
            result["shiftId"] = self.shiftId
            
        return result

    def __str__(self) -> str:
        """String representation of the time tracking entry."""
        if self.is_active_session:
            duration_ms = self.current_duration_milliseconds
            duration_hours = duration_ms / (1000 * 60 * 60)
            duration = f"Active ({duration_hours:.2f}h so far)"
        else:
            duration_hours = self.duration_milliseconds / (1000 * 60 * 60)
            duration = f"{duration_hours:.2f}h"
        return f"TimeTracking(start={self.start}, end={self.end}, duration={duration})"

    def __repr__(self) -> str:
        """Detailed string representation of the time tracking entry."""
        status = "active" if self.is_active_session else "completed"
        return (f"TimeTracking(start={self.start}, end={self.end}, status='{status}', "
                f"employeeId='{self.employeeId}', projectId='{self.projectId}')")
