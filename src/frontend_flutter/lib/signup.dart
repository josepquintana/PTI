import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:flutter_session/flutter_session.dart';
import 'package:http/http.dart' as http;

import 'constrains.dart';
import 'main.dart';

class signup extends StatefulWidget {
  @override
  _signupState createState() => _signupState();
}

class _signupState extends State<signup> {
  TextEditingController email = TextEditingController();
  TextEditingController password = TextEditingController();
  TextEditingController rPassword = TextEditingController();
  @override
  Widget build(BuildContext context) {
    final SignupButton = Material(
      elevation: 5.0,
      borderRadius: BorderRadius.circular(30.0),
      color: Color(0xff01A0C7),
      child: MaterialButton(
        minWidth: MediaQuery.of(context).size.width,
        padding: EdgeInsets.fromLTRB(20.0, 15.0, 20.0, 15.0),
        onPressed: () async {
          var data = {
            "email": email.text,
            "password": password.text,
            "repeat_password": rPassword.text,
          };
          print(data);
          http.Response r = await http
              .post('http://10.4.41.142/api/v1/users/signup', body: data);
          print(r.statusCode);

          if (r.statusCode == 201) {
            print(r.body);
            var apiData = jsonDecode(r.body);
            var session = FlutterSession();
            session.set("email", email.text);
            session.set("addrress", apiData["data"]["account"]);
            session.set("key", apiData["data"]["private_key"]);
            session.set("apiKey", apiData["data"]["api_key"]);
            Navigator.push(context, MaterialPageRoute(builder: (context) {
              return body();
            }));
          } else if (r.statusCode == 422 && password.text != rPassword.text) {
            showAlertDialog(
                context, "password and repeat password dosen't match", "Error");
          } else if (r.statusCode == 422) {
            showAlertDialog(context, "Bad Email", "Error");
          } else if (r.statusCode == 409) {
            showAlertDialog(context, "User arleady exisits", "Error");
          } else {
            showAlertDialog(context, "You have to fill all camps", "Error");
          }
        },
        child: Text("Signup",
            textAlign: TextAlign.center,
            style: style.copyWith(
                color: Colors.white, fontWeight: FontWeight.bold)),
      ),
    );
    return Scaffold(
      body: Container(
        padding: EdgeInsets.symmetric(horizontal: 10),
        child: Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              TextBox(
                text: "Email",
                cn: email,
              ),
              SizedBox(
                height: 10,
              ),
              TextBox(
                text: "Password",
                cn: password,
                hide: true,
              ),
              SizedBox(
                height: 10,
              ),
              TextBox(
                text: "Repeat your password",
                cn: rPassword,
                hide: true,
              ),
              SizedBox(
                height: 40,
              ),
              SignupButton
            ],
          ),
        ),
      ),
    );
  }
}
