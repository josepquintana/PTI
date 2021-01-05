import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:http/http.dart'; //You can also import the browser version
import 'package:web3dart/web3dart.dart';

class escrow extends StatefulWidget {
  @override
  _escrowState createState() => _escrowState();
}

class _escrowState extends State<escrow> {
  void initState() {
    // TODO: implement initState
    super.initState();
    Client httpClient = new Client();
    ethClient = new Web3Client("http://10.4.41.142:8545", httpClient);
  }

  Web3Client ethClient;

  Future<DeployedContract> loadContract(
      String contractAddress, String location) async {
    String abiCode = await rootBundle.loadString(location);
    final contract = DeployedContract(
        ContractAbi.fromJson(abiCode, "FiberToken"),
        EthereumAddress.fromHex(contractAddress));
    return contract;
  }

  Future<String> submit(String functionName, String privateKey,
      List<dynamic> args, String contractaddress) async {
    EthPrivateKey credentials = EthPrivateKey.fromHex(privateKey);

    DeployedContract contract =
        await loadContract(contractaddress, "res/abi.json");

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

  Future<List<dynamic>> query(String functionName, List<dynamic> args,
      String contractAddress, String location) async {
    final contract = await loadContract(contractAddress, location);
    final ethFunction = contract.function(functionName);
    final data = await ethClient.call(
        contract: contract, function: ethFunction, params: args);
    return data;
  }

  Future<String> sendCoind(String targetAddressHex, String privateKey,
      int amount, String contractaddress) async {
    Map contractAddresses = {
      "CTC": "0x5C3670E0Ac747b03CD0e3B3165b2fd69e6fB790A",
      "FBC": "0x9095b8e8a5a4E7Fcb7F569dDc325eAB089732B26",
      "UPC": "0x8ab4aFFe16B8986f4e049F24A7F67701312E2B8D",
      "BNC": "0xdA9FbD039c001e17e404a5bcEbA665e54F44bDE9"
    };
    EthereumAddress address = EthereumAddress.fromHex(targetAddressHex);
    // uint in smart contract means BigInt for us
    var bigAmount;
    var response;
    while (amount > 9) {
      amount = amount - 9;
      bigAmount = BigInt.from(9 * 1000000000000000000);
      response = await submit(
          "Escroww",
          privateKey,
          [
            "ppp",
            contractAddresses["FBC"],
            contractAddresses["BNC"],
            contractAddresses["UPC"],
            contractAddresses["CTC"]
          ],
          contractaddress);

      //(string memory moneda, FiberToken a, BarnaToken b, UpcToken c, CatToken d)
    }
    bigAmount = BigInt.from(amount * 1000000000000000000);
    // sendCoin transaction
    response = await submit(
        "transfer", privateKey, [address, bigAmount], contractaddress);
    return response;
  }

  @override
  Widget build(BuildContext context) {
    return Container();
  }
}
