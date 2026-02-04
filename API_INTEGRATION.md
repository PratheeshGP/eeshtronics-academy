# Eeshtronics Academy - API Integration Guide

## Backend API Connection

The frontend is configured to connect to: `http://localhost:8000/api/`

## Authentication Flow

### 1. Register
```javascript
// POST /api/auth/register/
{
  "username": "testuser",
  "email": "test@example.com",
  "password": "SecurePass123",
  "password2": "SecurePass123"
}

// Response:
{
  "user": {
    "id": 1,
    "username": "testuser",
    "email": "test@example.com",
    "level": 1,
    "xp_points": 0,
    "ether_balance": "100.00"
  },
  "tokens": {
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
  }
}
```

### 2. Login
```javascript
// POST /api/auth/login/
{
  "username": "testuser",
  "password": "SecurePass123"
}

// Same response as register
```

### 3. Get Profile
```javascript
// GET /api/auth/profile/
// Headers: Authorization: Bearer <access_token>

// Response:
{
  "id": 1,
  "username": "testuser",
  "email": "test@example.com",
  "xp_points": 150,
  "level": 2,
  "ether_balance": "250.00",
  "streak_count": 5,
  "clan": null
}
```

## Security Features Implemented

✅ **Password Hashing**
- Django uses PBKDF2 algorithm with SHA256
- Automatically hashed on registration
- Never stored as plain text

✅ **JWT Tokens**
- Access token: 1 hour expiry
- Refresh token: 7 days expiry
- Stored in localStorage

✅ **Protected Routes**
- Frontend checks authentication
- Backend validates JWT on every request

✅ **CORS**
- Configured for localhost:5173
- UPDATE for production domain

## Frontend Auth Integration

All handled in `src/contexts/AuthContext.tsx`:
- `login()` - authenticates user
- `register()` - creates new account
- `logout()` - clears tokens
- `user` - current user object
- `token` - JWT access token

Usage in components:
```tsx
import { useAuth } from '../contexts/AuthContext';

function MyComponent() {
  const { user, logout } = useAuth();
  
  return (
    <div>
      <h1>Welcome {user?.username}</h1>
      <button onClick={logout}>Logout</button>
    </div>
  );
}
```

## Password Storage - Google/Microsoft OAuth

**Current**: Users stored in PostgreSQL database

**For Cloud Storage**:
1. Google: Use Firebase Authentication
2. Microsoft: Use Azure AD B2C
3. Both: Implement social auth in Django

These require API keys and configuration (see startup_guide.md).
