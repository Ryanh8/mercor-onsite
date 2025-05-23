#!/usr/bin/env python3
"""
Simple tests for the time tracking application
"""

import json
from datetime import datetime
from src.models.time_tracking import TimeTracking
from src.models.employee import Employee
from src.models.project import Project


def test_time_tracking_creation():
    """Test creating a simple time tracking entry"""
    print("🧪 Testing TimeTracking creation...")
    
    # Create an active session
    entry = TimeTracking.create_active_session(
        start=1640995200000,  # Jan 1, 2022
        employeeId="emp_001_sarah_johnson",
        projectId="proj_website_redesign",
        taskId="task_default_website_redesign",
        teamId="team_frontend_dev",
        timezone="UTC"
    )
    
    print(f"✅ Created entry: {entry}")
    print(f"✅ Is active: {entry.is_active_session}")
    print(f"✅ JSON: {json.dumps(entry.to_dict(), indent=2)}")
    print()


def test_clock_in_out():
    """Test clock in and clock out functionality"""
    print("🧪 Testing clock in/out...")
    
    # Clock in
    start_time = int(datetime.now().timestamp() * 1000)
    entry = TimeTracking.create_active_session(
        start=start_time,
        employeeId="emp_001_sarah_johnson",
        projectId="proj_website_redesign"
    )
    
    print(f"✅ Clocked in: {entry.is_active_session}")
    print(f"✅ Start time: {entry.start}")
    
    # Clock out
    end_time = start_time + (2 * 60 * 60 * 1000)  # 2 hours later
    entry.clock_out(end_time)
    
    print(f"✅ Clocked out: {not entry.is_active_session}")
    print(f"✅ End time: {entry.end}")
    print(f"✅ Duration: {entry.duration_milliseconds / (1000 * 60 * 60):.2f} hours")
    print()


def test_load_mock_data():
    """Test loading mock data"""
    print("🧪 Testing mock data loading...")
    
    try:
        # Test employee data
        with open("mock-db/employee.json", "r") as f:
            employees_data = json.load(f)
        
        print(f"✅ Loaded {len(employees_data)} employees")
        
        # Create an employee object
        first_employee = Employee.from_dict(employees_data[0])
        print(f"✅ First employee: {first_employee.name} ({first_employee.id})")
        print(f"✅ Is active: {first_employee.is_active}")
        
        # Test project data
        with open("mock-db/project.json", "r") as f:
            projects_data = json.load(f)
        
        print(f"✅ Loaded {len(projects_data)} projects")
        
        # Create a project object
        first_project = Project.from_dict(projects_data[0])
        print(f"✅ First project: {first_project.name} ({first_project.id})")
        print(f"✅ Is billable: {first_project.billable}")
        print(f"✅ Bill rate: ${first_project.payroll.bill_rate}/hour")
        
    except Exception as e:
        print(f"❌ Error loading mock data: {e}")
    
    print()


def test_time_tracking_json_storage():
    """Test saving and loading time tracking data"""
    print("🧪 Testing time tracking JSON storage...")
    
    # Create some test entries
    entries = [
        TimeTracking.create_active_session(
            start=1640995200000,
            employeeId="emp_001_sarah_johnson",
            projectId="proj_website_redesign"
        ),
        TimeTracking(
            start=1640995200000,
            end=1640998800000,  # 1 hour later
            employeeId="emp_002_michael_chen",
            projectId="proj_api_development"
        )
    ]
    
    # Convert to JSON
    json_data = [entry.to_dict() for entry in entries]
    print(f"✅ Created {len(entries)} entries")
    
    # Save to file
    with open("mock-db/time_tracking.json", "w") as f:
        json.dump(json_data, f, indent=2)
    
    print("✅ Saved to time_tracking.json")
    
    # Load back from file
    with open("mock-db/time_tracking.json", "r") as f:
        loaded_data = json.load(f)
    
    loaded_entries = [TimeTracking.from_dict(data) for data in loaded_data]
    print(f"✅ Loaded {len(loaded_entries)} entries")
    
    # Check first entry
    first_entry = loaded_entries[0]
    print(f"✅ First entry: {first_entry}")
    print(f"✅ Is active: {first_entry.is_active_session}")
    
    print()


def main():
    """Run all tests"""
    print("🚀 Running simple tests for time tracking application\n")
    
    test_time_tracking_creation()
    test_clock_in_out()
    test_load_mock_data()
    test_time_tracking_json_storage()
    
    print("✅ All tests completed!")


if __name__ == "__main__":
    main() 