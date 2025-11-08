create extension if not exists "pgcrypto";

-- USERS
create table users (
  id uuid primary key default gen_random_uuid(),
  name text not null,
  bad_sites text,
  photo_url text,
  mbti text,
  personality_good text,
  personality_bad text,
  suggested_careers text,
  created_at timestamptz default now()
);

-- DATAMAP (per user)
create table datamaps (
  id uuid primary key default gen_random_uuid(),
  user_id uuid references users(id) on delete cascade unique,
  analytical numeric default 0,
  creative numeric default 0,
  social numeric default 0,
  physical numeric default 0,
  updated_at timestamptz default now()
);

-- AI INTERACTIONS
create table ai_interactions (
  id uuid primary key default gen_random_uuid(),
  user_id uuid references users(id) on delete cascade,
  prompt text not null,        
  fun_fact text,
  category text not null check (category in ('analytical','creative','social','physical')),
  user_feedback int check (user_feedback between 1 and 5),
  response text,
  media_url text,
  created_at timestamptz default now()
);
