# Family Hub

A static, mobile-friendly private family dashboard deployed to Cloudflare Pages.

## Edit

Most routine changes are made directly in `index.html`:

- Update **Today** and **This week** once a week.
- Replace `href="#"` placeholders with trusted shared links.
- Keep schedules in Google Calendar and files in Google Drive; use this page as an index.
- Never store passwords, alarm codes, identity documents, Social Security numbers, or financial account details here.

## Cloudflare Pages settings

- Project: `wangder-pages-test`
- Production branch: `main`
- Root directory: `family-hub`
- Build command: `exit 0`
- Output directory: `.`
- Custom domain: `test.wangder.xyz`

Cloudflare Access should remain enabled for the custom domain. Add family members by exact email address rather than allowing all one-time-PIN users.

## Local preview

Run this command from the `family-hub` directory:

```bash
python3 -m http.server 8000
```

Then open `http://localhost:8000`.
