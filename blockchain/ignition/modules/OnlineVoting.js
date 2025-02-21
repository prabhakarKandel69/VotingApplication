const { buildModule } = require("@nomicfoundation/hardhat-ignition/modules");

module.exports = buildModule("OnlineVoting", (m) => {
  // Define voting period
  const votingStartTime = Math.floor(Date.now() / 1000) + 3600; // 1 hour from now (in seconds)
  const votingEndTime = votingStartTime + 86400; // Voting lasts 24 hours (in seconds)

  console.log("Deploying OnlineVoting...");
  console.log("Voting Start Time (Unix):", votingStartTime);
  console.log("Voting End Time (Unix):", votingEndTime);

  // Deploy the OnlineVoting contract with constructor arguments
  const voting = m.contract("OnlineVoting", [votingStartTime, votingEndTime]);

  return { voting };
});
