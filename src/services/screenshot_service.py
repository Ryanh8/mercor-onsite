"""
Screenshot capture service for monitoring work sessions
"""

from datetime import datetime
from pathlib import Path
from typing import Optional

import pyautogui
from PIL import Image

from ..models.screenshots import Screenshot


class ScreenshotService:
    """Service for capturing and managing screenshots during work sessions"""
    
    def __init__(self, screenshots_dir: str = "screenshots"):
        self.screenshots_dir = Path(screenshots_dir)
        self.screenshots_dir.mkdir(exist_ok=True)
    
    def capture_screenshot(self, employee_id: str, project_id: str, task_id: str) -> Optional[Screenshot]:
        """Capture a screenshot and create Screenshot object"""
        timestamp = int(datetime.now().timestamp() * 1000)
        filename = f"{employee_id}_{project_id}_{timestamp}.png"
        filepath = self.screenshots_dir / filename
        
        try:
            screenshot_img = pyautogui.screenshot()
            screenshot_img.save(filepath)
            
            # Create Screenshot object
            screenshot = Screenshot.create_scheduled_screenshot(
                project_id=project_id,
                task_id=task_id,
                employee_id=employee_id,
                organization_id="org_techcorp_main",
                timestamp=timestamp,
                app="Time Tracker",
                title="Work Session Screenshot"
            )
            screenshot.set_screenshot_link(str(filepath))
            screenshot.set_productivity_score(0.8)  # Default productive score
            
            return screenshot
        except Exception as e:
            print(f"Failed to capture screenshot: {e}")
            return None 