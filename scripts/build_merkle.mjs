#!/usr/bin/env node
// Build the UwU GF guest-list merkle tree (OpenZeppelin MerkleProof compatible:
// leaf = keccak256(abi.encodePacked(address)), pairs hashed sorted).
//
//   node build_merkle.mjs <addresses.txt> <out-proofs.json>
//
// Prints the root (feed to setGuestList) and writes { root, proofs } for the site.
import { readFileSync, writeFileSync } from "node:fs";
import { ethers } from "ethers";

const [addrFile, outFile] = process.argv.slice(2);
if (!addrFile || !outFile) {
  console.error("usage: node build_merkle.mjs <addresses.txt> <out-proofs.json>");
  process.exit(1);
}

const addrs = readFileSync(addrFile, "utf8")
  .split("\n").map((l) => l.trim()).filter((l) => l && !l.startsWith("#"))
  .map((a) => ethers.getAddress(a)); // checksums + validates

const dedup = [...new Set(addrs.map((a) => a.toLowerCase()))];
const leaves = dedup.map((a) => ethers.solidityPackedKeccak256(["address"], [a]));

const pairHash = (a, b) =>
  ethers.keccak256(a.toLowerCase() < b.toLowerCase() ? ethers.concat([a, b]) : ethers.concat([b, a]));

// build levels bottom-up; odd node is carried up unhashed (OZ-style)
const levels = [leaves];
while (levels[0].length > 1) {
  const prev = levels[0];
  const next = [];
  for (let i = 0; i < prev.length; i += 2) {
    next.push(i + 1 < prev.length ? pairHash(prev[i], prev[i + 1]) : prev[i]);
  }
  levels.unshift(next);
}
const root = levels[0][0];

const proofFor = (leafIdx) => {
  const proof = [];
  let idx = leafIdx;
  for (let lv = levels.length - 1; lv > 0; lv--) {
    const nodes = levels[lv];
    const sib = idx ^ 1;
    if (sib < nodes.length) proof.push(nodes[sib]);
    idx = Math.floor(idx / 2);
  }
  return proof;
};

const proofs = Object.fromEntries(dedup.map((a, i) => [a, proofFor(i)]));
writeFileSync(outFile, JSON.stringify({ root, count: dedup.length, proofs }, null, 2));
console.log("guest list root:", root);
console.log("addresses:", dedup.length, "→", outFile);
