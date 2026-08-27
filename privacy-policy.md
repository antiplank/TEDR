---
title: Privacy Policy
---

# Privacy Policy for The Expanse Dice Roller

**Effective date:** 27 August 2026
**Last updated:** 27 August 2026

The Expanse Dice Roller ("the Bot") is a dice-rolling and counter-tracking bot for Discord,
operated by Plank ("we", "us"). This policy explains what data the
Bot collects, why, how long it is kept, and how to have it removed.

By adding the Bot to a server or using its commands, you agree to this policy.
If you do not agree, do not use the Bot.

---

## 1. Data we store

The Bot stores exactly two pieces of information, and only for people who use
the `!churn` command:

| Data | Purpose | Example |
| --- | --- | --- |
| Your Discord user ID | Identifies whose counter is whose | `123456789012345678` |
| Your churn value | The counter itself, an integer from 0 to 30 | `7` |

That is the entire persistent data set. Your Discord user ID is a public
identifier assigned by Discord; it is not your email address, your real name, or
your password.

**We do not store:** message content, usernames, nicknames, avatars, server
names, server IDs, channel IDs, email addresses, IP addresses, payment
information, or the results of any dice roll.

## 2. Data we process but do not keep

To respond to a command, the Bot briefly reads information in memory and then
discards it. None of the following is written to persistent storage:

- **Message content.** The Bot reads messages in channels it can see in order to
  detect its command prefix (`!`). Messages that are not commands are discarded
  immediately and are never stored, logged, forwarded, or analysed.
- **Your display name and avatar image URL.** Used to label the roll result, and
  discarded once the message is sent.
- **Dice results.** Generated, displayed, and discarded. No roll history exists.

## 3. Operational logs

The Bot writes technical logs for the purpose of diagnosing errors. These logs
may incidentally contain Discord user IDs, Discord message IDs, and error
traces. They do not contain message content.

Logs are retained for no longer than 30 days and are then
deleted. They are accessible only to Plank.

## 4. Legal basis and purpose

We process the data in Section 1 on the basis of your consent, which you give by
choosing to run the `!churn` command, and on the basis of our legitimate
interest in operating and debugging the service. The data is used solely to
provide the Bot's features. It is not used for profiling, advertising, or
automated decision-making.

## 5. Sharing

We do not sell, rent, trade, or share your data with anyone. There are no
third-party analytics services, no advertising networks, and no data brokers
involved in the operation of the Bot.

The Bot necessarily exchanges data with Discord itself in order to function.
Your use of Discord is governed by
[Discord's Privacy Policy](https://discord.com/privacy), which is separate from
this one.

## 6. Storage and security

Data is stored in a single file on a server controlled by Plank,
located in United States. Access is restricted to Plank.

We take reasonable measures to protect the data, but no system is perfectly
secure. Given the nature of the data — a Discord user ID and a number between 0
and 30 — the consequences of a breach would be minimal. If a breach occurs that
is likely to affect your rights, we will notify affected users through
email to antiplank@gmail.com and comply with any applicable notification laws.

## 7. Retention

Your churn value and user ID are kept until you ask us to delete them, or until
the Bot is permanently shut down, whichever comes first.

Please note that **removing the Bot from a server does not delete your churn
counter.** Counters are tied to your Discord account rather than to any
particular server, so they persist across every server the Bot is in.

## 8. Your rights and how to exercise them

You may request, at any time and free of charge:

- **Access** — a copy of the data we hold about you.
- **Correction** — amendment of an inaccurate value.
- **Deletion** — removal of your entry entirely.
- **Withdrawal of consent** — stop using `!churn` and request deletion.

To make a request, contact us at antiplank@gmail.com. We
will respond within 30 days. To verify a request, we will ask you to send it
from the Discord account concerned, or to confirm the user ID you are asking
about.

You may also reset your own counter to zero at any time with `!churn reset`,
though this leaves your user ID on file with a value of 0. Use the deletion
process above to remove the entry completely.

Depending on where you live, you may have additional rights under laws such as
the GDPR, the UK GDPR, or the CCPA, including the right to lodge a complaint
with your local data protection authority.

## 9. Children

The Bot is not directed at children. Discord's own Terms of Service require
users to be at least 13 years old, or older where local law sets a higher
minimum age. We do not knowingly collect data from anyone below the minimum age
for their region. If you believe a child has used the Bot, contact us at
antiplank@gmail.com and we will delete the associated entry.

## 10. International transfers

The Bot is operated from United States. If you use it from elsewhere,
your user ID and churn value will be processed there.

## 11. Changes to this policy

We may update this policy. Material changes will be announced through
email to antiplank@gmail.com and reflected in the "Last updated" date above. Continued
use of the Bot after a change constitutes acceptance of the revised policy.

## 12. Contact

Plank
antiplank@gmail.com
