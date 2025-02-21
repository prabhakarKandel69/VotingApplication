// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract OnlineVoting {
    address public admin;
    uint public candidatesCount;
    uint public votingStartTime;
    uint public votingEndTime;

    struct Candidate {
        uint id;
        string name;
        uint voteCount;
    }

    struct Voter {
        bool isRegistered;
        bool hasVoted;
        uint vote; // Candidate ID
    }

    mapping(uint => Candidate) public candidates; // Candidate ID -> Candidate
    mapping(address => Voter) public voters; // Address -> Voter

    event CandidateAdded(uint candidateId, string name);
    event VoterRegistered(address voter);
    event VoteCasted(address voter, uint candidateId);
    event AdminTransferred(address oldAdmin, address newAdmin);

    // Errors (for gas efficiency)
    error OnlyAdmin();
    error VotingNotStarted();
    error VotingEnded();
    error InvalidCandidate();
    error AlreadyVoted();
    error NotRegistered();
    error AlreadyRegistered();

    modifier onlyAdmin() {
        if (msg.sender != admin) {
            revert OnlyAdmin();
        }
        _;
    }

    modifier duringVoting() {
        if (block.timestamp < votingStartTime) {
            revert VotingNotStarted();
        }
        if (block.timestamp > votingEndTime) {
            revert VotingEnded();
        }
        _;
    }

    constructor(uint _votingStartTime, uint _votingEndTime) {
        require(_votingStartTime < _votingEndTime, "Invalid voting period");
        admin = msg.sender;
        votingStartTime = _votingStartTime;
        votingEndTime = _votingEndTime;
    }

    // Add a new candidate (only by admin)
    function addCandidate(string memory _name) public onlyAdmin {
        candidatesCount++;
        candidates[candidatesCount] = Candidate({
            id: candidatesCount,
            name: _name,
            voteCount: 0
        });
        emit CandidateAdded(candidatesCount, _name);
    }

    // Register a new voter (only by admin)
    function registerVoter(address _voter) public onlyAdmin {
        if (voters[_voter].isRegistered) {
            revert AlreadyRegistered();
        }
        voters[_voter].isRegistered = true;
        emit VoterRegistered(_voter);
    }

    // Cast a vote (only during voting period)
    function vote(uint _candidateId) public duringVoting {
        if (!voters[msg.sender].isRegistered) {
            revert NotRegistered();
        }
        if (voters[msg.sender].hasVoted) {
            revert AlreadyVoted();
        }
        if (_candidateId == 0 || _candidateId > candidatesCount) {
            revert InvalidCandidate();
        }

        voters[msg.sender].hasVoted = true;
        voters[msg.sender].vote = _candidateId;
        candidates[_candidateId].voteCount++;

        emit VoteCasted(msg.sender, _candidateId);
    }

    // Get results for all candidates
    function getResults() public view returns (Candidate[] memory) {
        Candidate[] memory results = new Candidate[](candidatesCount);
        for (uint i = 1; i <= candidatesCount; i++) {
            results[i - 1] = candidates[i];
        }
        return results;
    }

    // Admin can transfer ownership to another address
    function transferAdmin(address _newAdmin) public onlyAdmin {
        require(_newAdmin != address(0), "New admin cannot be zero address");
        emit AdminTransferred(admin, _newAdmin);
        admin = _newAdmin;
    }

    // Utility: Check if voting is active
    function isVotingActive() public view returns (bool) {
        return block.timestamp >= votingStartTime && block.timestamp <= votingEndTime;
    }
}
