---
name: write-post
description: Turn rough, verbose input (a rant, a brain-dump, dictated notes, a half-formed draft) into a polished post in the user's own voice, and commit it to their Hugo blog repo. Use when the user gives verbose raw material and asks to write it up, turn it into a post, or blog about something.
argument-hint: "[rough notes, or a path to a file containing them]"
---

# write-post

Takes whatever raw material the user hands over and turns it into a
finished blog post that reads like they wrote it, then adds it to their
blog repo as a new post.

The blog is a Hugo site: source at `github.com/wegotoeleven/blog`
(SSH: `git@github.com:wegotoeleven/blog.git`), deployed via GitHub Actions
to `blog.wegotoeleven.xyz`. Posts are Hugo page bundles at
`content/technical/<slug>/index.md` or `content/travelling/<slug>/index.md`.

## Step 1 — Get the raw material

Use whatever was given in args or pasted into the conversation. If args
point to a file path, read it. If nothing usable was provided yet, ask
the user to paste their notes or point at a file — don't guess at a topic.

## Step 2 — Locate the blog repo

The user runs this from inside the blog repo sometimes, but not always.
Don't assume the working directory.

1. Try `git rev-parse --show-toplevel` from cwd. If it succeeds, confirm
   it's actually the blog repo by checking for `hugo.toml` and a
   `content/technical` directory at that root.
2. If that doesn't check out, look for `~/Projects/blog` and apply the
   same fingerprint check.
3. If neither exists, clone it: `git clone git@github.com:wegotoeleven/blog.git ~/Projects/blog`.
4. Run `git status` in the located repo. If the working tree isn't clean,
   stop and tell the user what's uncommitted rather than working around
   it — it might be in-progress work.
5. If clean, `git fetch origin && git pull --ff-only origin main` so the
   new post lands on the latest deployed state.

## Step 3 — Calibrate voice

Read `references/voice-notes.md` in this skill for a starting point, then
read the 2-3 most recently modified posts in whichever of
`content/technical/` or `content/travelling/` matches the new post
(`git log -3 --name-only -- content/<category>` is a quick way to find
the most recent ones). Voice notes are a snapshot and may have drifted —
the actual recent posts are the source of truth.

## Step 4 — Decide category, title, slug, tags, date

- **Category**: `technical` or `travelling`. Infer from the content; ask
  if it's genuinely ambiguous rather than guessing wrong.
- **Title**: derive from the content. Ask if nothing in the material
  suggests one.
- **Slug**: kebab-case of the title, matching existing posts
  (e.g. `using-markdown-to-write-documentation`).
- **Tags**: 2-4 lowercase tags. Check existing posts in the category
  first (`grep -h '^tags:' content/<category>/*/index.md`) and reuse
  matching ones instead of inventing near-duplicates.
- **Date**: today, `date +%F`, in the site's `date: YYYY-MM-DD` format.

## Step 5 — Rewrite

This is a rewrite, not new authorship:

- Preserve every fact, opinion, and technical detail from the source.
  Don't add claims, steps, or opinions that weren't in the original.
- Cut filler, false starts, and repetition — the artifacts of rough or
  spoken input.
- Restructure for readability: headers if it's long enough to warrant
  them (matching how existing posts in that category use headers — the
  travel posts essentially never do), code fences for anything command-
  line, short paragraphs.
- Match the calibrated voice from Step 3, not a generic "blog voice".
- If the source material is ambiguous, contradicts itself, or is missing
  something a reader would need, ask — don't silently resolve it or
  paper over the gap.

## Step 6 — Write the file

Create `content/<category>/<slug>/index.md`:

```
---
title: "<title>"
date: <YYYY-MM-DD>
categories: ["<category>"]
tags: ["<tag1>", "<tag2>"]
---

<body>
```

If the user attached or referenced local images, copy them into an
`images/` subfolder alongside `index.md` and reference them with relative
paths (`images/foo.png`), matching the existing page-bundle convention.

## Step 7 — Verify

If `hugo` is installed, run `hugo --minify` from the repo root and fix
anything that errors before moving on. Delete the generated `public/`
directory afterward (it's gitignored, don't let it linger uncommitted).
If `hugo` isn't installed on this machine, say so and skip this step
rather than blocking on it.

## Step 8 — Show and confirm

Show the user the finished post (rendered markdown, not raw HTML) and get
a go/no-go before touching git. Apply requested edits and re-verify.

## Step 9 — Commit and push

Once approved:

```
git add content/<category>/<slug>
git commit -m "<short, imperative summary of the post>"
git push origin main
```

This repo pushes straight to `main` — no PR workflow. Tell the user it's
committed and pushed, and that GitHub Actions will build and deploy it
automatically (link: the repo's Actions tab).
