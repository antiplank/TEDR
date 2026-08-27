# TEDR — The Expanse Dice Roller

A dice rolling Discord bot for **The Expanse Roleplaying Game**. Rolls any
number of dice or facets with an optional modifier and description. Doubles are
bolded, and a drama die is displayed on a roll of 3d6. Results appear as an
embed in the channel, headed with the name of whoever rolled.

Unofficial and not affiliated with Green Ronin Publishing.

**As of v2.0 the bot uses slash commands.** Type `/` in any channel it can see
and Discord will show you everything, with each option labelled as you fill it
in. The old `!` commands are retired.

---

## Rolling

```
/roll
```

That's the whole thing — with no options it rolls 3d6 and shows the drama die.
Everything below is optional.

```
/roll dice:4d12
/roll dice:2d10 bonus:5
/roll dice:4d12 bonus:-5
/roll dice:3d6 bonus:1 label:Initiative (Bob)
/roll dice:4d6 bonus:2 label:Damage (Eddie)
```

**Descriptions can contain spaces now.** The old parser had to guess where the
modifier ended and the description began, so descriptions had to be crammed
together like `Initiative(Bob)`. Named options removed the guesswork — write
whatever you like.

Options:

- `dice` — anything in `XdY` form. `d20` works as shorthand for `1d20`.
  Autocomplete suggests the common ones.
- `bonus` — added to the total. Negative numbers subtract.
- `label` — a note attached to the roll.
- `secret` — see below.

---

## GM rolls

Set `secret` to True and only you see the result. The channel gets a message
saying you rolled something, without the outcome.

```
/roll dice:3d6 bonus:5 secret:True
```

This replaces the old `!edm`. It uses an ephemeral reply rather than a DM, so
it can't fail because you have DMs closed — and it can't get lost in your
message requests.

---

## Churn counter

Tracks churn with a graphical display. Counters are per-person and persist
between sessions, so yours follows you across every server the bot is in.

```
/churn show           Displays your current churn
/churn add amount:3   Adds three
/churn add amount:-2  Takes two off
/churn reset          Back to zero
```

Churn is clamped to 0–30.

---

## Help

```
/help
```

DMs you the full instructions. If your DMs are closed, it replies privately in
the channel instead.

---

## Coming from the old version?

Every `!` command has a direct replacement:

```
!e 3d6 5              ->  /roll dice:3d6 bonus:5
!edm 3d6 5            ->  /roll dice:3d6 bonus:5 secret:True
!e 3d6 1 Init(Bob)    ->  /roll dice:3d6 bonus:1 label:Init (Bob)
!churn                ->  /churn show
!churn 3              ->  /churn add amount:3
!churn reset          ->  /churn reset
!e help               ->  /help
```

For now, typing an old command gets you a reply pointing at its replacement.
That reminder will be removed once everyone has switched.

Two things that changed along the way: the bot no longer deletes your command
message, because slash commands don't create one in the first place. And it no
longer needs permission to manage messages, or to read your channel history.

---

## Adding it to your server

Use the invite link on the app's Discord profile, or generate one in the
Developer Portal with the `bot` and `applications.commands` scopes. The
`applications.commands` scope is required — without it the slash commands
won't register.

Newly added global commands can take up to an hour to appear the first time.
That's Discord's propagation, not the bot.

---

## Privacy

The bot stores two things, and only for people who use the `/churn` commands: your Discord
user ID and your churn value. No message content, no roll history, no
usernames. Nothing is shared with anyone.

Full [Terms of Service](https://antiplank.github.io/TEDR/terms-of-service.html)
and [Privacy Policy](https://antiplank.github.io/TEDR/privacy-policy.html).

---

This is a labor of love for myself and my friends, but I hope other people can
find it useful.# TEDR — The Expanse Dice Roller

A dice rolling Discord bot for **The Expanse Roleplaying Game**. Rolls any
number of dice or facets with an optional modifier and description. Doubles are
bolded, and a drama die is displayed on a roll of 3d6. Results appear as an
embed in the channel, headed with the name of whoever rolled.

Unofficial and not affiliated with Green Ronin Publishing.

**As of v2.0 the bot uses slash commands.** Type `/` in any channel it can see
and Discord will show you everything, with each option labelled as you fill it
in. The old `!` commands are retired.

---

## Rolling

```
/roll
```

That's the whole thing — with no options it rolls 3d6 and shows the drama die.
Everything below is optional.

```
/roll dice:4d12
/roll dice:2d10 bonus:5
/roll dice:4d12 bonus:-5
/roll dice:3d6 bonus:1 label:Initiative (Bob)
/roll dice:4d6 bonus:2 label:Damage (Eddie)
```

**Descriptions can contain spaces now.** The old parser had to guess where the
modifier ended and the description began, so descriptions had to be crammed
together like `Initiative(Bob)`. Named options removed the guesswork — write
whatever you like.

Options:

- `dice` — anything in `XdY` form. `d20` works as shorthand for `1d20`.
  Autocomplete suggests the common ones.
- `bonus` — added to the total. Negative numbers subtract.
- `label` — a note attached to the roll.
- `secret` — see below.

---

## GM rolls

Set `secret` to True and only you see the result. The channel gets a message
saying you rolled something, without the outcome.

```
/roll dice:3d6 bonus:5 secret:True
```

This replaces the old `!edm`. It uses an ephemeral reply rather than a DM, so
it can't fail because you have DMs closed — and it can't get lost in your
message requests.

---

## Churn counter

Tracks churn with a graphical display. Counters are per-person and persist
between sessions, so yours follows you across every server the bot is in.

```
/churn show           Displays your current churn
/churn add amount:3   Adds three
/churn add amount:-2  Takes two off
/churn reset          Back to zero
```

Churn is clamped to 0–30.

---

## Help

```
/help
```

DMs you the full instructions. If your DMs are closed, it replies privately in
the channel instead.

---

## Coming from the old version?

Every `!` command has a direct replacement:

```
!e 3d6 5              ->  /roll dice:3d6 bonus:5
!edm 3d6 5            ->  /roll dice:3d6 bonus:5 secret:True
!e 3d6 1 Init(Bob)    ->  /roll dice:3d6 bonus:1 label:Init (Bob)
!churn                ->  /churn show
!churn 3              ->  /churn add amount:3
!churn reset          ->  /churn reset
!e help               ->  /help
```

For now, typing an old command gets you a reply pointing at its replacement.
That reminder will be removed once everyone has switched.

Two things that changed along the way: the bot no longer deletes your command
message, because slash commands don't create one in the first place. And it no
longer needs permission to manage messages, or to read your channel history.

---

## Adding it to your server

Use the invite link on the app's Discord profile, or generate one in the
Developer Portal with the `bot` and `applications.commands` scopes. The
`applications.commands` scope is required — without it the slash commands
won't register.

Newly added global commands can take up to an hour to appear the first time.
That's Discord's propagation, not the bot.

---

## Privacy

The bot stores two things, and only for people who use the `/churn` commands: your Discord
user ID and your churn value. No message content, no roll history, no
usernames. Nothing is shared with anyone.

Full [Terms of Service](https://antiplank.github.io/TEDR/terms-of-service.html)
and [Privacy Policy](https://antiplank.github.io/TEDR/privacy-policy.html).

---

This is a labor of love for myself and my friends, but I hope other people can
find it useful.# TEDR — The Expanse Dice Roller

A dice rolling Discord bot for **The Expanse Roleplaying Game**. Rolls any
number of dice or facets with an optional modifier and description. Doubles are
bolded, and a drama die is displayed on a roll of 3d6. Results appear as an
embed in the channel, headed with the name of whoever rolled.

Unofficial and not affiliated with Green Ronin Publishing.

**As of v2.0 the bot uses slash commands.** Type `/` in any channel it can see
and Discord will show you everything, with each option labelled as you fill it
in. The old `!` commands are retired.

---

## Rolling

```
/roll
```

That's the whole thing — with no options it rolls 3d6 and shows the drama die.
Everything below is optional.

```
/roll dice:4d12
/roll dice:2d10 bonus:5
/roll dice:4d12 bonus:-5
/roll dice:3d6 bonus:1 label:Initiative (Bob)
/roll dice:4d6 bonus:2 label:Damage (Eddie)
```

**Descriptions can contain spaces now.** The old parser had to guess where the
modifier ended and the description began, so descriptions had to be crammed
together like `Initiative(Bob)`. Named options removed the guesswork — write
whatever you like.

Options:

- `dice` — anything in `XdY` form. `d20` works as shorthand for `1d20`.
  Autocomplete suggests the common ones.
- `bonus` — added to the total. Negative numbers subtract.
- `label` — a note attached to the roll.
- `secret` — see below.

---

## GM rolls

Set `secret` to True and only you see the result. The channel gets a message
saying you rolled something, without the outcome.

```
/roll dice:3d6 bonus:5 secret:True
```

This replaces the old `!edm`. It uses an ephemeral reply rather than a DM, so
it can't fail because you have DMs closed — and it can't get lost in your
message requests.

---

## Churn counter

Tracks churn with a graphical display. Counters are per-person and persist
between sessions, so yours follows you across every server the bot is in.

```
/churn show           Displays your current churn
/churn add amount:3   Adds three
/churn add amount:-2  Takes two off
/churn reset          Back to zero
```

Churn is clamped to 0–30.

---

## Help

```
/help
```

DMs you the full instructions. If your DMs are closed, it replies privately in
the channel instead.

---

## Coming from the old version?

Every `!` command has a direct replacement:

```
!e 3d6 5              ->  /roll dice:3d6 bonus:5
!edm 3d6 5            ->  /roll dice:3d6 bonus:5 secret:True
!e 3d6 1 Init(Bob)    ->  /roll dice:3d6 bonus:1 label:Init (Bob)
!churn                ->  /churn show
!churn 3              ->  /churn add amount:3
!churn reset          ->  /churn reset
!e help               ->  /help
```

For now, typing an old command gets you a reply pointing at its replacement.
That reminder will be removed once everyone has switched.

Two things that changed along the way: the bot no longer deletes your command
message, because slash commands don't create one in the first place. And it no
longer needs permission to manage messages, or to read your channel history.

---

## Adding it to your server

Use the invite link on the app's Discord profile, or generate one in the
Developer Portal with the `bot` and `applications.commands` scopes. The
`applications.commands` scope is required — without it the slash commands
won't register.

Newly added global commands can take up to an hour to appear the first time.
That's Discord's propagation, not the bot.

---

## Privacy

The bot stores two things, and only for people who use the `/churn` commands: your Discord
user ID and your churn value. No message content, no roll history, no
usernames. Nothing is shared with anyone.

Full [Terms of Service](https://antiplank.github.io/TEDR/terms-of-service.html)
and [Privacy Policy](https://antiplank.github.io/TEDR/privacy-policy.html).

---

This is a labor of love for myself and my friends, but I hope other people can
find it useful.
