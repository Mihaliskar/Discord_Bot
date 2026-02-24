import discord
from discord.ext import commands
import logging
from pathlib import Path
import sqlite3

from ai import *

class discord_func(commands.Cog):
    def __init__(self, bot, openai_key):
        self.bot = bot
        self.openai = ai(openai_key)
        self.db = sqlite3.connect("Discord_Bot/usage.db")
        self.db.execute("""
            CREATE TABLE IF NOT EXISTS user_usage (
                name   TEXT PRIMARY KEY,
                tokens INTEGER NOT NULL DEFAULT 0
            )
        """)
        self.db.commit()

    def add_usage(self, name: str, usage):
        # Responses API fields
        in_tok = getattr(usage, "input_tokens", 0) or 0
        out_tok = getattr(usage, "output_tokens", 0) or 0
        tot_tok = getattr(usage, "total_tokens", 0) or (in_tok + out_tok)

        self.db.execute("""
            INSERT INTO user_usage(name, tokens)
            VALUES (?, ?)
            ON CONFLICT(name) DO UPDATE SET
            tokens = tokens + excluded.tokens
        """, (name, tot_tok))
        self.db.commit()

        return tot_tok

    async def get_file(self, msg):
        files = []
        for attachment in msg.attachments:
            SAVE_DIR = Path("Discord_Bot/reply_files")
            SAVE_DIR.mkdir(parents=True, exist_ok=True)

            safe_name = Path(attachment.filename).name
            dest = SAVE_DIR / safe_name

            if dest.exists():
                stem, suffix = dest.stem, dest.suffix
                n = 1
                while True:
                    candidate = SAVE_DIR / f"{stem} ({n}){suffix}"
                    if not candidate.exists():
                        dest = candidate
                        break
                    n += 1

            await attachment.save(dest)
            files.append(dest)
        return files
    
    def save_file(self, text):
        SAVE_DIR = Path("Discord_Bot/reply_files")
        SAVE_DIR.mkdir(parents=True, exist_ok=True)

        safe_name = Path("reply.txt").name
        dest = SAVE_DIR / safe_name

        if dest.exists():
            stem, suffix = dest.stem, dest.suffix
            n = 1
            while True:
                candidate = SAVE_DIR / f"{stem} ({n}){suffix}"
                if not candidate.exists():
                    dest = candidate
                    break
                n += 1
        with open(dest, "w") as file:
                file.write(text)
        return dest
    
    def split_message(self, msg):
        max_len=975
        if max_len <= 0:
            return ["oops"]

        chunks = ["name"]

        if msg is None:
            return chunks

        if msg == "":
            return chunks

        i = 0
        n = len(msg)

        while i < n:
            end = i + max_len
            if end > n:
                end = n

            chunk = msg[i:end]
            chunks.append(chunk)

            i = end

        return chunks

        

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Hello, {self.bot.user.name}")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        
        #await self.bot.process_commands(message)

    

    @commands.command()
    async def hello(self, ctx):
        #message = "Hello"
        #instruct = "Give a friendly reply to the message by the user" + ctx.author
        #response = talk_openai(message, instruct)
        #await ctx.send(response)
        await ctx.send(f"Hello, {ctx.author.mention}!")

    @commands.command()
    async def ask(self, ctx, *, msg):
        user_name = ctx.author.display_name
        message = msg
        instruct = f"give a short and friendly reply to the user named {user_name}"
        reply = ""
        async with ctx.typing():
            try:
                reply, usage = self.openai.talk_openai(message, instruct)
                self.add_usage(ctx.author.name, usage)
            except Exception as e:
                await ctx.send(f"Sorry {ctx.author.mention}, I run into an error: {e}")
                return

        replies = self.split_message(reply)
        replies[0] = ctx.author.mention 
        for r in replies:
            await ctx.send(f"{r}")


    @commands.command()
    async def jarvis(self, ctx):
        await ctx.send("/hello -> Say hello to the bot \n /ask message -> Ask a question to chat gpt \n /jarvis -> Get a list of all the commands " \
        "\n /code message -> Ask chat gpt for coding help \n /vibe message or file -> Fix code using chat gpt by providing a file containing the code \n /solve message or file -> Solve assignments using chat gpt " \
        "\n /summarize message or file -> Get a summary of lecture slides \n /quiz message or file -> Get a quiz on slides \n /usage -> Get the total tockens the users have used")

    @commands.command()
    async def code(self, ctx, *, msg):
        user_name = ctx.author.display_name
        message = msg
        instruct = f"give a complete and friendly reply to the user named {user_name}, But keep it correct and informative"
        reply = ""
        async with ctx.typing():
            try:
                reply, usage = self.openai.code_openai(message, instruct)
                self.add_usage(ctx.author.name, usage)
            except Exception as e:
                await ctx.send(f"Sorry {ctx.author.mention}, I run into an error: {e}")
                return

        replies = self.split_message(reply)
        replies[0] = ctx.author.mention 
        for r in replies:
            await ctx.send(f"{r}")

    @commands.command()
    async def vibe(self, ctx, *, msg):
        files = await self.get_file(ctx.message)
        if(len(files) != 1):
            await ctx.send(f"{ctx.author.mention} Please provide one file")
            return
        user_name = ctx.author.display_name
        message = msg
        instruct = f"Return only the fixed code. No explanations needed"
        reply = ""
        async with ctx.typing():
            try:
                reply, usage = self.openai.vibe_openai(message, instruct, files[0], 0)
                self.add_usage(ctx.author.name, usage)
            except Exception as e:
                await ctx.send(f"Sorry {ctx.author.mention}, I run into an error: {e}")
                return

        dest = self.save_file(reply)

        message = reply
        instruct = f"Explain the improvements made in this code"
        reply = ""
        async with ctx.typing():
            try:
                reply, usage = self.openai.vibe_openai(message, instruct, files[0], 1)
                self.add_usage(ctx.author.name, usage)
            except Exception as e:
                await ctx.send(f"Sorry {ctx.author.mention}, I run into an error: {e}")
                return

        await ctx.send(content = f"{ctx.author.mention}", file = discord.File(dest, filename=dest.name))
        replies = self.split_message(reply)
        replies[0] = ctx.author.mention 
        for r in replies:
            await ctx.send(f"{r}")

    @commands.command()
    async def solve(self, ctx, *, msg = " "):
        files = await self.get_file(ctx.message)
        mode = 0
        if(len(files) == 0):
            mode = 0
        elif (len(files) == 1):
            mode = 1
        else:
            await ctx.send(f"{ctx.author.mention} Please provide at most one file")
            return
        user_name = ctx.author.display_name
        message = msg
        if (mode == 1):
            message = " "
        instruct = f"Solve the following."
        reply = ""
        async with ctx.typing():
            try:
                if (mode == 0):
                    reply, usage = self.openai.solve_openai(message, instruct, "", mode)
                    self.add_usage(ctx.author.name, usage)
                elif (mode == 1):
                    reply, usage = self.openai.solve_openai(message, instruct, files[0], mode)
                    self.add_usage(ctx.author.name, usage)
            except Exception as e:
                await ctx.send(f"Sorry {ctx.author.mention}, I run into an error: {e}")
                return
        replies = self.split_message(reply)
        replies[0] = ctx.author.mention 
        for r in replies:
            await ctx.send(f"{r}")

    @commands.command()
    async def summarize(self, ctx, *, msg = " "):
        files = await self.get_file(ctx.message)
        mode = 0
        if(len(files) == 0):
            mode = 0
        elif (len(files) == 1):
            mode = 1
        else:
            await ctx.send(f"{ctx.author.mention} Please provide at most one file")
            return
        user_name = ctx.author.display_name
        message = msg
        if (mode == 1):
            message = " "
        instruct = f"Summarize the following text."
        reply = ""
        async with ctx.typing():
            try:
                if (mode == 0):
                    reply, usage = self.openai.summarize_openai(message, instruct, "", mode)
                    self.add_usage(ctx.author.name, usage)
                elif (mode == 1):
                    reply, usage = self.openai.summarize_openai(message, instruct, files[0], mode)
                    self.add_usage(ctx.author.name, usage)
            except Exception as e:
                await ctx.send(f"Sorry {ctx.author.mention}, I run into an error: {e}")
                return
        replies = self.split_message(reply)
        replies[0] = ctx.author.mention 
        for r in replies:
            await ctx.send(f"{r}")

    @commands.command()
    async def quiz(self, ctx, *, msg = " "):
        files = await self.get_file(ctx.message)
        mode = 0
        if(len(files) == 0):
            mode = 0
        elif (len(files) == 1):
            mode = 1
        else:
            await ctx.send(f"{ctx.author.mention} Please provide at most one file")
            return
        user_name = ctx.author.display_name
        message = msg
        if (mode == 1):
            message = " "
        instruct = f"Give me 10 questions of multiple choise and the correct answers based on the input. FIrst all the questions and in the end all the answers"
        reply = ""
        async with ctx.typing():
            try:
                if (mode == 0):
                    reply, usage = self.openai.quiz_openai(message, instruct, "", mode)
                    self.add_usage(ctx.author.name, usage)
                elif (mode == 1):
                    reply, usage = self.openai.quiz_openai(message, instruct, files[0], mode)
                    self.add_usage(ctx.author.name, usage)
            except Exception as e:
                await ctx.send(f"Sorry {ctx.author.mention}, I run into an error: {e}")
                return
        replies = self.split_message(reply)
        replies[0] = ctx.author.mention
        for r in replies:
            await ctx.send(f"{r}")
        
    @commands.command()
    async def usage(self, ctx):
        rows = self.db.execute(
            "SELECT name, tokens FROM user_usage ORDER BY tokens DESC"
        ).fetchall()

        if not rows:
            await ctx.send("No usage data yet.")
            return

        # Build a readable leaderboard-style message
        lines = ["**Token usage:**"]
        for i, (name, tokens) in enumerate(rows, start=1):
            lines.append(f"{i}. {name}: {tokens}")

        # Discord has a 2000 char limit; send in chunks
        msg = "\n".join(lines)
        if len(msg) <= 1900:
            await ctx.send(msg)
        else:
            chunk = ""
            for line in lines:
                if len(chunk) + len(line) + 1 > 1900:
                    await ctx.send(chunk)
                    chunk = ""
                chunk += line + "\n"
            if chunk.strip():
                await ctx.send(chunk)
        

