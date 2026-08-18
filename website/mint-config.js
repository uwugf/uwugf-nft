// UwU GF mint page config.
//
// Chain: Robinhood Chain — an EVM L2 that pays gas in ETH, so the contract,
// the wallet flow and the prices all carry over from L1 unchanged.
//   mainnet  chainId 4663   rpc.mainnet.chain.robinhood.com
//   testnet  chainId 46630  rpc.testnet.chain.robinhood.com
//
// One switch (UWUGF_ACTIVE, below) flips the whole site between networks.
// The deploy script injects the deployed address into the matching block.

const UWUGF_NETWORKS = {
  // ── Robinhood Chain mainnet — real money ──
  robinhood: {
    chainId: 4663,
    chainHex: "0x1237",
    chainName: "Robinhood Chain",
    isTestnet: false,
    contract: "", // filled by scripts/deploy_robinhood.sh
    // Dedicated Alchemy endpoint, origin-locked to uwugf.xyz in the Alchemy
    // dashboard — the key is public by necessity (this file ships to browsers),
    // so the domain allowlist is what protects the quota. Deliberately NOT the
    // official rpc.mainnet.chain.robinhood.com: some ISPs (MyRepublic ID among
    // them) DNS-block *.robinhood.com, which would break both the mint page and
    // the visitor's own wallet.
    // Server-side callers (forge/cast) CANNOT use this URL — they send no Origin
    // and Alchemy rejects them. They use ROBINHOOD_RPC_URL from contract/.env.
    rpc: "https://robinhood-mainnet.g.alchemy.com/v2/alch_VsdmGJeNplEfTmeDBMZcd",
    explorer: "https://robinhoodchain.blockscout.com",
    nativeCurrency: { name: "Ether", symbol: "ETH", decimals: 18 },
    // token/collection viewers — {contract}/{id} are templated in by the page.
    // OpenSea lists Robinhood Chain as chain slug "robinhood" (confirmed against
    // their live /api/v2/chains), so secondary lives there. Blockscout stays the
    // explorer for the contract itself.
    collectionUrl: "https://opensea.io/assets/robinhood/{contract}",
    tokenUrl: "https://opensea.io/assets/robinhood/{contract}/{id}",
  },

  // ── Robinhood Chain testnet — play money, same code path ──
  robinhoodTestnet: {
    chainId: 46630,
    chainHex: "0xb626",
    chainName: "Robinhood Chain Testnet",
    isTestnet: true,
    contract: "0xfce1d7fcb0bfb2a846c7f4feb613c7a419215ab6",
    rpc: "https://robinhood-testnet.drpc.org", // unblocked mirror, see the mainnet note above

    explorer: "https://explorer.testnet.chain.robinhood.com",
    nativeCurrency: { name: "Ether", symbol: "ETH", decimals: 18 },
    collectionUrl: "https://explorer.testnet.chain.robinhood.com/token/{contract}",
    tokenUrl: "https://explorer.testnet.chain.robinhood.com/token/{contract}/instance/{id}",
  },
};

// ⚠️ flip to "robinhood" only after the testnet dress rehearsal passes.
const UWUGF_ACTIVE = "robinhoodTestnet";

window.UWUGF_CONFIG = Object.assign(
  {
    wlProofsUrl: "wl/proofs.json", // { root, proofs: { "0xaddr": [..] } }
    network: UWUGF_ACTIVE,
  },
  UWUGF_NETWORKS[UWUGF_ACTIVE],
);
