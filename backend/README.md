# EngineerLab Backend

Production-ready Django backend for the EngineerLab mission-based engineering learning platform with real-time Docker sandbox execution, WebSocket terminal streaming, and gamified progression system.

## 🏗 Architecture

- **Framework**: Django 4.2 + Django REST Framework
- **Real-time**: Django Channels (WebSockets)
- **Database**: PostgreSQL 15
- **Cache & Queue**: Redis
- **Task Queue**: Celery
- **Container Engine**: Docker SDK for Python
- **Authentication**: JWT (djangorestframework-simplejwt)

## 📂 Project Structure

```
backend/
├── config/                 # Django project settings
│   ├── settings.py        # Main settings
│   ├── urls.py            # URL routing
│   ├── asgi.py            # ASGI config for WebSockets
│   └── celery.py          # Celery configuration
├── apps/
│   ├── users/             # Authentication & user profiles
│   ├── paths/             # Learning paths
│   ├── modules/           # Learning modules
│   ├── missions/          # Missions & exercises
│   ├── labs/              # Lab definitions & sessions
│   ├── sandbox/           # Docker executor & Celery tasks
│   ├── realtime/          # WebSocket consumers
│   ├── progress/          # Progress tracking & achievements
│   ├── economy/           # Ether currency system
│   └── core/              # Shared utilities
├── docker-compose.yml     # Local development setup
├── Dockerfile             # Backend container
├── requirements.txt       # Python dependencies
└── manage.py              # Django CLI
```

## 🚀 Quick Start

### Prerequisites

- Docker & Docker Compose installed
- Git

### 1. Clone and Setup

```bash
git clone <repository>
cd antigravity/backend

# Copy environment variables
cp .env.example .env

# Edit .env with your settings (optional for local dev)
```

### 2. Start Services

```bash
# Build and start all services
docker-compose up --build

# Run in detached mode
docker-compose up -d
```

This starts:
- **PostgreSQL** on `localhost:5432`
- **Redis** on `localhost:6379`
- **Django API** on `http://localhost:8000`
- **Celery Worker** (async tasks)
- **Celery Beat** (periodic tasks)

### 3. Create Superuser

```bash
docker-compose exec backend python manage.py createsuperuser
```

### 4. Access Admin Panel

Navigate to `http://localhost:8000/admin` and login with superuser credentials.

## 📡 API Endpoints

### Authentication

```
POST /api/auth/register          # Register new user
POST /api/auth/login             # Login (returns JWT tokens)
GET  /api/auth/profile           # Get user profile
PUT  /api/auth/profile           # Update profile
POST /api/auth/token/refresh     # Refresh JWT token
```

### Learning Content

```
GET  /api/paths                  # List learning paths
GET  /api/paths/{slug}           # Get path details
POST /api/paths/{id}/enroll      # Enroll in path

GET  /api/modules                # List modules
GET  /api/modules/{slug}         # Get module details
POST /api/modules/{id}/unlock    # Unlock module (costs Ether)

GET  /api/missions               # List missions
GET  /api/missions/{slug}        # Get mission details
POST /api/missions/artifacts/submit  # Submit artifact
```

### Labs & Sandbox

```
GET  /api/labs                   # List available labs
GET  /api/labs/{id}              # Get lab details
POST /api/labs/start             # Start a lab session
POST /api/labs/{id}/stop         # Stop lab session
GET  /api/labs/{id}/status       # Get session status
GET  /api/labs/sessions          # My active sessions
```

**WebSocket**: `ws://localhost:8000/ws/lab/{session_id}/`

### Progress & Economy

```
POST /api/progress/update                # Update mission progress
POST /api/progress/mission/{id}/complete # Complete mission
GET  /api/progress/user                  # User progress summary
GET  /api/progress/achievements          # User achievements

GET  /api/ether/balance                  # Get Ether balance
GET  /api/ether/transactions             # Transaction history
```

## 🐳 Docker Sandbox Security

The Docker executor enforces strict security:

✅ **Non-privileged containers only**  
✅ **Resource limits** (memory, CPU)  
✅ **Network disabled by default**  
✅ **Command filtering** (blocks dangerous commands)  
✅ **Auto-cleanup** after timeout  
✅ **Session isolation per user**

## 🔥 Celery Tasks

Async tasks for performance:

- `launch_lab_container_task` - Start Docker container
- `terminate_lab_container_task` - Stop container
- `cleanup_expired_containers_task` - Periodic cleanup (Celery Beat)
- `validate_artifact_task` - Validate mission submissions

## 🧪 Testing the System

### 1. Register a User

```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","email":"test@example.com","password":"securepass123","password2":"securepass123"}'
```

### 2. Login

```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"securepass123"}'
```

Save the `access` token.

### 3. Start a Lab

```bash
curl -X POST http://localhost:8000/api/labs/start \
  -H "Authorization: Bearer <your_token>" \
  -H "Content-Type: application/json" \
  -d '{"lab_id":1}'
```

### 4. Connect via WebSocket

```javascript
const ws = new WebSocket('ws://localhost:8000/ws/lab/1/');

ws.onmessage = (event) => {
  console.log(JSON.parse(event.data));
};

// Execute command
ws.send(JSON.stringify({
  command: 'ls -la'
}));
```

## 🌐 Frontend Integration

The frontend at `http://localhost:5173` should connect to:

- **REST API**: `http://localhost:8000/api/`
- **WebSocket**: `ws://localhost:8000/ws/`

CORS is configured for `localhost:5173` by default.

## 🛠 Development

### Run Migrations

```bash
docker-compose exec backend python manage.py makemigrations
docker-compose exec backend python manage.py migrate
```

### Create Test Data

```bash
docker-compose exec backend python manage.py shell
```

```python
from apps.paths.models import Path
from apps.labs.models import Lab

# Create a learning path
path = Path.objects.create(
    title="Digital Electronics Fundamentals",
    slug="digital-electronics",
    description="Learn the basics of digital logic and electronics",
    difficulty="BEGINNER",
    estimated_hours=40
)

# Create a lab
lab = Lab.objects.create(
    name="Ubuntu Terminal Lab",
    slug="ubuntu-terminal",
    description="Basic Linux terminal environment",
    lab_type="LINUX",
    docker_image="ubuntu:22.04",
    memory_limit="512m",
    timeout_seconds=3600
)
```

### View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f celery_worker
```

### Stop Services

```bash
docker-compose down

# Remove volumes (clears database)
docker-compose down -v
```

## 📊 Database Schema

Key models:
- **User**: Custom user with XP, Level, Ether
- **Path → Module → Mission → Exercise**: Learning hierarchy
- **Lab / LabSession**: Container definitions and active sessions
- **MissionProgress / UserStreak / Achievement**: Gamification
- **EtherTransaction**: Currency tracking

## 🔐 Security Checklist

- [x] JWT authentication
- [x] Non-privileged Docker containers
- [x] Resource limits enforced
- [x] Network isolation
- [x] Command filtering
- [x] Input sanitization
- [x] Session expiration
- [x] Container activity logging

## 🚢 Production Deployment

For production:

1. Set `DEBUG=False` in `.env`
2. Generate strong `SECRET_KEY` and `JWT_SECRET_KEY`
3. Use managed PostgreSQL (AWS RDS, Cloud SQL)
4. Use managed Redis (ElastiCache, Cloud Memorystore)
5. Deploy with Kubernetes for container orchestration
6. Use load balancer for backend API
7. Configure SSL/TLS certificates
8. Set up monitoring (Sentry, DataDog)
9. Use production WSGI server (Gunicorn) + ASGI (Daphne)

## 📝 License

MIT

## 👥 Contributors

EngineerLab Development Team
