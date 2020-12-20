const BarnaToken = artifacts.require('BarnaToken');
const FiberToken = artifacts.require('FiberToken');
const UpcToken = artifacts.require('UpcToken');
const CatToken = artifacts.require('CatToken');
const Escrow = artifacts.require('Escrow');

/* Put the SmartContracts in the network */
module.exports = async function(deployer, network, accounts) 
{	
	const barnaToken = await BarnaToken.deployed();
	const fiberToken = await FiberToken.deployed();
	const upcToken = await UpcToken.deployed();	
	const catToken = await CatToken.deployed();
	
	// Deploy Escrow Contract
	await deployer.deploy(Escrow, barnaToken.address, fiberToken.address, upcToken.address, catToken.address);
	const escrow = await Escrow.deployed();

};
