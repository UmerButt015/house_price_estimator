import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:intl/intl.dart';

void main() {
  runApp(const HousePricePredictorApp());
}

class HousePricePredictorApp extends StatelessWidget {
  const HousePricePredictorApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'House Price Predictor',
      theme: ThemeData(
        primarySwatch: Colors.blue,
        scaffoldBackgroundColor: Colors.grey[50],
        inputDecorationTheme: InputDecorationTheme(
          border: OutlineInputBorder(
            borderRadius: BorderRadius.circular(12),
            borderSide: const BorderSide(color: Colors.blueGrey),
          ),
          filled: true,
          fillColor: Colors.white,
        ),
        elevatedButtonTheme: ElevatedButtonThemeData(
          style: ElevatedButton.styleFrom(
            padding: const EdgeInsets.symmetric(vertical: 16),
            textStyle: const TextStyle(
              fontSize: 18,
              fontWeight: FontWeight.bold,
            ),
          ),
        ),
      ),
      home: const PredictionForm(),
      debugShowCheckedModeBanner: false,
    );
  }
}

class PredictionForm extends StatefulWidget {
  const PredictionForm({super.key});

  @override
  _PredictionFormState createState() => _PredictionFormState();
}

class _PredictionFormState extends State<PredictionForm> {
  final _formKey = GlobalKey<FormState>();
  // Update with your actual server IP or localhost configuration
  final _apiUrl = "http://localhost:8000/house/predict"; // Corrected endpoint
  final _citiesUrl = "http://localhost:8000/house/cities";
  final _furnishingUrl = "http://localhost:8000/house/furnishing-options";

  // Form controllers
  final TextEditingController areaController = TextEditingController();
  final TextEditingController bedroomsController = TextEditingController();
  final TextEditingController bathroomsController = TextEditingController();
  final TextEditingController storiesController = TextEditingController();
  final TextEditingController parkingController = TextEditingController();
  final TextEditingController yearBuiltController = TextEditingController();

  // Dropdown values
  String? mainroadValue = 'yes';
  String? guestroomValue = 'no';
  String? basementValue = 'no';
  String? hotwaterheatingValue = 'no';
  String? airconditioningValue = 'yes';
  String? furnishingValue;
  String? cityValue;

  List<String> cities = [];
  List<String> furnishingOptions = [];
  bool isLoading = true; // Start in loading state
  bool isPredicting = false;
  double? predictedPrice;

  @override
  void initState() {
    super.initState();
    _fetchOptions();
  }

  Future<void> _fetchOptions() async {
    try {
      final citiesResponse = await http.get(Uri.parse(_citiesUrl));
      final furnishingResponse = await http.get(Uri.parse(_furnishingUrl));

      if (mounted) {
        if (citiesResponse.statusCode == 200) {
          cities = List<String>.from(json.decode(citiesResponse.body));
        } else {
          _showSnackBar('Failed to load cities: ${citiesResponse.statusCode}');
        }

        if (furnishingResponse.statusCode == 200) {
          furnishingOptions = List<String>.from(
            json.decode(furnishingResponse.body),
          );
        } else {
          _showSnackBar(
            'Failed to load furnishing options: ${furnishingResponse.statusCode}',
          );
        }

        // Set initial values after loading
        if (cities.isNotEmpty) cityValue = cities.first;
        if (furnishingOptions.isNotEmpty)
          furnishingValue = furnishingOptions.first;

        setState(() => isLoading = false);
      }
    } catch (e) {
      if (mounted) {
        _showSnackBar('Connection error: $e');
        setState(() => isLoading = false);
      }
    }
  }

  Future<void> _predictPrice() async {
    if (!_formKey.currentState!.validate()) return;
    if (cityValue == null || furnishingValue == null) {
      _showSnackBar('Please complete all selections');
      return;
    }

    setState(() => isPredicting = true);

    try {
      final response = await http.post(
        Uri.parse(_apiUrl),
        headers: {'Content-Type': 'application/json'},
        body: json.encode({
          'area': int.parse(areaController.text),
          'bedrooms': int.parse(bedroomsController.text),
          'bathrooms': int.parse(bathroomsController.text),
          'stories': int.parse(storiesController.text),
          'mainroad': mainroadValue,
          'guestroom': guestroomValue,
          'basement': basementValue,
          'hotwaterheating': hotwaterheatingValue,
          'airconditioning': airconditioningValue,
          'parking': int.parse(parkingController.text),
          'furnishingstatus': furnishingValue,
          'city': cityValue,
          'year_built': int.parse(yearBuiltController.text),
        }),
      );

      if (mounted) {
        if (response.statusCode == 200) {
          final result = json.decode(response.body);
          setState(() => predictedPrice = result['predicted_price']);
        } else {
          _showSnackBar(
            'Prediction failed: ${response.statusCode} - ${response.body}',
          );
        }
      }
    } catch (e) {
      if (mounted) _showSnackBar('Network error: $e');
    } finally {
      if (mounted) setState(() => isPredicting = false);
    }
  }

  void _showSnackBar(String message) {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text(message),
        backgroundColor: Colors.red,
        duration: const Duration(seconds: 3),
      ),
    );
  }

  void _resetForm() {
    _formKey.currentState?.reset();
    setState(() {
      mainroadValue = 'yes';
      guestroomValue = 'no';
      basementValue = 'no';
      hotwaterheatingValue = 'no';
      airconditioningValue = 'yes';
      predictedPrice = null;

      // Reset controllers
      areaController.clear();
      bedroomsController.clear();
      bathroomsController.clear();
      storiesController.clear();
      parkingController.clear();
      yearBuiltController.clear();
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('House Price Predictor'),
        centerTitle: true,
        actions: [
          IconButton(
            icon: const Icon(Icons.refresh),
            onPressed: _resetForm,
            tooltip: 'Reset Form',
          ),
        ],
      ),
      body:
          isLoading
              ? const Center(child: CircularProgressIndicator())
              : SingleChildScrollView(
                padding: const EdgeInsets.all(16),
                child: Form(
                  key: _formKey,
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.stretch,
                    children: [
                      Card(
                        elevation: 2,
                        child: Padding(
                          padding: const EdgeInsets.all(16),
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              const Text(
                                'Property Details',
                                style: TextStyle(
                                  fontSize: 18,
                                  fontWeight: FontWeight.bold,
                                  color: Colors.blueGrey,
                                ),
                              ),
                              const SizedBox(height: 16),
                              _buildInputGrid(),
                            ],
                          ),
                        ),
                      ),

                      const SizedBox(height: 20),

                      Card(
                        elevation: 2,
                        child: Padding(
                          padding: const EdgeInsets.all(16),
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              const Text(
                                'Features',
                                style: TextStyle(
                                  fontSize: 18,
                                  fontWeight: FontWeight.bold,
                                  color: Colors.blueGrey,
                                ),
                              ),
                              const SizedBox(height: 16),
                              _buildFeatureGrid(),
                            ],
                          ),
                        ),
                      ),

                      const SizedBox(height: 20),

                      Card(
                        elevation: 2,
                        child: Padding(
                          padding: const EdgeInsets.all(16),
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              const Text(
                                'Location & Status',
                                style: TextStyle(
                                  fontSize: 18,
                                  fontWeight: FontWeight.bold,
                                  color: Colors.blueGrey,
                                ),
                              ),
                              const SizedBox(height: 16),
                              _buildLocationFields(),
                            ],
                          ),
                        ),
                      ),

                      const SizedBox(height: 24),

                      ElevatedButton.icon(
                        onPressed: isPredicting ? null : _predictPrice,
                        icon:
                            isPredicting
                                ? const SizedBox(
                                  width: 24,
                                  height: 24,
                                  child: CircularProgressIndicator(
                                    strokeWidth: 2,
                                    color: Colors.white,
                                  ),
                                )
                                : const Icon(Icons.calculate),
                        label: Text(
                          isPredicting ? 'Predicting...' : 'Calculate Price',
                        ),
                        style: ElevatedButton.styleFrom(
                          padding: const EdgeInsets.symmetric(vertical: 16),
                          backgroundColor: Colors.blue[800],
                        ),
                      ),

                      if (predictedPrice != null) ...[
                        const SizedBox(height: 32),
                        _buildResultCard(),
                      ],
                    ],
                  ),
                ),
              ),
    );
  }

  Widget _buildInputGrid() {
    return GridView.count(
      shrinkWrap: true,
      physics: const NeverScrollableScrollPhysics(),
      crossAxisCount: 2,
      childAspectRatio: 3,
      crossAxisSpacing: 16,
      mainAxisSpacing: 16,
      children: [
        _buildInputField('Area (sq ft)', areaController, TextInputType.number),
        _buildInputField('Bedrooms', bedroomsController, TextInputType.number),
        _buildInputField(
          'Bathrooms',
          bathroomsController,
          TextInputType.number,
        ),
        _buildInputField('Stories', storiesController, TextInputType.number),
        _buildInputField(
          'Parking Spots',
          parkingController,
          TextInputType.number,
        ),
        _buildInputField(
          'Year Built',
          yearBuiltController,
          TextInputType.number,
        ),
      ],
    );
  }

  Widget _buildFeatureGrid() {
    return GridView.count(
      shrinkWrap: true,
      physics: const NeverScrollableScrollPhysics(),
      crossAxisCount: 2,
      childAspectRatio: 3,
      crossAxisSpacing: 16,
      mainAxisSpacing: 16,
      children: [
        _buildDropdown(
          'Main Road',
          ['yes', 'no'],
          mainroadValue,
          (v) => setState(() => mainroadValue = v),
        ),
        _buildDropdown(
          'Guest Room',
          ['yes', 'no'],
          guestroomValue,
          (v) => setState(() => guestroomValue = v),
        ),
        _buildDropdown(
          'Basement',
          ['yes', 'no'],
          basementValue,
          (v) => setState(() => basementValue = v),
        ),
        _buildDropdown(
          'Hot Water',
          ['yes', 'no'],
          hotwaterheatingValue,
          (v) => setState(() => hotwaterheatingValue = v),
        ),
        _buildDropdown(
          'Air Conditioning',
          ['yes', 'no'],
          airconditioningValue,
          (v) => setState(() => airconditioningValue = v),
        ),
      ],
    );
  }

  Widget _buildLocationFields() {
    return Column(
      children: [
        _buildDropdown(
          'Furnishing',
          furnishingOptions,
          furnishingValue,
          (v) => setState(() => furnishingValue = v),
        ),
        const SizedBox(height: 16),
        _buildDropdown(
          'City',
          cities,
          cityValue,
          (v) => setState(() => cityValue = v),
        ),
      ],
    );
  }

  Widget _buildInputField(
    String label,
    TextEditingController controller,
    TextInputType type,
  ) {
    return TextFormField(
      controller: controller,
      keyboardType: type,
      decoration: InputDecoration(
        labelText: label,
        border: const OutlineInputBorder(),
        filled: true,
        fillColor: Colors.grey[100],
      ),
      validator: (value) {
        if (value == null || value.isEmpty) return 'Required';
        if (type == TextInputType.number && double.tryParse(value) == null) {
          return 'Invalid number';
        }
        return null;
      },
    );
  }

  Widget _buildDropdown(
    String label,
    List<String> options,
    String? value,
    Function(String?) onChanged,
  ) {
    return DropdownButtonFormField<String>(
      value: value,
      items:
          options.map((String value) {
            return DropdownMenuItem<String>(
              value: value,
              child: Text(value.capitalize()),
            );
          }).toList(),
      onChanged: onChanged,
      decoration: InputDecoration(
        labelText: label,
        border: const OutlineInputBorder(),
        filled: true,
        fillColor: Colors.grey[100],
      ),
      validator: (value) => value == null ? 'Please select' : null,
    );
  }

  Widget _buildResultCard() {
    final formatter = NumberFormat.currency(
      locale: 'en_US',
      symbol: '₹',
      decimalDigits: 0,
    );
    return Card(
      elevation: 4,
      color: Colors.blue[50],
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
      child: Padding(
        padding: const EdgeInsets.all(24),
        child: Column(
          children: [
            const Text(
              'PREDICTED HOUSE PRICE',
              style: TextStyle(
                fontSize: 18,
                fontWeight: FontWeight.bold,
                color: Colors.blueGrey,
              ),
            ),
            const SizedBox(height: 20),
            Text(
              formatter.format(predictedPrice),
              style: const TextStyle(
                fontSize: 36,
                fontWeight: FontWeight.bold,
                color: Colors.blue,
              ),
            ),
            const SizedBox(height: 10),
            const Text(
              'Based on your property details',
              style: TextStyle(color: Colors.grey, fontStyle: FontStyle.italic),
            ),
            const SizedBox(height: 20),
            ElevatedButton(
              onPressed: _resetForm,
              child: const Text('New Prediction'),
            ),
          ],
        ),
      ),
    );
  }
}

extension StringExtension on String {
  String capitalize() {
    return "${this[0].toUpperCase()}${substring(1)}";
  }
}
