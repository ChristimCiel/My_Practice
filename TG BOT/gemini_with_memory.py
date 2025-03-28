import os
from dotenv import load_dotenv, find_dotenv
import google.generativeai as genai

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

_ = load_dotenv(find_dotenv())

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY not found in environment variables")

telegram_token = os.getenv('TELEGRAM_BOT_TOKEN')
if not telegram_token:
    raise ValueError("TELEGRAM_BOT_TOKEN not found in environment variables")

genai.configure(api_key=api_key)

# Create Gemini model instance
model = genai.GenerativeModel(model_name="gemini-2.0-flash")

chat_memories = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Hi！I'm Christim 😮‍💨。")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text
    chat_id = update.effective_chat.id

    if chat_id not in chat_memories:
        chat_memories[chat_id] = model.start_chat(history=[])


    try:
        # Get the current chat for this user
        chat = chat_memories[chat_id]
        # 使用模型生成响应
        response = chat.send_message(user_input)
        
        if update.effective_chat is not None:
            # 发送响应文本
            await context.bot.send_message(
                chat_id=update.effective_chat.id, 
                text=response.text)
        else:
            print("effective_chat is None")

    except Exception as e:
        print(f"Error generating response: {e}")
        if update.effective_chat is not None:
            await context.bot.send_message(
                chat_id=update.effective_chat.id, 
                text="Sorry, I couldn't process your request."
            )

if __name__ == '__main__':
    application = Application.builder().token(telegram_token).build()
    application.add_handler(CommandHandler("start", start)) 
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Bot is running...")
    application.run_polling()
