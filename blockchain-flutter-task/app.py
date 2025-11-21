from flask import Flask, request, jsonify, Response
from main import Blockchain
from uuid import uuid4
import json, random


app = Flask(__name__)
blockchain = Blockchain()

USER_WALLETS = {}

def get_wallet(user):
    if user not in USER_WALLETS:
        USER_WALLETS[user] = str(uuid4()).replace("-", "")
    return USER_WALLETS[user]


@app.route("/transactions/new", methods=["POST"])

def new_transaction():
    values = request.get_json()
    required = ["sender", "recipient", "amount"]

    if not all(k in values for k in required):
        return jsonify({"error": "brak wymaganych pól"}), 400

    sender_wallet = get_wallet(values["sender"])
    recipient_wallet = get_wallet(values["recipient"])
    
    index = blockchain.jj_add_transaction_to_mempool(
            sender_wallet,
            recipient_wallet,
            values["amount"],
            )
    return jsonify({"message": f"transakcja trafi do bloku {index}"}), 201


@app.route("/mine", methods=["GET"])

def mine_block():
     
    reward = 5 
    difficulty = 4 


    if not blockchain.jj_mempool:
        return jsonify({"error": "Brak transakcji w mempoolu"}), 400

 
    involved_wallets = list({tx["sender"] for tx in blockchain.jj_mempool} | {tx["recipient"] for tx in blockchain.jj_mempool})
    miner_wallet = random.choice(involved_wallets)

    blockchain.jj_add_transaction_to_mempool(sender="0", recipient=miner_wallet, amount=reward)

    block = blockchain.jj_mine_block(difficulty)
    miner_user = next((user for user, wallet in USER_WALLETS.items() if wallet == miner_wallet), miner_wallet)

    response = {
        "message": "Nowy blok wydobyty",
        "index": block["index"],
        "transactions": block["transactions"],
        "merkle_root": block["merkle_root"],
        "nonce": block["nonce"],
        "hash": block["hash"],
        "previous_hash": block["previous_hash"],
        "reward": reward,
        "miner": miner_user,
        "miner_wallet": miner_wallet
    }
    return Response(json.dumps(response, indent=4), status= 200, mimetype='application/json')

@app.route("/transactions/history/<user>", methods=["GET"])

def transaction_history(user):
    wallet = USER_WALLETS.get(user)
    if not wallet:
        return jsonify({"error": "Nie znaleziono uzytkownika"}), 404


    history = []
    for block in blockchain.jj_chain:
        for tx in block.get("transactions", []):
            if tx["sender"] == wallet or tx["recipient"] == wallet:
                history.append(tx)
    response = ({"addres": user, "wallet": wallet, "transactions": history})

    return Response(json.dumps(response, indent=4), status=200, mimetype='application/json')

@app.route("/chain", methods=["GET"])
    
def full_chain():
    response = {
            'chain': blockchain.jj_chain,
            'length': len(blockchain.jj_chain)
            }
    return Response(json.dumps(response, indent=4), status=200, mimetype='application/json')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
