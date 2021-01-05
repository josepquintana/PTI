import 'dart:convert';
import 'dart:io';

import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:http/http.dart'; //You can also import the browser version
import 'package:web3dart/web3dart.dart';

import 'Reusablecard.dart';

void main() {
  runApp(MaterialApp(
    theme: ThemeData.dark(),
    home: Scaffold(
      appBar: AppBar(
        title: Text("tradiing 2020"),
      ),
      body: body(),
    ),
  ));
}

class body extends StatefulWidget {
  @override
  _bodyState createState() => _bodyState();
}

class _bodyState extends State<body> {
  List<Widget> transtions = List<Widget>();

  Future<String> get_trans() async {
    transtions = List<Widget>();
    // http.Response result =
    //     await http.get('http://10.4.41.142/api/v1/bids/list/FBC/BNC');
    // print(result.body);
    var result =
        await getResponse('http://10.4.41.142/api/v1/bids/list/FBC/BNC');
    for (var dicts in result["bids"]) {
      List<Widget> words = List<Widget>();
      // words.add(Text(dicts.values[2].toString()));
      for (var content in dicts.values) {
        if (content.toString() != dicts.values.last) {
          String s = content.toString() + " ";
          words.add(Text(s));
        }
        print(content);
      }
      words.add(Container(
        color: Colors.blue,
        child: FlatButton(
          child: Text("get offer"),
        ),
      ));
      transtions.add(Card(
        child: Row(
          mainAxisAlignment: MainAxisAlignment.center,
          children: words,
        ),
      ));
    }
    print(transtions.length);
  }

  getResponse(String url) async {
    HttpClient httpClient = new HttpClient();
    HttpClientRequest request = await httpClient.getUrl(Uri.parse(url));
    HttpClientResponse response = await request.close();
    String responseBody = await response.transform(utf8.decoder).join();
    Map jsonResponse = jsonDecode(responseBody) as Map;
    httpClient.close();
    return jsonResponse;
  }

  Future<DeployedContract> loadContract() async {
    String abiCode = await rootBundle
        .loadString("http://10.4.41.142/files/abis/FiberToken.json");
    String contractAddress = "0xD13ebb5C39fB00C06122827E1cbD389930C9E0E3";
    //String "0xD13ebb5C39fB00C06122827E1cbD389930C9E0E3"
    final contract = DeployedContract(
        ContractAbi.fromJson(abiCode, "FiberToken"),
        EthereumAddress.fromHex(contractAddress));
    return contract;
  }

  @override
  Widget build(BuildContext context) {
    return Container(
      child: SafeArea(
        child: Padding(
          padding: const EdgeInsets.all(30.0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              FlatButton(
                color: Colors.blue,
                onPressed: () async {
                  //await get_trans();
                  print("que passa");
                  Client httpClient = new Client();
                  Web3Client ethClient =
                      new Web3Client("http://10.4.41.142:8545", httpClient);
                  var variable = await ethClient.getNetworkId();
                  EthereumAddress address = EthereumAddress.fromHex(
                      "0xFFcf8FDEE72ac11b5c542428B35EEF5769C409f0");
                  var balance = await ethClient.getBalance(address);
                  print(variable);
                  print(balance);
                  var contract = await loadContract();
                  print(contract.runtimeType);

                  //Navigator.of(context).push(MaterialPageRoute(
                  //builder: (context) => transactions(
                  //     view: transtions,
                  //    )));
                  //_navigateToNextScreen(context);
                },
                child: ReusableCard("FIBC"),
              ),
              FlatButton(
                color: Colors.blue,
                onPressed: () async {
                  await get_trans();
                  print("que passa");
                  Navigator.of(context).push(MaterialPageRoute(
                      builder: (context) => transactions(
                            view: transtions,
                          )));
                  //_navigateToNextScreen(context);
                },
                child: ReusableCard("BARNC"),
              ),
            ],
          ),
        ),
      ),
    );
  }

  void _navigateToNextScreen(BuildContext context) {
    Navigator.of(context).push(MaterialPageRoute(
        builder: (context) => transactions(
              view: transtions,
            )));
  }
}

// class transs extends StatelessWidget {
//   List<Widget> view = List<Widget>();
//   transs({@required view});
//   @override
//   Widget build(BuildContext context) {
//     return Theme(
//       data: ThemeData.dark(),
//       child: SafeArea(
//         child: Column(children: this.view),
//       ),
//     );
//   }
// }

class transactions extends StatefulWidget {
  List<Widget> view = List<Widget>();
  transactions({@required this.view}) {}
  @override
  _transactionsState createState() => _transactionsState(views: view);
}

class _transactionsState extends State<transactions> {
  List<Widget> views;

  _transactionsState({this.views});

  @override
  Widget build(BuildContext context) {
    print("lennn");
    print(views.length);
    return SafeArea(
      child: Theme(
        data: ThemeData.dark(),
        child: SafeArea(
          child: Column(children: views),
        ),
      ),
    );
  }
}
