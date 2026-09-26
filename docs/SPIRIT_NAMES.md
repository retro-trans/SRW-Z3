# Spirit naming reference

## Current Z3 corrections (2026-09-26)

The user requested [Akurasu's Z3 Spirit list](https://www.akurasu.net/wiki/Super_Robot_Wars/Z3/Spirits).
It names **闘志 Fury** and **直撃 Break**. The
[pilot database](https://akurasu.net/wiki/Super_Robot_Wars/Z3/Pilot_Database#Asuka_Langley_Shikinami)
confirms Asuka learns Fury at level 33 for 35 SP, matching the reported menu.
These replace Fighting Spirit and Fury respectively in the historical mapping
below. Bonuses, ability/part/Bravery descriptions and compact flags follow the
same identities: U+E007 / 0x86BF becomes Fu; U+E012 / 0x86CA becomes Br.
Costs, effects, unlock levels and glyph cell IDs are unchanged. The separate
戦意高揚 pilot skill remains Fighting Sp; 闘争心 remains Instinct. Canonical names live in
localization/locales/en/spirits.json; translation/ is a generated view.

The current ally strip is `Va So Fu Al Wa Gu Fo St Ac Ze Me Sn As Br Lu Ga Di`.
The earlier Wall/Persist mapping was also superseded by the project's Akurasu
correction: 不屈 is Wall and 鉄壁 is Guard. This request does not rename other
accepted command aliases such as Intuition or Assail.

## Historical reference (2026-09-05; superseded as noted above)

Requested reference: [Spirit Commands, Super Robot Wars Wiki](https://superrobotwars.fandom.com/wiki/Spirit_Commands), checked 2026-09-05.
Names are matched by Japanese identity, not by the old English label.
The page describes several games. Z3's Japanese effect text remains the
authority for damage, healing, targeting and duration; these values are not
changed by the naming correction.

| Japanese | Previous name | Reference name used |
| --- | --- | --- |
| 鉄壁 / 鉄壁＋ | Iron Wall / Iron Wall+ | Wall / Wall+ |
| 不屈 / 不屈＋ | Guard / Guard+ | Persist / Persist+ |
| 覚醒 | Enable | Zeal |
| 闘志 | Zeal | Fighting Spirit |
| 根性 / 根性＋ | Guts / Guts+ | Vigor / Vigor+ |
| ド根性 | Vigor | Guts |
| 直撃 | Direct Hit | Fury |
| 幸運 | Fortune | Luck |
| 努力 | Effort | Gain |
| かく乱 | Confuse | Disrupt |
| 勇気 | Courage | Bravery |
| 友情 | Bonds | Faith |
| 絆 | Ties | Bonds |
| 復活 | Renew | Revival |

Keep existing names when listed as accepted aliases: Accel, Alert, Intuition,
Strike, Assail, Resupply and Hope. Analyze is absent from the supplied page,
so its existing name is retained. Preserve the game's plus variants.

Wall reduces damage to one quarter for one turn in Z3. Persist reduces
damage to one eighth for one battle. Fighting Spirit guarantees a critical
for one attack; Zeal grants the team an extra action.

The ally status row is:

`Va So Fs Al Pe Wa Fo St Ac Ze Me Sn As Fu Lu Ga Di`

The enemy row replaces its last three slots with `/ Di An` (Analyze).
Each abbreviation remains one fixed cell with an uppercase and lowercase
letter. Full names come from `translation/spirits.json`. Descriptions quoting
these commands must use the same names. RPW spirit-name overrides prevent
a shared weapon entry from taking precedence over the Spirit list.
