import os
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv()) # read local .env file
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from langchain_openai import OpenAI
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

from langchain_openai import OpenAI
from langchain.chains import ConversationChain

# api_key = os.getenv("OPENAI_API_KEY")
# llm = OpenAI(api_key=api_key, model="gpt-3.5-turbo")
llm = OpenAI(temperature=0)
# 初始化 LangChain 和 OpenAI
memory = ConversationBufferMemory()
conversation = ConversationChain(
    llm=llm, 
    memory=memory,
    verbose=True
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Hi！I'm Christim 😮‍💨。")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text
    
    output = conversation.predict(input=user_input)
    if update.effective_chat is not None:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=output)
    else:
        print("effective_chat is None")

if __name__ == '__main__':
    application = Application.builder().token(os.getenv('TELEGRAM_BOT_TOKEN')).build()
    application.add_handler(CommandHandler("start", start)) 
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND,  handle_message))
    # application.add_handler(CommandHandler('query',query))
    application.run_polling()
