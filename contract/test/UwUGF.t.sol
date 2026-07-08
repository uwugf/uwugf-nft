// SPDX-License-Identifier: MIT
pragma solidity ^0.8.23;

import "forge-std/Test.sol";
import "../src/UwUGF.sol";

contract UwUGFTest is Test {
    UwUGF gf;
    address owner = address(this);
    address alice = makeAddr("alice");
    address bob   = makeAddr("bob");

    function setUp() public {
        gf = new UwUGF("ipfs://hidden/hidden.json", owner);
        vm.deal(alice, 10 ether);
        vm.deal(bob, 10 ether);
    }

    function test_publicMint() public {
        gf.openHerHeart(false, true); // public on
        // two-arg prank sets msg.sender AND tx.origin (sheIsReal rejects tx.origin != msg.sender)
        vm.prank(alice, alice);
        gf.mint{value: 0.001 ether * 2}(2);
        assertEq(gf.balanceOf(alice), 2);
        assertEq(gf.ownerOf(1), alice);
    }

    function test_publicMint_revertsWhenClosed() public {
        vm.prank(alice, alice);
        vm.expectRevert("her heart isn't open yet");
        gf.mint{value: 0.001 ether}(1);
    }

    function test_publicMint_revertsUnderpaid() public {
        gf.openHerHeart(false, true);
        vm.prank(alice, alice);
        vm.expectRevert("send more love (eth)");
        gf.mint{value: 0.00069 ether}(1);
    }

    function test_publicCap() public {
        gf.openHerHeart(false, true);
        vm.prank(alice, alice);
        vm.expectRevert("leave some for others anon");
        gf.mint{value: 0.001 ether * 11}(11); // maxPerDegen = 10
    }

    function test_whitelistMint_singleLeafTree() public {
        // for a 1-address tree, root == leaf and the proof is empty
        bytes32 leaf = keccak256(abi.encodePacked(alice));
        gf.setGuestList(leaf);
        gf.openHerHeart(true, false); // wl on
        bytes32[] memory proof = new bytes32[](0);
        vm.prank(alice, alice);
        gf.uwuList{value: 0.00069 ether * 3}(proof, 3);
        assertEq(gf.balanceOf(alice), 3);
    }

    function test_whitelistMint_rejectsNonMember() public {
        bytes32 leaf = keccak256(abi.encodePacked(alice));
        gf.setGuestList(leaf);
        gf.openHerHeart(true, false);
        bytes32[] memory proof = new bytes32[](0);
        vm.prank(bob, bob);
        vm.expectRevert("you're not on the list");
        gf.uwuList{value: 0.00069 ether}(proof, 1);
    }

    function test_reveal() public {
        gf.openHerHeart(false, true);
        vm.prank(alice, alice);
        gf.mint{value: 0.001 ether}(1);
        assertEq(gf.tokenURI(1), "ipfs://hidden/hidden.json");
        gf.glowUp("ipfs://realCID/");
        assertEq(gf.tokenURI(1), "ipfs://realCID/1.json");
    }

    function test_devReserveCap() public {
        vm.expectRevert("over the reserve");
        gf.devUwu(owner, 170); // TEAM_RESERVE = 169
    }

    function test_provenancePinkySwearOnce() public {
        gf.pinkySwear("abc123");
        assertEq(gf.provenance(), "abc123");
        vm.expectRevert("already promised");
        gf.pinkySwear("def456");
    }

    function test_withdrawLove() public {
        gf.openHerHeart(false, true);
        vm.prank(alice, alice);
        gf.mint{value: 0.001 ether}(1);
        gf.setLoveJar(bob);
        uint256 before = bob.balance;
        gf.withdrawLove();
        assertEq(bob.balance, before + 0.001 ether);
    }

    function test_royaltyInfo() public view {
        (address recv, uint256 amt) = gf.royaltyInfo(1, 1 ether);
        assertEq(recv, owner);
        assertEq(amt, 0.069 ether); // 6.9%
    }
}
