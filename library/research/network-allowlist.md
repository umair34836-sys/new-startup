# Network domains for this environment (saved Oct 24 2026)

On Oct 24 2026 the owner switched Network access to FULL (all sites open: visit.talkember.site and www.firecraft.fun
answered 200; both answered 200 again on 2026-10-24 in the audit, curl). If it is ever switched back to "Limited / Allowed domains", this is the list to paste back, one per line.

## Added by the owner
```
huggingface.co
us.aws.cdn.hf.co
cas-server.xethub.hf.co
transfer.xethub.hf.co
openaipublic.azureedge.net
youtube.com
www.youtube.com
*.googlevideo.com
i.ytimg.com
pixabay.com
freesound.org
cdn.freesound.org
api.openverse.org
commons.wikimedia.org
upload.wikimedia.org
archive.org
freemusicarchive.org
incompetech.com
r.jina.ai
s.jina.ai
mcp.exa.ai
api.exa.ai
www.reddit.com
old.reddit.com
```

## Open by default / package managers
```
registry.npmjs.org
pypi.org
files.pythonhosted.org
archive.ubuntu.com
github.com
raw.githubusercontent.com
storage.googleapis.com
fonts.googleapis.com
youtubei.googleapis.com
```

## Worth adding if access is limited again (owner's own sites, for free Crawl4AI screenshots)
```
visit.talkember.site
talkember.site
www.firecraft.fun
firecraft.fun
```

Notes: even with the network open, some services block this cloud IP: Freesound (cdn.freesound.org and freesound.org
return 403; re-checked 2026-10-24), Wikimedia (commons API answered 429 to a single request on 2026-10-24; uploads 429
in bursts: go slowly), pixabay.com (403, 2026-10-24). Jina reader without a key: an earlier session saw 401 "bad IP
reputation"; on 2026-10-24 r.jina.ai answered 403 to a browser User-Agent but 200 to curl's default one, and
`agent-reach read` worked. github.com pages/API: 403 for repos outside the session (proxy), but `git clone` and
raw.githubusercontent.com of public repos worked (2026-10-24).
