# main.py

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackQueryHandler
import os

# Replace with your bot token
BOT_TOKEN = "7860310378:AAGoFdufVg_v2aG3aTuRxnXWCBrM-mb79Eg"

# Sample lessons
lessons = {
    "Word": {
        "Beginner": {
            "text": "📘 *Word - Beginner*\n\nCreate and format documents, save and open files.",
            "video": "https://www.youtube.com/watch?v=H1pXayJxN4k"
        },
        "Intermediate": {
            "text": "📘 *Word - Intermediate*\n\nWorking with tables, images, and headers.",
            "video": "https://www.youtube.com/watch?v=Jt_qdXIXg5U"
        },
        "Advanced": {
            "text": "📘 *Word - Advanced*\n\nMail merge, macros, and style templates.",
            "video": "https://www.youtube.com/watch?v=E_2TscbJ-NY"
        }
    },
    "Excel": {
        "Beginner": {
            "text": "📗 *Excel - Beginner*\n\nLearn data entry, autofill, and basic functions like SUM.",
            "video": "https://www.youtube.com/watch?v=VhcjCPICsOg"
        },
        "Intermediate": {
            "text": "📗 *Excel - Intermediate*\n\nCharts, conditional formatting, IF statements.",
            "video": "https://www.youtube.com/watch?v=9NUjHBNWe9M"
        },
        "Advanced": {
            "text": "📗 *Excel - Advanced*\n\nPivotTables, VLOOKUP, data analysis.",
            "video": "https://www.youtube.com/watch?v=HkkDYyDKeZ4"
        }
    },
    "Skills": {
        "Beginner": {
            "text": "💻 *Computer Skills - Beginner*\n\nUnderstand hardware, software, and basic navigation.",
            "video": "https://www.youtube.com/watch?v=mmCuNbBdMgA"
        },
        "Intermediate": {
            "text": "💻 *Computer Skills - Intermediate*\n\nLearn file management, browsers, email use.",
            "video": "https://www.youtube.com/watch?v=BW9yDWLJH_4"
        },
        "Advanced": {
            "text": "💻 *Computer Skills - Advanced*\n\nOperating systems, installations, troubleshooting.",
            "video": "https://www.youtube.com/watch?v=F2iFTzq9gSo"
        }
    }
}


# Sample quiz
quiz_data = {
    "question": "How do you save a Word document?",
    "options": ["File > Save As", "Insert > Save", "Ctrl + P"],
    "correct_index": 0
}

# User progress (in-memory)
user_scores = {}

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome to Kalaphol Bot!\nLearn Microsoft Office and Computer Skills.\n\n"
        "Use /lessons to view lessons\nUse /quiz to test yourself"
    )

# /lessons command
async def lessons_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Microsoft Word", callback_data="lesson_Word")],
        [InlineKeyboardButton("Microsoft Excel", callback_data="lesson_Excel")],
        [InlineKeyboardButton("Computer Skills", callback_data="lesson_Skills")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Choose a lesson:", reply_markup=reply_markup)

# /quiz command
async def quiz_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton(opt, callback_data=f"quiz_{i}")]
        for i, opt in enumerate(quiz_data["options"])
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(f"🧠 Quiz Time!\n\n{quiz_data['question']}", reply_markup=reply_markup)

# Button callbacks
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data.startswith("lesson_"):
        lesson_key = data.split("_")[1]
        content = lessons.get(lesson_key, "Lesson not found.")
        await query.edit_message_text(content, parse_mode="Markdown")
    
    elif data.startswith("quiz_"):
        user_id = query.from_user.id
        selected = int(data.split("_")[1])
        correct = quiz_data["correct_index"]

        if user_id not in user_scores:
            user_scores[user_id] = 0

        if selected == correct:
            user_scores[user_id] += 1
            await query.edit_message_text("✅ Correct! You earned 1 point.")
        else:
            await query.edit_message_text("❌ Wrong answer. Try again with /quiz.")

# Main bot setup
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("lessons", lessons_command))
    app.add_handler(CommandHandler("quiz", quiz_command))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("🤖 Kalaphol Bot is running...")
    app.run_polling()

if __name__ == '__main__':
    main()
