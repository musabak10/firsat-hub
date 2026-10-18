create extension if not exists pgcrypto;
create extension if not exists pg_trgm;

create table if not exists events (
  id uuid primary key default gen_random_uuid(),
  slug text unique not null,
  title text not null,
  organization text not null,
  description text,
  category text not null check (category in ('staj','hackathon','yarisma','bootcamp','konferans')),
  education_levels text[] not null default '{}',   -- lise | lisans | yuksek-lisans
  application_url text not null,
  image_url text,
  deadline timestamptz,                             -- null = sürekli başvuru
  is_online boolean default false,
  location text,
  source text not null default 'manual',
  source_url text unique,                           -- dedup anahtarı 1
  content_hash text unique,                         -- dedup anahtarı 2
  status text not null default 'pending' check (status in ('pending','approved')),
  created_at timestamptz not null default now()
);

create index if not exists events_deadline_idx on events (deadline);
create index if not exists events_category_idx on events (category);
create index if not exists events_status_idx on events (status);
create index if not exists events_title_trgm on events using gin (title gin_trgm_ops);

alter table events enable row level security;
create policy "herkes onaylı etkinlikleri okuyabilir" on events
  for select using (status = 'approved');
-- Yazma: yalnızca service_role anahtarı (scraper) RLS'yi atlayarak yazar.
