"""Time tracking model schema for the application."""

from dataclasses import dataclass, field
from typing import Optional, Dict, Any
from datetime import datetime, timezone
import uuid


@dataclass
class TimeTracking:
    """
    Time tracking model matching Insightful API response structure.
    
    Input parameters (simplified):
        start: Start timestamp (Unix timestamp in milliseconds) - required
        end: End timestamp (Unix timestamp in milliseconds) - required (0 for active sessions)
        timezone: Timezone string - optional
        employeeId: Employee ID - optional
        teamId: Team ID - optional  
        projectId: Project ID - optional
        taskId: Task ID - optional
        shiftId: Shift ID - optional
    
    Full API response includes all these additional fields:
    """
    
    # Core required fields
    start: int
    end: int = 0  # 0 for active sessions
    
    # Optional input fields
    timezone: Optional[str] = None
    employeeId: Optional[str] = None
    teamId: Optional[str] = None
    projectId: Optional[str] = None
    taskId: Optional[str] = None
    shiftId: Optional[str] = None
    
    # Full API response fields (auto-generated or populated by system)
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    type: str = "manual"  # "manual" or "automatic"
    note: str = ""
    timezoneOffset: int = 0  # in milliseconds
    paid: bool = False
    billable: bool = True
    overtime: bool = False
    billRate: float = 0.0
    overtimeBillRate: float = 0.0
    payRate: float = 0.0
    overtimePayRate: float = 0.0
    taskStatus: str = "in progress"
    taskPriority: str = "medium"
    user: Optional[str] = None  # username
    computer: Optional[str] = None  # computer name
    domain: str = ""
    name: Optional[str] = None  # employee full name
    hwid: Optional[str] = None  # hardware ID
    os: str = "darwin"  # operating system
    osVersion: Optional[str] = None
    processed: bool = False
    createdAt: Optional[str] = None
    updatedAt: Optional[str] = None
    sharedSettingsId: Optional[str] = None
    organizationId: Optional[str] = None
    startTranslated: Optional[int] = None
    endTranslated: Optional[int] = None
    negativeTime: int = 0
    deletedScreenshots: int = 0
    _index: Optional[str] = None

    def __post_init__(self) -> None:
        """Initialize computed fields and validate data."""
        if self.start <= 0:
            raise ValueError("Start timestamp must be positive")
        
        # Only validate end > start if end is not 0 (active session)
        if self.end != 0 and self.start >= self.end:
            raise ValueError("Start time must be before end time")
        
        # Set computed fields
        if self.createdAt is None:
            self.createdAt = datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
        if self.updatedAt is None:
            self.updatedAt = self.createdAt
        if self.startTranslated is None:
            self.startTranslated = self.start
        if self.endTranslated is None:
            self.endTranslated = self.end
        
        # Generate hardware ID if not provided
        if self.hwid is None:
            self.hwid = str(uuid.uuid4())

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
        self.endTranslated = end_timestamp
        self.updatedAt = datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')

    def set_employee_info(self, employee_name: str, username: str) -> None:
        """Set employee information."""
        self.name = employee_name
        self.user = username

    def set_system_info(self, computer_name: str, os_version: str, domain: str = "") -> None:
        """Set system information."""
        self.computer = computer_name
        self.osVersion = os_version
        self.domain = domain

    def set_billing_info(self, bill_rate: float, pay_rate: float = 0.0, 
                        overtime_bill_rate: float = 0.0, overtime_pay_rate: float = 0.0) -> None:
        """Set billing information."""
        self.billRate = bill_rate
        self.payRate = pay_rate
        self.overtimeBillRate = overtime_bill_rate
        self.overtimePayRate = overtime_pay_rate

    def set_task_info(self, status: str = "in progress", priority: str = "medium") -> None:
        """Set task status and priority."""
        self.taskStatus = status
        self.taskPriority = priority

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
        # Handle both simplified input and full API response
        instance = cls(
            start=data.get("start"),
            end=data.get("end", 0),
            timezone=data.get("timezone"),
            employeeId=data.get("employeeId"),
            teamId=data.get("teamId"),
            projectId=data.get("projectId"),
            taskId=data.get("taskId"),
            shiftId=data.get("shiftId")
        )
        
        # Set additional fields if present in data
        for field_name in [
            "id", "type", "note", "timezoneOffset", "paid", "billable", "overtime",
            "billRate", "overtimeBillRate", "payRate", "overtimePayRate",
            "taskStatus", "taskPriority", "user", "computer", "domain", "name",
            "hwid", "os", "osVersion", "processed", "createdAt", "updatedAt",
            "sharedSettingsId", "organizationId", "startTranslated", "endTranslated",
            "negativeTime", "deletedScreenshots", "_index"
        ]:
            if field_name in data:
                setattr(instance, field_name, data[field_name])
        
        return instance

    def to_dict(self) -> dict:
        """
        Convert TimeTracking instance to dictionary (full API response format).
        
        Returns:
            Dictionary representation of the time tracking entry
        """
        result = {
            "id": self.id,
            "type": self.type,
            "note": self.note,
            "start": self.start,
            "end": self.end,
            "timezoneOffset": self.timezoneOffset,
            "paid": self.paid,
            "billable": self.billable,
            "overtime": self.overtime,
            "billRate": self.billRate,
            "overtimeBillRate": self.overtimeBillRate,
            "payRate": self.payRate,
            "overtimePayRate": self.overtimePayRate,
            "taskStatus": self.taskStatus,
            "taskPriority": self.taskPriority,
            "user": self.user,
            "computer": self.computer,
            "domain": self.domain,
            "name": self.name,
            "hwid": self.hwid,
            "os": self.os,
            "osVersion": self.osVersion,
            "processed": self.processed,
            "createdAt": self.createdAt,
            "updatedAt": self.updatedAt,
            "startTranslated": self.startTranslated,
            "endTranslated": self.endTranslated,
            "negativeTime": self.negativeTime,
            "deletedScreenshots": self.deletedScreenshots
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
        if self.sharedSettingsId is not None:
            result["sharedSettingsId"] = self.sharedSettingsId
        if self.organizationId is not None:
            result["organizationId"] = self.organizationId
        if self._index is not None:
            result["_index"] = self._index
            
        return result

    def to_simple_dict(self) -> dict:
        """
        Convert to simplified dictionary with only the core input fields.
        
        Returns:
            Simplified dictionary with only input parameters
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
        return f"TimeTracking(id={self.id[:8]}..., start={self.start}, end={self.end}, duration={duration})"

    def __repr__(self) -> str:
        """Detailed string representation of the time tracking entry."""
        status = "active" if self.is_active_session else "completed"
        return (f"TimeTracking(id='{self.id}', start={self.start}, end={self.end}, status='{status}', "
                f"employeeId='{self.employeeId}', projectId='{self.projectId}')")
