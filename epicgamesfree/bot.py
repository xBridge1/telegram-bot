from telegram import Update 
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from telegram.constants import ParseMode
from scraper import fetch_epic_page_with_browser, parse_free_games, format_games_message
from apscheduler.schedulers.background import BackgroundScheduler
import asyncio

chat_id = None 

subscribers = set()

BOT_TOKEN= ""


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
      global chat_id
      chat_id=update.effective_chat.id
      await update.message.reply_text("Olá, bem vindo ao bot do jão para ver os jogos gratís da epic," \
      " digite /freegames para verificar o jogo gratis da semana, se desejar utilize /subscribe para ser notificado diariamente, se desejar sair digite /unsubscribe.")


async def send_daily_message(app):
     for chat_id in subscribers:
          html = fetch_epic_page_with_browser()
          games = parse_free_games(html)
          message = format_games_message(games)
     try:
          await app.bot.send_message(chat_id=chat_id, text=message, parse_mode=ParseMode.MARKDOWN)
     except Exception as e:
          print(f"[erro] nao foi possivel encaminhar esta mensagem para {chat_id}: {e}")

def setup_daily_task(app):
    scheduler = BackgroundScheduler()

    def job():
        asyncio.get_event_loop().create_task(send_daily_message(app))

    scheduler.add_job(job, trigger='cron', hour=10, minute=0)
    scheduler.start()


async def subscribe(update: Update, context: ContextTypes.DEFAULT_TYPE):
     chat_id = update.effective_chat.id  
     subscribers.add(chat_id)
     
     await update.message.reply_text("Obrigado por se inscrever, você recebera updates automaticos todos os dias.✅")


async def unsubscribe(update: Update, context: ContextTypes.DEFAULT_TYPE):
     chat_id = update.effective_chat.id 
     if chat_id in subscribers:
          subscribers.remove(chat_id)
          await update.message.reply_text("Removido da lista de alerta; ⛔")

     else:
          await update.message.reply_text("Você não está inscrito para os alarmes. ⚠️")

async def freegames(update: Update, context: ContextTypes.DEFAULT_TYPE):
    html = fetch_epic_page_with_browser()
    games = parse_free_games(html)
    message = format_games_message(games)

    await update.message.reply_text(message, parse_mode=ParseMode.MARKDOWN)

if __name__  == '__main__':

      app = ApplicationBuilder().token(BOT_TOKEN).build()
      app.add_handler(CommandHandler("start",start))
      app.add_handler(CommandHandler("freegames",freegames))
      app.add_handler(CommandHandler("subscribe",subscribe))
      app.add_handler(CommandHandler("unsubscribe",unsubscribe))

      setup_daily_task(app)

print("Bot esta online ✅")
app.run_polling()
