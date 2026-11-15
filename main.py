import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import boto3

TOKEN = os.getenv("BOT_TOKEN")
R2_ACCESS = os.getenv("R2_ACCESS_KEY")
R2_SECRET = os.getenv("R2_SECRET_KEY")
R2_ENDPOINT = os.getenv("R2_ENDPOINT")
BUCKET = os.getenv("R2_BUCKET")
PUBLIC_URL = os.getenv("R2_PUBLIC_URL")

s3 = boto3.client('s3',
    endpoint_url=R2_ENDPOINT,
    aws_access_key_id=R2_ACCESS,
    aws_secret_access_key=R2_SECRET,
    region_name='auto'
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome to MovieLand! 🎬\nMovie එකක් එවන්න, මම Link එකක් දෙන්නම්.")

async def handle_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = await update.message.reply_text("Uploading... ⏳ Please wait")
    file = await update.message.video.get_file()
    file_name = update.message.video.file_name or f"{update.message.video.file_id}.mp4"
    local_path = f"/tmp/{file_name}"
    await file.download_to_drive(local_path)
    s3.upload_file(local_path, BUCKET, file_name)
    link = f"{PUBLIC_URL}/{file_name}"
    await msg.edit_text(f"✅ Uploaded!\n\n🎬 {file_name}\n\n🔗 Link: {link}")

app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.VIDEO, handle_video))
app.run_polling()