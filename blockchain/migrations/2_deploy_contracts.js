const BarnaToken = artifacts.require('BarnaToken');
const FiberToken = artifacts.require('FiberToken');
const UpcToken = artifacts.require('UpcToken');
const CatToken = artifacts.require('CatToken');
const Escrow = artifacts.require('Escrow');

/* Put the SmartContracts in the network */
module.exports = async function(deployer, network, accounts) 
{	
	// Deploy BarnaToken Token
	await deployer.deploy(BarnaToken);
	const barnaToken = await BarnaToken.deployed();
	
	// Deploy FiberToken Token
	await deployer.deploy(FiberToken);
	const fiberToken = await FiberToken.deployed();
	
	// Deploy UpcToken Token
	await deployer.deploy(UpcToken);
	const upcToken = await UpcToken.deployed();	
	
	// Deploy CatToken Token
	await deployer.deploy(CatToken);
	const catToken = await CatToken.deployed();
	
	// Deploy Escrow Contract
	await deployer.deploy(Escrow, barnaToken.address, fiberToken.address, upcToken.address, catToken.address);
	const escrow = await Escrow.deployed();

	// REMARK: initially all Tokens are assigned to the account that deployed the contracts		
	// Transfer 1.5m BarnaToken (with "integer decimals") to the first trader 
	await barnaToken.transfer(accounts[1], '1500000000000000000000000');
	// Transfer 1.5m BarnaToken (with "integer decimals") to the second trader 
	await barnaToken.transfer(accounts[2], '1500000000000000000000000');
	
	// Transfer 3m FiberToken (with "integer decimals") to the first trader 
	await fiberToken.transfer(accounts[1], '3000000000000000000000000');
	// Transfer 3m FiberToken (with "integer decimals") to the second trader 
	await fiberToken.transfer(accounts[2], '3000000000000000000000000');
	
	// Transfer 4.5m UpcToken (with "integer decimals") to the first trader 
	await upcToken.transfer(accounts[1], '4500000000000000000000000');
	// Transfer 4.5m UpcToken (with "integer decimals") to the second trader 
	await upcToken.transfer(accounts[2], '4500000000000000000000000');
	
	// Transfer 6m CatToken (with "integer decimals") to the first trader 
	await catToken.transfer(accounts[1], '6000000000000000000000000');
	// Transfer 6m CatToken (with "integer decimals") to the second trader 
	await catToken.transfer(accounts[2], '6000000000000000000000000');
		
};
