
import discord
import openai
import re

TOKEN = '{TOKEN}'
OPENAI_API_KEY = '7de5e98dee8dd69bf628b936fb0fd210c650e125b00fda14cabe9da3255cae0a'

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.message_content = True

client = discord.Client(intents=intents)
openai.api_key = OPENAI_API_KEY

# Keywords to detect web development relevance
WEB_DEV_KEYWORDS = ["web development", "website", "frontend", "backend", "full stack", "React", "Node", "HTML", "CSS", "JavaScript"]

# Scam or low-budget keywords
SCAM_KEYWORDS = ["exposure", "unpaid", "free", "low budget", "no budget", "50$", "10$", "cheap", "commission only"]

def is_web_dev_related(text):
    return any(kw.lower() in text.lower() for kw in WEB_DEV_KEYWORDS)

def is_scam_or_low_budget(text):
    return any(kw.lower() in text.lower() for kw in SCAM_KEYWORDS)

def ai_job_check(text):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an assistant helping filter freelance job posts for web development."},
                {"role": "user", "content": f"Is the following message a genuine web development job offer with a fair budget?\n\n{text}"}
            ]
        )
        return "yes" in response['choices'][0]['message']['content'].lower()
    except Exception as e:
        print("OpenAI error:", e)
        return False

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    content = message.content.lower()

    if is_web_dev_related(content) and not is_scam_or_low_budget(content):
        if ai_job_check(content):
            try:
                await message.reply("Hello, Kira is an experienced full-stack developer. He will reply to you in 10 hours.\nPortfolio: https://your-portfolio-link.com")
                kira_user = await client.fetch_user(YOUR_USER_ID)
                await kira_user.send(f"📢 New Web Dev Job:\n{message.content}\nLink: {message.jump_url}")
            except Exception as e:
                print("Error sending message:", e)

client.run(TOKEN)
