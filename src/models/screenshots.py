"""Screenshot model schema for the application."""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, Literal
from datetime import datetime, timezone, timedelta
import uuid


@dataclass
class Screenshot:
    """
    Screenshot model representing a captured screenshot during work time.
    
    This model handles screenshot data including application context,
    productivity tracking, device information, and work context.
    
    Attributes:
        id: Unique identifier for the screenshot
        type: Type of screenshot capture (scheduled, manual, etc.)
        timestamp: When the screenshot was taken (Unix timestamp in milliseconds)
        timezone_offset: Timezone offset in milliseconds
        app: Name of the active application
        app_file_name: Filename of the application executable
        app_file_path: Full file path to the application executable
        title: Window title of the active application
        url: URL if the application is a web browser
        document: Document name or path (if applicable)
        window_id: Unique identifier for the window
        shift_id: ID of the work shift
        project_id: ID of the project being worked on
        task_id: ID of the specific task being worked on
        task_status: Status of the task during screenshot
        task_priority: Priority of the task during screenshot
        user: Username of the employee
        computer: Name/identifier of the computer
        domain: Domain name (if applicable)
        name: Full name of the employee
        hwid: Hardware ID of the device
        os: Operating system
        os_version: Operating system version
        active: Whether the user was active during screenshot
        processed: Whether this screenshot has been processed
        created_at: When the entry was created (ISO string)
        updated_at: When the entry was last updated (ISO string)
        employee_id: ID of the employee
        team_id: ID of the team
        shared_settings_id: ID of shared settings
        organization_id: ID of the organization
        app_id: ID of the application
        app_label_id: ID of the application label
        category_id: ID of the productivity category
        category_label_id: ID of the category label
        productivity: Productivity score (typically 0-1 or 1-5 scale)
        site: Website domain (if applicable)
        timestamp_translated: Translated timestamp
        index: Index identifier for the entry
        link: Link to the screenshot file
        gateways: List of network gateway MAC addresses
    """
    
    id: str
    type: str
    timestamp: int
    project_id: str
    task_id: str
    employee_id: str
    organization_id: str
    app: str = ""
    app_file_name: str = ""
    app_file_path: str = ""
    title: str = ""
    url: str = ""
    document: str = ""
    window_id: str = ""
    shift_id: str = ""
    task_status: str = ""
    task_priority: str = ""
    user: str = ""
    computer: str = ""
    domain: str = ""
    name: str = ""
    hwid: str = ""
    os: str = ""
    os_version: str = ""
    active: bool = True
    processed: bool = False
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    team_id: Optional[str] = None
    shared_settings_id: Optional[str] = None
    app_id: Optional[str] = None
    app_label_id: Optional[str] = None
    category_id: Optional[str] = None
    category_label_id: Optional[str] = None
    productivity: float = 0.0
    site: str = ""
    timestamp_translated: Optional[int] = None
    index: Optional[str] = None
    link: str = ""
    timezone_offset: int = 0
    gateways: List[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        """Validate screenshot data after initialization."""
        if not self.id:
            self.id = str(uuid.uuid4())
        
        if not self.project_id:
            raise ValueError("Project ID is required")
        
        if not self.task_id:
            raise ValueError("Task ID is required")
        
        if not self.employee_id:
            raise ValueError("Employee ID is required")
        
        if not self.organization_id:
            raise ValueError("Organization ID is required")
        
        # Set translated timestamp if not provided
        if self.timestamp_translated is None:
            self.timestamp_translated = self.timestamp
        
        # Validate productivity score
        if self.productivity < 0:
            self.productivity = 0.0

    @property
    def screenshot_datetime(self) -> datetime:
        """Convert timestamp to datetime object."""
        return datetime.fromtimestamp(self.timestamp / 1000, tz=timezone.utc)

    @property
    def local_screenshot_datetime(self) -> datetime:
        """Get screenshot time adjusted for timezone offset."""
        offset_hours = self.timezone_offset / (1000 * 60 * 60)
        tz = timezone(timedelta(hours=offset_hours))
        return datetime.fromtimestamp(self.timestamp / 1000, tz=tz)

    @property
    def created_datetime(self) -> Optional[datetime]:
        """Convert created_at ISO string to datetime object."""
        if self.created_at:
            return datetime.fromisoformat(self.created_at.replace('Z', '+00:00'))
        return None

    @property
    def updated_datetime(self) -> Optional[datetime]:
        """Convert updated_at ISO string to datetime object."""
        if self.updated_at:
            return datetime.fromisoformat(self.updated_at.replace('Z', '+00:00'))
        return None

    @property
    def is_web_browser(self) -> bool:
        """Check if the screenshot is from a web browser."""
        browser_apps = ['chrome', 'firefox', 'safari', 'edge', 'opera', 'brave']
        return any(browser in self.app.lower() for browser in browser_apps)

    @property
    def is_productive(self) -> bool:
        """Check if the screenshot indicates productive activity."""
        return self.productivity > 0.5  # Assuming 0.5 is the threshold

    @property
    def is_active_session(self) -> bool:
        """Check if the user was active during this screenshot."""
        return self.active

    @property
    def has_url(self) -> bool:
        """Check if the screenshot has an associated URL."""
        return bool(self.url.strip())

    @property
    def gateway_count(self) -> int:
        """Get the number of network gateways detected."""
        return len(self.gateways)

    # Screenshot management methods
    def mark_as_processed(self) -> None:
        """Mark this screenshot as processed."""
        self.processed = True

    def set_productivity_score(self, score: float) -> None:
        """Set the productivity score for this screenshot."""
        self.productivity = max(0.0, score)  # Ensure non-negative

    def update_app_context(self, app: Optional[str] = None,
                          title: Optional[str] = None,
                          url: Optional[str] = None) -> None:
        """Update application context information."""
        if app is not None:
            self.app = app
        if title is not None:
            self.title = title
        if url is not None:
            self.url = url

    def update_task_context(self, status: Optional[str] = None,
                           priority: Optional[str] = None) -> None:
        """Update task status and priority context."""
        if status is not None:
            self.task_status = status
        if priority is not None:
            self.task_priority = priority

    def set_active_status(self, active: bool) -> None:
        """Set whether the user was active during this screenshot."""
        self.active = active

    def add_gateway(self, gateway_mac: str) -> None:
        """Add a network gateway MAC address."""
        if gateway_mac not in self.gateways:
            self.gateways.append(gateway_mac)

    def remove_gateway(self, gateway_mac: str) -> None:
        """Remove a network gateway MAC address."""
        if gateway_mac in self.gateways:
            self.gateways.remove(gateway_mac)

    def set_screenshot_link(self, link: str) -> None:
        """Set the link to the screenshot file."""
        self.link = link

    # Productivity analysis methods
    def categorize_productivity(self) -> str:
        """Categorize productivity level based on score."""
        if self.productivity >= 0.8:
            return "highly_productive"
        elif self.productivity >= 0.6:
            return "productive"
        elif self.productivity >= 0.4:
            return "neutral"
        elif self.productivity >= 0.2:
            return "distracting"
        else:
            return "unproductive"

    def get_app_category(self) -> str:
        """Get a general category for the application."""
        app_lower = self.app.lower()
        
        if any(browser in app_lower for browser in ['chrome', 'firefox', 'safari', 'edge']):
            return "web_browser"
        elif any(ide in app_lower for ide in ['vscode', 'visual studio', 'intellij', 'pycharm']):
            return "development"
        elif any(office in app_lower for office in ['word', 'excel', 'powerpoint', 'outlook']):
            return "office"
        elif any(design in app_lower for design in ['photoshop', 'illustrator', 'figma', 'sketch']):
            return "design"
        elif any(comm in app_lower for comm in ['slack', 'teams', 'zoom', 'discord']):
            return "communication"
        else:
            return "other"

    # API-compatible methods
    def get_screenshot_details(self) -> Dict[str, Any]:
        """Get detailed screenshot information for API responses."""
        return {
            "id": self.id,
            "type": self.type,
            "timestamp": self.timestamp,
            "timezoneOffset": self.timezone_offset,
            "localTime": self.local_screenshot_datetime.isoformat(),
            "application": {
                "name": self.app,
                "fileName": self.app_file_name,
                "filePath": self.app_file_path,
                "title": self.title,
                "url": self.url,
                "document": self.document,
                "category": self.get_app_category()
            },
            "window": {
                "id": self.window_id,
                "title": self.title
            },
            "work_context": {
                "shiftId": self.shift_id,
                "projectId": self.project_id,
                "taskId": self.task_id,
                "taskStatus": self.task_status,
                "taskPriority": self.task_priority
            },
            "employee": {
                "id": self.employee_id,
                "user": self.user,
                "name": self.name,
                "teamId": self.team_id
            },
            "device": {
                "computer": self.computer,
                "domain": self.domain,
                "hwid": self.hwid,
                "os": self.os,
                "osVersion": self.os_version,
                "gateways": self.gateways
            },
            "productivity": {
                "score": self.productivity,
                "category": self.categorize_productivity(),
                "isProductive": self.is_productive
            },
            "status": {
                "active": self.active,
                "processed": self.processed
            },
            "metadata": {
                "appId": self.app_id,
                "appLabelId": self.app_label_id,
                "categoryId": self.category_id,
                "categoryLabelId": self.category_label_id,
                "site": self.site,
                "link": self.link,
                "index": self.index
            },
            "timestamps": {
                "createdAt": self.created_at,
                "updatedAt": self.updated_at,
                "timestampTranslated": self.timestamp_translated
            },
            "organizationId": self.organization_id,
            "sharedSettingsId": self.shared_settings_id
        }

    @classmethod
    def create_scheduled_screenshot(cls, project_id: str, task_id: str, 
                                  employee_id: str, organization_id: str,
                                  timestamp: int, app: str = "",
                                  title: str = "", url: str = "") -> "Screenshot":
        """
        Create a scheduled screenshot entry.
        
        Args:
            project_id: ID of the project
            task_id: ID of the task
            employee_id: ID of the employee
            organization_id: ID of the organization
            timestamp: Screenshot timestamp in milliseconds
            app: Application name
            title: Window title
            url: URL if applicable
            
        Returns:
            Screenshot instance for scheduled capture
        """
        now_iso = datetime.utcnow().isoformat() + 'Z'
        
        return cls(
            id=str(uuid.uuid4()),
            type="scheduled",
            timestamp=timestamp,
            project_id=project_id,
            task_id=task_id,
            employee_id=employee_id,
            organization_id=organization_id,
            app=app,
            title=title,
            url=url,
            created_at=now_iso,
            updated_at=now_iso
        )

    @classmethod
    def from_dict(cls, data: dict) -> "Screenshot":
        """
        Create a Screenshot instance from a dictionary.
        
        Args:
            data: Dictionary containing screenshot data
            
        Returns:
            Screenshot instance
        """
        # Map camelCase keys to snake_case
        mapped_data = {
            "id": data.get("id"),
            "type": data.get("type"),
            "timestamp": data.get("timestamp"),
            "timezone_offset": data.get("timezoneOffset", 0),
            "app": data.get("app", ""),
            "app_file_name": data.get("appFileName", ""),
            "app_file_path": data.get("appFilePath", ""),
            "title": data.get("title", ""),
            "url": data.get("url", ""),
            "document": data.get("document", ""),
            "window_id": data.get("windowId", ""),
            "shift_id": data.get("shiftId", ""),
            "project_id": data.get("projectId"),
            "task_id": data.get("taskId"),
            "task_status": data.get("taskStatus", ""),
            "task_priority": data.get("taskPriority", ""),
            "user": data.get("user", ""),
            "computer": data.get("computer", ""),
            "domain": data.get("domain", ""),
            "name": data.get("name", ""),
            "hwid": data.get("hwid", ""),
            "os": data.get("os", ""),
            "os_version": data.get("osVersion", ""),
            "active": data.get("active", True),
            "processed": data.get("processed", False),
            "created_at": data.get("createdAt"),
            "updated_at": data.get("updatedAt"),
            "employee_id": data.get("employeeId"),
            "team_id": data.get("teamId"),
            "shared_settings_id": data.get("sharedSettingsId"),
            "organization_id": data.get("organizationId"),
            "app_id": data.get("appId"),
            "app_label_id": data.get("appLabelId"),
            "category_id": data.get("categoryId"),
            "category_label_id": data.get("categoryLabelId"),
            "productivity": data.get("productivity", 0.0),
            "site": data.get("site", ""),
            "timestamp_translated": data.get("timestampTranslated"),
            "index": data.get("_index"),
            "link": data.get("link", ""),
            "gateways": data.get("gateways", []),
        }
        
        # Remove None values for required fields
        required_fields = ["timestamp", "project_id", "task_id", "employee_id", "organization_id"]
        for field in required_fields:
            if mapped_data.get(field) is None:
                raise ValueError(f"{field} is required")
        
        return cls(**{k: v for k, v in mapped_data.items() if v is not None})

    def to_dict(self) -> dict:
        """
        Convert Screenshot instance to dictionary with camelCase keys.
        
        Returns:
            Dictionary representation of the screenshot
        """
        return {
            "id": self.id,
            "type": self.type,
            "timestamp": self.timestamp,
            "timezoneOffset": self.timezone_offset,
            "app": self.app,
            "appFileName": self.app_file_name,
            "appFilePath": self.app_file_path,
            "title": self.title,
            "url": self.url,
            "document": self.document,
            "windowId": self.window_id,
            "shiftId": self.shift_id,
            "projectId": self.project_id,
            "taskId": self.task_id,
            "taskStatus": self.task_status,
            "taskPriority": self.task_priority,
            "user": self.user,
            "computer": self.computer,
            "domain": self.domain,
            "name": self.name,
            "hwid": self.hwid,
            "os": self.os,
            "osVersion": self.os_version,
            "active": self.active,
            "processed": self.processed,
            "createdAt": self.created_at,
            "updatedAt": self.updated_at,
            "employeeId": self.employee_id,
            "teamId": self.team_id,
            "sharedSettingsId": self.shared_settings_id,
            "organizationId": self.organization_id,
            "appId": self.app_id,
            "appLabelId": self.app_label_id,
            "categoryId": self.category_id,
            "categoryLabelId": self.category_label_id,
            "productivity": self.productivity,
            "site": self.site,
            "timestampTranslated": self.timestamp_translated,
            "_index": self.index,
            "link": self.link,
            "gateways": self.gateways,
        }

    def __str__(self) -> str:
        """String representation of the screenshot."""
        return f"Screenshot(id={self.id}, app='{self.app}', productivity={self.productivity}, active={self.active})"

    def __repr__(self) -> str:
        """Detailed string representation of the screenshot."""
        return (f"Screenshot(id='{self.id}', type='{self.type}', "
                f"app='{self.app}', productivity={self.productivity}, "
                f"active={self.active}, project='{self.project_id}')")
