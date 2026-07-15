import os
import logging
import requests
import json
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext, CallbackQueryHandler

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Get token from environment variable
TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

# Welcome message
WELCOME_TEXT = """
🧠 *Welcome to SmartBot!*

I'm your intelligent assistant bot. Here's what I can do:

🤖 *AI Chat* - Ask me anything
💡 *Get Advice* - Get random advice  
📝 *Get Quote* - Inspirational quotes
❓ *Ask Question* - Get answers

📌 *Commands:*
/start - Show this menu
/help - Get help
/chat [text] - Chat with AI
/advice - Get advice
/quote - Get quote
/ask [question] - Ask a question
/settings - Change preferences

🔍 Just type any message to chat with me!
"""

HELP_TEXT = """
📚 *SmartBot Help*

*Commands:*
• /start - Welcome menu
• /help - Show this help
• /chat [message] - Chat with AI
• /advice - Get random advice
• /quote - Get inspirational quote
• /ask [question] - Ask AI a question
• /settings - Change settings

*About:*
SmartBot uses free APIs to provide intelligent responses without any API keys needed.

Made with ❤️ for Telegram
"""

# ============ COMMAND HANDLERS ============

async def start(update: Update, context: CallbackContext):
    """Send a welcome message when /start is issued."""
    user = update.effective_user
    keyboard = [
        [InlineKeyboardButton("💬 Chat", callback_data='chat'),
         InlineKeyboardButton("📝 Advice", callback_data='advice')],
        [InlineKeyboardButton("📄 Quote", callback_data='quote'),
         InlineKeyboardButton("❓ Ask", callback_data='ask')],
        [InlineKeyboardButton("⚙️ Settings", callback_data='settings')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        f"👋 Hello {user.first_name}!\n\n" + WELCOME_TEXT,
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def help_command(update: Update, context: CallbackContext):
    """Send a help message."""
    await update.message.reply_text(
        HELP_TEXT,
        parse_mode='Markdown'
    )

async def advice_command(update: Update, context: CallbackContext):
    """Get random advice."""
    await update.message.reply_text("💭 Getting advice for you...")
    
    try:
        response = requests.get("https://api.adviceslip.com/advice")
        if response.status_code == 200:
            data = response.json()
            advice = data['slip']['advice']
            await update.message.reply_text(
                f"💡 *Advice of the Day:*\n\n{advice}",
                parse_mode='Markdown'
            )
        else:
            await update.message.reply_text("❌ Sorry, couldn't get advice right now. Try again later.")
    except Exception as e:
        logger.error(f"Error getting advice: {e}")
        await update.message.reply_text("❌ Error fetching advice. Please try again.")

async def quote_command(update: Update, context: CallbackContext):
    """Get inspirational quote."""
    await update.message.reply_text("📝 Finding an inspirational quote...")
    
    try:
        response = requests.get("https://api.quotable.io/random")
        if response.status_code == 200:
            data = response.json()
            quote = f"*{data['content']}*\n\n— _{data['author']}_"
            await update.message.reply_text(
                quote,
                parse_mode='Markdown'
            )
        else:
            await update.message.reply_text("❌ Sorry, couldn't get a quote right now.")
    except Exception as e:
        logger.error(f"Error getting quote: {e}")
        await update.message.reply_text("❌ Error fetching quote. Please try again.")

async def ask_command(update: Update, context: CallbackContext):
    """Handle /ask command."""
    if not context.args:
        await update.message.reply_text(
            "❓ Please ask a question.\nExample: `/ask What is the capital of France?`",
            parse_mode='Markdown'
        )
        return
    
    question = ' '.join(context.args)
    await update.message.reply_text(f"🤔 Thinking about: '{question}'...")
    
    # Simple response for demonstration
    response = f"🤖 *SmartBot's Response:*\n\nI received your question: '{question}'\n\nTry /advice for advice or /quote for inspiration!"
    
    await update.message.reply_text(
        response,
        parse_mode='Markdown'
    )

async def chat_command(update: Update, context: CallbackContext):
    """Handle /chat command."""
    if not context.args:
        await update.message.reply_text(
            "💬 Please provide a message.\nExample: `/chat Hello, how are you?`",
            parse_mode='Markdown'
        )
        return
    
    message = ' '.join(context.args)
    
    # Simple response logic
    response = f"🤖 *SmartBot:*\n\nYou said: '{message}'\n\nI'm here to help! Try /advice for wisdom or /quote for inspiration."
    
    await update.message.reply_text(
        response,
        parse_mode='Markdown'
    )

async def settings_command(update: Update, context: CallbackContext):
    """Handle /settings command."""
    keyboard = [
        [InlineKeyboardButton("🔄 Reset Settings", callback_data='reset_settings')],
        [InlineKeyboardButton("📊 Show Current Settings", callback_data='show_settings')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "⚙️ *Settings*\n\nConfigure your bot preferences:",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

# ============ MESSAGE HANDLER ============

async def echo_message(update: Update, context: CallbackContext):
    """Handle regular text messages."""
    user_message = update.message.text
    
    # Simple response logic
    if "hello" in user_message.lower() or "hi" in user_message.lower():
        response = "👋 Hello there! How can I help you today?"
    elif "how are you" in user_message.lower():
        response = "🤖 I'm doing great! Thanks for asking. How about you?"
    elif "help" in user_message.lower():
        response = "🆘 I can help with many things! Try /help to see all my commands."
    elif "thanks" in user_message.lower() or "thank you" in user_message.lower():
        response = "😊 You're welcome! Happy to help."
    elif "advice" in user_message.lower():
        response = "💡 Try using /advice for some wisdom!"
    elif "quote" in user_message.lower():
        response = "📝 Try using /quote for inspirational quotes!"
    else:
        response = f"🤖 *SmartBot:*\n\nYou said: '{user_message}'\n\nI'm here to help! Try /help to see what I can do."
    
    await update.message.reply_text(
        response,
        parse_mode='Markdown'
    )

# ============ CALLBACK QUERY HANDLER ============

async def button_handler(update: Update, context: CallbackContext):
    """Handle inline button clicks."""
    query = update.callback_query
    await query.answer()
    
    if query.data == 'chat':
        await query.edit_message_text(
            "💬 *Chat Mode*\n\nSend me a message and I'll respond!\nYou can also use /chat [message]",
            parse_mode='Markdown'
        )
    elif query.data == 'advice':
        await query.edit_message_text("💭 Getting advice for you...")
        try:
            response = requests.get("https://api.adviceslip.com/advice")
            if response.status_code == 200:
                data = response.json()
                advice = data['slip']['advice']
                await query.edit_message_text(
                    f"💡 *Advice of the Day:*\n\n{advice}",
                    parse_mode='Markdown'
                )
        except:
            await query.edit_message_text("❌ Sorry, couldn't get advice right now.")
    elif query.data == 'quote':
        await query.edit_message_text("📝 Finding an inspirational quote...")
        try:
            response = requests.get("https://api.quotable.io/random")
            if response.status_code == 200:
                data = response.json()
                quote = f"*{data['content']}*\n\n— _{data['author']}_"
                await query.edit_message_text(
                    quote,
                    parse_mode='Markdown'
                )
        except:
            await query.edit_message_text("❌ Sorry, couldn't get a quote right now.")
    elif query.data == 'ask':
        await query.edit_message_text(
            "❓ *Ask Mode*\n\nUse /ask [your question]\nExample: /ask What is the meaning of life?",
            parse_mode='Markdown'
        )
    elif query.data == 'settings':
        await query.edit_message_text(
            "⚙️ *Settings*\n\n• Language: English\n• Notifications: Enabled\n• Theme: Default\n\nMore settings coming soon!",
            parse_mode='Markdown'
        )
    elif query.data == 'show_settings':
        await query.edit_message_text(
            "⚙️ *Current Settings*\n\n• Language: English\n• Notifications: Enabled\n• Theme: Default\n\nMore settings coming soon!",
            parse_mode='Markdown'
        )
    elif query.data == 'reset_settings':
        await query.edit_message_text(
            "🔄 *Settings Reset*\n\nAll settings have been restored to default.",
            parse_mode='Markdown'
        )

# ============ ERROR HANDLER ============

async def error_handler(update: Update, context: CallbackContext):
    """Handle errors."""
    logger.error(f"Update {update} caused error {context.error}")
    
    if update and update.effective_message:
        await update.effective_message.reply_text(
            "❌ Sorry, something went wrong. Please try again later."
        )

# ============ MAIN FUNCTION ============

def main():
    """Start the bot."""
    if not TOKEN:
        logger.error("No TELEGRAM_BOT_TOKEN found in environment variables!")
        return
    
    # Create the Application
    application = Application.builder().token(TOKEN).build()

    # Add command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("advice", advice_command))
    application.add_handler(CommandHandler("quote", quote_command))
    application.add_handler(CommandHandler("ask", ask_command))
    application.add_handler(CommandHandler("chat", chat_command))
    application.add_handler(CommandHandler("settings", settings_command))
    
    # Add message handler for text messages
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo_message))
    
    # Add callback query handler for buttons
    application.add_handler(CallbackQueryHandler(button_handler))
    
    # Add error handler
    application.add_error_handler(error_handler)

    # Start the bot
    logger.info("Starting SmartBot...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
