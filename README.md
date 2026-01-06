# ⛓️ Blockchain & Distributed Ledger System

[![Python](https://img.shields.io/badge/Python-3.x-blue?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-Web%20Framework-green?style=flat-square&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Blockchain](https://img.shields.io/badge/Blockchain-Proof%20of%20Work-orange?style=flat-square&logo=bitcoin&logoColor=white)](https://en.wikipedia.org/wiki/Proof_of_work)
[![SHA256](https://img.shields.io/badge/Hashing-SHA256-yellow?style=flat-square)](https://en.wikipedia.org/wiki/SHA-2)
[![REST API](https://img.shields.io/badge/API-RESTful-red?style=flat-square&logo=api&logoColor=white)](.)
[![License](https://img.shields.io/badge/License-Open%20Source-success?style=flat-square)](LICENSE)

> 🚀 A complete blockchain implementation from scratch featuring Proof-of-Work consensus, distributed ledger synchronization, and production-grade REST API.

---

## 🎯 Features

| Feature | Description |
|---------|-------------|
| ⛏️ **Proof-of-Work Mining** | SHA-256 based algorithm with configurable difficulty (1, 2, ..., n) |
| 🔗 **Blockchain Core** | Genesis block, chaining, and hash validation |
| 🌳 **Merkle Trees** | Transaction integrity verification |
| 💰 **Transaction Management** | Mempool-based pipeline with wallet support |
| 🎁 **Mining Rewards** | Automatic miner compensation system |
| 👛 **User Wallets** | UUID-based generation & persistent history |
| 🌐 **REST API** | Complete Flask API with 6 endpoints |
| 🔀 **Distributed Consensus** | Multi-node sync & conflict resolution |
| ✅ **Chain Validation** | Block integrity, hash continuity, PoW verification |

---

## 🛠️ Technology Stack

```
┌─────────────────────────────────┐
│   Technology Stack              │
├─────────────────────────────────┤
│ 🐍 Backend       → Python 3.x   │
│ 🌶️ Framework     → Flask        │
│ 🔐 Hashing       → SHA-256      │
│ 🏗️ Architecture  → REST API     │
│ 🔄 Pattern       → Distributed  │
│ 📊 Consensus     → PoW + LoC    │
└─────────────────────────────────┘
```

---

## 📁 Project Structure

```
blockchain-flutter-task/
│
├── 🔐 main.py          # Core blockchain logic
├── 🌐 app.py           # Flask API (Node 1 - Port 5000)
├── 🌐 app2.py          # Flask API (Node 2 - Port 5001)
└── 📖 README.md        # Documentation
```

---

## ⚙️ Installation & Setup

### 📋 Prerequisites
```bash
pip install flask requests
```

### 🚀 Running the Blockchain

**Start Node 1 (Port 5000):**
```bash
python app.py
```

**Start Node 2 (Port 5001):**
```bash
python app2.py
```

> ✅ Both nodes should output: `Running on http://0.0.0.0:5000` and `http://0.0.0.0:5001`

---

## 🔌 API Endpoints

### 1️⃣ Create Transaction
```bash
POST /transactions/new
Content-Type: application/json

{
  "sender": "alice",
  "recipient": "bob",
  "amount": 50
}
```
**📤 Response:**
```json
{
  "message": "the transaction will go to block 1"
}
```

### 2️⃣ Mine Block
```bash
GET /mine
```
**📤 Response:**
```json
{
  "message": "New block mined",
  "index": 1,
  "transactions": [...],
  "merkle_root": "abc123...",
  "nonce": 12345,
  "hash": "0000abc...",
  "previous_hash": "...",
  "reward": 5,
  "miner": "alice",
  "miner_wallet": "..."
}
```

### 3️⃣ Get Transaction History
```bash
GET /transactions/history/<user>
```
**📤 Response:**
```json
{
  "addres": "alice",
  "wallet": "abc123def456...",
  "transactions": [
    {
      "sender": "alice_wallet",
      "recipient": "bob_wallet",
      "amount": 50
    }
  ]
}
```

### 4️⃣ Get Full Blockchain
```bash
GET /chain
```
**📤 Response:**
```json
{
  "chain": [...],
  "length": 3
}
```

### 5️⃣ Register Node
```bash
POST /nodes/register
Content-Type: application/json

{
  "nodes": ["http://localhost:5000", "http://localhost:5001"]
}
```

### 6️⃣ Consensus/Resolve Conflicts
```bash
GET /node/resolve
```

---

## ⚙️ How It Works

### ⛏️ Mining Process
```
1️⃣  Pending transactions → mempool
2️⃣  Random miner selection from participants
3️⃣  Mining reward (5 tokens) added
4️⃣  PoW algorithm searches for valid hash:
    • Hash starts with N zeros (difficulty)
    • Hash ends with for example "09" or any other value that you can set in code 
5️⃣  New block added to chain
6️⃣  Mempool cleared for next block
```

### 🔐 Blockchain Validation
- ✅ Each block contains hash of previous block
- ✅ Hash integrity verified through recalculation
- ✅ Proof-of-Work difficulty validated
- ✅ Merkle root ensures transaction integrity

### 🔄 Consensus Mechanism
- 📡 Nodes register other nodes in network
- 📊 Each node maintains chain copy
- 🔀 On `/node/resolve`:
  - Request chains from all nodes
  - Validate each received chain
  - Adopt longest valid chain (LoC rule)
  - Return replacement status

---

## 🧪 Example Workflow

```bash
# 🖥️ Terminal 1 - Start Node 1
python app.py

# 🖥️ Terminal 2 - Start Node 2  
python app2.py

# 🖥️ Terminal 3 - Make transactions
curl -X POST http://localhost:5000/transactions/new \
  -H "Content-Type: application/json" \
  -d '{"sender":"alice","recipient":"bob","amount":50}'

# ⛏️ Mine block on Node 1
curl http://localhost:5000/mine

# 🔗 Register nodes
curl -X POST http://localhost:5000/nodes/register \
  -H "Content-Type: application/json" \
  -d '{"nodes":["http://localhost:5001"]}'

# 🔄 Resolve conflicts
curl http://localhost:5000/node/resolve

# 📊 View blockchain
curl http://localhost:5000/chain
```

---

## 🔍 Key Implementation Details

### 📦 Block Structure
```python
{
  "index": 0,                          # Block number
  "timestamp": 1704571200.123,         # Creation time
  "transactions": [...],               # Tx list
  "merkle_root": "hash...",            # Root hash
  "previous_hash": "hash...",          # Previous block hash
  "nonce": 99999,                      # Proof-of-Work value
  "hash": "0000abc..."                 # Block hash
}
```

### 💸 Transaction Structure
```python
{
  "sender": "wallet_id",               # From
  "recipient": "wallet_id",            # To
  "amount": 50                         # Value
}
```

### 🏗️ Genesis Block
| Property | Value |
|----------|-------|
| Index | 0 |
| Previous Hash | "**genesis_hash_root**" |
| Data | "Genesis Block" |
| Pre-mined Nonce | "**99999**" |

---

# ⚡ Performance Metrics

| Difficulty | Time | Hardware Impact | Practical Use |
|-----------|------|-----------------|---|
| **3** | ⚡ ~50ms | Instant | ✅ Testing |
| **4** | 🔥 1-5s | Standard | ✅ Demo |
| **5** | 🔥🔥 5-30s | Intensive | ✅ Learning |
| **8** | 🔥🔥🔥🔥🔥 ~2-5h | Extreme | ❌ Not Recommended |
| **10** | 💀 ~10-20 days | Prohibitive | ❌ Impossible |
| **50+** | ☠️ **YEARS** | Impossible | ❌ Do Not Use |

> 💡 **Note:** Performance depends on system specs. Each difficulty level increases time by ~16x. For testing/learning, stick to difficulty **3-5**. Higher difficulties demonstrate exponential scaling of P
---

## ⚠️ Security Notes

### 🎓 Educational Project
This is a **learning implementation**. For production use, add:

- 🔐 Proper cryptographic signatures
- ✅ Transaction validation logic
- 💰 UTXO or account-based system
- 💾 Persistent database storage
- 🌍 Proper P2P networking
- 🏦 Transaction fee mechanism
- 🛡️ DDoS protection
- 🔑 Key management system

---

## 📚 Learning Outcomes

This project demonstrates:

- 🔗 Core blockchain fundamentals
- ⛏️ Proof-of-Work consensus
- 🔀 Distributed ledger sync
- 🌐 RESTful API design
- 🔄 Network consensus algorithms
- 💼 Transaction management pipelines
- 🏗️ Distributed system architecture

---

## 👨‍💻 Author

Created as an **educational blockchain implementation** project to learn distributed systems and cryptographic fundamentals.

---
