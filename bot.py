import json
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# In-memory registry for simplicity (you can persist it)
registered = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome! Use /register <your_wallet_address> to continue.")

async def register(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) != 1:
        await update.message.reply_text("Please provide your wallet like /register 0x123...")
        return

    wallet = context.args[0]
    username = update.effective_user.username
    registered[wallet] = username

    # Save temp data for verifying
    with open("data.json", "w") as f:
        json.dump(registered, f)

    # Verification link
    link = f"https://wallet-verifier.onrender.com/verify?wallet={wallet}&user={username}"
    await update.message.reply_text(f"Click to verify your wallet: {link}")

app = ApplicationBuilder().token("7648743572:AAGHvI_-EjsLyuqDiSQEdg0tkdx-BGbf2cg").build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("register", register))

app.run_polling()
