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
    // NOT the official rpc.mainnet.chain.robinhood.com: some ISPs (MyRepublic ID
    // among them) DNS-block *.robinhood.com, which would break the mint page AND
    // the visitor's wallet. This mirror serves the same chain 4663 from an
    // unblocked domain. Still shared + rate limited, and the page polls every 15s,
    // so buy a dedicated endpoint (chainstack / quicknode / dwellir) before mint day.
    rpc: "https://robinhood.drpc.org",
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
    contract: "0xaab5a750ed652117ad4856782c11e2891db5794a",
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
