/* 
 * NOTE: Always convert to Wei when interacting with the Smart Contracts
 */

/**********/
/* USER 1 */
/**********/

/* First, Create new Bid */

var bidId = '5fdf7bd0fe0a1aef41d4f4bd';

var sellAmount = window.web3.utils.toWei((6789).toString()); 

await upcToken.methods.balanceOf(escrow._address).call();

await escrow.methods.createPayment(bidId, sellAmount, 'UPC').send({ from: myAccount }).on('transactionHash', async (hash) => {
	console.log('done');
	console.log(hash);
})

await escrow.methods.payments(0).call();

await escrow.methods.getPaymentOwner(bidId).call()

await escrow.methods.getPaymentSellAmount(bidId).call()


/**********/
/* USER 2 */
/**********/

var bidId = '5fdf7bd0fe0a1aef41d4f4bd';

await escrow.methods.payments(0).call();

await escrow.methods.requestPayment(bidId).send({ from: myAccount }).on('transactionHash', async (hash) => {
	console.log('done');
	console.log(hash);
})




/* Delete from Payments Array */
await escrow.methods.deleteOpenBidFromPayments(0).send({ from: myAccount }).on('transactionHash', async (hash) => {
	console.log('deleted');
})

escrow.methods.payments(0).call({ from: myAccount}, function(error, result) {
    console.log(errror);
});



await escrow.methods.payments(0).call().then((result) => async {
  console.log("Success! Got result: " + result);
}).catch((err) => {
  console.log("Failed with error: " + err);
});





