#!/usr/bin/env python3
"""Local JSON-RPC proxy for Robinhood Chain, for networks whose ISP DNS-blocks
*.robinhood.com (MyRepublic ID resolves every host to 158.140.186.3).

The endpoints themselves are reachable — only the DNS answer is poisoned — so we
resolve the hostname ourselves and keep the real Host/SNI so Cloudflare routes it.
Two gotchas baked in: the upstream 403s on a default Python user-agent, and the
IPs move, so they're re-resolved over DNS-over-HTTPS at startup rather than pinned.

    python3 scripts/rh_rpc_proxy.py --net testnet --port 8546
    ROBINHOOD_TESTNET_RPC_URL=http://127.0.0.1:8546 ./scripts/deploy_robinhood.sh testnet

Also fronts the Blockscout explorer, so contract verification works from a
blocked network too:

    python3 scripts/rh_rpc_proxy.py --net explorer-testnet --port 8548
    forge verify-contract <addr> src/UwUGF.sol:UwUGF --root contract \
      --chain-id 46630 --verifier blockscout --verifier-url http://127.0.0.1:8548/api/

Dev convenience only. Don't point the public mint page at this — use the real
endpoint, or the unblocked mirror https://rpc.arrowrpc.com for mainnet.
"""
import argparse, json, socket, sys, urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

UPSTREAM = {
    "mainnet": "rpc.mainnet.chain.robinhood.com",
    "testnet": "rpc.testnet.chain.robinhood.com",
    "explorer-mainnet": "robinhoodchain.blockscout.com",
    "explorer-testnet": "explorer.testnet.chain.robinhood.com",
}
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0 Safari/537.36")


def resolve_via_doh(host):
    """Ask Cloudflare over HTTPS, since port-53 answers here are poisoned."""
    req = urllib.request.Request(
        f"https://cloudflare-dns.com/dns-query?name={host}&type=A",
        headers={"accept": "application/dns-json", "user-agent": UA},
    )
    answers = json.loads(urllib.request.urlopen(req, timeout=20).read())["Answer"]
    ips = [a["data"] for a in answers if a.get("type") == 1]
    if not ips:
        sys.exit(f"DoH returned no A record for {host}")
    return ips[0]


def install_resolver(host, ip):
    original = socket.getaddrinfo

    def patched(h, port, *args, **kwargs):
        return original(ip if h == host else h, port, *args, **kwargs)

    socket.getaddrinfo = patched


def make_handler(host):
    class Handler(BaseHTTPRequestHandler):
        protocol_version = "HTTP/1.1"

        def _forward(self, method):
            # Path and query are preserved, so this also fronts Blockscout's
            # /api?module=contract&action=... verification endpoints, not just JSON-RPC.
            body = self.rfile.read(int(self.headers.get("content-length", 0) or 0)) or None
            headers = {"user-agent": UA, "accept": "*/*"}
            if ct := self.headers.get("content-type"):
                headers["content-type"] = ct
            req = urllib.request.Request(f"https://{host}{self.path}", data=body,
                                         method=method, headers=headers)
            try:
                resp = urllib.request.urlopen(req, timeout=120)
                payload, code = resp.read(), resp.status
                ctype = resp.headers.get("content-type", "application/json")
            except urllib.error.HTTPError as exc:      # pass upstream errors through verbatim
                payload, code = exc.read(), exc.code
                ctype = exc.headers.get("content-type", "application/json")
            except Exception as exc:
                payload = json.dumps({"jsonrpc": "2.0", "id": None,
                                      "error": {"code": -32603, "message": f"proxy: {exc}"}}).encode()
                code, ctype = 502, "application/json"
            self.send_response(code)
            self.send_header("content-type", ctype)
            self.send_header("content-length", str(len(payload)))
            self.end_headers()
            self.wfile.write(payload)

        do_POST = lambda self: self._forward("POST")
        do_GET = lambda self: self._forward("GET")

        def log_message(self, *args):
            pass  # forge is chatty enough

    return Handler


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--net", choices=UPSTREAM, default="testnet")
    ap.add_argument("--port", type=int, default=8546)
    args = ap.parse_args()

    host = UPSTREAM[args.net]
    ip = resolve_via_doh(host)
    install_resolver(host, ip)
    print(f"{host} -> {ip}; proxying http://127.0.0.1:{args.port}", flush=True)
    ThreadingHTTPServer(("127.0.0.1", args.port), make_handler(host)).serve_forever()
