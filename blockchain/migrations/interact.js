const { ethers } = require("hardhat");

async function main() {
    const contractAddress = "0xYourDeployedContractAddress";
    const abi = [/* Contract ABI */];
    const provider = ethers.getDefaultProvider("goerli");
    const contract = new ethers.Contract(contractAddress, abi, provider);

    const candidatesCount = await contract.candidatesCount();
    console.log("Total candidates:", candidatesCount);
}

main();
