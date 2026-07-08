// UwU GF mint page config — swap these when moving testnet → mainnet.
// Deployed contract address is injected here after each deploy.
window.UWUGF_CONFIG = {
  chainId: 11155111,                      // Sepolia (mainnet = 1)
  chainHex: "0xaa36a7",
  chainName: "Sepolia",
  isTestnet: true,
  contract: "0x9fdA76223560fEBf5D36C8Af3D80Ee500206c294",                           // filled by deploy step
  rpc: "https://sepolia.gateway.tenderly.co",
  explorer: "https://sepolia.etherscan.io",
  // token/collection viewers — {contract}/{id} are templated in by the page.
  // testnet: Blockscout (OpenSea killed testnets); prod swap →
  //   collectionUrl: "https://opensea.io/assets/ethereum/{contract}"
  //   tokenUrl:      "https://opensea.io/assets/ethereum/{contract}/{id}"
  collectionUrl: "https://eth-sepolia.blockscout.com/token/{contract}",
  tokenUrl: "https://eth-sepolia.blockscout.com/token/{contract}/instance/{id}",
  wlProofsUrl: "wl/proofs.json",          // { root, proofs: { "0xaddr": [..] } }
};
