import 'dart:convert';
import 'dart:io';

import 'package:basic_utils/basic_utils.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_session/flutter_session.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:http/http.dart'; //You can also import the browser version
import 'package:http/http.dart' as http;
import 'package:web3dart/web3dart.dart';

import 'Reusablecard.dart';
import 'constrains.dart';
import 'login.dart';

void main() {
  runApp(MaterialApp(
    theme: ThemeData.dark(),
    home: Scaffold(
      appBar: AppBar(
        title: Text("Itoken"),
      ),
      body: login(),
    ),
  ));
}

class body extends StatefulWidget {
  @override
  _bodyState createState() => _bodyState();
}

class _bodyState extends State<body> {
  Web3Client ethClient;
  //String abi;
  List<Widget> transtions = List<Widget>();

  Future<String> get_trans(String url, sell_currency, buy_currency) async {
    transtions = List<Widget>();
    http.Response result = await http.get(url);
    print(json.decode(result.body)["bids"].runtimeType);
    print(json.decode(result.body).runtimeType);
    var resultDict = json.decode(result.body);
    for (var dicts in resultDict["bids"]) {
      List<Widget> words = List<Widget>();
      print(dicts);
      for (var content in dicts.values) {
        if (content.toString() != dicts.values.last &&
            content.toString() != dicts.values.first) {
          String s = content.toString() + " ";
          words.add(Text(s));
        }
        print(content);
      }
      String Urlapi =
          "http://10.4.41.142/api/v1/users/list/email/" + dicts["owner"];
      http.Response seller_Data = await http.get(Urlapi);
      var dataDecoded = jsonDecode(seller_Data.body);
      print("errorrrrr");
      print(dataDecoded);
      //10.4.41.142/api/v1/users/list/private_key/0xFFcf8FDEE72ac11b5c542428B35EEF5769C409f0
      Urlapi = "http://10.4.41.142/api/v1/users/list/private_key/" +
          dataDecoded["users"][0]["account"];

      http.Response key_response = await http.get(Urlapi);
      Map private_key = jsonDecode(key_response.body);

      print(dataDecoded["users"][0]["account"]);
      words.add(Container(
          color: Colors.blue,
          child: FlatButton(
            child: Text("get offer"),
            onPressed: () async {
              print(await FlutterSession().get("addrress"));
              print("privatee_keey");
              print(private_key["accounts"][0]["private_key"]);
              print(dataDecoded["users"][0]["account"]);
              print("public_cetificate");
              print(await FlutterSession().get("addrress"));
              print(await FlutterSession().get("key"));

              try {
                String deleteurl =
                    "http://10.4.41.142/api/v1/bids/block/" + dicts.values.last;
                http.Response delete_request = await http.get(deleteurl);
                print(dicts.values.last);
                print(delete_request.statusCode);

                await tranfer(
                    private_key["accounts"][0]["private_key"],
                    await FlutterSession().get("addrress"),
                    dicts['sell_amount'],
                    dicts['sell_currency']);
                await tranfer(
                    await FlutterSession().get("key"),
                    dataDecoded["users"][0]["account"],
                    dicts['buy_amount'],
                    dicts['buy_currency']);
                deleteurl = "http://10.4.41.142/api/v1/bids/unblock/" +
                    dicts.values.last;
                delete_request = await http.get(deleteurl);
                print(dicts.values.last);
                print(delete_request.statusCode);
                await Navigator.push(
                    context, MaterialPageRoute(builder: (context) => body()));
              } catch (e) {
                print(e.runtimeType);
                showAlertDialog(context, e.toString(), "Error ");

                //                 Navigator.push(
                //                       context, MaterialPageRoute(builder: (context) => body()));

              }
            },
          )));
      transtions.add(Card(
        child: Row(
          mainAxisAlignment: MainAxisAlignment.center,
          children: words,
        ),
      ));
    }
    transtions.add(Row(
      mainAxisAlignment: MainAxisAlignment.center,
      children: [
        Container(
          margin: EdgeInsets.symmetric(horizontal: 10, vertical: 10),
          color: Colors.blue,
          child: FlatButton(
            child: Text("create offer"),
            onPressed: () async {
              dynamic balance = await getBalance(
                  publicAddressR, contractAddresses[buy_currency]);
              Navigator.push(
                  context,
                  MaterialPageRoute(
                      builder: (context) => creatoffer(
                            data: {
                              "balance": balance[0],
                              "sell_currency": sell_currency,
                              "buy_currency": buy_currency,
                            },
                          )));
            },
          ),
        ),
        Container(
            color: Colors.blue,
            child: FlatButton(
              child: Text("get balance"),
              onPressed: () async {
                var amount = await getBalance(
                    await FlutterSession().get("addrress"),
                    contractAddresses[sell_currency]);
                Navigator.push(
                    context,
                    MaterialPageRoute(
                        builder: (context) => balance(amount: amount)));
              },
            ))
      ],
    ));
  }

  Future<String> sendCoind(String targetAddressHex, String privateKey,
      int amount, String contractaddress) async {
    EthereumAddress address = EthereumAddress.fromHex(targetAddressHex);
    // uint in smart contract means BigInt for us
    var bigAmount;
    var response;
    while (amount > 9) {
      amount = amount - 9;
      bigAmount = BigInt.from(9 * 100000000000000000);
      response = await submit(
          "transfer", privateKey, [address, bigAmount], contractaddress);
    }
    bigAmount = BigInt.from(amount * 100000000000000000);
    // sendCoin transaction
    response = await submit(
        "transfer", privateKey, [address, bigAmount], contractaddress);
    return response;
  }

  Future<String> submit(String functionName, String privateKey,
      List<dynamic> args, String contractaddress) async {
    EthPrivateKey credentials = EthPrivateKey.fromHex(privateKey);

    DeployedContract contract = await loadContract(contractaddress);

    final ethFunction = contract.function(functionName);

    var result = await ethClient.sendTransaction(
      credentials,
      Transaction.callContract(
        contract: contract,
        function: ethFunction,
        parameters: args,
      ),
    );
    return result;
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

  Future<List<dynamic>> getBalance(
      String targetAddressHex, String contractAddress) async {
    EthereumAddress address = EthereumAddress.fromHex(targetAddressHex);
    // getBalance transaction
    List<dynamic> result = await query("balanceOf", [address], contractAddress);
    // returns list of results, in this case a list with only the balance
    return result;
  }

  Future<List<dynamic>> query(
      String functionName, List<dynamic> args, String contractAddress) async {
    final contract = await loadContract(contractAddress);
    final ethFunction = contract.function(functionName);
    final data = await ethClient.call(
        contract: contract, function: ethFunction, params: args);
    return data;
  }

  Future<DeployedContract> loadContract(String contractAddress) async {
    String abiCode = await rootBundle.loadString("res/abi.json");
    final contract = DeployedContract(
        ContractAbi.fromJson(abiCode, "FiberToken"),
        EthereumAddress.fromHex(contractAddress));
    return contract;
  }

  @override
  void initState() {
    // TODO: implement initState
    super.initState();
    Client httpClient = new Client();
    ethClient = new Web3Client("http://10.4.41.142:8545", httpClient);
    publicAddress = FlutterSession().get("addrress");
    privateKey = FlutterSession().get("addrress");
    apikey = FlutterSession().get("api_key");
  }

  String privateKeyS =
      "6cbed15c793ce57650b9877cf6fa156fbef513c4e6134f022a85b1ffdd59b2a1";
  String privateKeyR =
      "6370fd033278c143179d81c5526140625662b8daa446c22ee2d73db3707e620c";
  String publicAddressS = "0xFFcf8FDEE72ac11b5c542428B35EEF5769C409f0";
  String publicAddressR = "0x22d491Bde2303f2f43325b2108D26f1eAbA1e32b";
  var publicAddress;
  var privateKey;
  var apikey;
  Map contractAddresses = {
    "CTC": "0x5C3670E0Ac747b03CD0e3B3165b2fd69e6fB790A",
    "FBC": "0x9095b8e8a5a4E7Fcb7F569dDc325eAB089732B26",
    "UPC": "0x8ab4aFFe16B8986f4e049F24A7F67701312E2B8D",
    "BNC": "0xdA9FbD039c001e17e404a5bcEbA665e54F44bDE9"
  };

  Future<void> tranfer(
      String keyS, String addressR, amount, String coin) async {
    //print("transfer");
    //print(await getBalance(addressR, contractAddresses[coin]));
    //print(await getBalance(publicAddressR, contractAddresses[coin]));
    //print(contractAddresses[coin]);
    String contractaddress = contractAddresses[coin];
    // print(await getBalance(publicAddressR, contractaddress));
    // print("Sender");
    // print(await getBalance(publicAddressS, contractaddress));
    // print(addressR);
    // print(keyS);
    // print(amount);
    // print(contractaddress);
    var respon = await sendCoind(addressR, keyS, amount, contractaddress);
    // print("Reciever");
    // print(await getBalance(publicAddressR, contractaddress));
    // print("Sender");
    // print(await getBalance(publicAddressS, contractaddress));
  }

  @override
  Widget build(BuildContext context) {
    return Container(
      child: SafeArea(
        child: Padding(
          padding: const EdgeInsets.all(30.0),
          child: Row(
            children: [
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Row(
                      mainAxisAlignment: MainAxisAlignment.spaceAround,
                      children: [
                        FlatButton(
                          color: Colors.blue,
                          onPressed: () async {
                            // abi = "res/fbc.json";
                            await get_trans(
                                'http://10.4.41.142/api/v1/bids/list/FBC/BNC',
                                'FBC',
                                'BNC');
                            Navigator.push(
                                context,
                                MaterialPageRoute(
                                    builder: (context) => transactions(
                                          view: transtions,
                                        )));
                          },
                          child: ReusableCard("FBC/BNC"),
                        ),
                        FlatButton(
                          color: Colors.blue,
                          onPressed: () async {
                            await get_trans(
                                'http://10.4.41.142/api/v1/bids/list/FBC/CTC',
                                'FBC',
                                'CTC');
                            var variable = await ethClient.getNetworkId();
                            EthereumAddress address = EthereumAddress.fromHex(
                                "0xFFcf8FDEE72ac11b5c542428B35EEF5769C409f0");
                            // await tranfer_fbc(privateKeyS, publicAddressR, 3);
                            //await tranfer_ctc(privateKeyS, publicAddressR, 3);
                            Navigator.of(context).push(MaterialPageRoute(
                                builder: (context) => transactions(
                                      view: transtions,
                                    )));
                            _navigateToNextScreen(context);
                          },
                          child: ReusableCard("FBC/CTC"),
                        ),
                      ],
                    ),
                    Row(
                      mainAxisAlignment: MainAxisAlignment.spaceAround,
                      children: [
                        FlatButton(
                          color: Colors.blue,
                          onPressed: () async {
                            // abi = "res/fbc.json";
                            await get_trans(
                                'http://10.4.41.142/api/v1/bids/list/FBC/UPC',
                                'FBC',
                                'UPC');

                            Navigator.push(
                                context,
                                MaterialPageRoute(
                                    builder: (context) => transactions(
                                          view: transtions,
                                        )));
                          },
                          child: ReusableCard("FBC/UPC"),
                        ),
                        FlatButton(
                          color: Colors.blue,
                          onPressed: () async {
                            await get_trans(
                                'http://10.4.41.142/api/v1/bids/list/UPC/CTC',
                                'UPC',
                                'CTC');
                            var variable = await ethClient.getNetworkId();
                            EthereumAddress address = EthereumAddress.fromHex(
                                "0xFFcf8FDEE72ac11b5c542428B35EEF5769C409f0");
                            Navigator.of(context).push(MaterialPageRoute(
                                builder: (context) => transactions(
                                      view: transtions,
                                    )));
                            _navigateToNextScreen(context);
                          },
                          child: ReusableCard("UPC/CTC"),
                        ),
                      ],
                    ),
                    Row(
                      mainAxisAlignment: MainAxisAlignment.spaceAround,
                      children: [
                        FlatButton(
                          color: Colors.blue,
                          onPressed: () async {
                            // abi = "res/fbc.json";
                            await get_trans(
                                'http://10.4.41.142/api/v1/bids/list/UPC/BNC',
                                'UPC',
                                'BNC');
                            Navigator.push(
                                context,
                                MaterialPageRoute(
                                    builder: (context) => transactions(
                                          view: transtions,
                                        )));
                          },
                          child: ReusableCard("UPC/BNC"),
                        ),
                        FlatButton(
                          color: Colors.blue,
                          onPressed: () async {
                            await get_trans(
                                'http://10.4.41.142/api/v1/bids/list/UPC/FBC',
                                'UPC',
                                'FBC');
                            var variable = await ethClient.getNetworkId();
                            EthereumAddress address = EthereumAddress.fromHex(
                                "0xFFcf8FDEE72ac11b5c542428B35EEF5769C409f0");
                            Navigator.of(context).push(MaterialPageRoute(
                                builder: (context) => transactions(
                                      view: transtions,
                                    )));
                            _navigateToNextScreen(context);
                          },
                          child: ReusableCard("UPC/FBC"),
                        ),
                      ],
                    ),
                    Row(
                      mainAxisAlignment: MainAxisAlignment.spaceAround,
                      children: [
                        FlatButton(
                          color: Colors.blue,
                          onPressed: () async {
                            // abi = "res/fbc.json";
                            await get_trans(
                                'http://10.4.41.142/api/v1/bids/list/CTC/BNC',
                                'CTC',
                                'BNC');

                            Navigator.push(
                                context,
                                MaterialPageRoute(
                                    builder: (context) => transactions(
                                          view: transtions,
                                        )));
                          },
                          child: ReusableCard("CTC/BNC"),
                        ),
                        FlatButton(
                          color: Colors.blue,
                          onPressed: () async {
                            await get_trans(
                                'http://10.4.41.142/api/v1/bids/list/CTC/FBC',
                                'CTC',
                                'FBC');
                            var variable = await ethClient.getNetworkId();
                            EthereumAddress address = EthereumAddress.fromHex(
                                "0xFFcf8FDEE72ac11b5c542428B35EEF5769C409f0");
                            Navigator.of(context).push(MaterialPageRoute(
                                builder: (context) => transactions(
                                      view: transtions,
                                    )));
                            _navigateToNextScreen(context);
                          },
                          child: ReusableCard("CTC/FBC"),
                        ),
                      ],
                    ),
                    Row(
                      mainAxisAlignment: MainAxisAlignment.spaceAround,
                      children: [
                        FlatButton(
                          color: Colors.blue,
                          onPressed: () async {
                            // abi = "res/fbc.json";
                            await get_trans(
                                'http://10.4.41.142/api/v1/bids/list/CTC/UPC',
                                'CTC',
                                'UPC');

                            Navigator.push(
                                context,
                                MaterialPageRoute(
                                    builder: (context) => transactions(
                                          view: transtions,
                                        )));
                          },
                          child: ReusableCard("CTC/UPC"),
                        ),
                        FlatButton(
                          color: Colors.blue,
                          onPressed: () async {
                            await get_trans(
                                'http://10.4.41.142/api/v1/bids/list/BNC/CTC',
                                'BNC',
                                'CTC');
                            var variable = await ethClient.getNetworkId();
                            EthereumAddress address = EthereumAddress.fromHex(
                                "0xFFcf8FDEE72ac11b5c542428B35EEF5769C409f0");
                            Navigator.of(context).push(MaterialPageRoute(
                                builder: (context) => transactions(
                                      view: transtions,
                                    )));
                            _navigateToNextScreen(context);
                          },
                          child: ReusableCard("BNC/CTC"),
                        ),
                      ],
                    ),
                    Row(
                      mainAxisAlignment: MainAxisAlignment.spaceAround,
                      children: [
                        FlatButton(
                          color: Colors.blue,
                          onPressed: () async {
                            // abi = "res/fbc.json";
                            await get_trans(
                                'http://10.4.41.142/api/v1/bids/list/BNC/FBC',
                                'BNC',
                                'FBC');

                            Navigator.push(
                                context,
                                MaterialPageRoute(
                                    builder: (context) => transactions(
                                          view: transtions,
                                        )));
                          },
                          child: ReusableCard("BNC/FBC"),
                        ),
                        FlatButton(
                          color: Colors.blue,
                          onPressed: () async {
                            await get_trans(
                                'http://10.4.41.142/api/v1/bids/list/BNC/UPC',
                                'BNC',
                                'UPC');
                            Navigator.of(context).push(MaterialPageRoute(
                                builder: (context) => transactions(
                                      view: transtions,
                                    )));
                            _navigateToNextScreen(context);
                          },
                          child: ReusableCard("BNC/UPC"),
                        ),
                      ],
                    ),
                    Center(
                      child: FlatButton(
                        color: Colors.blue,
                        onPressed: () async {
                          Navigator.push(context,
                              MaterialPageRoute(builder: (context) => login()));
                        },
                        child: ReusableCard("logout"),
                      ),
                    ),
                  ],
                ),
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

class balance extends StatelessWidget {
  var amount;
  balance({this.amount}) {}
  @override
  Widget build(BuildContext context) {
    String amountS = amount.toString();
    if (amountS.length > 18) {
      int aux = amountS.length - 18;
      amountS = StringUtils.addCharAtPosition(amountS, ",", aux);
    }
    String content = "Your balance is : " + "\n" + amountS;
    print(content.length);
    return Scaffold(
      body: Container(
        child: Center(
          child: RichText(
            text: TextSpan(text: content, style: new TextStyle(fontSize: 20)),
          ),
        ),
      ),
    );
  }
}

class creatoffer extends StatefulWidget {
  @override
  Map data;
  creatoffer({@required this.data}) {}
  _creatofferState createState() => _creatofferState(data: data);
}

class _creatofferState extends State<creatoffer> {
  Map data;
  TextEditingController amount_sell = TextEditingController();
  TextEditingController amount_buy = TextEditingController();
  _creatofferState({@required this.data});
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
          child: Container(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            TextField(
              controller: amount_buy,
              obscureText: false,
              decoration: InputDecoration(
                  contentPadding: EdgeInsets.fromLTRB(20.0, 15.0, 20.0, 15.0),
                  hintText: "buy_currency_amount",
                  border: OutlineInputBorder(
                      borderRadius: BorderRadius.circular(32.0))),
            ),
            SizedBox(
              height: 10,
            ),
            TextField(
              controller: amount_sell,
              obscureText: false,
              decoration: InputDecoration(
                  contentPadding: EdgeInsets.fromLTRB(20.0, 15.0, 20.0, 15.0),
                  hintText: "sell_currency_amount",
                  border: OutlineInputBorder(
                      borderRadius: BorderRadius.circular(32.0))),
            ),
            SizedBox(
              height: 10,
            ),
            Container(
              color: Colors.blue,
              child: FlatButton(
                child: Text("submit"),
                onPressed: () async {
                  int value = int.parse(amount_sell.text);
                  // BigInt b = BigInt.from(value * 1000000000000000000);
                  var dataapi = {
                    'sell_amount': amount_buy.text,
                    'sell_currency': data["buy_currency"],
                    'buy_amount': amount_sell.text,
                    'buy_currency': data["sell_currency"],
                    "API_KEY": await FlutterSession().get("apiKey")
                  };
                  //body
                  print(dataapi);
                  Response r = await http.post(
                      'http://10.4.41.142/api/v1/bids/new',
                      body: dataapi);

                  Navigator.push(
                      context, MaterialPageRoute(builder: (context) => body()));
                },
              ),
            ),
          ],
        ),
      )),
    );
  }
}

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
