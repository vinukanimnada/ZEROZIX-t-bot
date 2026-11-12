import os
import random
from datetime import datetime
from telegram import Update
from telegram.ext import (
    Application, CommandHandler, MessageHandler, ContextTypes, filters
)

TOKEN = os.environ.get("BOT_TOKEN")


async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    name = update.effective_user.first_name
    await update.message.reply_text(
        f"ආයුබෝවන් {name}! 👋\n/help ගහලා බලන්න."
    )


async def help_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "/start - ආරම්භය\n/time - වෙලාව\n/dice - දාදු කැටය 🎲\n/echo <text>"
    )


async def time_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🕒 " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))


async def dice(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"🎲 {random.randint(1, 6)}")


async def echo(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(" ".join(ctx.args) or "/echo hello")


async def text_msg(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("මට තේරුණේ නැහැ 😅 /help බලන්න.")


app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_cmd))
app.add_handler(CommandHandler("time", time_cmd))
app.add_handler(CommandHandler("dice", dice))
app.add_handler(CommandHandler("echo", echo))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_msg))
print("Bot running...")
app.run_polling()
