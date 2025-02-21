require("@nomicfoundation/hardhat-toolbox");

module.exports = {
    solidity: "0.8.0",
    networks: {
        localhost: {
            url: "http://127.0.0.1:8545",
        },
        goerli: {
            url: "https://goerli.infura.io/v3/YOUR_INFURA_PROJECT_ID",
            accounts: ["YOUR_PRIVATE_KEY"],
        },
    },
};
