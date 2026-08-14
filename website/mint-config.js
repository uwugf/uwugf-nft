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
    // public rpc is shared + rate limited — swap for a dedicated endpoint
    // (chainstack / quicknode / dwellir) before mint day, the site polls every 15s.
    rpc: "https://rpc.mainnet.chain.robinhood.com",
    explorer: "https://robinhoodchain.blockscout.com",
    nativeCurrency: { name: "Ether", symbol: "ETH", decimals: 18 },
    // token/collection viewers — {contract}/{id} are templated in by the page.
    // Blockscout is the chain's official explorer and indexes ERC-721 natively.
    // If a marketplace lists us later, point collectionUrl/tokenUrl at it instead.
    collectionUrl: "https://robinhoodchain.blockscout.com/token/{contract}",
    tokenUrl: "https://robinhoodchain.blockscout.com/token/{contract}/instance/{id}",
  },

  // ── Robinhood Chain testnet — play money, same code path ──
  robinhoodTestnet: {
    chainId: 46630,
    chainHex: "0xb626",
    chainName: "Robinhood Chain Testnet",
    isTestnet: true,
    contract: "",
    rpc: "https://rpc.testnet.chain.robinhood.com",
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
