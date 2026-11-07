# Thumbnails through the Canva MCP and the gallery Pro editor (measured here 2026-11-07)

Job: SkilloraClouds tutorial thumbnails (skillora-reel-v3 session). Everything below was run in this session.

## Canva MCP (owner asked for Canva; uses the owner's Canva account)
- Upload a local file: `create-upload-url` (name, mime, byte size) then `curl -X POST --data-binary @file <upload_url>`
  (raw bytes, not multipart) -> returns a media id `MAHa...`. Worked for JPG and PNG.
- `create-design` with a brief + `format: "YouTube Thumbnail"` -> job id; poll `get-create-design-async-job` until done.
  The generated layout had an EMPTY image frame (a rect with an image fill) where the brief asked for a screenshot.
- Fill it with the real screenshot: `read-design` with `open_transaction: true` -> transaction id + element locator ids;
  `edit-design` `update_fill` {locator_id, asset_type image, asset_id <media id>} -> auto center-crops the image into the rect;
  then `edit-design` `finalize: "commit"` (no operations). Both designs committed first try.
- `export-design` {type png, width 1280, height 720} -> signed export-download.canva.com URL (curl works, expires in hours).
- Getting a PUBLIC URL for any local image: copy a design (`copy-design`), `add_page` x2, `insert_fill` the asset full-page,
  `resize_element`+`crop_media` for a square logo, commit, `export-design` with `pages: [2]` -> public PNG URL.
  `read-design` with `page_metadata` does NOT see draft pages; use `design_content` with the transaction id.
- Canva's "generate" step is a Canva credit action on the owner's account; two designs were generated for this job.

## gallery Pro editor (gallery.talkember.site MCP, paid plan feature)
- `add_photo_from_url` only takes a public URL: the Canva export URLs above worked (1280x720 PNG saved).
- `edit_photo` with `crop` {left, top, width, height} (fractions) made a clean console crop (bars measured with numpy first).
- `design_image` (size youtube-thumbnail): background photo blur 20 darken 75; photo layer with radius 0.03, border 0.006
  #22c55e, shadow; text font outfit weight 800 size 0.12 with *starred* accent words; pill = text with box_color.
  Result ids are gallery photos; `get_download_link` (60 min) gives a URL curl can fetch. Each design is one edit of the
  daily limit.
- Lesson: "cover" + focus left on a plate that has black bars shows the bars; crop the plate first.

## Both outputs
- Ran `library/tools/thumb_check.py` on every PNG: all ok (no text cut-offs at 168x94).
- Never commit the thumbnails (client media); they live in the session scratchpad and go to the owner with SendUserFile.
