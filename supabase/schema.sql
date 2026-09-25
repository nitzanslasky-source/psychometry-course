-- Psychometry Course — database setup (Supabase / Postgres).
-- Run once in Supabase → SQL Editor → New query → paste → Run.

-- ------------------------------------------------------------------ access
-- One row per purchase (or manual grant). Keyed by EMAIL so access can be granted before the
-- student has ever logged in: when they log in with that email, they're in.
create table if not exists public.entitlements (
  id          bigint generated always as identity primary key,
  email       text        not null,
  product     text        not null default 'full-course',
  status      text        not null default 'active' check (status in ('active', 'revoked')),
  source      text        not null default 'manual',     -- 'manual' | 'grow' | 'cardcom' | 'stripe' ...
  reference   text,                                       -- payment / invoice id
  expires_at  timestamptz,                                -- null = lifetime access
  created_at  timestamptz not null default now()
);
create index if not exists entitlements_email_idx on public.entitlements (lower(email));

alter table public.entitlements enable row level security;
-- A student can see their own access rows; only the server (service role) can write them.
drop policy if exists "read own entitlements" on public.entitlements;
create policy "read own entitlements" on public.entitlements
  for select using (lower(email) = lower(auth.jwt() ->> 'email'));

-- ------------------------------------------------------------------ saved progress
-- Everything a student does, so it follows them across devices.
create table if not exists public.student_state (
  user_id     uuid primary key references auth.users (id) on delete cascade,
  progress    jsonb not null default '{}'::jsonb,   -- lessons done, answers, last step
  srs         jsonb not null default '{}'::jsonb,   -- spaced review schedule
  attempts    jsonb not null default '[]'::jsonb,   -- exam simulation attempts
  updated_at  timestamptz not null default now()
);

alter table public.student_state enable row level security;
drop policy if exists "own state" on public.student_state;
create policy "own state" on public.student_state
  for all using (auth.uid() = user_id) with check (auth.uid() = user_id);

-- ------------------------------------------------------------------ helper
-- True when the logged-in student has active access (used by the website).
create or replace function public.has_access() returns boolean
language sql stable security definer set search_path = public as $$
  select exists (
    select 1 from public.entitlements
    where lower(email) = lower(auth.jwt() ->> 'email')
      and status = 'active'
      and (expires_at is null or expires_at > now())
  );
$$;
grant execute on function public.has_access() to authenticated;
