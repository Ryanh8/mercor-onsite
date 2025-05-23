#!/usr/bin/env python3
"""
Test checking current active status for employees
"""

from src.services.data_manager import MockDataManager
from src.services.time_tracking_service import TimeTrackingService


def check_all_active_status():
    """Check active status for all employees"""
    print("📊 Current Active Status for All Employees:")
    
    data_manager = MockDataManager()
    time_service = TimeTrackingService(data_manager)
    employees = data_manager.load_employees()
    
    active_count = 0
    for emp in employees:
        if emp.is_active:
            active_session = time_service.get_active_session(emp.id)
            if active_session:
                duration_hours = active_session.current_duration_milliseconds / (1000 * 60 * 60)
                print(f"  🟢 {emp.name}: ACTIVE - {duration_hours:.2f}h on {active_session.projectId}")
                active_count += 1
            else:
                print(f"  ⚪ {emp.name}: Not clocked in")
    
    print(f"\n📈 Summary: {active_count} employees currently active")


def check_specific_employee(employee_id: str):
    """Check active status for a specific employee"""
    print(f"\n🔍 Checking status for employee: {employee_id}")
    
    data_manager = MockDataManager()
    time_service = TimeTrackingService(data_manager)
    
    employee = data_manager.get_employee_by_id(employee_id)
    if not employee:
        print(f"  ❌ Employee {employee_id} not found")
        return
    
    active_session = time_service.get_active_session(employee_id)
    if active_session:
        duration_hours = active_session.current_duration_milliseconds / (1000 * 60 * 60)
        print(f"  🟢 {employee.name} is ACTIVE")
        print(f"  📊 Duration: {duration_hours:.2f} hours")
        print(f"  📁 Project: {active_session.projectId}")
        print(f"  📋 Task: {active_session.taskId}")
        print(f"  🕐 Started: {active_session.start}")
    else:
        print(f"  ⚪ {employee.name} is not currently clocked in")


if __name__ == "__main__":
    check_all_active_status()
    check_specific_employee("emp_001_sarah_johnson")
    check_specific_employee("emp_002_michael_chen") 