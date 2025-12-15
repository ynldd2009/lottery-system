# Lottery System Frontend

## Overview
Flutter frontend application for the lottery system with authentication, betting, and order management.

## Features
- User authentication (login/register)
- Browse lottery items
- Place bets with custom numbers
- View and manage orders
- Real-time order status tracking
- Order history logs

## Prerequisites
- Flutter SDK (3.0.0 or higher)
- Dart SDK
- Android Studio or Xcode (for mobile development)
- Running backend server

## Installation

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
flutter pub get
```

## Configuration

### Backend URL
The app is configured to connect to the backend server. Update the `baseUrl` in `lib/services/api_service.dart` based on your platform:

- **Android Emulator**: `http://10.0.2.2:3000/api` (default)
- **iOS Simulator**: `http://localhost:3000/api`
- **Desktop/Web**: `http://localhost:3000/api`
- **Physical Device**: `http://YOUR_MACHINE_IP:3000/api`

## Running the App

### Android Emulator
```bash
flutter run
```

### iOS Simulator
```bash
flutter run -d ios
```

### Desktop
```bash
flutter run -d macos   # For macOS
flutter run -d windows # For Windows
flutter run -d linux   # For Linux
```

### Web
```bash
flutter run -d chrome
```

## Development

### Code Analysis
```bash
flutter analyze
```

### Format Code
```bash
flutter format lib/
```

## Project Structure

```
frontend/
├── lib/
│   ├── main.dart                    # App entry point and routes
│   ├── services/
│   │   └── api_service.dart         # API client for backend communication
│   └── pages/
│       ├── login_page.dart          # Login and registration
│       ├── items_page.dart          # Browse lottery items
│       ├── bet_page.dart            # Place bets
│       ├── orders_page.dart         # View orders list
│       └── order_detail_page.dart   # Order details and actions
├── pubspec.yaml                     # Dependencies and configuration
└── README.md                        # This file
```

## Features by Page

### Login Page
- User login with username and password
- User registration
- Auto-redirect to items page after successful authentication

### Items Page
- Display all available lottery items
- Navigate to bet page for each item
- Access orders page via header button

### Bet Page
- Input lottery numbers (comma-separated)
- Set stake amount
- Submit bet (creates order)

### Orders Page
- List all user orders
- Display order status with color coding
- Navigate to order details

### Order Detail Page
- View order information and bets
- Pay for pending orders (simulated payment)
- Cancel orders (if allowed by status)
- View order history and status transitions

## Order Status Flow

```
pending → paid → issued → completed
   |        |       |
   +---> cancelled <+
```

- **pending**: Order awaiting payment
- **paid**: Payment processed (auto-transitions to issued)
- **issued**: Order issued to user
- **completed**: Order fulfilled
- **cancelled**: Order cancelled

## API Integration

The app communicates with the backend API using JWT authentication. All requests (except login/register) require a valid token stored in SharedPreferences.

### Error Handling
- Network errors display snackbar messages
- Invalid tokens automatically redirect to login
- Validation errors shown in forms

## Testing

Run tests with:
```bash
flutter test
```

## Building for Production

### Android APK
```bash
flutter build apk --release
```

### Android App Bundle
```bash
flutter build appbundle --release
```

### iOS
```bash
flutter build ios --release
```

**Note**: For production builds, ensure:
- Backend URL is correctly configured
- SSL/TLS is enabled for API calls
- App signing is properly configured
- Proper error handling and logging

## Troubleshooting

### Cannot connect to backend
- Verify backend server is running
- Check `baseUrl` in `api_service.dart` matches your setup
- For Android emulator, use `10.0.2.2` instead of `localhost`
- For physical devices, use your machine's IP address

### Build errors
- Run `flutter clean` then `flutter pub get`
- Ensure Flutter SDK is up to date: `flutter upgrade`
- Check for dependency conflicts in `pubspec.yaml`

## Security Notes
- JWT tokens are stored in SharedPreferences
- Passwords are transmitted securely to backend (ensure HTTPS in production)
- No sensitive data is logged or exposed
- In production, implement certificate pinning and additional security measures

## Future Enhancements
- Offline support with local caching
- Push notifications for order status updates
- Biometric authentication
- Multi-language support
- Dark mode
