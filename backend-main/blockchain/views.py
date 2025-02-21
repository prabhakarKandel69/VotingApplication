from django.http import JsonResponse
from web3 import Web3
from .blockchain_utils import sync_candidates_to_blockchain, sync_voters_to_blockchain, vote_on_blockchain

# ✅ Initialize Web3 instance
web3 = Web3()

# ✅ Sync Candidates from Backend to Blockchain
def sync_candidates(request):
    transactions = sync_candidates_to_blockchain()
    return JsonResponse({"message": "✅ Candidates synced", "transactions": transactions})

# ✅ Sync Voters from Backend to Blockchain
def sync_voters(request):
    transactions = sync_voters_to_blockchain()
    return JsonResponse({"message": "✅ Voters synced", "transactions": transactions})

# ✅ Allow a Voter to Vote
def vote(request):
    """Allow a voter to vote for a candidate with proper address validation."""

    # ✅ Get parameters safely
    voter_address = request.GET.get("voter_address")
    candidate_id = request.GET.get("candidate_id")

    print(f"🔍 Received voter_address: {voter_address}, candidate_id: {candidate_id}")  # ✅ Debugging print

    # ✅ Check if required parameters are missing
    if not voter_address or not candidate_id:
        return JsonResponse({"error": "Missing voter_address or candidate_id"}, status=400)

    # ✅ Validate Ethereum address
    if not web3.is_address(voter_address):
        return JsonResponse({"error": "Invalid Ethereum voter_address"}, status=400)

    try:
        # ✅ Convert voter_address to EIP-55 checksum format
        voter_address = web3.to_checksum_address(voter_address)

        # ✅ Convert candidate_id to integer safely
        candidate_id = int(candidate_id)
    except ValueError:
        return JsonResponse({"error": "Invalid candidate_id format"}, status=400)

    response = vote_on_blockchain(voter_address, candidate_id)
    return JsonResponse(response)
