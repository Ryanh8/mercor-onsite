"""
HTML dashboard for the time tracking application
"""

from ..services.data_manager import MockDataManager


def generate_dashboard_html() -> str:
    """Generate the HTML dashboard for contractors"""
    # Load employees for dropdown
    data_manager = MockDataManager()
    employees = data_manager.load_employees()
    active_employees = [emp for emp in employees if emp.is_active]
    
    employee_options = ""
    for emp in active_employees:
        employee_options += f'<option value="{emp.id}">{emp.name} ({emp.email})</option>'
    
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Contractor Time Tracker</title>
        <style>
            body {{ font-family: Arial, sans-serif; max-width: 1000px; margin: 0 auto; padding: 20px; }}
            .card {{ border: 1px solid #ddd; border-radius: 8px; padding: 20px; margin: 10px 0; }}
            .btn {{ background: #007bff; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; margin: 5px; }}
            .btn:hover {{ background: #0056b3; }}
            .btn.danger {{ background: #dc3545; }}
            .btn.danger:hover {{ background: #c82333; }}
            .btn.success {{ background: #28a745; }}
            .btn.success:hover {{ background: #218838; }}
            .status {{ padding: 10px; border-radius: 4px; margin: 10px 0; }}
            .status.active {{ background: #d4edda; color: #155724; }}
            .status.inactive {{ background: #f8d7da; color: #721c24; }}
            .form-group {{ margin: 10px 0; }}
            .form-group label {{ display: block; margin-bottom: 5px; }}
            .form-group select, .form-group input {{ width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px; }}
            .employee-info {{ background: #f8f9fa; padding: 15px; border-radius: 8px; margin: 10px 0; }}
            .project-list {{ background: #e7f3ff; padding: 15px; border-radius: 8px; margin: 10px 0; }}
            .time-entry {{ background: #fff3cd; padding: 10px; border-radius: 4px; margin: 5px 0; }}
        </style>
    </head>
    <body>
        <h1>🕐 Contractor Time Tracker v2.0</h1>
        <p>Integrated with Mock Data - Compatible with Insightful.io API</p>
        
        <div class="card">
            <h3>Employee Time Tracking</h3>
            <div class="form-group">
                <label>Select Employee:</label>
                <select id="employeeId" onchange="loadEmployeeInfo()">
                    <option value="">-- Select Employee --</option>
                    {employee_options}
                </select>
            </div>
            
            <div id="employeeInfo" style="display: none;">
                <div class="employee-info">
                    <h4>Employee Information</h4>
                    <div id="employeeDetails"></div>
                </div>
                
                <div class="project-list">
                    <h4>Assigned Projects</h4>
                    <div id="projectList"></div>
                    <div class="form-group">
                        <label>Select Project for Time Tracking:</label>
                        <select id="projectId">
                            <option value="">-- Select Project --</option>
                        </select>
                    </div>
                </div>
                
                <div id="timeTrackingControls">
                    <button class="btn success" onclick="clockIn()">🟢 Clock In</button>
                    <button class="btn danger" onclick="clockOut()">🔴 Clock Out</button>
                    <button class="btn" onclick="checkActiveSession()">📊 Check Active Session</button>
                </div>
                
                <div id="status"></div>
                <div id="activeSession"></div>
            </div>
        </div>
        
        <div class="card">
            <h3>Recent Time Entries</h3>
            <button class="btn" onclick="loadTimeEntries()">🔄 Refresh Time Entries</button>
            <div id="timeEntries"></div>
        </div>
        
        <div class="card">
            <h3>System Information</h3>
            <button class="btn" onclick="getSystemInfo()">Get System Info</button>
            <div id="systemInfo"></div>
        </div>
        
        <script>
            let currentEmployee = null;
            let employeeProjects = [];
            
            async function loadEmployeeInfo() {{
                const employeeId = document.getElementById('employeeId').value;
                if (!employeeId) {{
                    document.getElementById('employeeInfo').style.display = 'none';
                    return;
                }}
                
                try {{
                    const response = await fetch(`/api/employees/${{employeeId}}`);
                    const employee = await response.json();
                    currentEmployee = employee;
                    
                    document.getElementById('employeeDetails').innerHTML = `
                        <strong>${{employee.name}}</strong><br>
                        Email: ${{employee.email}}<br>
                        Team: ${{employee.team_id || 'No team assigned'}}<br>
                        Status: ${{employee.deactivated === 0 ? '✅ Active' : '❌ Inactive'}}
                    `;
                    
                    // Load employee projects
                    const projectsResponse = await fetch(`/api/employees/${{employeeId}}/projects`);
                    employeeProjects = await projectsResponse.json();
                    
                    let projectListHtml = '';
                    let projectOptions = '<option value="">-- Select Project --</option>';
                    
                    employeeProjects.forEach(project => {{
                        projectListHtml += `
                            <div class="time-entry">
                                <strong>${{project.name}}</strong> - ${{project.billable ? 'Billable' : 'Non-billable'}}<br>
                                Rate: $${{project.payroll.billRate}}/hour
                            </div>
                        `;
                        projectOptions += `<option value="${{project.id}}">${{project.name}}</option>`;
                    }});
                    
                    document.getElementById('projectList').innerHTML = projectListHtml;
                    document.getElementById('projectId').innerHTML = projectOptions;
                    document.getElementById('employeeInfo').style.display = 'block';
                    
                    // Check for active session
                    checkActiveSession();
                    
                }} catch (error) {{
                    document.getElementById('status').innerHTML = 
                        '<div class="status inactive">❌ Error loading employee: ' + error.message + '</div>';
                }}
            }}
            
            async function clockIn() {{
                const employeeId = document.getElementById('employeeId').value;
                const projectId = document.getElementById('projectId').value;
                
                if (!employeeId) {{
                    alert('Please select an employee');
                    return;
                }}
                
                try {{
                    const response = await fetch('/api/clock-in', {{
                        method: 'POST',
                        headers: {{ 'Content-Type': 'application/json' }},
                        body: JSON.stringify({{ 
                            employee_id: employeeId,
                            project_id: projectId || null
                        }})
                    }});
                    const data = await response.json();
                    
                    if (response.ok) {{
                        document.getElementById('status').innerHTML = 
                            '<div class="status active">✅ Clocked in successfully!<br>' +
                            'Project: ' + data.projectId + '<br>' +
                            'Task: ' + data.taskId + '<br>' +
                            'Start Time: ' + new Date(data.start).toLocaleString() + '</div>';
                        checkActiveSession();
                    }} else {{
                        document.getElementById('status').innerHTML = 
                            '<div class="status inactive">❌ ' + data.detail + '</div>';
                    }}
                }} catch (error) {{
                    document.getElementById('status').innerHTML = 
                        '<div class="status inactive">❌ Error: ' + error.message + '</div>';
                }}
            }}
            
            async function clockOut() {{
                const employeeId = document.getElementById('employeeId').value;
                
                if (!employeeId) {{
                    alert('Please select an employee');
                    return;
                }}
                
                try {{
                    const response = await fetch('/api/clock-out', {{
                        method: 'POST',
                        headers: {{ 'Content-Type': 'application/json' }},
                        body: JSON.stringify({{ employee_id: employeeId }})
                    }});
                    const data = await response.json();
                    
                    if (response.ok) {{
                        const duration = (data.end - data.start) / 1000 / 60; // minutes
                        const hours = Math.floor(duration / 60);
                        const minutes = Math.floor(duration % 60);
                        
                        document.getElementById('status').innerHTML = 
                            '<div class="status inactive">🔴 Clocked out successfully!<br>' +
                            'Duration: ' + hours + 'h ' + minutes + 'm<br>' +
                            'End Time: ' + new Date(data.end).toLocaleString() + '</div>';
                        checkActiveSession();
                        loadTimeEntries();
                    }} else {{
                        document.getElementById('status').innerHTML = 
                            '<div class="status inactive">❌ ' + data.detail + '</div>';
                    }}
                }} catch (error) {{
                    document.getElementById('status').innerHTML = 
                        '<div class="status inactive">❌ Error: ' + error.message + '</div>';
                }}
            }}
            
            async function checkActiveSession() {{
                const employeeId = document.getElementById('employeeId').value;
                if (!employeeId) return;
                
                try {{
                    const response = await fetch(`/api/employees/${{employeeId}}/active-session`);
                    if (response.ok) {{
                        const session = await response.json();
                        if (session) {{
                            const startTime = new Date(session.start);
                            const now = new Date();
                            const duration = (now - startTime) / 1000 / 60; // minutes
                            const hours = Math.floor(duration / 60);
                            const minutes = Math.floor(duration % 60);
                            
                            document.getElementById('activeSession').innerHTML = 
                                '<div class="status active">🟢 Currently Clocked In<br>' +
                                'Project: ' + session.projectId + '<br>' +
                                'Task: ' + session.taskId + '<br>' +
                                'Started: ' + startTime.toLocaleString() + '<br>' +
                                'Duration: ' + hours + 'h ' + minutes + 'm</div>';
                        }} else {{
                            document.getElementById('activeSession').innerHTML = 
                                '<div class="status inactive">⚪ Not currently clocked in</div>';
                        }}
                    }}
                }} catch (error) {{
                    console.log('No active session');
                }}
            }}
            
            async function loadTimeEntries() {{
                try {{
                    const response = await fetch('/api/time-tracking');
                    const entries = await response.json();
                    
                    let html = '';
                    entries.slice(0, 10).forEach(entry => {{
                        const startTime = new Date(entry.start);
                        const endTime = entry.end ? new Date(entry.end) : null;
                        const duration = endTime ? (endTime - startTime) / 1000 / 60 : 0;
                        const hours = Math.floor(duration / 60);
                        const minutes = Math.floor(duration % 60);
                        
                        html += `
                            <div class="time-entry">
                                <strong>${{entry.employeeId || 'Unknown'}}</strong> - ${{entry.projectId || 'No project'}}<br>
                                Start: ${{startTime.toLocaleString()}}<br>
                                ${{endTime ? 'End: ' + endTime.toLocaleString() + '<br>Duration: ' + hours + 'h ' + minutes + 'm' : 'Currently Active'}}
                            </div>
                        `;
                    }});
                    
                    document.getElementById('timeEntries').innerHTML = html || '<p>No time entries found</p>';
                }} catch (error) {{
                    document.getElementById('timeEntries').innerHTML = 
                        '<div class="status inactive">❌ Error loading time entries</div>';
                }}
            }}
            
            async function getSystemInfo() {{
                try {{
                    const response = await fetch('/api/system-info');
                    const data = await response.json();
                    
                    document.getElementById('systemInfo').innerHTML = 
                        '<pre>' + JSON.stringify(data, null, 2) + '</pre>';
                }} catch (error) {{
                    document.getElementById('systemInfo').innerHTML = 
                        '<div class="status inactive">❌ Error: ' + error.message + '</div>';
                }}
            }}
            
            // Load time entries on page load
            loadTimeEntries();
        </script>
    </body>
    </html>
    """ 