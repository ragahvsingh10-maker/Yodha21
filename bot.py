
      import os
import re
import asyncio
import httpx
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, BotCommand

# 🔑 क्रेडेंशियल्स सेटअप
API_ID = "29771444"  
API_HASH = "ce4f9ddc714be71959049cc2a8b6554e"
BOT_TOKEN = "8823361453:AAFR7CfpKHtC1UDOMSaDGJMRnl6ISLORRsY"

app = Client("clean_extractor_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# ⚙️ मास्टर लिस्ट
AVAILABLE_APPS = [
    {"name": "RG VIKRAMJEET", "platform": "classplus", "org_code": "RGVIK"},
    {"name": "RK SIR", "platform": "classplus", "org_code": "VPPST"},
    {"name": "RWA", "platform": "appx", "api_url": "https://appx.co.in"},
    {"name": "SACHIN ACADEMY", "platform": "classplus", "org_code": "ABCD"},
    {"name": "SAMYAK", "platform": "classplus", "org_code": "XYZW"},
    {"name": "SANKALP", "platform": "classplus", "org_code": "MNOQ"},
    {"name": "SCIENCE FUN", "platform": "classplus", "org_code": "SFUN"},
    {"name": "SINGHKORI", "platform": "classplus", "org_code": "SINGH"},
    {"name": "SPACE IAS", "platform": "classplus", "org_code": "SPACE"},
    {"name": "STUDY MANTRA", "platform": "classplus", "org_code": "MANTRA"},
    {"name": "SSC GURUKUL", "platform": "classplus", "org_code": "GURU"},
    {"name": "SSC MAKER", "platform": "classplus", "org_code": "MAKER"},
    {"name": "TARGET PLUS", "platform": "classplus", "org_code": "TPLUS"},
    {"name": "TARGET UPSC", "platform": "classplus", "org_code": "UPSC"},
    {"name": "TEACHING PARIKSHA", "platform": "classplus", "org_code": "TEACH"},
    {"name": "THINK SSC", "platform": "classplus", "org_code": "THINK"},
    {"name": "TUTORS ADDA", "platform": "classplus", "org_code": "TUTOR"},
    {"name": "UC LIVE", "platform": "classplus", "org_code": "UCLIVE"},
    {"name": "Physics Wallah", "platform": "appx", "api_url": "https://appx.co.in"},
    {"name": "Khan Sir Official", "platform": "appx", "api_url": "https://appx.co.in"},
    {"name": "Exampur App", "platform": "appx", "api_url": "https://appx.co.in"},
    {"name": "KTDT", "platform": "classplus", "org_code": "KTDT1"},
    {"name": "MD CLASSES", "platform": "classplus", "org_code": "MDCLS"},
    {"name": "MG CONCEPT", "platform": "classplus", "org_code": "MGCON"},
    {"name": "MOTHER'S LIVE", "platform": "classplus", "org_code": "MOTH"},
    {"name": "NEO SPARK", "platform": "classplus", "org_code": "NEOS"},
    {"name": "NEON CLASSES", "platform": "classplus", "org_code": "NEON"},
    {"name": "NEET KAKAJEE", "platform": "classplus", "org_code": "KAKA"},
    {"name": "NG LEARNERS", "platform": "classplus", "org_code": "NGLR"},
    {"name": "NIDHI ACADEMY", "platform": "classplus", "org_code": "NIDHI"},
    {"name": "NIMISHA BANSAL", "platform": "classplus", "org_code": "NIMI"},
    {"name": "NIRMAN IAS", "platform": "classplus", "org_code": "NIRMAN"},
    {"name": "NOTE BOOK", "platform": "classplus", "org_code": "NOTE"},
    {"name": "OCEAN GURUKUL", "platform": "classplus", "org_code": "OCEAN"},
    {"name": "OFFICERS ACADEMY", "platform": "classplus", "org_code": "OFFIC"},
    {"name": "PARMAR SSC", "platform": "classplus", "org_code": "PARMAR"},
    {"name": "PERFECT ACADEMY", "platform": "classplus", "org_code": "PERF"},
    {"name": "PHYSICS ASINGH", "platform": "classplus", "org_code": "ASINGH"},
    {"name": "PLATFORM", "platform": "classplus", "org_code": "PLAT"},
    {"name": "VASU CONCEPT", "platform": "classplus", "org_code": "VASU"},
    {"name": "VIDYA EDUCATION", "platform": "classplus", "org_code": "VIDYA"},
    {"name": "WINNERS", "platform": "classplus", "org_code": "WIN"},
    {"name": "VIDYA BIHAR", "platform": "classplus", "org_code": "VBIHAR"},
    {"name": "VJ EDUCATION", "platform": "classplus", "org_code": "VJEDU"},
    {"name": "YODHA", "platform": "classplus", "org_code": "YODHA"}
]

USER_DATA = {}

def generate_apps_keyboard(page=0, per_page=10):
    start_idx = page * per_page
    end_idx = start_idx + per_page
    page_apps = AVAILABLE_APPS[start_idx:end_idx]
    buttons = []
    current_row = []
    for idx, app_item in enumerate(page_apps):
        global_idx = start_idx + idx
        btn = InlineKeyboardButton(app_item["name"], callback_data=f"selapp_{global_idx}")
        current_row.append(btn)
        if len(current_row) == 2:
            buttons.append(current_row)
            current_row = []
    if current_row:
        buttons.append(current_row)
    nav_row = []
    if page > 0:
        nav_row.append(InlineKeyboardButton("⬅️ PREVIOUS", callback_data=f"page_{page-1}"))
    if end_idx < len(AVAILABLE_APPS):
        nav_row.append(InlineKeyboardButton("NEXT ➡️", callback_data=f"page_{page+1}"))
    if nav_row:
        buttons.append(nav_row)
    buttons.append([InlineKeyboardButton("🏠 HOME", callback_data="back_home")])
    return InlineKeyboardMarkup(buttons)

async def fetch_courses(client, message, user_id, platform, token):
    buttons = [[InlineKeyboardButton("Batch 1 (Demo)", callback_data="course_01")]]
    await message.reply_text("📚 **Your Purchased Batches:**\nClick to extract parameters.", reply_markup=InlineKeyboardMarkup(buttons))

@app.on_message(filters.command("start"))
async def start_cmd(client, message):
    USER_DATA[message.from_user.id] = {"res": "720", "thumb": None, "platform": None, "target_app": None, "token": None}
    await message.reply_text(
        "🚀 **Bot Started Successfully!**\n\nऐप्स की सूची देखने के लिए बटन दबाएं या सीधे `/apps` लिखें।",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🛍️ Show Apps Menu", callback_data="page_0")]])
    )

@app.on_message(filters.command("apps"))
async def show_apps(client, message):
    await message.reply_text("📱 **Select Target App From Menu:**", reply_markup=generate_apps_keyboard(page=0))

@app.on_callback_query(filters.regex("^(page_|selapp_|back_home)"))
async def callback_dispatcher(client, query: CallbackQuery):
    user_id = query.from_user.id
    data = query.data
    if data == "back_home":
        await query.message.edit_text("🚀 **Welcome Home!**", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🛍️ Show Apps Menu", callback_data="page_0")]]))
    elif data.startswith("page_"):
        numbers = re.findall(r'\d+', data)
        target_page = int(numbers[0]) if numbers else 0
        await query.message.edit_text("📱 **Select Target App From Menu:**", reply_markup=generate_apps_keyboard(page=target_page))
    elif data.startswith("selapp_"):
        numbers = re.findall(r'\d+', data)
        global_idx = int(numbers[0]) if numbers else 0
        selected_app = AVAILABLE_APPS[global_idx]
        USER_DATA[user_id] = {"res": "720", "thumb": None, "platform": selected_app["platform"], "target_app": selected_app}
        back_btn = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back to Apps List", callback_data="page_0")]])
        await query.message.edit_text(f"🎯 **Target Chosen:** {selected_app['name']}\n\nकृपया अपना **ID|Password** भेजें:", reply_markup=back_btn)
    await query.answer()

# ================= अपडेटेड क्रेडेंशियल्स स्प्लिट इंजन =================

@app.on_message(filters.text & ~filters.command(["start", "apps"]))
async def handle_credentials(client, message):
    user_id = message.from_user.id
    if user_id not in USER_DATA or not USER_DATA[user_id].get("platform"):
        await message.reply_text("⚠️ पहले मेनू से ऐप चुनें। कमान: /apps")
        return
        
    raw_text = message.text.strip()
    parsed = re.split(r'[|\s]+', raw_text, maxsplit=1)
    
    if len(parsed) < 2:
        await message.reply_text("❌ फॉर्मेट गलत है। `UserID|Password` भेजें।")
        return
        
    username = parsed[0].strip()
    password = parsed[1].strip()
    platform = USER_DATA[user_id]["platform"]
    target_app = USER_DATA[user_id]["target_app"]
    status = await message.reply_text(f"⏳ {target_app['name']} में लॉगिन किया जा रहा है...")

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/json"
    }

    org_code = target_app.get("org_code", "").lower()
    url = f"https://{org_code}://"
    payload = {"email": username, "password": password} if "@" in username else {"mobileNumber": username, "password": password}
        
    if platform == "appx":
        url = f"{target_app.get('api_url', '')}/v1/auth/login"
        payload = {"email_phone": username, "password": password}

    async with httpx.AsyncClient(headers=headers, timeout=30.0) as http_client:
        try:
            response = await http_client.post(url, json=payload)
            res = response.json()
            token = res.get("data", {}).get("token") or res.get("data", {}).get("access_token") or res.get("token")
            if token:
                USER_DATA[user_id]["token"] = token
                await status.edit_text("✅ लॉगिन सफल! कोर्स लोड हो रहे हैं...")
                await fetch_courses(client, message, user_id, platform, token)
            else:
                await status.edit_text(f"❌ लॉगिन फेल: {res.get('message', 'गलत आईडी या पासवर्ड।')}")
        except Exception as e:
            await status.edit_text(f"❌ एपीआई कनेक्शन त्रुटि: {str(e)}")

if __name__ == "__main__":
    async def set_menu():
        try:
            commands = [BotCommand("start", "🚀 Start the bot"), BotCommand("apps", "🛍️ Show apps menu")]
            await app.set_bot_commands(commands)
        except: pass
    app.start()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(set_menu())
    print("🤖 Bot is live on Koyeb!")
    asyncio.get_event_loop().run_forever()
  
