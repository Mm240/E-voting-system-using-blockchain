// Sepolia deployment: set SEPOLIA_RPC_URL and DEPLOYER_MNEMONIC (never commit them).
const HDWalletProvider = process.env.SEPOLIA_RPC_URL ? require("@truffle/hdwallet-provider") : null;

module.exports = {
  networks: {
    development: {
      host: "127.0.0.1",     // Ganache GUI/CLI default
      port: 8545,            // Ganache default RPC port
      network_id: "*",       // match any network id
      gas: 6721975,
    },
    ...(HDWalletProvider && {
      sepolia: {
        provider: () => new HDWalletProvider(process.env.DEPLOYER_MNEMONIC, process.env.SEPOLIA_RPC_URL),
        network_id: 11155111,
        confirmations: 2,
        timeoutBlocks: 200,
      },
    }),
  },
  compilers: {
    solc: {
      version: "0.8.17",   // match solidity version
    }
  }
};
