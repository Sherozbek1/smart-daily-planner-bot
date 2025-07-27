from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import json
import os

DATA_FILE = "tasks.json"

def load_tasks():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}

def save_tasks(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Welcome to Smart Daily Planner!\nUse /add, /list, /done, /clear.")

async def add_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    tasks = load_tasks()
    task_text = " ".join(context.args)

    if not task_text:
        await update.message.reply_text("❗Please provide a task after /add.")
        return

    tasks.setdefault(user_id, []).append(task_text)
    save_tasks(tasks)
    await update.message.reply_text(f"✅ Task added: {task_text}")

async def list_tasks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    tasks = load_tasks().get(user_id, [])

    if not tasks:
        await update.message.reply_text("📭 No tasks yet.")
        return

    response = "\n".join([f"{i+1}. {t}" for i, t in enumerate(tasks)])
    await update.message.reply_text("🗒️ Your tasks:\n" + response)

async def done_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    tasks = load_tasks()

    try:
        index = int(context.args[0]) - 1
        if user_id not in tasks or index < 0 or index >= len(tasks[user_id]):
            raise ValueError()
        done = tasks[user_id].pop(index)
        save_tasks(tasks)
        await update.message.reply_text(f"✅ Completed task: {done}")
    except:
        await update.message.reply_text("❗Usage: /done [task number]")

async def clear_tasks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    tasks = load_tasks()
    tasks[user_id] = []
    save_tasks(tasks)
    await update.message.reply_text("🧹 All tasks cleared.")

if __name__ == '__main__':
    TOKEN = os.environ.get("8387365932:AAGmMO0h2TVNE-bKpHME22sqWApfm7_UW6c")
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("add", add_task))
    app.add_handler(CommandHandler("list", list_tasks))
    app.add_handler(CommandHandler("done", done_task))
    app.add_handler(CommandHandler("clear", clear_tasks))

    print("🤖 Bot is running...")
    app.run_polling()
