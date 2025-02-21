const OnlineVoting = artifacts.require("OnlineVoting");

module.exports = function (deployer) {
    deployer.deploy(OnlineVoting);
};
