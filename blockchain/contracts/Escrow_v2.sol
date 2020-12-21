pragma solidity >=0.4.22 <0.7.0;

import "./BarnaToken.sol";
import "./FiberToken.sol";
import "./UpcToken.sol";
import "./CatToken.sol";

contract Escrow {

    string public name = "Escrow";
    
    BarnaToken private barnaToken;
    FiberToken private fiberToken;
    UpcToken private upcToken;
    CatToken private catToken;
    
    uint256 private balanceBNC;
    uint256 private balanceFBC;
    uint256 private balanceUPC;
    uint256 private balanceCTC;
    
	event EscrowInit(address escrowAddress);
 
    struct openBidData {
        string bidId;
        address ownerAddress;
        uint256 sellAmount;
		string sellCurrency;
    }
    
    openBidData[] public payments;
    	
	constructor(BarnaToken _barnaToken, FiberToken _fiberToken, UpcToken _upcToken, CatToken _catToken) public {
        emit EscrowInit(address(this));
		
		// payments = new openBidData[](maxSize);
		// availableCryptocurrencies = ["BNC", "FBC", "UPC", "CTC"];
		
		barnaToken = _barnaToken;
		fiberToken = _fiberToken;
		upcToken = _upcToken;
		catToken = _catToken;
		
		balanceBNC = barnaToken.balanceOf(address(this));
		balanceFBC = fiberToken.balanceOf(address(this));
		balanceUPC = upcToken.balanceOf(address(this));
		balanceCTC = catToken.balanceOf(address(this));
		
		require(true, "Escrow Created");
    }

    function createPayment(string memory bidId, uint256 sellAmount, string memory sellCurrency) public returns (bool created) { 
        /* Verify that Escrow balanceOf of working token has increased by sellAmount */
        require(verifyReceivedSellAmount(sellAmount, sellCurrency) == true, "Escrow: Have not received 'sellAmount'");
        require(sellAmount >= 0, "sellAmount cannot be 0");
        require(isValidCurrency(sellCurrency) == true, "Invalid sellCurrency");
		/* Add new openBid data to the main array */
        openBidData memory bid = openBidData(bidId, msg.sender, sellAmount, sellCurrency);
        payments.push(bid);
		return true;
    }
    
    // TO DO: Add verification method to check if the SELL transfer from acceptingUser has been done
    function requestPayment(string memory bidId) public returns (bool completed) {
        for (uint256 i = 0; i < payments.length; i++) { 
            if (keccak256(abi.encodePacked(payments[i].bidId)) == keccak256(abi.encodePacked(bidId))) {
				/* Send staked 'sellAmount' consisting of the SELL transfer from the owner user to the user accepting the open bid 'bidId' */
				sendPaymentToRequestingUser(msg.sender, payments[i].sellAmount, payments[i].sellCurrency);
				/* Delete this openBid data from the main array once completely traded */
				deleteOpenBidFromPayments(i);
                return true;
            }
        }
        return false;
    }
    
    function getPaymentOwner(string memory bidId) public returns (address ownerAddress) {
        for (uint256 i = 0; i < payments.length; i++) { 
            if (keccak256(abi.encodePacked(payments[i].bidId)) == keccak256(abi.encodePacked(bidId))) { return payments[i].ownerAddress; }
        }
        return address(0);
    }
    
   function getPaymentSellAmount(string memory bidId) public returns (uint256 sellAmount) {
        for (uint256 i = 0; i < payments.length; i++) { 
            if (keccak256(abi.encodePacked(payments[i].bidId)) == keccak256(abi.encodePacked(bidId))) { return payments[i].sellAmount; }
        }
        return 0; // CAUTION!!
    }
   
    function verifyReceivedSellAmount(uint256 sellAmount, string memory sellCurrency) public returns (bool) {
        if (keccak256(abi.encodePacked(sellCurrency)) == keccak256(abi.encodePacked(barnaToken.symbol()))) { 
            require(balanceBNC + sellAmount == barnaToken.balanceOf(address(this)), "Payment Not Received");
            balanceBNC = balanceBNC + sellAmount;
            return true;
        }
        else if (keccak256(abi.encodePacked(sellCurrency)) == keccak256(abi.encodePacked(fiberToken.symbol()))) { 
            require(balanceFBC + sellAmount == fiberToken.balanceOf(address(this)), "Payment Not Received");
            balanceFBC = balanceFBC + sellAmount;
            return true;
        }
        else if (keccak256(abi.encodePacked(sellCurrency)) == keccak256(abi.encodePacked(upcToken.symbol()))) { 
            require(balanceUPC + sellAmount == upcToken.balanceOf(address(this)), "Payment Not Received");
            balanceUPC = balanceUPC + sellAmount;
            return true;
        }
        else if (keccak256(abi.encodePacked(sellCurrency)) == keccak256(abi.encodePacked(catToken.symbol()))) { 
            require(balanceCTC + sellAmount == catToken.balanceOf(address(this)), "Payment Not Received");
            balanceCTC = balanceCTC + sellAmount;
            return true;
        }
        return false;
    }
	
	function sendPaymentToRequestingUser(address receiver, uint256 sellAmount, string memory sellCurrency) internal returns (bool) {
		if (keccak256(abi.encodePacked(sellCurrency)) == keccak256(abi.encodePacked(barnaToken.symbol()))) { 
			barnaToken.transfer(receiver, sellAmount);
			balanceBNC = balanceBNC - sellAmount;
            return true;
        }
        else if (keccak256(abi.encodePacked(sellCurrency)) == keccak256(abi.encodePacked(fiberToken.symbol()))) { 
            fiberToken.transfer(receiver, sellAmount);
            balanceFBC = balanceFBC - sellAmount;
            return true;
        }
        else if (keccak256(abi.encodePacked(sellCurrency)) == keccak256(abi.encodePacked(upcToken.symbol()))) { 
            upcToken.transfer(receiver, sellAmount);
            balanceUPC = balanceUPC - sellAmount;
            return true;
        }
        else if (keccak256(abi.encodePacked(sellCurrency)) == keccak256(abi.encodePacked(catToken.symbol()))) { 
			catToken.transfer(receiver, sellAmount);
            balanceCTC = balanceCTC - sellAmount;
            return true;
        }
		return false;
	}
	
	function isValidCurrency(string memory currency) internal returns (bool) {
        if (keccak256(abi.encodePacked(currency)) == keccak256(abi.encodePacked(barnaToken.symbol()))) { return true; }
        else if (keccak256(abi.encodePacked(currency)) == keccak256(abi.encodePacked(fiberToken.symbol()))) { return true; }
        else if (keccak256(abi.encodePacked(currency)) == keccak256(abi.encodePacked(upcToken.symbol()))) { return true; }
        else if (keccak256(abi.encodePacked(currency)) == keccak256(abi.encodePacked(catToken.symbol()))) { return true; }
        else { return false; }
    }
 
	function deleteOpenBidFromPayments(uint256 index) public returns (bool) {
        require(index < payments.length, "Array index out of bounds");
        for (uint256 i = index; i < payments.length - 1; i++) {
            payments[i] = payments[i+1];
        }
        delete payments[payments.length-1];
        payments.length--;
        return true;
    }
 
}
