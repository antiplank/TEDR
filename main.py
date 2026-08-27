"""TEDR - The Expanse Dice Roller, a Discord dice bot.

Slash-command rewrite. Prefix commands (!e, !churn, ...) are gone; what remains
of them is a migration notice that points people at the new commands.

The notice is a SUNSET FEATURE. Reading "!e" out of a channel requires the
Message Content privileged intent, which is the very thing slash commands let
you drop. So:

  TEDR_LEGACY_NOTICE=on   -> notice active, message_content intent requested
  TEDR_LEGACY_NOTICE=off  -> notice gone, intent not requested

Run with it on for a few weeks, then turn it off AND untick Message Content in
the Developer Portal. Until you do both, you are still a privileged-intent bot.

Requires Python 3.10+ and discord.py 2.x.

Environment:
  DISCORD_TOKEN         (required) bot token
  TEDR_DATA_DIR        (optional) defaults to /home/plank
  TEDR_GUILD_ID        (optional) sync commands to one guild for instant
                        testing; leave unset to sync globally
  TEDR_LEGACY_NOTICE   (optional) "on" (default) or "off"
"""

from __future__ import annotations

import asyncio
import collections
import inspect
import json
import logging
import os
import random
import re
import tempfile
from pathlib import Path
from typing import Optional

import discord
from discord import app_commands
from dotenv import load_dotenv

__version__ = "2.1.0"

log = logging.getLogger("tedr")

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
DATA_DIR = Path(os.getenv("TEDR_DATA_DIR", "/home/plank"))
IMAGE_DIR = DATA_DIR / "images"
CHURN_FILE = DATA_DIR / "churn.json"
GUILD_ID = os.getenv("TEDR_GUILD_ID")
LEGACY_NOTICE = os.getenv("TEDR_LEGACY_NOTICE", "on").strip().lower() != "off"

MAX_DICE = 100
MAX_SIDES = 1000
MAX_BONUS = 10_000
MAX_LABEL = 200
MIN_CHURN = 0
MAX_CHURN = 30

DICE_RE = re.compile(r"\A(\d*)d(\d+)\Z", re.IGNORECASE)

CHURN_INTRO = (
    "Your churn counter has been created and set to zero. "
    "Use `/churn add` to change it and `/churn reset` to zero it again."
)

POPCORN = "<a:meow_popcorn:897966437556183050>"
TEASES = (
    "{user} is sealing your fate. " + POPCORN,
    "{user} is deciding whether to space you or not. " + POPCORN,
    "Get ready for the juice, {user} is rolling in secret. " + POPCORN,
    "Don't worry, I'm sure {user} is just rolling dice for fun. " + POPCORN,
)

DICE_SUGGESTIONS = ("3d6", "1d20", "2d6", "1d100", "4d6", "2d10", "1d8", "1d4")


# discord.py added the "silent" send kwarg in 2.3; degrade gracefully below it.
NOTICE_SUPPORTS_SILENT = "silent" in inspect.signature(
    discord.abc.Messageable.send
).parameters


class RollInputError(app_commands.AppCommandError):
    """Bad dice string. Message is shown to the user verbatim."""


# ---------------------------------------------------------------- storage


class ChurnStore:
    """Churn counters keyed by Discord user ID, persisted as one JSON file.

    All mutations go through a single asyncio.Lock, and disk writes happen in
    a worker thread so the event loop never blocks on I/O. Writes are atomic
    (temp file + os.replace), so a crash mid-write cannot truncate the data.
    """

    def __init__(self, path: Path) -> None:
        self._path = path
        self._lock = asyncio.Lock()
        self._data: Optional[dict[str, int]] = None

    # -- blocking helpers, only ever called via asyncio.to_thread ----------

    def _load_sync(self) -> dict[str, int]:
        try:
            with self._path.open(encoding="utf-8") as handle:
                raw = json.load(handle)
        except FileNotFoundError:
            return {}
        except (OSError, json.JSONDecodeError):
            log.exception("Could not read %s; starting empty", self._path)
            return {}

        if not isinstance(raw, dict):
            log.error("%s is not a JSON object; starting empty", self._path)
            return {}

        cleaned: dict[str, int] = {}
        for key, value in raw.items():
            try:
                cleaned[str(key)] = _clamp_churn(int(value))
            except (TypeError, ValueError):
                log.warning("Dropping malformed churn entry %r=%r", key, value)
        return cleaned

    def _save_sync(self, data: dict[str, int]) -> None:
        self._path.parent.mkdir(parents=True, exist_ok=True)
        handle_fd, tmp_name = tempfile.mkstemp(dir=self._path.parent, suffix=".tmp")
        tmp_path = Path(tmp_name)
        try:
            with os.fdopen(handle_fd, "w", encoding="utf-8") as handle:
                json.dump(data, handle)
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(tmp_path, self._path)
        except BaseException:
            tmp_path.unlink(missing_ok=True)
            raise

    # -- async API; each method takes the lock exactly once ----------------

    async def _loaded(self) -> dict[str, int]:
        if self._data is None:
            self._data = await asyncio.to_thread(self._load_sync)
        return self._data

    async def _flush(self, data: dict[str, int]) -> None:
        await asyncio.to_thread(self._save_sync, dict(data))

    async def ensure(self, user_id: int) -> bool:
        """Create a zeroed entry if absent. Returns True if it was created."""
        async with self._lock:
            data = await self._loaded()
            key = str(user_id)
            if key in data:
                return False
            data[key] = 0
            await self._flush(data)
            return True

    async def get(self, user_id: int) -> int:
        async with self._lock:
            data = await self._loaded()
            return data.get(str(user_id), 0)

    async def add(self, user_id: int, delta: int) -> int:
        async with self._lock:
            data = await self._loaded()
            key = str(user_id)
            data[key] = _clamp_churn(data.get(key, 0) + delta)
            await self._flush(data)
            return data[key]

    async def reset(self, user_id: int) -> int:
        async with self._lock:
            data = await self._loaded()
            data[str(user_id)] = 0
            await self._flush(data)
            return 0


def _clamp_churn(value: int) -> int:
    return max(MIN_CHURN, min(MAX_CHURN, value))


# ---------------------------------------------------------------- dice


def parse_dice(raw: str) -> tuple[int, int]:
    """Turn "2d10" / "d20" into (count, sides), or raise RollInputError."""
    match = DICE_RE.match(raw.strip())
    if not match:
        raise RollInputError(
            f"`{raw}` isn't a dice format I recognise. Try `3d6`, `2d10` or `d20`."
        )
    count = int(match.group(1) or 1)
    sides = int(match.group(2))
    if not 1 <= count <= MAX_DICE:
        raise RollInputError(f"Roll between 1 and {MAX_DICE} dice, please.")
    if not 1 <= sides <= MAX_SIDES:
        raise RollInputError(f"Dice need 1 to {MAX_SIDES} sides.")
    return count, sides


def _sanitize(text: str) -> str:
    """Strip characters that would break out of a Markdown code block."""
    return text.replace("`", "'").replace("\n", " ").strip()


def format_roll(count: int, sides: int, bonus: int, label: str,
                results: list[int]) -> str:
    tally = collections.Counter(results)
    shown = [f"**{v}**" if tally[v] > 1 else str(v) for v in results]
    total = sum(results) + bonus

    body = (
        f"**{count}d{sides}** + ***{bonus}***\n\n"
        f"{' + '.join(shown)} + *{bonus}* = **{total}**"
    )
    if count == 3 and sides == 6:
        body += f"\n\nDRAMA\n```css\n   [{results[-1]}]```"
    if label:
        body = f"```ini\n[{label}]```\n{body}"
    return body


# ---------------------------------------------------------------- client


class TEDR(discord.Client):
    def __init__(self) -> None:
        intents = discord.Intents.default()
        # Only ask for the privileged intent while the migration notice needs it.
        intents.message_content = LEGACY_NOTICE
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)
        self.store = ChurnStore(CHURN_FILE)
        # command name -> id, used to render clickable </command:id> mentions
        self.command_ids: dict[str, int] = {}
        self._warned_empty = False

    async def setup_hook(self) -> None:
        if GUILD_ID:
            guild = discord.Object(id=int(GUILD_ID))
            self.tree.copy_global_to(guild=guild)
            synced = await self.tree.sync(guild=guild)
            log.info("Synced %d commands to guild %s", len(synced), GUILD_ID)
        else:
            synced = await self.tree.sync()
            log.info("Synced %d commands globally", len(synced))
        self.command_ids = {command.name: command.id for command in synced}

    async def on_ready(self) -> None:
        log.info("Logged in as %s (v%s) in %d guild(s)",
                 self.user, __version__, len(self.guilds))
        if LEGACY_NOTICE:
            log.info(
                "Legacy prefix notice: ON (watching for %s). Message Content "
                "intent requested: %s. Set TEDR_LEGACY_NOTICE=off and untick "
                "Message Content in the Developer Portal once users have moved.",
                ", ".join("!" + k for k in sorted(LEGACY_MAP)),
                self.intents.message_content,
            )
        else:
            log.info("Legacy prefix notice: OFF")

    def mention(self, path: str) -> str:
        """Render "roll" or "churn add" as a clickable command mention."""
        root = path.split()[0]
        command_id = self.command_ids.get(root)
        return f"</{path}:{command_id}>" if command_id else f"`/{path}`"

    # -- migration notice --------------------------------------------------

    async def on_message(self, message: discord.Message) -> None:
        if not LEGACY_NOTICE or message.author.bot:
            return

        if not message.content:
            # Either a genuinely empty message (embed/attachment only), or the
            # Message Content intent is not actually granted. Warn once so the
            # cause is visible instead of looking like the feature is missing.
            if not self._warned_empty:
                self._warned_empty = True
                log.warning(
                    "Received a message with no content. If this happens for "
                    "every message, the Message Content intent is not enabled "
                    "in the Developer Portal."
                )
            return

        target = legacy_target(message.content)
        if target is None:
            return

        old, new = target
        text = (
            f"`!{old}` has retired - I use slash commands now. "
            f"Try {self.mention(new)} instead, or type `/` in the message "
            f"box to see everything I can do."
        )
        log.info("Legacy !%s from %s in channel %s; sending notice",
                 old, message.author.id, message.channel.id)

        kwargs = dict(allowed_mentions=discord.AllowedMentions.none())
        if NOTICE_SUPPORTS_SILENT:
            kwargs["silent"] = True

        try:
            await message.reply(text, mention_author=False, **kwargs)
            return
        except discord.Forbidden:
            log.warning(
                "No permission to reply in channel %s (needs Read Message "
                "History); falling back to a plain message",
                message.channel.id,
            )
        except discord.HTTPException as exc:
            log.warning("Reply failed in %s (%s); falling back to a plain message",
                        message.channel.id, exc)

        try:
            await message.channel.send(text, **kwargs)
        except discord.Forbidden:
            log.warning(
                "No permission to send messages in channel %s, so the "
                "migration notice cannot be delivered there",
                message.channel.id,
            )
        except discord.HTTPException:
            log.exception("Could not post migration notice in %s", message.channel.id)


HELP_TOKENS = frozenset({"help", "?", "h", "halp"})

# old prefix command -> new slash command path
LEGACY_MAP = {
    "e": "roll",
    "edm": "roll",
    "churn": "churn show",
    "servers": "servers",
    "help": "help",
}


def legacy_target(content: str) -> Optional[tuple[str, str]]:
    """Map an old prefix message to (old_name, new_command_path), or None."""
    content = content.lstrip()
    if not content.startswith("!") or content.startswith("!!"):
        return None
    body = content[1:].strip()
    if not body:
        return None

    parts = body.split(maxsplit=1)
    name = parts[0].lower()
    rest = parts[1] if len(parts) > 1 else ""

    if name not in LEGACY_MAP:
        return None
    if name in {"e", "edm"} and rest.strip().lower() in HELP_TOKENS:
        return name, "help"
    return name, LEGACY_MAP[name]


client = TEDR()
tree = client.tree


# ---------------------------------------------------------------- help


def build_help_embed() -> discord.Embed:
    """The manual. Limits are interpolated so they track the constants."""
    embed = discord.Embed(
        title="TEDR - The Expanse Dice Roller",
        description=(
            "I roll dice and I keep score. Type `/` in any channel I can see "
            "to browse my commands, or use the ones below directly."
        ),
        color=discord.Color.blurple(),
    )
    embed.add_field(
        name="Rolling",
        value=(
            f"{client.mention('roll')} - 3d6 by default, with the last die "
            "called out as DRAMA\n"
            "`dice` - `2d10`, `d20`, `4d6`; anything in `XdY` form\n"
            "`bonus` - added to the total, positive or negative\n"
            "`label` - a note attached to the roll\n"
            "`secret` - only you see the result\n\n"
            "Dice that come up matching are shown in bold."
        ),
        inline=False,
    )
    embed.add_field(
        name="Churn",
        value=(
            f"{client.mention('churn show')} - your current churn\n"
            f"{client.mention('churn add')} - add or subtract an amount\n"
            f"{client.mention('churn reset')} - back to zero\n\n"
            "Churn is per-person and survives restarts."
        ),
        inline=False,
    )
    embed.add_field(
        name="Odds and ends",
        value=(
            f"{client.mention('servers')} - {client.mention('help')} for this "
            "message again"
        ),
        inline=False,
    )
    embed.add_field(
        name="Limits",
        value=(
            f"{MAX_DICE} dice per roll, {MAX_SIDES} sides per die, "
            f"bonus within +/-{MAX_BONUS:,}, labels up to {MAX_LABEL} "
            f"characters, churn from {MIN_CHURN} to {MAX_CHURN}."
        ),
        inline=False,
    )
    embed.set_footer(text=f"TEDR v{__version__}")
    return embed


async def send_image(interaction: discord.Interaction, filename: str,
                     content: Optional[str] = None) -> None:
    path = IMAGE_DIR / filename
    if not path.is_file():
        log.warning("Missing image %s", path)
        await interaction.response.send_message(
            content or "That image has gone missing on my end.",
            ephemeral=content is None,
        )
        return
    await interaction.response.send_message(content, file=discord.File(path))


# ---------------------------------------------------------------- commands


async def dice_autocomplete(
    interaction: discord.Interaction, current: str
) -> list[app_commands.Choice[str]]:
    typed = current.strip().lower()
    pool = [d for d in DICE_SUGGESTIONS if d.startswith(typed)] or list(DICE_SUGGESTIONS)
    if typed and DICE_RE.match(typed) and typed not in pool:
        pool.insert(0, typed)
    return [app_commands.Choice(name=d, value=d) for d in pool[:25]]


@tree.command(name="roll", description="Roll some dice")
@app_commands.describe(
    dice="Dice to roll, e.g. 3d6, 2d10, d20. Defaults to 3d6.",
    bonus="Number added to the total. Can be negative.",
    label="A note to attach to the roll.",
    secret="Only you see the result; the channel just sees that you rolled.",
)
@app_commands.autocomplete(dice=dice_autocomplete)
@app_commands.checks.cooldown(5, 10.0)
async def roll(
    interaction: discord.Interaction,
    dice: str = "3d6",
    bonus: app_commands.Range[int, -MAX_BONUS, MAX_BONUS] = 0,
    label: app_commands.Range[str, None, MAX_LABEL] = "",
    secret: bool = False,
) -> None:
    count, sides = parse_dice(dice)
    results = [random.randint(1, sides) for _ in range(count)]

    embed = discord.Embed(
        description=format_roll(count, sides, bonus, _sanitize(label), results),
        color=discord.Color.random(),
    )
    embed.set_author(
        name=interaction.user.display_name,
        icon_url=interaction.user.display_avatar.url,
    )

    if not secret:
        await interaction.response.send_message(embed=embed)
        return

    await interaction.response.send_message(embed=embed, ephemeral=True)
    await interaction.followup.send(
        random.choice(TEASES).format(user=interaction.user.display_name),
        ephemeral=False,
        allowed_mentions=discord.AllowedMentions.none(),
    )


churn_group = app_commands.Group(
    name="churn", description="Track your personal churn counter"
)
tree.add_command(churn_group)


async def _show_churn(interaction: discord.Interaction, value: int,
                      note: str) -> None:
    await send_image(interaction, f"churn_{value}.png", note)


@churn_group.command(name="show", description="Show your current churn")
async def churn_show(interaction: discord.Interaction) -> None:
    created = await client.store.ensure(interaction.user.id)
    value = await client.store.get(interaction.user.id)
    await _show_churn(interaction, value, f"Churn is at {value}.")
    if created:
        await interaction.followup.send(CHURN_INTRO, ephemeral=True)


@churn_group.command(name="add", description="Add to or subtract from your churn")
@app_commands.describe(amount="How much to add. Use a negative number to subtract.")
async def churn_add(
    interaction: discord.Interaction,
    amount: app_commands.Range[int, -MAX_CHURN, MAX_CHURN],
) -> None:
    created = await client.store.ensure(interaction.user.id)
    value = await client.store.add(interaction.user.id, amount)
    await _show_churn(interaction, value, f"Churn is now at {value}.")
    if created:
        await interaction.followup.send(CHURN_INTRO, ephemeral=True)


@churn_group.command(name="reset", description="Reset your churn to zero")
async def churn_reset(interaction: discord.Interaction) -> None:
    await client.store.ensure(interaction.user.id)
    value = await client.store.reset(interaction.user.id)
    await _show_churn(interaction, value, "Churn has been reset to zero.")


@tree.command(name="help", description="How to use this bot")
async def help_command(interaction: discord.Interaction) -> None:
    await interaction.response.defer(ephemeral=True, thinking=False)
    embed = build_help_embed()
    try:
        await interaction.user.send(embed=embed)
    except discord.Forbidden:
        await interaction.followup.send(embed=embed, ephemeral=True)
        return
    await interaction.followup.send(
        "Sent you a DM with the instructions.", ephemeral=True
    )


@tree.command(name="servers", description="How many servers am I in?")
async def servers(interaction: discord.Interaction) -> None:
    total = len(client.guilds)
    plural = "server" if total == 1 else "servers"
    await interaction.response.send_message(f"I'm in {total} {plural}!")


# ---------------------------------------------------------------- errors


@tree.error
async def on_app_command_error(
    interaction: discord.Interaction, error: app_commands.AppCommandError
) -> None:
    if isinstance(error, RollInputError):
        message = str(error)
    elif isinstance(error, app_commands.CommandOnCooldown):
        message = f"Easy there - try again in {error.retry_after:.0f}s."
    elif isinstance(error, app_commands.TransformerError):
        message = "That value isn't one I can use. Check the command's hints."
    else:
        log.exception(
            "Unhandled error in %s",
            interaction.command.qualified_name if interaction.command else "?",
            exc_info=error,
        )
        message = "Something went wrong on my end."

    try:
        if interaction.response.is_done():
            await interaction.followup.send(message, ephemeral=True)
        else:
            await interaction.response.send_message(message, ephemeral=True)
    except discord.HTTPException:
        log.exception("Could not report error to user")


def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
    log.info("TEDR v%s starting from %s", __version__, Path(__file__).resolve())

    if not TOKEN:
        raise SystemExit("DISCORD_TOKEN is not set. Check your .env file.")
    client.run(TOKEN, log_handler=None)


if __name__ == "__main__":
    main()
