import { useState, useEffect } from "react";
import { ethers } from "ethers";
import { abi as contractABI } from "../../../artifacts/contracts/OnlineVoting.sol/OnlineVoting.json";

const contractAddress = "0x5FbDB2315678afecb367f032d93F642f64180aa3";

export default function useWallet() {
  const [currentUserAddress, setCurrentUserAddress] = useState(null);
  const [provider, setProvider] = useState(null);
  const [contract, setContract] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    // Check if ethereum object exists (MetaMask or similar wallet)
    if (window.ethereum) {
      console.log("Eth Detected!");
      const ethereumProvider = new ethers.BrowserProvider(window.ethereum);
      setProvider(ethereumProvider);
      console.log("Eth Connected!");
    }

    connectWallet();
  }, []);

  useEffect(() => {
    if (provider) {
      initContract();
    }
  }, [provider]);

  const initContract = async () => {
    const userSigner = await provider.getSigner();

    const connectedContract = new ethers.Contract(
      contractAddress,
      contractABI,
      userSigner
    );

    setContract(connectedContract);
    console.log("Contract Connected!", { signer: userSigner.address });
  };

  const connectWallet = async () => {
    try {
      // Request account access
      const [account] = await window.ethereum.request({
        method: "eth_requestAccounts",
      });

      // Set the first account
      setCurrentUserAddress(account);
      console.log("Wallet Connected!", { wallet: account });
    } catch (error) {
      console.error("Connection failed", error);
      throw error;
    }
  };

  const executeContractFunction = async (functionName, ...args) => {
    if (contract) {
      setIsLoading(true);
      try {
        const tx = await contract[functionName](...args);
        console.log("Transaction sent:", tx);
        // await tx.wait();
        console.log("Transaction confirmed:", tx);
        return tx;
      } catch (error) {
        console.error("Failed to execute contract function:", error);
        throw error;
      } finally {
        setIsLoading(false);
      }
    } else {
      console.error("Contract is not connected");
    }
  };

  return {
    currentUserAddress,
    provider,
    executeContractFunction,
    isLoading,
  };
}
