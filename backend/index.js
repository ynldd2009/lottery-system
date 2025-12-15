const express = require('express');
const cors = require('cors');
const bodyParser = require('body-parser');
const bcrypt = require('bcrypt');
const jwt = require('jsonwebtoken');
const db = require('./db');

const app = express();
const PORT = process.env.PORT || 3000;
const JWT_SECRET = process.env.JWT_SECRET || 'your-secret-key-change-in-production';
const ADMIN_KEY = process.env.ADMIN_KEY || 'admin-key-change-in-production';

app.use(cors());
app.use(bodyParser.json());

// Middleware to verify JWT token
const authenticateToken = (req, res, next) => {
  const authHeader = req.headers['authorization'];
  const token = authHeader && authHeader.split(' ')[1];

  if (!token) {
    return res.status(401).json({ error: 'Access token required' });
  }

  jwt.verify(token, JWT_SECRET, (err, user) => {
    if (err) {
      return res.status(403).json({ error: 'Invalid or expired token' });
    }
    req.user = user;
    next();
  });
};

// Middleware to verify admin key
const authenticateAdmin = (req, res, next) => {
  const adminKey = req.headers['x-admin-key'];
  
  if (!adminKey || adminKey !== ADMIN_KEY) {
    return res.status(403).json({ error: 'Admin key required' });
  }
  next();
};

// Auth endpoints
app.post('/api/auth/register', async (req, res) => {
  const { username, password } = req.body;

  if (!username || !password) {
    return res.status(400).json({ error: 'Username and password required' });
  }

  try {
    const hashedPassword = await bcrypt.hash(password, 10);
    
    db.run(
      'INSERT INTO users (username, password, role) VALUES (?, ?, ?)',
      [username, hashedPassword, 'user'],
      function(err) {
        if (err) {
          if (err.message.includes('UNIQUE')) {
            return res.status(400).json({ error: 'Username already exists' });
          }
          return res.status(500).json({ error: 'Failed to create user' });
        }

        const token = jwt.sign({ id: this.lastID, username, role: 'user' }, JWT_SECRET, { expiresIn: '24h' });
        res.status(201).json({ token, user: { id: this.lastID, username, role: 'user' } });
      }
    );
  } catch (error) {
    res.status(500).json({ error: 'Server error' });
  }
});

app.post('/api/auth/login', async (req, res) => {
  const { username, password } = req.body;

  if (!username || !password) {
    return res.status(400).json({ error: 'Username and password required' });
  }

  db.get('SELECT * FROM users WHERE username = ?', [username], async (err, user) => {
    if (err) {
      return res.status(500).json({ error: 'Server error' });
    }

    if (!user) {
      return res.status(401).json({ error: 'Invalid credentials' });
    }

    const validPassword = await bcrypt.compare(password, user.password);
    if (!validPassword) {
      return res.status(401).json({ error: 'Invalid credentials' });
    }

    const token = jwt.sign({ id: user.id, username: user.username, role: user.role }, JWT_SECRET, { expiresIn: '24h' });
    res.json({ token, user: { id: user.id, username: user.username, role: user.role } });
  });
});

app.get('/api/auth/me', authenticateToken, (req, res) => {
  db.get('SELECT id, username, role, created_at FROM users WHERE id = ?', [req.user.id], (err, user) => {
    if (err || !user) {
      return res.status(404).json({ error: 'User not found' });
    }
    res.json(user);
  });
});

// Items endpoints
app.get('/api/items', authenticateToken, (req, res) => {
  db.all('SELECT * FROM items WHERE active = 1', [], (err, items) => {
    if (err) {
      return res.status(500).json({ error: 'Failed to fetch items' });
    }
    res.json(items);
  });
});

app.get('/api/items/:id', authenticateToken, (req, res) => {
  db.get('SELECT * FROM items WHERE id = ?', [req.params.id], (err, item) => {
    if (err) {
      return res.status(500).json({ error: 'Failed to fetch item' });
    }
    if (!item) {
      return res.status(404).json({ error: 'Item not found' });
    }
    res.json(item);
  });
});

app.post('/api/items', authenticateToken, authenticateAdmin, (req, res) => {
  const { name, description, price } = req.body;

  if (!name || !price) {
    return res.status(400).json({ error: 'Name and price required' });
  }

  db.run(
    'INSERT INTO items (name, description, price) VALUES (?, ?, ?)',
    [name, description, price],
    function(err) {
      if (err) {
        return res.status(500).json({ error: 'Failed to create item' });
      }
      res.status(201).json({ id: this.lastID, name, description, price, active: 1 });
    }
  );
});

app.put('/api/items/:id', authenticateToken, authenticateAdmin, (req, res) => {
  const { name, description, price, active } = req.body;

  db.run(
    'UPDATE items SET name = COALESCE(?, name), description = COALESCE(?, description), price = COALESCE(?, price), active = COALESCE(?, active) WHERE id = ?',
    [name, description, price, active, req.params.id],
    function(err) {
      if (err) {
        return res.status(500).json({ error: 'Failed to update item' });
      }
      if (this.changes === 0) {
        return res.status(404).json({ error: 'Item not found' });
      }
      res.json({ message: 'Item updated successfully' });
    }
  );
});

// Bets endpoint
app.post('/api/bets', authenticateToken, (req, res) => {
  const { item_id, numbers, stake } = req.body;

  if (!item_id || !numbers || !stake) {
    return res.status(400).json({ error: 'item_id, numbers, and stake required' });
  }

  // Validate item exists
  db.get('SELECT * FROM items WHERE id = ? AND active = 1', [item_id], (err, item) => {
    if (err) {
      return res.status(500).json({ error: 'Failed to validate item' });
    }
    if (!item) {
      return res.status(404).json({ error: 'Item not found or inactive' });
    }

    const totalAmount = stake;

    // Create order
    db.run(
      'INSERT INTO orders (user_id, total_amount, status) VALUES (?, ?, ?)',
      [req.user.id, totalAmount, 'pending'],
      function(err) {
        if (err) {
          return res.status(500).json({ error: 'Failed to create order' });
        }

        const orderId = this.lastID;

        // Create bet
        db.run(
          'INSERT INTO bets (order_id, item_id, numbers, stake) VALUES (?, ?, ?, ?)',
          [orderId, item_id, numbers, stake],
          function(err) {
            if (err) {
              return res.status(500).json({ error: 'Failed to create bet' });
            }

            // Log order creation
            db.run(
              'INSERT INTO order_logs (order_id, from_status, to_status, note) VALUES (?, ?, ?, ?)',
              [orderId, null, 'pending', 'Order created'],
              (err) => {
                if (err) console.error('Failed to log order creation:', err);
              }
            );

            res.status(201).json({
              order_id: orderId,
              bet_id: this.lastID,
              message: 'Bet placed successfully'
            });
          }
        );
      }
    );
  });
});

// Orders endpoints
app.get('/api/orders', authenticateToken, (req, res) => {
  db.all(
    'SELECT o.*, COUNT(b.id) as bet_count FROM orders o LEFT JOIN bets b ON o.id = b.order_id WHERE o.user_id = ? GROUP BY o.id ORDER BY o.created_at DESC',
    [req.user.id],
    (err, orders) => {
      if (err) {
        return res.status(500).json({ error: 'Failed to fetch orders' });
      }
      res.json(orders);
    }
  );
});

app.get('/api/orders/:id', authenticateToken, (req, res) => {
  db.get('SELECT * FROM orders WHERE id = ? AND user_id = ?', [req.params.id, req.user.id], (err, order) => {
    if (err) {
      return res.status(500).json({ error: 'Failed to fetch order' });
    }
    if (!order) {
      return res.status(404).json({ error: 'Order not found' });
    }

    // Fetch bets for this order
    db.all(
      'SELECT b.*, i.name as item_name FROM bets b JOIN items i ON b.item_id = i.id WHERE b.order_id = ?',
      [req.params.id],
      (err, bets) => {
        if (err) {
          return res.status(500).json({ error: 'Failed to fetch bets' });
        }
        res.json({ ...order, bets });
      }
    );
  });
});

// Pay order endpoint - simulates async payment processing
app.post('/api/orders/:id/pay', authenticateToken, (req, res) => {
  db.get('SELECT * FROM orders WHERE id = ? AND user_id = ?', [req.params.id, req.user.id], (err, order) => {
    if (err) {
      return res.status(500).json({ error: 'Failed to fetch order' });
    }
    if (!order) {
      return res.status(404).json({ error: 'Order not found' });
    }
    if (order.status !== 'pending') {
      return res.status(400).json({ error: 'Order cannot be paid in current status' });
    }

    // Simulate async payment - immediately transition to paid
    db.run(
      'UPDATE orders SET status = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?',
      ['paid', req.params.id],
      (err) => {
        if (err) {
          return res.status(500).json({ error: 'Failed to update order status' });
        }

        // Log transition
        db.run(
          'INSERT INTO order_logs (order_id, from_status, to_status, note) VALUES (?, ?, ?, ?)',
          [req.params.id, 'pending', 'paid', 'Payment successful (simulated)'],
          (err) => {
            if (err) console.error('Failed to log transition:', err);
          }
        );

        // Simulate async processing: after payment, automatically transition to issued
        setTimeout(() => {
          db.run(
            'UPDATE orders SET status = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?',
            ['issued', req.params.id],
            (err) => {
              if (!err) {
                db.run(
                  'INSERT INTO order_logs (order_id, from_status, to_status, note) VALUES (?, ?, ?, ?)',
                  [req.params.id, 'paid', 'issued', 'Order issued automatically'],
                  (err) => {
                    if (err) console.error('Failed to log transition:', err);
                  }
                );
              }
            }
          );
        }, 2000);

        res.json({ message: 'Payment processed successfully', status: 'paid' });
      }
    );
  });
});

// Transition order status endpoint
app.post('/api/orders/:id/transition', authenticateToken, (req, res) => {
  const { to_status, note } = req.body;

  if (!to_status) {
    return res.status(400).json({ error: 'to_status required' });
  }

  const validTransitions = {
    'pending': ['cancelled'],
    'paid': ['cancelled'],
    'issued': ['completed', 'cancelled'],
    'completed': [],
    'cancelled': []
  };

  db.get('SELECT * FROM orders WHERE id = ? AND user_id = ?', [req.params.id, req.user.id], (err, order) => {
    if (err) {
      return res.status(500).json({ error: 'Failed to fetch order' });
    }
    if (!order) {
      return res.status(404).json({ error: 'Order not found' });
    }

    const allowedStatuses = validTransitions[order.status] || [];
    if (!allowedStatuses.includes(to_status)) {
      return res.status(400).json({ error: `Cannot transition from ${order.status} to ${to_status}` });
    }

    db.run(
      'UPDATE orders SET status = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?',
      [to_status, req.params.id],
      (err) => {
        if (err) {
          return res.status(500).json({ error: 'Failed to update order status' });
        }

        // Log transition
        db.run(
          'INSERT INTO order_logs (order_id, from_status, to_status, note) VALUES (?, ?, ?, ?)',
          [req.params.id, order.status, to_status, note || 'User requested transition'],
          (err) => {
            if (err) console.error('Failed to log transition:', err);
          }
        );

        res.json({ message: 'Order status updated successfully', status: to_status });
      }
    );
  });
});

// Cancel order endpoint (convenience method)
app.post('/api/orders/:id/cancel', authenticateToken, (req, res) => {
  db.get('SELECT * FROM orders WHERE id = ? AND user_id = ?', [req.params.id, req.user.id], (err, order) => {
    if (err) {
      return res.status(500).json({ error: 'Failed to fetch order' });
    }
    if (!order) {
      return res.status(404).json({ error: 'Order not found' });
    }
    if (!['pending', 'paid', 'issued'].includes(order.status)) {
      return res.status(400).json({ error: 'Order cannot be cancelled in current status' });
    }

    db.run(
      'UPDATE orders SET status = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?',
      ['cancelled', req.params.id],
      (err) => {
        if (err) {
          return res.status(500).json({ error: 'Failed to cancel order' });
        }

        // Log transition
        db.run(
          'INSERT INTO order_logs (order_id, from_status, to_status, note) VALUES (?, ?, ?, ?)',
          [req.params.id, order.status, 'cancelled', 'Cancelled by user'],
          (err) => {
            if (err) console.error('Failed to log transition:', err);
          }
        );

        res.json({ message: 'Order cancelled successfully', status: 'cancelled' });
      }
    );
  });
});

// Admin transition endpoint
app.post('/api/orders/:id/admin_transition', authenticateToken, authenticateAdmin, (req, res) => {
  const { to_status, note } = req.body;

  if (!to_status) {
    return res.status(400).json({ error: 'to_status required' });
  }

  db.get('SELECT * FROM orders WHERE id = ?', [req.params.id], (err, order) => {
    if (err) {
      return res.status(500).json({ error: 'Failed to fetch order' });
    }
    if (!order) {
      return res.status(404).json({ error: 'Order not found' });
    }

    db.run(
      'UPDATE orders SET status = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?',
      [to_status, req.params.id],
      (err) => {
        if (err) {
          return res.status(500).json({ error: 'Failed to update order status' });
        }

        // Log transition
        db.run(
          'INSERT INTO order_logs (order_id, from_status, to_status, note) VALUES (?, ?, ?, ?)',
          [req.params.id, order.status, to_status, note || 'Admin transition'],
          (err) => {
            if (err) console.error('Failed to log transition:', err);
          }
        );

        res.json({ message: 'Order status updated successfully', status: to_status });
      }
    );
  });
});

// Get order logs endpoint
app.get('/api/orders/:id/logs', authenticateToken, (req, res) => {
  // Verify user owns the order
  db.get('SELECT * FROM orders WHERE id = ? AND user_id = ?', [req.params.id, req.user.id], (err, order) => {
    if (err) {
      return res.status(500).json({ error: 'Failed to fetch order' });
    }
    if (!order) {
      return res.status(404).json({ error: 'Order not found' });
    }

    db.all(
      'SELECT * FROM order_logs WHERE order_id = ? ORDER BY created_at DESC',
      [req.params.id],
      (err, logs) => {
        if (err) {
          return res.status(500).json({ error: 'Failed to fetch logs' });
        }
        res.json(logs);
      }
    );
  });
});

app.listen(PORT, () => {
  console.log(`Lottery system backend server listening on port ${PORT}`);
  console.log(`Environment: ${process.env.NODE_ENV || 'development'}`);
  console.log(`JWT_SECRET is ${JWT_SECRET === 'your-secret-key-change-in-production' ? 'using default (CHANGE IN PRODUCTION!)' : 'configured'}`);
  console.log(`ADMIN_KEY is ${ADMIN_KEY === 'admin-key-change-in-production' ? 'using default (CHANGE IN PRODUCTION!)' : 'configured'}`);
});
