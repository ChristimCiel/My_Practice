import os
import openai

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file

client = openai.OpenAI()
llm_model = "gpt-3.5-turbo"

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Hi！I'm Christim 😮‍💨。")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE, prompt, model="gpt-3.5-turbo") -> None:
    messages = [{"role" : "system", "content": prompt}]
    response = client.chat.completions.create(
        model = model,
        messages = messages,
        temperature=0.5,
        max_tokens=100,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0)
    chat_response = response.choices[0].message.content.strip() 

    
    await update.message.reply_text(chat_response)
    
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prompt = update.message.text
    await echo(update, context, prompt)

if __name__ == '__main__':
    application = Application.builder().token(os.getenv('TELEGRAM_BOT_TOKEN')).build()
    application.add_handler(CommandHandler("start", start)) 
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND,  handle_message))
    application.run_polling()
