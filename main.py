import os
from telethon import TelegramClient, events
import boto3

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

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

client = TelegramClient('movieland_bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    await event.reply("Welcome to MovieLand! 🎬\nMovie File එකක් Forward කරන්න, මම Link එකක් දෙන්නම්.")

@client.on(events.NewMessage)
async def handle_forward(event):
    # Forward කරපු File එකක්ද කියලා බලනවා
    if not event.message.media:
        return
    if event.message.text and event.message.text.startswith('/'):
        return

    msg = await event.reply("Uploading... ⏳ ටිකක් ඉන්න, 774MB වගේ ලොකු File එකක් නිසා ටිකක් වෙලා යයි")
    
    # File එකේ නම හොයනවා
    file_name = "movie.mp4"
    if event.message.file:
        file_name = event.message.file.name or f"{event.message.id}.mp4"
    file_name = file_name.replace(" ", "_")
    local_path = os.path.join(os.getcwd(), file_name)

    try:
        # Telethon එකෙන් ලොකු File එකත් බාගන්න පුළුවන්
        await event.message.download_media(file=local_path)
        
        s3.upload_file(local_path, BUCKET, file_name)
        link = f"{PUBLIC_URL}/{file_name}"
        
        await msg.edit(f"✅ Uploaded!\n\n🎬 {file_name}\n\n🔗 Link: {link}")
        
        if os.path.exists(local_path):
            os.remove(local_path)
            
    except Exception as e:
        await msg.edit(f"❌ Error: {e}")

print("Bot Running... Forward ekak enakan balan innawa")
client.run_until_disconnected()