import 'package:flutter/material.dart';

class TextBox extends StatelessWidget {
  String text;
  bool hide;
  TextEditingController cn;
  TextBox({@required this.text, this.cn, this.hide = false});
  @override
  Widget build(BuildContext context) {
    return TextField(
      controller: cn,
      obscureText: hide,
      style: style,
      decoration: InputDecoration(
          contentPadding: EdgeInsets.fromLTRB(20.0, 15.0, 20.0, 15.0),
          hintText: text,
          border:
              OutlineInputBorder(borderRadius: BorderRadius.circular(32.0))),
    );
    ;
  }
}

TextStyle style = TextStyle(fontFamily: 'Montserrat', fontSize: 20.0);
final emailField = TextField(
  obscureText: false,
  style: style,
  decoration: InputDecoration(
      contentPadding: EdgeInsets.fromLTRB(20.0, 15.0, 20.0, 15.0),
      hintText: "Email",
      border: OutlineInputBorder(borderRadius: BorderRadius.circular(32.0))),
);
final passwordField = TextField(
  obscureText: true,
  style: style,
  decoration: InputDecoration(
      contentPadding: EdgeInsets.fromLTRB(20.0, 15.0, 20.0, 15.0),
      hintText: "Password",
      border: OutlineInputBorder(borderRadius: BorderRadius.circular(32.0))),
);

showAlertDialog(BuildContext context, String msg, String header) {
  // set up the button
  Widget okButton = FlatButton(
    child: Text("OK"),
    onPressed: () {
      Navigator.of(context).pop(); // dismiss dialog
    },
  );

  // set up the AlertDialog
  AlertDialog alert = AlertDialog(
    title: Text(header),
    content: Text(msg),
    actions: [
      okButton,
    ],
  );

  // show the dialog
  showDialog(
    context: context,
    builder: (BuildContext context) {
      return alert;
    },
  );
}

// transAlertDialog(BuildContext context, String msg, String header, void f) {
//   // set up the button
//   Widget okButton = FlatButton(
//     child: Text("OK"),
//     onPressed: () async {
//       await Navigator.push(
//           context, MaterialPageRoute(builder: (context) => body()));
//     },
//   );
//
//   // set up the AlertDialog
//   AlertDialog alert = AlertDialog(
//     title: Text(header),
//     content: Text(msg),
//     actions: [
//       okButton,
//     ],
//   );
//
//   // show the dialog
//   showDialog(
//     context: context,
//     builder: (BuildContext context) {
//       return alert;
//     },
//   );
// }
