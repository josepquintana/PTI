import 'package:flutter/material.dart';

class ReusableCard extends StatelessWidget {
  ReusableCard(this.tockenName);
  String tockenName;
  @override
  Widget build(BuildContext context) {
    return Card(
      child: Text(tockenName),
    );
  }
}
