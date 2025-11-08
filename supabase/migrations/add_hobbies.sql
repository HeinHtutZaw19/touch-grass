-- hobbies
create table hobbies (
  id uuid primary key default gen_random_uuid(),
  name text not null unique,
  category text not null check (category in ('analytical','creative','social','physical')),
  description text,
  created_at timestamptz default now()
);
