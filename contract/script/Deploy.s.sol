// SPDX-License-Identifier: MIT
pragma solidity ^0.8.23;

import "forge-std/Script.sol";
import "../src/UwUGF.sol";

/// @notice Deploys UwU GF.
///   env:  HIDDEN_URI         pre-reveal metadata uri (ipfs://CID/hidden.json)
///         ROYALTY_RECEIVER   address that receives 6.9% royalties
///         PRIVATE_KEY        deployer key
///
/// e.g.  forge script script/Deploy.s.sol:Deploy \
///         --rpc-url mainnet --broadcast --verify -vvvv
contract Deploy is Script {
    function run() external {
        string memory hiddenURI = vm.envString("HIDDEN_URI");
        address royaltyReceiver = vm.envAddress("ROYALTY_RECEIVER");
        uint256 pk = vm.envUint("PRIVATE_KEY");

        vm.startBroadcast(pk);
        UwUGF gf = new UwUGF(hiddenURI, royaltyReceiver);
        vm.stopBroadcast();

        console2.log("UwU GF deployed at:", address(gf));
        console2.log("owner / loveJar:", gf.owner());
        console2.log("next: setGuestList(root) -> openHerHeart(true,false) -> mint -> glowUp(baseURI)");
    }
}
