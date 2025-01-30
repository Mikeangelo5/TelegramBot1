
import re
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters

# Replace this with your actual bot token
TOKEN = "7588383150:AAEC_xfm3dUk_di8JoURRjIMEKFSGnT_ydw"

# Regular expression to detect Twitter/X links
X_LINK_REGEX = re.compile(r"(https?://(?:www\.)?(?:twitter|x)\.com/\S+)")

# Enable logging
logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)

async def clean_x_links(update: Update, context):
    """Detects Twitter/X links, cleans them, and reposts the cleaned link."""
    message = update.message.text

    # Search for Twitter/X links
    match = X_LINK_REGEX.search(message)
    if match:
        original_link = match.group(0)

        # Remove tracking parameters like ?s=46
        cleaned_link = original_link.split("?")[0]

        # Delete the original message
        try:
            await update.message.delete()
        except Exception as e:
            logging.warning(f"Failed to delete message: {e}")

        # Send cleaned link back to chat
        await update.message.reply_text(f"✅ Cleaned Link: {cleaned_link}")

async def start(update: Update, context):
    """Handles /start command."""
    await update.message.reply_text("Hello! I will clean X (Twitter) links by removing tracking parameters.")

def main():
    """Main function to start the bot."""
    app = Application.builder().token(TOKEN).build()

    # Start command handler
    app.add_handler(CommandHandler("start", start))

    # Message handler to detect and clean X links
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, clean_x_links))

    # Start the bot
    logging.info("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
