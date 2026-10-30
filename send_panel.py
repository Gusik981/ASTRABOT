import asyncio
import json
import os
import sys
import discord

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

from cogs.tickets import TicketLauncherView, ASTRAGRIEF_COLOR

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config.json")


def load_token():
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            cfg = json.load(f)
            return cfg.get("token")
    return os.getenv("DISCORD_TOKEN") or os.getenv("TOKEN")


TOKEN = load_token()

intents = discord.Intents.default()
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f"Подключен как: {client.user} (ID: {client.user.id})")

    if not client.guilds:
        print("\n[!] Бот еще не добавлен ни на один сервер Discord!")
        print("Перейдите по ссылке и пригласите бота:")
        print(f"https://discord.com/oauth2/authorize?client_id={client.user.id}&permissions=8&scope=bot%20applications.commands")
        await client.close()
        return

    target_channel = None

    for guild in client.guilds:
        print(f"\n==========================================")
        print(f"Сервер: {guild.name} (ID: {guild.id})")
        print(f"==========================================")
        print("Каналы сервера:")
        for ch in guild.text_channels:
            print(f" - #{ch.name} (ID: {ch.id})")
            if "тикет" in ch.name.lower() or "ticket" in ch.name.lower():
                target_channel = ch

    if target_channel:
        print(f"\n[+] Найден целевой канал для тикетов: #{target_channel.name} (ID: {target_channel.id})")

        embed = discord.Embed(
            title="📌 >> AstraGrief | Центр поддержки",
            description=(
                "Добро пожаловать в центр поддержки сервера **AstraGrief**!\n\n"
                "Возникли вопросы по донату, технические сложности, краши или хотите предложить идею? "
                "Создайте приватное обращение к персоналу проекта.\n\n"
                "**Правила подачи тикета:**\n"
                "│ 📌・Формулируйте вопрос четко, понятно и без лишнего спама.\n"
                "│ 📎・Прикрепляйте скриншоты, чеки или логи при наличии.\n"
                "│ ⏳・Специалисты ответят вам в порядке очереди прямо в канале тикета.\n\n"
                "⬇️ **Для создания тикета выберите нужный раздел в меню ниже:**"
            ),
            color=ASTRAGRIEF_COLOR
        )
        embed.set_footer(text="AstraGrief >> Поддержка • Выберите раздел в меню ⬇️")

        view = TicketLauncherView(None)
        msg = await target_channel.send(embed=embed, view=view)
        print(f"✅ УСПЕХ! Панель тикетов отправлена в #{target_channel.name}! ID сообщения: {msg.id}")
    else:
        print("\n[?] Канал со словом 'тикет' или 'ticket' не найден автоматически.")
        print("Вы можете создать такой канал на сервере и перезапустить send_panel.py,")
        print("либо использовать слэш-команду /ticket-panel прямо в нужном канале Discord!")

    await client.close()


if __name__ == "__main__":
    if not TOKEN or TOKEN == "YOUR_BOT_TOKEN_HERE":
        print("Укажите токен в config.json перед запуском send_panel.py!")
        sys.exit(1)
    asyncio.run(client.start(TOKEN))
