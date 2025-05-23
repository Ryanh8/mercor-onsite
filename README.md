# Contractor Time Tracker

A local application that allows active contractors to clock in and clock out with automatic screenshot capture and system monitoring. Built to be compatible with [Insightful.io](https://developers.insightful.io/) API structure.

## 🚀 Features

### Core Time Tracking
- **Clock In/Out**: Simple one-click time tracking for contractors
- **Automatic Time Calculation**: Precise work duration tracking
- **Real-time Status**: Live dashboard showing current work status

### Screenshot Capture
- **Automatic Screenshots**: Captures screenshots during clock in/out events
- **Secure Storage**: Screenshots stored locally with organized file structure
- **API Access**: Screenshots accessible via REST API endpoints

### System Monitoring
- **IP & MAC Address Collection**: Automatic network information gathering
- **System Metrics**: CPU, memory, and disk usage monitoring
- **OS Information**: Operating system and hardware details

### Insightful.io Compatibility
- **API Structure**: Data models compatible with Insightful.io format
- **Attendance Reports**: Generate reports in Insightful.io format
- **User Management**: Contractor profiles matching Insightful.io structure

## 📋 Requirements

- Python 3.9+
- Operating System: Windows, macOS, or Linux
- Screen capture permissions (for screenshots)
- Network access (for system monitoring)

## 🛠️ Installation

1. **Clone or download the project**
   ```bash
   cd /path/to/project
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python main.py
   ```

4. **Access the dashboard**
   - Open your browser to: http://localhost:8000
   - API documentation: http://localhost:8000/docs

## 💻 Usage

### Web Dashboard

1. **Register a New Contractor**
   - Enter name and email
   - System automatically generates unique contractor ID
   - Records system information

2. **Clock In**
   - Enter contractor ID
   - Click "Clock In" button
   - Screenshot automatically captured
   - System information recorded

3. **Clock Out**
   - Enter contractor ID
   - Click "Clock Out" button
   - Final screenshot captured
   - Work duration calculated

### API Endpoints

#### Contractor Management
```http
POST /api/contractors
GET /api/contractors
```

#### Time Tracking
```http
POST /api/clock-in
POST /api/clock-out
```

#### Reports & Monitoring
```http
GET /api/attendance-report/{contractor_id}?from_date=2024-01-01&to_date=2024-01-31
GET /api/system-info
```

### Example API Usage

**Register Contractor:**
```bash
curl -X POST "http://localhost:8000/api/contractors" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com"
  }'
```

**Clock In:**
```bash
curl -X POST "http://localhost:8000/api/clock-in" \
  -H "Content-Type: application/json" \
  -d '{
    "contractor_id": "your-contractor-id"
  }'
```

**Clock Out:**
```bash
curl -X POST "http://localhost:8000/api/clock-out" \
  -H "Content-Type: application/json" \
  -d '{
    "contractor_id": "your-contractor-id"
  }'
```

## 📊 Data Structure

### Contractor Profile (Insightful.io Compatible)
```json
{
  "id": "uuid",
  "name": "John Doe",
  "email": "john@example.com",
  "active": true,
  "phone": "+1234567890",
  "team_id": "team-uuid",
  "team_name": "Development Team",
  "user_type": "contractor",
  "role": "contractor",
  "time_zone": "UTC",
  "app_and_os": "Darwin 24.1.0"
}
```

### Time Entry
```json
{
  "id": "uuid",
  "contractor_id": "contractor-uuid",
  "clock_in": "2024-01-15T09:00:00Z",
  "clock_out": "2024-01-15T17:00:00Z",
  "time_at_work": "08h 00m",
  "productive_time": "07h 30m",
  "idle_time": "00h 30m",
  "activity_percentage": 85.5,
  "screenshots": ["path/to/screenshot1.png"],
  "system_info": {
    "ip_address": "192.168.1.100",
    "mac_address": "00:11:22:33:44:55",
    "hostname": "contractor-laptop",
    "os_info": "Darwin 24.1.0",
    "cpu_usage": 25.5,
    "memory_usage": 60.2,
    "disk_usage": 45.8
  }
}
```

### Attendance Report (Insightful.io Format)
```json
[
  {
    "contractor_id": "uuid",
    "name": "John Doe",
    "email": "john@example.com",
    "team_name": "Development Team",
    "clock_in": "09:00 AM",
    "clock_out": "05:00 PM",
    "time_at_work": "08h 00m",
    "productive_time": "07h 30m",
    "idle_time": "00h 30m",
    "activity_percentage": 85,
    "date": "2024-01-15"
  }
]
```

## 🗄️ Database Schema

The application uses SQLite with the following tables:

- **contractors**: Contractor profiles and information
- **time_entries**: Clock in/out records and work sessions
- **screenshots**: Screenshot metadata and file paths

## 📁 File Structure

```
project/
├── main.py                 # Main application file
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── contractor_tracker.db  # SQLite database (created automatically)
└── screenshots/           # Screenshot storage (created automatically)
    ├── contractor1_entry1_20240115_090000.png
    └── contractor1_entry1_20240115_170000.png
```

## 🔒 Security Features

- **Local Data Storage**: All data stored locally, no external transmission
- **Unique IDs**: UUID-based identification for all entities
- **Input Validation**: Pydantic models ensure data integrity
- **Error Handling**: Comprehensive error handling and logging

## 🔧 Configuration

The application can be configured by modifying variables in `main.py`:

- **Database Path**: Change `db_path` in `DatabaseManager`
- **Screenshot Directory**: Modify `screenshots_dir` in `ScreenshotService`
- **Server Settings**: Update host/port in `uvicorn.run()`

## 🚨 Troubleshooting

### Common Issues

1. **Screenshot Permission Denied**
   - Grant screen recording permissions in system settings
   - On macOS: System Preferences > Security & Privacy > Screen Recording

2. **Database Locked Error**
   - Ensure only one instance of the application is running
   - Check file permissions on the database file

3. **Port Already in Use**
   - Change the port in `main.py` or stop other services using port 8000

### Logs and Debugging

- Check console output for error messages
- Database errors are logged with full stack traces
- Screenshot failures are logged but don't stop the application

## 🔗 Insightful.io Integration

This application is designed to be compatible with Insightful.io's API structure:

- **Data Models**: Match Insightful.io user and time entry formats
- **Attendance Reports**: Generate reports in Insightful.io format
- **System Information**: Collect data similar to Insightful.io monitoring

For full integration with Insightful.io, you would need to:
1. Obtain API credentials from Insightful.io
2. Implement API client to sync data
3. Configure webhook endpoints for real-time updates

## 📝 License

This project is for educational and demonstration purposes. Please ensure compliance with local labor laws and privacy regulations when tracking employee time and capturing screenshots.

## 🤝 Contributing

This is a demonstration project for a take-home assignment. For production use, consider:

- Adding authentication and authorization
- Implementing data encryption
- Adding comprehensive logging
- Creating automated tests
- Implementing data backup and recovery
- Adding configuration management
