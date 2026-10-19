# B.I.T. — Better Items Trading · Blockchain Item Trading Platform

A concept-demo peer-to-peer trading platform for virtual game items, built as a final-year project (Hong Kong Metropolitan University, 2025) by CHAN Man Kit and CHEUNG Ka Hin.

All platform logic lives in this repository: Flask backend, web frontend, smart contracts, and demo scripts. (The contracts are also mirrored in the [BIT](https://github.com/MikeC-08/BIT) repo for reference.)

## What it does

- **Browse & search** game-asset listings by name or contract address, with live on-chain price, availability, and owner
- **Asset detail pages** — price, owner, settlement currency, platform fee, plus a 12-month average trade-price graph generated from on-chain events
- **Asset generation ("gacha")** — mint new FPS game-skin assets: metadata is created, uploaded (simulated IPFS), and deployed as a new asset contract
- **Wallet-direct trading** — purchases are signed in the user's own MetaMask; the server never sees private keys or routes funds

## Design philosophy

**Non-custodial by design.** The server's job is to *provide transaction scripts* to the browser and *track* asset state — it never intervenes in trades:

- Every Flask page pushes its logic to the user's browser, where MetaMask (via embedded web3.js) signs transactions directly against the contracts
- The server only records which assets were created and syncs their on-chain status into its registry
- Platform revenue is a fee in ETH, enforced by the contract itself (`platform_fee_eth`)
- The settlement token is an ERC-20 chosen by the contract owner — because ownership and trading live entirely on-chain, users keep full control of their items even if the platform goes offline

## Architecture

<img width="900" height="603" alt="image" src="https://github.com/user-attachments/assets/5ef2ee15-c724-49cc-a9e6-ea525d446b9d" />
<img width="900" height="512" alt="image" src="https://github.com/user-attachments/assets/268c0aa7-e4cb-460e-ac66-cc11428ee60e" />


## Repository layout

| Path | Purpose |
|---|---|
| `server.py` | Flask app: routes for browse/search (`/`), asset detail (`/detail`), asset generation (`/gacha`), allowance check (`/check_approve`) |
| `function/contract.py` | web3.py contract interactions (deploy, price/owner/allowance queries, event reads) |
| `function/assetGenerator.py` | Generates game-asset metadata (e.g. FPS skins) |
| `function/dataScript.py` | Loads/saves/searches the local asset registry (`data.json`) |
| `function/IPFS_simulate.py` | Simulated IPFS upload for the demo |
| `contracts/` | Solidity contracts: `GameAsset.sol` (ERC-721), `USDC.sol` / `USDT.sol` / `FiatTokenV1.sol` (settlement tokens) |
| `templates/` + `static/` | Web frontend (web3.js embedded — MetaMask needs zero configuration) |
| `data.json` | Runtime config + local asset registry (see below) |
| `Server.bat` | Demo launcher (`server.py`) |

## Configuration & running the demo

1. **Fill in `data.json`** (replace the test addresses left from development):
   - `init.BIT_owner` — must be the address that **owns** the BIT contract
   - `BIT_address` — leave unset and the server will deploy the BIT contract automatically on startup
   - `settings.TestMode` — selects which token config (`test` / `normal`) is active
   - `test.defaultAddress` / `normal.defaultAddress` — the ERC-20 used for settlement in each mode
2. **Put the deployer's private key in `.env`** (required for auto-deploy)
3. **Run `Server.bat`** (or `python server.py`) — the server detects whether the BIT contract exists and deploys it if needed, then serves the frontend
4. **Open in a browser with MetaMask** — no MetaMask configuration is required; connection logic is already in the pages' web3.js. The server never learns your wallet.

> Note: this is a concept demonstration. `data.json` still contains test addresses from development — the deployer is expected to replace them.

## Tech stack

Python · Flask 3.1 · web3.py 7.8 · Solidity · JavaScript + MetaMask
