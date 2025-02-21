// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract OnlineVoting {
    address public admin;

    enum ElectionState {
        NotStarted,
        InProgress,
        Ended
    }
    ElectionState public electionState;

    struct Candidate {
        uint id;
        string name;
        uint voteCount;
    }

    struct Voter {
        bool isRegistered;
        bool hasVoted;
        uint vote;
    }

    mapping(uint => Candidate) public candidates;
    uint public candidatesCount;

    mapping(address => Voter) public voters;

    event ElectionStarted();
    event ElectionEnded();
    event CandidateAdded(uint candidateId, string name);
    event VoterRegistered(address registeredBy, address voter);
    event VoteCasted(address voter, uint candidateId);

    modifier onlyAdmin() {
        require(msg.sender == admin, "Only admin can perform this action");
        _;
    }

    modifier onlyDuringElection() {
        require(
            electionState == ElectionState.InProgress,
            "Election is not active"
        );
        _;
    }

    constructor() {
        admin = msg.sender;
        electionState = ElectionState.NotStarted;
    }

    function addCandidate(string memory _name) public onlyAdmin {
        require(
            electionState == ElectionState.NotStarted,
            "Cannot add candidates after election starts"
        );
        candidatesCount++;
        candidates[candidatesCount] = Candidate(candidatesCount, _name, 0);
        emit CandidateAdded(candidatesCount, _name);
    }

    function registerVoter(address _voter) public {
        require(!voters[_voter].isRegistered, "Voter already registered");
        voters[_voter] = Voter(true, false, 0);
        emit VoterRegistered(msg.sender, _voter);
    }

    function startElection() public onlyAdmin {
        require(
            electionState == ElectionState.NotStarted,
            "Election already started or ended"
        );
        electionState = ElectionState.InProgress;
        emit ElectionStarted();
    }

    function vote(uint _candidateId) public onlyDuringElection {
        require(
            voters[msg.sender].isRegistered,
            "You are not registered to vote"
        );
        require(!voters[msg.sender].hasVoted, "You have already voted");
        require(
            _candidateId > 0 && _candidateId <= candidatesCount,
            "Invalid candidate ID"
        );

        voters[msg.sender].hasVoted = true;
        voters[msg.sender].vote = _candidateId;

        candidates[_candidateId].voteCount++;

        emit VoteCasted(msg.sender, _candidateId);
    }

    function endElection() public onlyAdmin {
        require(
            electionState == ElectionState.InProgress,
            "Election is not in progress"
        );
        electionState = ElectionState.Ended;
        emit ElectionEnded();
    }

    function getResults(
        uint _candidateId
    ) public view returns (string memory, uint) {
        require(electionState == ElectionState.Ended, "Election has not ended");
        Candidate storage candidate = candidates[_candidateId];
        return (candidate.name, candidate.voteCount);
    }
}

