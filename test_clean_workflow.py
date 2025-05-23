#!/usr/bin/env python3
"""
Clean workflow test - starts fresh and tests complete clock in/out
"""

import json
from datetime import datetime
from main import MockDataManager, TimeTrackingService


def test_clean_workflow():
    """Test complete workflow starting with clean time tracking data"""
    print("🧪 Testing clean workflow...")
    
    # Clear time tracking data
    with open("mock-db/time_tracking.json", "w") as f:
        json.dump([], f)
    print("✅ Cleared time tracking data")
    
    # Initialize services
    data_manager = MockDataManager()
    time_service = TimeTrackingService(data_manager)
    
    # Get Sarah
    sarah = data_manager.get_employee_by_id("emp_001_sarah_johnson")
    print(f"✅ Found employee: {sarah.name}")
    
    # Get her projects
    projects = data_manager.get_employee_projects(sarah.id)
    print(f"✅ Sarah has {len(projects)} projects")
    
    # Test 1: Clock in
    print("\n🕐 Step 1: Clock in...")
    time_entry = time_service.clock_in(sarah.id)
    print(f"✅ Clocked in to project: {time_entry.projectId}")
    print(f"✅ Task: {time_entry.taskId}")
    print(f"✅ Is active: {time_entry.is_active_session}")
    
    # Test 2: Check active session
    print("\n🕐 Step 2: Check active session...")
    active = time_service.get_active_session(sarah.id)
    if active:
        print(f"✅ Active session confirmed: {active.projectId}")
    else:
        print("❌ No active session found")
    
    # Test 3: Try to clock in again (should fail)
    print("\n🕐 Step 3: Try double clock in...")
    try:
        time_service.clock_in(sarah.id)
        print("❌ Should have failed")
    except Exception as e:
        print(f"✅ Correctly prevented double clock in: {str(e)}")
    
    # Test 4: Clock out
    print("\n🕐 Step 4: Clock out...")
    completed = time_service.clock_out(sarah.id)
    print(f"✅ Clocked out successfully")
    print(f"✅ Duration: {completed.duration_milliseconds / (1000 * 60):.2f} minutes")
    print(f"✅ Is active: {completed.is_active_session}")
    
    # Test 5: Check no active session
    print("\n🕐 Step 5: Verify no active session...")
    active = time_service.get_active_session(sarah.id)
    if not active:
        print("✅ No active session (correctly clocked out)")
    else:
        print("❌ Still has active session")
    
    # Test 6: Check persisted data
    print("\n🕐 Step 6: Check persisted data...")
    with open("mock-db/time_tracking.json", "r") as f:
        data = json.load(f)
    
    print(f"✅ Found {len(data)} entries in JSON")
    if data:
        entry = data[0]
        print(f"✅ Employee: {entry['employeeId']}")
        print(f"✅ Project: {entry['projectId']}")
        print(f"✅ Start: {entry['start']}")
        print(f"✅ End: {entry['end']}")
        print(f"✅ Completed: {entry['end'] != 0}")
    
    print()


def test_multiple_employees():
    """Test multiple employees can work simultaneously"""
    print("🧪 Testing multiple employees...")
    
    # Clear data
    with open("mock-db/time_tracking.json", "w") as f:
        json.dump([], f)
    
    data_manager = MockDataManager()
    time_service = TimeTrackingService(data_manager)
    
    # Clock in Sarah and Michael
    sarah_entry = time_service.clock_in("emp_001_sarah_johnson")
    michael_entry = time_service.clock_in("emp_002_michael_chen")
    
    print(f"✅ Sarah clocked in to: {sarah_entry.projectId}")
    print(f"✅ Michael clocked in to: {michael_entry.projectId}")
    
    # Check both have active sessions
    sarah_active = time_service.get_active_session("emp_001_sarah_johnson")
    michael_active = time_service.get_active_session("emp_002_michael_chen")
    
    print(f"✅ Sarah active: {sarah_active is not None}")
    print(f"✅ Michael active: {michael_active is not None}")
    
    # Clock out Sarah only
    time_service.clock_out("emp_001_sarah_johnson")
    
    # Check states
    sarah_active = time_service.get_active_session("emp_001_sarah_johnson")
    michael_active = time_service.get_active_session("emp_002_michael_chen")
    
    print(f"✅ Sarah active after clock out: {sarah_active is not None}")
    print(f"✅ Michael still active: {michael_active is not None}")
    
    # Clock out Michael
    time_service.clock_out("emp_002_michael_chen")
    michael_active = time_service.get_active_session("emp_002_michael_chen")
    print(f"✅ Michael active after clock out: {michael_active is not None}")
    
    print()


def main():
    """Run clean workflow tests"""
    print("🚀 Running clean workflow tests\n")
    
    test_clean_workflow()
    test_multiple_employees()
    
    print("✅ All clean workflow tests completed!")


if __name__ == "__main__":
    main() 