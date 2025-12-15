# Lottery System Backend

## Overview
Express.js backend API for the lottery system with SQLite database.

## Features
- User authentication (register/login) with JWT
- Items management (lottery types)
- Betting functionality
- Order management with status transitions
- Simulated payment processing
- Order logging for audit trail

## Prerequisites
- Node.js (v14 or higher)
- npm

## Installation

```bash
cd backend
npm install
```

## Configuration

Set the following environment variables:

- `JWT_SECRET`: Secret key for JWT token signing (required in production)
- `ADMIN_KEY`: Key for admin operations (required in production)
- `PORT`: Server port (default: 3000)

Example:
```bash
export JWT_SECRET="your-secure-jwt-secret"
export ADMIN_KEY="your-secure-admin-key"
export PORT=3000
```

**⚠️ Security Note:** Never commit secrets to the repository. Always use environment variables for sensitive data.

## Running the Server

Development mode:
```bash
npm run dev
```

Production mode:
```bash
npm start
```

The server will start on `http://localhost:3000` (or the port specified in PORT environment variable).

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register a new user
- `POST /api/auth/login` - Login and get JWT token
- `GET /api/auth/me` - Get current user info (requires auth)

### Items
- `GET /api/items` - List all active items (requires auth)
- `GET /api/items/:id` - Get item details (requires auth)
- `POST /api/items` - Create item (requires auth + admin key)
- `PUT /api/items/:id` - Update item (requires auth + admin key)

### Bets
- `POST /api/bets` - Place a bet (creates order + bet) (requires auth)

### Orders
- `GET /api/orders` - List user's orders (requires auth)
- `GET /api/orders/:id` - Get order details with bets (requires auth)
- `POST /api/orders/:id/pay` - Pay for order (simulated payment) (requires auth)
- `POST /api/orders/:id/cancel` - Cancel order (requires auth)
- `POST /api/orders/:id/transition` - Transition order status (requires auth)
- `POST /api/orders/:id/admin_transition` - Admin transition (requires auth + admin key)
- `GET /api/orders/:id/logs` - Get order transition logs (requires auth)

## Order Status Flow

```
pending -> paid -> issued -> completed
   |         |        |
   +-----> cancelled <+
```

- **pending**: Order created, awaiting payment
- **paid**: Payment received (simulated), automatically transitions to issued after 2 seconds
- **issued**: Order issued to user
- **completed**: Order fulfilled
- **cancelled**: Order cancelled

## Database Schema

The system uses SQLite with the following tables:
- `users`: User accounts
- `items`: Lottery items/types
- `orders`: User orders
- `bets`: Bet details linked to orders
- `order_logs`: Audit log of order status transitions

## Payment Simulation

The payment endpoint (`POST /api/orders/:id/pay`) simulates an async payment flow:
1. Immediately transitions order from `pending` to `paid`
2. After 2 seconds, automatically transitions to `issued`
3. All transitions are logged in `order_logs`

**Note:** This is a prototype simulation. In production, integrate with a real payment gateway.

## Security Considerations

- JWT tokens expire after 24 hours
- Passwords are hashed using bcrypt
- Admin operations require an admin key in the `X-Admin-Key` header
- CORS is enabled for all origins (configure appropriately in production)
- **Production checklist:**
  - Set strong JWT_SECRET
  - Set strong ADMIN_KEY
  - Configure CORS for specific origins
  - Use HTTPS
  - Implement rate limiting
  - Add request validation
  - Set up proper logging and monitoring
