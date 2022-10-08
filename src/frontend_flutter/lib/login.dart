import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:flutter_session/flutter_session.dart';
import 'package:http/http.dart' as http;
import 'package:trading2000/signup.dart';

import 'constrains.dart';
import 'main.dart';

class login extends StatelessWidget {
  void _navigateToNextScreen(BuildContext context) {
    Navigator.of(context)
        .push(MaterialPageRoute(builder: (context) => signup()));
  }

  @override
  Widget build(BuildContext context) {
    TextEditingController email = TextEditingController();
    TextEditingController password = TextEditingController();
    final loginButon = Material(
      elevation: 5.0,
      borderRadius: BorderRadius.circular(30.0),
      color: Color(0xff01A0C7),
      child: MaterialButton(
        minWidth: MediaQuery.of(context).size.width,
        padding: EdgeInsets.fromLTRB(20.0, 15.0, 20.0, 15.0),
        onPressed: () async {
          var data = {"email": email.text, "password": password.text};
          http.Response r = await http
              .post('http://10.4.41.142/api/v1/users/login_alt', body: data);
          if (r.statusCode == 200) {
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
          } else if (r.statusCode == 422) {
            showAlertDialog(context, "Bad Email", "Error");
          } else {
            showAlertDialog(
                context, "Email or password is not correct ", "Error");
          }
        },
        child: Text("Login",
            textAlign: TextAlign.center,
            style: style.copyWith(
                color: Colors.white, fontWeight: FontWeight.bold)),
      ),
    );
    return Scaffold(
      body: Container(
        padding: EdgeInsets.symmetric(horizontal: 10),
        child: Center(
          child: Padding(
            padding: const EdgeInsets.all(8.0),
            child: SingleChildScrollView(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  TextBox(
                    cn: email,
                    text: "Email",
                  ),
                  SizedBox(height: 45.0),
                  TextBox(
                    cn: password,
                    text: "Password",
                    hide: true,
                  ),
                  SizedBox(height: 45.0),
                  loginButon,
                  SizedBox(height: 20.0),
                  GestureDetector(
                    child: Text("signup"),
                    onTap: () async {
                      Navigator.of(context).push(
                          MaterialPageRoute(builder: (context) => signup()));
                      _navigateToNextScreen(context);
                    },
                  ),
                ],
              ),
            ),
          ),
        ),
      ),
    );
  }
}
