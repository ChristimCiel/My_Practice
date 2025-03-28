import os
import tempfile
from dotenv import load_dotenv, find_dotenv
import google.generativeai as genai

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

# Load environment variables
_ = load_dotenv(find_dotenv())
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY not found in environment variables")

telegram_token = os.getenv('TELEGRAM_BOT_TOKEN')
if not telegram_token:
    raise ValueError("TELEGRAM_BOT_TOKEN not found in environment variables")

# Configure Gemini
genai.configure(api_key=api_key)

# Create Gemini model instance
model = genai.GenerativeModel('gemini-2.0-flash')

# Conversation and audio tracking
chat_memories = {}
audio_prompts = {}
audio_processing_state = {}

# Allowed audio types
ALLOWED_AUDIO_TYPES = ["wav", "mp3", "aiff", "aac", "ogg", "flac", "mp4", "m4a"]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Hi！I'm Christim 😮‍💨。")

def is_allowed_audio(filename):
    return filename.split('.')[-1].lower() in ALLOWED_AUDIO_TYPES

async def handle_audio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    audio_file = update.message.audio or update.message.voice

    file_name = audio_file.file_name or "voice_message.ogg"

    if not is_allowed_audio(file_name):
        allowed = ", ".join(ALLOWED_AUDIO_TYPES).upper()
        await update.message.reply_text(f"❌ Unsupported audio format! Please use: {allowed}")
        return

    # Download and process audio
    file = await context.bot.get_file(audio_file.file_id)
    with tempfile.NamedTemporaryFile(delete=False, suffix='.' + file_name.split('.')[-1]) as temp_audio:
        await file.download_to_drive(custom_path=temp_audio.name)
        
        # Store audio file path for later processing
        audio_prompts[chat_id] = temp_audio.name

    await update.message.reply_text(
        "✅ Audio received! 🎧\n\n"
        "What would you like me to do with this audio?"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text
    chat_id = update.effective_chat.id

    # Check if there's a pending audio prompt
    if chat_id in audio_prompts:
        audio_file_path = audio_prompts.pop(chat_id)
        
        try:
            # Create or retrieve chat session
            chat = chat_memories.setdefault(chat_id, model.start_chat(history=[]))
            
            # Generate content with audio and text
            response = chat.send_message([
                user_input, 
                genai.upload_file(path=audio_file_path)
            ])
            
            await context.bot.send_message(
                chat_id=chat_id, 
                text= f"{response.text}\n\n"
                     "Are you satisfied with this result? 🤔\n"
                     "If not, please tell me what specific changes or additional information you'd like."
            )
        except Exception as e:
            print(f"Error processing audio prompt: {e}")
            await context.bot.send_message(chat_id=chat_id, text="Sorry, I couldn't process your audio request.")
        finally:
            # Clean up temporary audio file
            os.unlink(audio_file_path)
    else:
        # Standard text chat handling
        try:
            # Create or retrieve chat session
            chat = chat_memories.setdefault(chat_id, model.start_chat(history=[]))
            
            # Send message and get response
            response = chat.send_message(user_input)
            
            await context.bot.send_message(chat_id=chat_id, text=response.text)
        except Exception as e:
            print(f"Error generating response: {e}")
            await context.bot.send_message(chat_id=chat_id, text="Sorry, I couldn't process your request.")

def main():
    application = Application.builder().token(telegram_token).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.AUDIO | filters.VOICE, handle_audio))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("Bot is running...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
