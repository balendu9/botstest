from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import json

app = FastAPI()

@app.get("/verify", response_class=HTMLResponse)
async def verify(wallet: str, user: str):
    html = f"""
    <html>
    <head>
        <script src="https://cdn.jsdelivr.net/npm/web3@latest/dist/web3.min.js"></script>
    </head>
    <body>
        <h2>Connect your wallet to verify</h2>
        <button onclick="connect()">Connect Wallet</button>
        <p id="status"></p>
        <script>
            async function connect() {{
                if (typeof window.ethereum !== 'undefined') {{
                    const web3 = new Web3(window.ethereum);
                    try {{
                        const accounts = await window.ethereum.request({{ method: 'eth_requestAccounts' }});
                        const address = accounts[0];

                        if (address.toLowerCase() === "{wallet.lower()}") {{
                            document.getElementById("status").innerText = "Wallet verified!";
                            fetch('/save', {{
                                method: 'POST',
                                headers: {{ 'Content-Type': 'application/json' }},
                                body: JSON.stringify({{ wallet: address, user: "{user}" }})
                            }});
                        }} else {{
                            document.getElementById("status").innerText = "Wallet mismatch!";
                        }}
                    }} catch (err) {{
                        console.error(err);
                        document.getElementById("status").innerText = "Error connecting wallet";
                    }}
                }} else {{
                    alert("Please install MetaMask.");
                }}
            }}
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html)

@app.post("/save")
async def save_data(request: Request):
    data = await request.json()
    wallet = data["wallet"]
    user = data["user"]

    try:
        with open("verified.json", "r") as f:
            verified = json.load(f)
    except:
        verified = {}

    verified[wallet] = user

    with open("verified.json", "w") as f:
        json.dump(verified, f, indent=2)

    return {"status": "success", "wallet": wallet}

