#!/usr/bin/env python3
"""
Simple test for the main application functionality
"""

import json
from datetime import datetime
from src.services.data_manager import MockDataManager
from src.services.time_tracking_service import TimeTrackingService


def test_real_employee_workflow():
    """Test the complete workflow with a real employee from mock data"""
    print("🧪 Testing real employee workflow...")
    
    # Initialize services
    data_manager = MockDataManager()
    time_service = TimeTrackingService(data_manager)
    
    # Load a real employee
    employees = data_manager.load_employees()
    sarah = None
    for emp in employees:
        if emp.id == "emp_001_sarah_johnson":
            sarah = emp
            break
    
    if not sarah:
        print("❌ Could not find Sarah Johnson in mock data")
        return
    
    print(f"✅ Found employee: {sarah.name} ({sarah.id})")
    print(f"✅ Is active: {sarah.is_active}")
    
    # Get her projects
    projects = data_manager.get_employee_projects(sarah.id)
    print(f"✅ Sarah is assigned to {len(projects)} projects:")
    for project in projects:
        print(f"   - {project.name} (${project.payroll.bill_rate}/hour)")
    
    # Test clock in
    try:
        print("\n🕐 Testing clock in...")
        time_entry = time_service.clock_in(sarah.id)
        print(f"✅ Clocked in successfully!")
        print(f"✅ Project: {time_entry.projectId}")
        print(f"✅ Task: {time_entry.taskId}")
        print(f"✅ Start time: {time_entry.start}")
        print(f"✅ Is active: {time_entry.is_active_session}")
        
        # Check active session
        active_session = time_service.get_active_session(sarah.id)
        if active_session:
            print(f"✅ Active session found: {active_session.projectId}")
        else:
            print("❌ No active session found")
        
        # Test clock out
        print("\n🕐 Testing clock out...")
        completed_entry = time_service.clock_out(sarah.id)
        print(f"✅ Clocked out successfully!")
        print(f"✅ End time: {completed_entry.end}")
        print(f"✅ Duration: {completed_entry.duration_milliseconds / (1000 * 60)} minutes")
        print(f"✅ Is active: {completed_entry.is_active_session}")
        
        # Check no active session
        active_session = time_service.get_active_session(sarah.id)
        if not active_session:
            print(f"✅ No active session (correctly clocked out)")
        else:
            print("❌ Still has active session")
        
    except Exception as e:
        print(f"❌ Error during workflow: {e}")
    
    print()


def test_time_tracking_persistence():
    """Test that time tracking data persists to JSON file"""
    print("🧪 Testing time tracking persistence...")
    
    # Check if we have time tracking data
    try:
        with open("mock-db/time_tracking.json", "r") as f:
            data = json.load(f)
        
        print(f"✅ Found {len(data)} time tracking entries in JSON file")
        
        if data:
            first_entry = data[0]
            print(f"✅ First entry: employeeId={first_entry.get('employeeId')}, projectId={first_entry.get('projectId')}")
            print(f"✅ Start: {first_entry.get('start')}, End: {first_entry.get('end')}")
            
            # Check if it's an active session
            if first_entry.get('end') == 0:
                print("✅ Found active session in data")
            else:
                duration_ms = first_entry.get('end') - first_entry.get('start')
                duration_hours = duration_ms / (1000 * 60 * 60)
                print(f"✅ Found completed session: {duration_hours:.2f} hours")
        
    except FileNotFoundError:
        print("❌ No time_tracking.json file found")
    except Exception as e:
        print(f"❌ Error reading time tracking data: {e}")
    
    print()


def test_employee_project_validation():
    """Test that employee-project validation works"""
    print("🧪 Testing employee-project validation...")
    
    data_manager = MockDataManager()
    time_service = TimeTrackingService(data_manager)
    
    # Try to clock in Sarah to a project she's not assigned to
    try:
        time_service.clock_in(
            employee_id="emp_001_sarah_johnson",
            project_id="proj_security_audit"  # Sarah is not assigned to this
        )
        print("❌ Should have failed - Sarah not assigned to security audit")
    except Exception as e:
        print(f"✅ Correctly rejected invalid project assignment: {str(e)}")
    
    # Try to clock in non-existent employee
    try:
        time_service.clock_in(employee_id="emp_999_fake")
        print("❌ Should have failed - fake employee")
    except Exception as e:
        print(f"✅ Correctly rejected fake employee: {str(e)}")
    
    print()


def main():
    """Run all application tests"""
    print("🚀 Running application tests\n")
    
    test_real_employee_workflow()
    test_time_tracking_persistence()
    test_employee_project_validation()
    
    print("✅ All application tests completed!")


if __name__ == "__main__":
    main() 