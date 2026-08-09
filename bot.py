
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters
)

import requests
import time


# =========================
# TOKEN
# =========================




# =========================
# محدودیت استفاده
# =========================

MAX_REQUESTS = 20
TIME_WINDOW = 60 * 60  # یک ساعت

user_requests = {}


def check_rate_limit(user_id):

    now = time.time()

    # اگر کاربر قبلاً در لیست نبوده
    if user_id not in user_requests:
        user_requests[user_id] = []

    # فقط درخواست‌های یک ساعت اخیر
    user_requests[user_id] = [
        request_time
        for request_time in user_requests[user_id]
        if now - request_time < TIME_WINDOW
    ]

    # آیا محدودیت تمام شده؟
    if len(user_requests[user_id]) >= MAX_REQUESTS:
        return False

    # ثبت درخواست جدید
    user_requests[user_id].append(now)

    return True


# =========================
# START
# =========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
        [" راهنما"],
        [" انتخاب دارایی"]
    ]

    reply_markup = ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True
    )

    await update.message.reply_text(
        "سلام 👋\n\n"
        "به ربات قیمت بازار خوش آمدید.\n\n"
        "یک گزینه را انتخاب کنید:",
        reply_markup=reply_markup
    )


# =========================
# راهنما
# =========================

async def guide(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "📖 راهنمای ربات\n\n"
        "با استفاده از این ربات می‌توانید "
        "قیمت دارایی‌های مختلف را مشاهده کنید.\n\n"
        "دارایی‌های موجود:\n\n"
        "🪙 تتر\n"
        "₿ بیت کوین\n"
        "🥇 طلای ۱۸ عیار\n"
        "🥈 نقره\n\n"
        "⚠️ هر کاربر حداکثر ۲۰ بار در هر ساعت "
        "می‌تواند قیمت دریافت کند."
    )


# =========================
# انتخاب دارایی
# =========================

async def choose_asset(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
        ["🪙 تتر", "₿ بیت کوین"],
        ["🥇 طلا", "🥈 نقره"],
        ["🔙 بازگشت"]
    ]

    reply_markup = ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True
    )

    await update.message.reply_text(
        " دارایی موردنظر را انتخاب کنید:",
        reply_markup=reply_markup
    )


# =========================
# دریافت قیمت از نوبیتکس
# =========================

def get_nobitex_price(src_currency, dst_currency="rls"):

    url = "https://apiv2.nobitex.ir/market/stats"

    params = {
        "srcCurrency": src_currency,
        "dstCurrency": dst_currency
    }

    headers = {
        "Accept": "application/json",
        "User-Agent": "TraderBot/MyBot-1.0.0"
    }

    response = requests.get(
        url,
        params=params,
        headers=headers,
        timeout=10
    )

    response.raise_for_status()

    data = response.json()

    if data.get("status") != "ok":
        raise Exception("Nobitex API Error")

    pair = f"{src_currency}-{dst_currency}"

    if pair not in data["stats"]:
        raise Exception(
            f"Market {pair} not found"
        )

    return float(
        data["stats"][pair]["latest"]
    )


# =========================
# تبدیل ریال به تومان
# =========================

def rial_to_toman(price):

    return price / 10


# =========================
# بررسی محدودیت
# =========================

async def check_user_limit(update):

    user_id = update.effective_user.id

    if not check_rate_limit(user_id):

        await update.message.reply_text(
            "⛔ محدودیت استفاده\n\n"
            "شما در یک ساعت گذشته به سقف "
            "۲۰ درخواست رسیده‌اید.\n\n"
            "لطفاً بعداً دوباره تلاش کنید."
        )

        return False

    return True


# =========================
# تتر
# =========================

async def tether_price(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if not await check_user_limit(update):
        return

    try:

        price = get_nobitex_price("usdt")

        toman = rial_to_toman(price)

        await update.message.reply_text(
            "🪙 قیمت تتر\n\n"
            f"💰 {toman:,.0f} تومان"
        )

    except Exception as e:

        print("Tether Error:", e)

        await update.message.reply_text(
            "❌ خطا در دریافت قیمت تتر"
        )


# =========================
# بیت کوین
# =========================

async def bitcoin_price(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if not await check_user_limit(update):
        return

    try:

        price = get_nobitex_price("btc")

        toman = rial_to_toman(price)

        await update.message.reply_text(
            "₿ قیمت بیت کوین\n\n"
            f"💰 {toman:,.0f} تومان"
        )

    except Exception as e:

        print("Bitcoin Error:", e)

        await update.message.reply_text(
            "❌ خطا در دریافت قیمت بیت کوین"
        )


# =========================
# طلای ۱۸ عیار
# =========================

async def gold_price(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if not await check_user_limit(update):
        return

    try:

        xaut_price_irr = get_nobitex_price("xaut")

        xaut_price_toman = rial_to_toman(
            xaut_price_irr
        )

        TROY_OUNCE_GRAMS = 31.1034768
        PURITY_18K = 0.75

        gold_18k_per_gram = (
            xaut_price_toman
            / TROY_OUNCE_GRAMS
            * PURITY_18K
        )

        await update.message.reply_text(
            "🥇 قیمت طلای ۱۸ عیار\n\n"
            f"⚖️ هر گرم:\n"
            f"💰 {gold_18k_per_gram:,.0f} تومان"
        )

    except Exception as e:

        print("Gold Error:", e)

        await update.message.reply_text(
            "❌ خطا در دریافت قیمت طلا"
        )


# =========================
# نقره
# =========================

async def silver_price(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if not await check_user_limit(update):
        return

    try:

        silver_price_irr = get_nobitex_price("slvon")

        silver_price_toman = rial_to_toman(
            silver_price_irr
        )

        TROY_OUNCE_GRAMS = 31.1034768

        silver_per_gram = (
            silver_price_toman
            / TROY_OUNCE_GRAMS
        )

        await update.message.reply_text(
            "🥈 قیمت نقره\n\n"
            f"⚖️ هر گرم:\n"
            f"💰 {silver_per_gram:,.0f} تومان"
        )

    except Exception as e:

        print("Silver Error:", e)

        await update.message.reply_text(
            "❌ قیمت نقره در API نوبیتکس قابل دریافت نیست."
        )


# =========================
# بازگشت
# =========================

async def back_to_start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    keyboard = [
        ["📖 راهنما"],
        ["💱 انتخاب دارایی"]
    ]

    reply_markup = ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True
    )

    await update.message.reply_text(
        "🔙 به منوی اصلی برگشتید.",
        reply_markup=reply_markup
    )


# =========================
# ساخت ربات
# =========================

app = Application.builder().token(TOKEN).build()


# =========================
# Handler ها
# =========================

app.add_handler(
    CommandHandler("start", start)
)

app.add_handler(
    MessageHandler(
        filters.TEXT & filters.Regex("^📖 راهنما$"),
        guide
    )
)

app.add_handler(
    MessageHandler(
        filters.TEXT & filters.Regex("^💱 انتخاب دارایی$"),
        choose_asset
    )
)

app.add_handler(
    MessageHandler(
        filters.TEXT & filters.Regex("^🪙 تتر$"),
        tether_price
    )
)

app.add_handler(
    MessageHandler(
        filters.TEXT & filters.Regex("^₿ بیت کوین$"),
        bitcoin_price
    )
)

app.add_handler(
    MessageHandler(
        filters.TEXT & filters.Regex("^🥇 طلا$"),
        gold_price
    )
)

app.add_handler(
    MessageHandler(
        filters.TEXT & filters.Regex("^🥈 نقره$"),
        silver_price
    )
)

app.add_handler(
    MessageHandler(
        filters.TEXT & filters.Regex("^🔙 بازگشت$"),
        back_to_start
    )
)


# =========================
# اجرا
# =========================

print("Bot Started...")

app.run_polling()

