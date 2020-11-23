const FiberToken = artifacts.require('FiberToken');
const BarnaToken = artifacts.require('BarnaToken');

/* Put the SmartContracts in the network */
module.exports = async function(deployer, network, accounts) 
{
	// Deploy FiberToken Token
	await deployer.deploy(FiberToken);
	const fiberToken = await FiberToken.deployed();
	
	// Deploy BarnaToken Token
	await deployer.deploy(BarnaToken);
	const barnaToken = await BarnaToken.deployed();
	
	// REMARK: initially all Tokens are assigned to the account that deployed the contracts
	// Transfer 3m FiberToken (with "integer decimals") to the first trader 
	await fiberToken.transfer(accounts[1], '3000000000000000000000000');
	// Transfer 3m FiberToken (with "integer decimals") to the second trader 
	await fiberToken.transfer(accounts[2], '3000000000000000000000000');
		
	// Transfer 1.5m BarnaToken (with "integer decimals") to the first trader 
	await barnaToken.transfer(accounts[1], '1500000000000000000000000');
	// Transfer 1.5m BarnaToken (with "integer decimals") to the second trader 
	await barnaToken.transfer(accounts[2], '1500000000000000000000000');
		
};
