/**
 * Use this file to configure your truffle project. It's seeded with some
 * common settings for different networks and features like migrations,
 * compilation and testing. Uncomment the ones you need or modify
 * them to suit your project as necessary.
 *
 * More information about configuration can be found at:
 *
 * trufflesuite.com/docs/advanced/configuration
 *
 * To deploy via Infura you'll need a wallet provider (like @truffle/hdwallet-provider)
 * to sign your transactions before they're sent to a remote public node. Infura accounts
 * are available for free at: infura.io/register.
 *
 * You'll also need a mnemonic - the twelve word phrase the wallet uses to generate
 * public/private key pairs. If you're publishing your code to GitHub make sure you load this
 * phrase from a file you've .gitignored so it doesn't accidentally become public.
 *
 * $ truffle test --network <network-name>
 *
 */ 
 
module.exports = {
  networks: {
    development: {
      host: "127.0.0.1", // Localhost (default: none)
      port: 8545, // Standard Ethereum port (default: none)
      network_id: "*" // Any network (default: none)
    }
  },
  
  // An additional network, but with some advanced options…
  // advanced: {
  //   port: 8777,             // Custom port
  //   network_id: 1342,       // Custom network
  //   gas: 8500000,           // Gas sent with each transaction (default: ~6700000)
  //   gasPrice: 20000000000,  // 20 gwei (in wei) (default: 100 gwei)
  //   from: <address>,        // Account to send transactions from (default: accounts[0])
  //   websocket: true         // Enable EventEmitter interface for web3 (default: false)
  // },

  // Smart Contracts directory
  contracts_directory: './contracts/',
  contracts_build_directory: './abis/',
  
  // Set default mocha options here, use special reporters etc.
  mocha: {
    // timeout: 100000
  },
  
  // Configure your compilers
  compilers: {
    solc: {
      // version: "0.5.1", // Fetch exact version from solc-bin (default: truffle's version)
      // docker: true, // Use "0.5.1" you've installed locally with docker (default: false)
      // settings: { // See the solidity docs for advice about optimization and evmVersion
      // optimizer: {
      // enabled: false,
      // runs: 200
      // },
      // evmVersion: "byzantium"
      // }
    }
  }
};
