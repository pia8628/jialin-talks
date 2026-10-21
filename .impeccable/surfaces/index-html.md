---
version: 1
slug: "index-html"
primary_target: "index.html"
related_targets: []
---

---
version: 1
slug: "index-html"
primary_target: "index.html"
related_targets: []
---

## Scope

Root `index.html` of talks.iterlab.dev (the talk index). Visitor mode: Persuade (personal storefront first, but a talk must be one click away). Talk pages are out of scope for this round.

## Audience and job

Attendees coming back after a talk, colleagues from in-house training, strangers from 方格子/social/search, and organisers sizing up whether to invite her. Actions: open a talk; follow 方格子; invite her to speak (contact channel still undecided by the user).

## Constraints

Real photos only (assets/talks/<slug>/0N.webp); a talk without photos renders text-only. All cards equal weight, no featured card. Colours live in a handful of CSS custom properties because the owner plans to re-skin later. Site name: IterLab Talks (user decision, replaces the comp's placeholder 「IterLab 講義夾」).

## Direction contract

THESIS: The site is a training binder that never gets shelved: an iron-grey cover band with a clear name sleeve, one coloured divider tab per talk standing up from its lower edge, and the active talk's hole-punched page open below. It refuses the speaker-site default of headshot hero plus card grid.

OWN-WORLD: Iron-grey #474C55 embossed PP cover (tiled texture), pure white punched page, near-black #16181B ink, divider tabs coloured by topic (品質管理 #E2583E with dark text, AI 協作開發 #3A6FD8 with white text), one yellow highlighter swipe per talk, metal ring edge at the page's left margin, Noto Sans TC 800 headings, JetBrains Mono for dates and durations only.

STORY: A visitor reads who this is from the name sleeve and tagline, sees every talk as a tab, clicks one and the page flips to it: real classroom photos, the title, date and length, the one sentence that matters, and 翻開講義 →. Then follows 方格子 or invites her.

FIRST VIEWPORT: Cover band is the top 32%: name sleeve top-left (IterLab Talks / 製造業 × Vibe Coder), two-line tagline centre, two outlined white buttons top-right (追蹤方格子, 邀請我分享); tabs as trapezoids along the band's bottom edge, active tab in front. Below, the white page: photo carousel left (47% wide, round dark prev/next, dots under), title 800-weight right with topic chip, mono meta, highlighter line, underlined 翻開講義 → link. Primary action = the tab and the 翻開講義 link.

FORM: Training binder with top divider tabs (comp-3, approved), grounded list position 4 of round 1; seed key dbd4aaeb.

FINISH: unreviewed and undocumented is unfinished; this build ends with the finish review, the verdict, DESIGN.md, and every shipping raster carrying its provenance

Approved comp: .impeccable/mocks/comp-3-top-tabs.webp

## Resolved (2026-10-21)

- Invite channel: mailto iterlab8628@gmail.com (user decision).
- APQP highlighter sentence: 「不用為了改版而全部重寫。」, verbatim from the handout.
- Finish review: ship after three rounds; DESIGN.md and .impeccable/design.json written from the built world.
