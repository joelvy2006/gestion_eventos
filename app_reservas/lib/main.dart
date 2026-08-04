import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

void main() => runApp(const ReservasApp());

class ReservasApp extends StatelessWidget {
  const ReservasApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Sistema de Reservas',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(
          seedColor: const Color(0xFF1E88E5),
          brightness: Brightness.dark,
        ),
        useMaterial3: true,
      ),
      home: const MainNavigationScreen(),
    );
  }
}

const String baseIp = " 192.168.0.117"; 

class MainNavigationScreen extends StatefulWidget {
  const MainNavigationScreen({super.key});

  @override
  State<MainNavigationScreen> createState() => _MainNavigationScreenState();
}

class _MainNavigationScreenState extends State<MainNavigationScreen> {
  int _currentIndex = 0;

  final List<Widget> _pages = [
    const EspaciosView(),
    const MisReservasView(),
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Gestión de Reservas'),
        elevation: 2,
        backgroundColor: const Color(0xFF0F172A),
      ),
      body: _pages[_currentIndex],
      bottomNavigationBar: NavigationBar(
        selectedIndex: _currentIndex,
        onDestinationSelected: (index) {
          setState(() {
            _currentIndex = index;
          });
        },
        destinations: const [
          NavigationDestination(
            icon: Icon(Icons.event_seat),
            label: 'Espacios',
          ),
          NavigationDestination(
            icon: Icon(Icons.calendar_today),
            label: 'Mis Reservas',
          ),
        ],
      ),
    );
  }
}

// Vista para listar espacios y recintos
class EspaciosView extends StatelessWidget {
  const EspaciosView({super.key});

  @override
  Widget build(BuildContext context) {
    return ListView(
      padding: const EdgeInsets.all(16),
      children: [
        Card(
          color: const Color(0xFF1E293B),
          child: ListTile(
            leading: const Icon(Icons.location_city, size: 40, color: Color(0xFF3B82F6)),
            title: const Text('Salón Principal de Eventos', style: TextStyle(fontWeight: FontWeight.bold)),
            subtitle: const Text('Capacidad: 200 personas | Estado: Disponible'),
            trailing: ElevatedButton(
              onPressed: () {
                ScaffoldMessenger.of(context).showSnackBar(
                  const SnackBar(content: Text('Formulario de reserva en desarrollo')),
                );
              },
              child: const Text('Reservar'),
            ),
          ),
        ),
      ],
    );
  }
}

// Vista conectada a la API de Django para ver reservas
class MisReservasView extends StatefulWidget {
  const MisReservasView({super.key});

  @override
  State<MisReservasView> createState() => _MisReservasViewState();
}

class _MisReservasViewState extends State<MisReservasView> {
  List<dynamic> reservas = [];
  bool cargando = true;

  @override
  void initState() {
    super.initState();
    cargarReservas();
  }

  Future<void> cargarReservas() async {
    final url = Uri.parse('http://$baseIp:8000/api/reservas/');
    try {
      final response = await http.get(url);
      if (response.statusCode == 200) {
        setState(() {
          reservas = json.decode(response.body);
          cargando = false;
        });
      } else {
        setState(() => cargando = false);
      }
    } catch (e) {
      setState(() => cargando = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: cargando
          ? const Center(child: CircularProgressIndicator())
          : reservas.isEmpty
              ? const Center(
                  child: Text(
                    "No hay reservas registradas.",
                    style: TextStyle(color: Colors.grey),
                  ),
                )
              : RefreshIndicator(
                  onRefresh: cargarReservas,
                  child: ListView.builder(
                    itemCount: reservas.length,
                    itemBuilder: (context, index) {
                      final item = reservas[index];
                      return Card(
                        color: const Color(0xFF1E293B),
                        margin: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                        child: ListTile(
                          leading: const Icon(Icons.event, color: Color(0xFF3B82F6)),
                          title: Text(item['nombre_evento'] ?? 'Reserva de Evento'),
                          subtitle: Text("Fecha: ${item['fecha'] ?? 'N/A'}"),
                          trailing: Text(
                            item['estado'] ?? 'Confirmado',
                            style: const TextStyle(color: Colors.greenAccent),
                          ),
                        ),
                      );
                    },
                  ),
                ),
    );
  }
}