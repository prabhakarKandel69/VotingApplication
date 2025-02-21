from web3 import Web3
import os
from candidate.models import Candidate  # Import Django model for candidates
from voters.models import Voter  # Import Django model for voters

# ✅ Blockchain Configuration
PROVIDER_URL = "http://127.0.0.1:8545"  # Hardhat/Ganache RPC URL
CONTRACT_ADDRESS = "0x5FbDB2315678afecb367f032d93F642f64180aa3"  # Replace with deployed contract address

# ✅ Smart Contract ABI
CONTRACT_ABI = [
    {
        "inputs": [{"internalType": "string", "name": "_fullName", "type": "string"}],
        "name": "addCandidate",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [{"internalType": "address", "name": "_voterAddress", "type": "address"}],
        "name": "addVoter",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [{"internalType": "uint256", "name": "_candidateId", "type": "uint256"}],
        "name": "vote",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "getResults",
        "outputs": [
            {
                "components": [
                    {"internalType": "uint256", "name": "id", "type": "uint256"},
                    {"internalType": "string", "name": "fullName", "type": "string"},
                    {"internalType": "uint256", "name": "voteCount", "type": "uint256"},
                ],
                "internalType": "struct OnlineVoting.Candidate[]",
                "name": "",
                "type": "tuple[]",
            }
        ],
        "stateMutability": "view",
        "type": "function",
    }
]

# ✅ Connect to Blockchain
web3 = Web3(Web3.HTTPProvider(PROVIDER_URL))
contract = web3.eth.contract(address=CONTRACT_ADDRESS, abi=CONTRACT_ABI)

# ✅ Get Default Account (For Transactions)
if "PRIVATE_KEY" in os.environ and "ACCOUNT_ADDRESS" in os.environ:
    PRIVATE_KEY = os.getenv("PRIVATE_KEY")
    ACCOUNT_ADDRESS = os.getenv("ACCOUNT_ADDRESS")
else:
    ACCOUNT_ADDRESS = web3.eth.accounts[0]  # Use first Hardhat/Ganache account
    PRIVATE_KEY = None  # Use unlocked account

# ✅ Ensure Ethereum Address is Valid
def get_checksum_address(address):
    if not web3.is_address(address):
        raise ValueError(f"Invalid Ethereum address: {address}")
    return web3.to_checksum_address(address)

# ✅ Sync Candidates from Django to Blockchain
def sync_candidates_to_blockchain():
    candidates = Candidate.objects.all()
    transactions = []

    for candidate in candidates:
        try:
            nonce = web3.eth.get_transaction_count(ACCOUNT_ADDRESS)
            transaction = contract.functions.addCandidate(candidate.full_name).build_transaction({
                "from": ACCOUNT_ADDRESS,
                "nonce": nonce,
                "gas": 200000,
                "gasPrice": web3.to_wei("50", "gwei"),
            })
            
            if PRIVATE_KEY:
                signed_txn = web3.eth.account.sign_transaction(transaction, private_key=PRIVATE_KEY)
                tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
            else:
                tx_hash = web3.eth.send_transaction(transaction)

            transactions.append({"candidate": candidate.full_name, "transaction_hash": tx_hash.hex()})
        except Exception as e:
            print(f"❌ Error adding candidate {candidate.full_name}: {e}")

    return transactions

# ✅ Sync Voters from Django to Blockchain
def sync_voters_to_blockchain():
    """Fetch voters from Django database and store them in blockchain."""
    voters = Voter.objects.exclude(wallet_address__isnull=True).exclude(wallet_address="")  # Ignore null addresses
    transactions = []

    if not voters.exists():
        return {"message": "❌ No voters found with a valid wallet address.", "transactions": []}

    for voter in voters:
        try:
            voter_address = get_checksum_address(voter.wallet_address)

            nonce = web3.eth.get_transaction_count(ACCOUNT_ADDRESS)
            transaction = contract.functions.addVoter(voter_address).build_transaction({
                "from": ACCOUNT_ADDRESS,
                "nonce": nonce,
                "gas": 200000,
                "gasPrice": web3.to_wei("50", "gwei"),
            })

            tx_hash = web3.eth.send_transaction(transaction)
            transactions.append({"voter_address": voter_address, "transaction_hash": tx_hash.hex()})
        except Exception as e:
            print(f"❌ Error adding voter {voter.wallet_address}: {e}")

    return {"message": "✅ Voters synced", "transactions": transactions}

# ✅ Function for Voter to Vote
def vote_on_blockchain(voter_address, candidate_id):
    """Allow a voter to vote for a candidate"""
    try:
        voter_address = get_checksum_address(voter_address)  # Ensure valid Ethereum address

        if voter_address not in web3.eth.accounts:
            print(f"⚠️ Voter {voter_address} is not an unlocked account. Using default.")
            voter_address = ACCOUNT_ADDRESS  # ✅ Use an unlocked account

        nonce = web3.eth.get_transaction_count(voter_address)
        transaction = contract.functions.vote(candidate_id).build_transaction({
            "from": voter_address,
            "nonce": nonce,
            "gas": 200000,
            "gasPrice": web3.to_wei("50", "gwei"),
        })

        # ✅ If the voter address is locked, sign the transaction
        if PRIVATE_KEY:
            signed_txn = web3.eth.account.sign_transaction(transaction, private_key=PRIVATE_KEY)
            tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        else:
            tx_hash = web3.eth.send_transaction(transaction)

        return {"message": "✅ Vote recorded", "transaction_hash": tx_hash.hex()}
    except Exception as e:
        return {"message": f"❌ Error voting: {str(e)}"}
