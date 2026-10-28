# Heaven Developer + Bhupendra thumbnails (2026-10-28, skill thumbnail-design incl. step 3b)

Owner (relayed by the main session): "portfolio and promotion videos k lie in skills ka use ker k 2 thumbnails for each
video bana do", "as a professional designer". Specs here; images never committed (scratchpad thumb/a, thumb/out).
Assets (all the clients' own): Heaven logo = https://bhupendra.pages.dev/heaven-developer-logo.jpg (1536x1517, cut to a
circle r 588 around (739,760) with PIL); Bhupendra avatar = https://bhupendra.pages.dev/avatar.jpg (rembg isnet cutout
made the shirt pattern see-through -> used the square avatar as a card instead); post crops from the 2 recordings
(proj assets/img: pricing, services, invite, review, orders banner); site hero = rec2 recording frame at 1.2 s.
Cards: library/tools/thumb_card.py (rounded, gold or ice border, soft shadow). Build: thumb_make.py spec out.png --variants;
check: thumb_check.py (all 6 "ok": true, issues [] after fixes; every _check.png looked at).

| file | video | direction | fonts | colours | hero | why |
|---|---|---|---|---|---|---|
| t1a | 30 s promo 9:16 | "Gilded seal": quiet luxury, the logo is the whole story | Gloock + InstrumentSerif (+Outfit support) | #020203/#140f1c/#2a1d0c, gold #f7dc94 | logo circle, gold glow 110 px | brand tagline "Premium development, delivered" (footer of every bot post); reads as one gold mark at 108x192 |
| t1b | 30 s promo 9:16 | "Price punch": offer poster | BigShoulders 900 + Outfit | Discord blurple #7c86ff->#1c1f6b, $4 #ffd76a | giant "$4" + real Limited Edition price card | the promo's offer; $4 reads at 108x192 |
| t2a | FULL 119 s 9:16 | "Everything inside": real posts fanned like a dossier | Anton + Montserrat 900 | black/gold | 3 real post cards (services, invite rewards, 5/5 review) | the full video's promise = all the details; cards prove it is real |
| t2b | FULL 119 s 9:16 | "Ember how-to": the orders banner's fiery palette | BebasNeue + WorkSans 800 | ember #ff9a3c / #ffb35c on the banner blurred | real "Heaven Orders" banner | answers the viewer's next question (how to order), 3 verified steps |
| t3a | portfolio 16:9 | "Editorial portrait": the site's own serif mood | InstrumentSerif + Outfit | site --bg #07090d, --ice #6fd3ff | avatar card, ice border | name-first personal brand; avatar + name read at 168x94 |
| t3b | portfolio 16:9 | "Screen showcase": the real site in a tilted frame | BigShoulders 900 + Outfit 800 | black + ice #6fd3ff | site hero screenshot | the video IS a site walkthrough; 3-word skill hook |
Fixes from the checks: t1a logo was bottom-anchored (thumb_make had no vertical placement: added subject "bottom");
t1b "$" overlapped the line above and the price card was cut mid-line; t2a cards ran off the edges; t3a/t3b support text
under 14 px at 320 wide (raised to 64/62 px, dropped one line); t3b boxed line wrapped and overlapped itself.
