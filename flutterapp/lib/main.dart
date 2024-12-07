import 'package:flutter/material.dart';
import 'dart:convert';
import 'package:http/http.dart' as http;

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: Scaffold(
        appBar: AppBar(title: Text('Basic API App')),
        body: QueryApp(),
      ),
    );
  }
}

class QueryApp extends StatefulWidget {
  @override
  QueryAppState createState() => QueryAppState();
}

class QueryAppState extends State<QueryApp> {
  final TextEditingController _controller = TextEditingController();
  String _response = '';

  Future<void> sendQuery() async {
    String query = _controller.text; // 取得用戶輸入內容
    final url = Uri.parse('http://10.0.2.2:5000/query'); // 後端 API 地址

    try {
      // 發送 POST 請求
      final response = await http.post(
        url,
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({'query': query}), // JSON 請求體
      );

      // 如果請求成功，解析回應內容
      if (response.statusCode == 200) {
        setState(() {
          _response = jsonDecode(response.body)['response'];
        });
      } else {
        setState(() {
          _response = 'Error: ${response.statusCode}';
        });
      }
    } catch (e) {
      setState(() {
        _response = 'Error: $e';
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return SingleChildScrollView(
      // Wrap the entire content in SingleChildScrollView
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: [
            TextField(
              controller: _controller, // 綁定輸入控制器
              decoration: InputDecoration(labelText: 'Enter your query'),
            ),
            SizedBox(height: 10),
            ElevatedButton(
              onPressed: sendQuery, // 點擊按鈕發送請求
              child: Text('Send'),
            ),
            SizedBox(height: 20),
            Text(
              _response, // 顯示回應內容
              style: TextStyle(fontSize: 16),
            ),
          ],
        ),
      ),
    );
  }
}
