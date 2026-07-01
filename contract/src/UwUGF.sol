// SPDX-License-Identifier: MIT
pragma solidity ^0.8.23;

/*
 ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
 ░░                                                                  ░░
 ░░    █  █ █   █ █  █   █     ▄████  ███████                        ░░
 ░░    █  █ █ █ █ █  █   █     █      █          ♡  u w u   g f  ♡    ░░
 ░░    █▄▄█ █▄▀▄█ █▄▄█   ▀▄▄▄▀ █▄███  █                              ░░
 ░░                                                                  ░░
 ░░         ( ｡♥‿♥｡ )   6969 hand-drawn girlfriends, on-chain         ░░
 ░░                                                                  ░░
 ░░    she's cute · she's degen · she's kinda your exit liquidity    ░░
 ░░    wl 0.00069Ξ  ·  public 0.001Ξ  ·  6.9% royalties  ·  wgmi     ░░
 ░░                                                                  ░░
 ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
*/

import "erc721a/contracts/ERC721A.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/cryptography/MerkleProof.sol";
import "@openzeppelin/contracts/token/common/ERC2981.sol";

/// @title  UwU GF
/// @notice 6969 cute degen girlfriends. ERC721A + Merkle whitelist + on-chain
///         provenance + EIP-2981 royalties. Cute on the outside, audited-clean
///         on the inside — no hidden mints, supply is capped & immutable. ♡
contract UwUGF is ERC721A, ERC2981, Ownable {
    // ───────────────────────── immutable promises ─────────────────────────
    uint256 public constant MAX_CUTIES   = 6969;  // hard supply cap (immutable)
    uint256 public constant TEAM_RESERVE = 100;   // team + 1/1s + KOL gifts cap

    // ───────────────────────────── tunable knobs ──────────────────────────
    uint256 public uwuListPrice = 0.00069 ether;    // whitelist (cheaper, bestie ♡)
    uint256 public publicPrice  = 0.001 ether;   // public
    uint256 public maxPerUwu    = 3;              // per-wallet whitelist cap
    uint256 public maxPerDegen  = 10;             // per-wallet public cap

    bytes32 public guestList;                     // whitelist merkle root
    bool    public uwuListOpen;                   // whitelist phase live?
    bool    public heartsOpen;                    // public phase live?
    bool    public revealed;                      // art revealed?
    uint256 public teamMinted;                    // counts against TEAM_RESERVE

    string  public provenance;                    // sha256 of the image set
    address public loveJar;                       // withdrawal payout address

    string  private _hiddenURI;                   // pre-reveal metadata (single uri)
    string  private _revealedURI;                 // post-reveal base uri (ipfs://CID/)

    mapping(address => uint256) public uwuMinted;   // wl minted per wallet
    mapping(address => uint256) public degenMinted; // public minted per wallet

    event Adopted(address indexed degen, uint256 quantity, bool whitelist);
    event GlowUp(string baseURI);

    constructor(string memory hiddenURI_, address royaltyReceiver)
        ERC721A("UwU GF", "UWUGF")
        Ownable(msg.sender)
    {
        _hiddenURI = hiddenURI_;
        loveJar = msg.sender;
        _setDefaultRoyalty(royaltyReceiver, 690); // 6.9% — on theme ♡
    }

    // ─────────────────────────────── minting ──────────────────────────────

    modifier sheIsReal(uint256 qty) {
        require(qty > 0, "mint at least one bestie");
        require(tx.origin == msg.sender, "no bots allowed uwu");      // anti-bot
        require(_totalMinted() + qty <= MAX_CUTIES, "she's all gone :(");
        _;
    }

    /// @notice whitelist mint — you sweet-talked your way onto the guest list ♡
    function uwuList(bytes32[] calldata proof, uint256 qty)
        external
        payable
        sheIsReal(qty)
    {
        require(uwuListOpen, "guest list not open yet");
        require(uwuMinted[msg.sender] + qty <= maxPerUwu, "don't be greedy uwu");
        bytes32 leaf = keccak256(abi.encodePacked(msg.sender));
        require(MerkleProof.verify(proof, guestList, leaf), "you're not on the list");
        require(msg.value >= uwuListPrice * qty, "send more love (eth)");
        uwuMinted[msg.sender] += qty;
        _mint(msg.sender, qty);
        emit Adopted(msg.sender, qty, true);
    }

    /// @notice public mint — adopt your UwU GF
    function adopt(uint256 qty) external payable sheIsReal(qty) {
        require(heartsOpen, "her heart isn't open yet");
        require(degenMinted[msg.sender] + qty <= maxPerDegen, "leave some for others anon");
        require(msg.value >= publicPrice * qty, "send more love (eth)");
        degenMinted[msg.sender] += qty;
        _mint(msg.sender, qty);
        emit Adopted(msg.sender, qty, false);
    }

    /// @notice owner mint for team, 1/1s & KOL gifts — capped by TEAM_RESERVE
    function devUwu(address to, uint256 qty) external onlyOwner {
        require(teamMinted + qty <= TEAM_RESERVE, "over the reserve");
        require(_totalMinted() + qty <= MAX_CUTIES, "she's all gone :(");
        teamMinted += qty;
        _mint(to, qty);
    }

    // ─────────────────────────────── reveal ───────────────────────────────

    function tokenURI(uint256 tokenId) public view override returns (string memory) {
        require(_exists(tokenId), "she doesn't exist");
        if (!revealed) return _hiddenURI;
        return string(abi.encodePacked(_revealedURI, _toString(tokenId), ".json"));
    }

    /// @notice the big reveal — let her glow up ✨ (set the real ipfs base uri)
    function glowUp(string calldata revealedBaseURI) external onlyOwner {
        _revealedURI = revealedBaseURI;
        revealed = true;
        emit GlowUp(revealedBaseURI);
    }

    function setHiddenLook(string calldata hiddenURI_) external onlyOwner {
        _hiddenURI = hiddenURI_;
    }

    // ───────────────────────────── owner knobs ────────────────────────────

    /// @notice flip the mint phases ( whitelist , public )
    function openHerHeart(bool wl_, bool public_) external onlyOwner {
        uwuListOpen = wl_;
        heartsOpen = public_;
    }

    function setGuestList(bytes32 root) external onlyOwner {
        guestList = root;
    }

    function setBagPrices(uint256 wl, uint256 pub) external onlyOwner {
        uwuListPrice = wl;
        publicPrice = pub;
    }

    function setCaps(uint256 wl, uint256 pub) external onlyOwner {
        maxPerUwu = wl;
        maxPerDegen = pub;
    }

    /// @notice lock in the provenance hash once, before reveal — pinky swear ♡
    function pinkySwear(string calldata provenance_) external onlyOwner {
        require(bytes(provenance).length == 0, "already promised");
        provenance = provenance_;
    }

    function setLoveJar(address jar) external onlyOwner {
        require(jar != address(0), "no burning love");
        loveJar = jar;
    }

    function setRoyalty(address receiver, uint96 bps) external onlyOwner {
        _setDefaultRoyalty(receiver, bps);
    }

    /// @notice withdraw the love (eth) to the love jar
    function withdrawLove() external onlyOwner {
        uint256 bal = address(this).balance;
        (bool ok, ) = loveJar.call{value: bal}("");
        require(ok, "withdraw failed");
    }

    // ────────────────────────────── plumbing ──────────────────────────────

    function _startTokenId() internal pure override returns (uint256) {
        return 1; // gf #1 .. gf #6969
    }

    function supportsInterface(bytes4 id)
        public
        view
        override(ERC721A, ERC2981)
        returns (bool)
    {
        return ERC721A.supportsInterface(id) || ERC2981.supportsInterface(id);
    }
}
