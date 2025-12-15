import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';

class ApiService {
  // For Android emulator: use 10.0.2.2 to access host machine's localhost
  // For desktop/web: use http://localhost:3000/api
  // For iOS simulator: use http://localhost:3000/api
  static const String baseUrl = 'http://10.0.2.2:3000/api';
  
  String? _token;

  // Get stored token
  Future<String?> getToken() async {
    if (_token != null) return _token;
    final prefs = await SharedPreferences.getInstance();
    _token = prefs.getString('auth_token');
    return _token;
  }

  // Save token
  Future<void> saveToken(String token) async {
    _token = token;
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString('auth_token', token);
  }

  // Clear token
  Future<void> clearToken() async {
    _token = null;
    final prefs = await SharedPreferences.getInstance();
    await prefs.remove('auth_token');
  }

  // Get auth headers
  Future<Map<String, String>> _getHeaders() async {
    final token = await getToken();
    return {
      'Content-Type': 'application/json',
      if (token != null) 'Authorization': 'Bearer $token',
    };
  }

  // Auth endpoints
  Future<Map<String, dynamic>> register(String username, String password) async {
    final response = await http.post(
      Uri.parse('$baseUrl/auth/register'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({'username': username, 'password': password}),
    );

    if (response.statusCode == 201) {
      final data = jsonDecode(response.body);
      await saveToken(data['token']);
      return data;
    } else {
      throw Exception(jsonDecode(response.body)['error'] ?? 'Registration failed');
    }
  }

  Future<Map<String, dynamic>> login(String username, String password) async {
    final response = await http.post(
      Uri.parse('$baseUrl/auth/login'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({'username': username, 'password': password}),
    );

    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);
      await saveToken(data['token']);
      return data;
    } else {
      throw Exception(jsonDecode(response.body)['error'] ?? 'Login failed');
    }
  }

  Future<Map<String, dynamic>> getMe() async {
    final response = await http.get(
      Uri.parse('$baseUrl/auth/me'),
      headers: await _getHeaders(),
    );

    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      throw Exception('Failed to fetch user info');
    }
  }

  // Items endpoints
  Future<List<dynamic>> getItems() async {
    final response = await http.get(
      Uri.parse('$baseUrl/items'),
      headers: await _getHeaders(),
    );

    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      throw Exception('Failed to fetch items');
    }
  }

  Future<Map<String, dynamic>> getItem(int id) async {
    final response = await http.get(
      Uri.parse('$baseUrl/items/$id'),
      headers: await _getHeaders(),
    );

    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      throw Exception('Failed to fetch item');
    }
  }

  // Bets endpoint
  Future<Map<String, dynamic>> placeBet(int itemId, String numbers, double stake) async {
    final response = await http.post(
      Uri.parse('$baseUrl/bets'),
      headers: await _getHeaders(),
      body: jsonEncode({
        'item_id': itemId,
        'numbers': numbers,
        'stake': stake,
      }),
    );

    if (response.statusCode == 201) {
      return jsonDecode(response.body);
    } else {
      throw Exception(jsonDecode(response.body)['error'] ?? 'Failed to place bet');
    }
  }

  // Orders endpoints
  Future<List<dynamic>> getOrders() async {
    final response = await http.get(
      Uri.parse('$baseUrl/orders'),
      headers: await _getHeaders(),
    );

    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      throw Exception('Failed to fetch orders');
    }
  }

  Future<Map<String, dynamic>> getOrder(int id) async {
    final response = await http.get(
      Uri.parse('$baseUrl/orders/$id'),
      headers: await _getHeaders(),
    );

    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      throw Exception('Failed to fetch order');
    }
  }

  Future<Map<String, dynamic>> payOrder(int orderId) async {
    final response = await http.post(
      Uri.parse('$baseUrl/orders/$orderId/pay'),
      headers: await _getHeaders(),
    );

    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      throw Exception(jsonDecode(response.body)['error'] ?? 'Failed to pay order');
    }
  }

  Future<Map<String, dynamic>> cancelOrder(int orderId) async {
    final response = await http.post(
      Uri.parse('$baseUrl/orders/$orderId/cancel'),
      headers: await _getHeaders(),
    );

    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      throw Exception(jsonDecode(response.body)['error'] ?? 'Failed to cancel order');
    }
  }

  Future<Map<String, dynamic>> transitionOrder(int orderId, String toStatus, {String? note}) async {
    final response = await http.post(
      Uri.parse('$baseUrl/orders/$orderId/transition'),
      headers: await _getHeaders(),
      body: jsonEncode({
        'to_status': toStatus,
        if (note != null) 'note': note,
      }),
    );

    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      throw Exception(jsonDecode(response.body)['error'] ?? 'Failed to transition order');
    }
  }

  Future<List<dynamic>> fetchOrderLogs(int orderId) async {
    final response = await http.get(
      Uri.parse('$baseUrl/orders/$orderId/logs'),
      headers: await _getHeaders(),
    );

    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      throw Exception('Failed to fetch order logs');
    }
  }
}
