# Going live — setup checklist

Everything below is done once. Until a step is done the site still works: without accounts everything is open
(like now), without video hosting every video shows "coming soon", without payment the Join page says
"Online payment opens soon".

All keys go into a file called `.env.local` in this folder (copy `.env.local.example`). Never share or commit it.

---

## 1. Accounts — Supabase (free to start)

1. Create an account at **supabase.com** → **New project** (region: *Frankfurt* is closest to Israel). Save the database password somewhere safe.
2. **SQL Editor → New query** → paste all of `supabase/schema.sql` → **Run**.
3. **Project Settings → API**: copy into `.env.local`
   - `Project URL` → `NEXT_PUBLIC_SUPABASE_URL`
   - `anon public` key → `NEXT_PUBLIC_SUPABASE_ANON_KEY`
   - `service_role` key → `SUPABASE_SERVICE_ROLE_KEY` (secret!)
4. **Authentication → Email templates → Magic Link**: make the email show the code. Replace the body with:
   ```
   <h2>Your Psychometry login code</h2>
   <p style="font-size:28px;letter-spacing:6px"><b>{{ .Token }}</b></p>
   <p>Enter it on the login page. It expires in an hour.</p>
   ```
5. **Authentication → URL configuration**: *Site URL* = your website address (e.g. `https://psychometry.co.il`);
   add `http://localhost:3001/**` and `https://<your-domain>/**` to *Redirect URLs*.
6. **Google login** (optional but recommended): **Authentication → Providers → Google → Enable**. It needs a
   Google "OAuth client" — Supabase's page links to the exact Google Cloud steps (about 10 minutes).
7. For real volumes of email, add your own email sender under **Authentication → SMTP** (e.g. Resend, free tier) —
   Supabase's built-in sender is limited to a few emails per hour.

**Giving access by hand** (bank transfer, free pass, testing):
```bash
node scripts/grant-access.mjs student@example.com            # give full access
node scripts/grant-access.mjs student@example.com --revoke   # remove it
node scripts/grant-access.mjs --list                         # see everyone with access
```
Access is tied to the email, so you can grant it before the student has ever logged in.

**What's free without paying** (edit in `src/lib/access.ts`): home page, all topic outlines, the first topic of
each subject, Dictionary, Listen, Mental math. Everything else needs access.

---

## 2. Videos — Bunny Stream

1. Create an account at **bunny.net** → **Stream → Add video library** (e.g. "Psychometry").
2. In the library: **API** → copy *Video Library ID* → `BUNNY_LIBRARY_ID`, *API Key* → `BUNNY_API_KEY`.
3. **Security**: turn on **Token authentication** → copy the key → `BUNNY_TOKEN_KEY`
   (links then expire after a few hours, so videos can't be shared). Also add your domain under *Allowed domains*.
4. Upload whatever you've recorded (safe to run as often as you like — only new or re-recorded takes are uploaded):
   ```bash
   python3 studio-build/upload_videos.py "/path/to/Course Recordings" --dry-run   # see what it will do
   python3 studio-build/upload_videos.py "/path/to/Course Recordings"             # upload
   ```
   Add `--replace` to delete the old version on Bunny when you re-record a lesson.
5. The script updates `content/full-course/video-manifest.json`. Locally the videos appear immediately; online,
   commit and push so the site redeploys.

---

## 3. Payment — later

When you choose a provider (Grow, Cardcom, Stripe…):
- create a hosted **payment page** for the course → `PAYMENT_LINK` (the Join page's button opens it, with the
  student's email filled in);
- set its **success notification / webhook** to
  `https://<your-domain>/api/payments/webhook?key=<PAYMENT_WEBHOOK_SECRET>` (pick any long random secret);
- tell me which provider — I'll adapt `src/app/api/payments/webhook/route.ts` to its exact format and signature.

Until then, grant access by hand (above). Set `NEXT_PUBLIC_PRICE_LABEL` and `NEXT_PUBLIC_CONTACT_EMAIL` to show the
price and a contact address on the Join page.

---

## 4. Putting the site online — Vercel

1. **vercel.com** → sign in with GitHub → **Add New → Project** → import `psychometry-course`.
2. Add every variable from `.env.local` under **Settings → Environment Variables**.
3. Deploy. Then **Settings → Domains** → add your domain and follow the DNS instructions.
