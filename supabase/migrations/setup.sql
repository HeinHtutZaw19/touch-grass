create extension if not exists "pgcrypto";

drop table if exists exercise_attempts cascade;
drop table if exists exercises cascade;
drop table if exists level_contents cascade;
drop table if exists user_hobbies cascade;
drop table if exists hobbies cascade;
drop table if exists users cascade;


-- users
create table users (
  id uuid primary key default gen_random_uuid(),
  name text not null,
  photo_url text,
  datamap jsonb default '{}'::jsonb, 
  mbti text,                         
  personality_good text,             
  personality_bad text,                
  created_at timestamptz default now()
);

-- hobbies
create table hobbies (
  id uuid primary key default gen_random_uuid(),
  name text not null,
  category text,
  description text,
  created_at timestamptz default now()
);

-- user preferences / connection to hobbies
create table user_hobbies (
  id uuid primary key default gen_random_uuid(),
  user_id uuid references users(id) on delete cascade,
  hobby_id uuid references hobbies(id) on delete cascade,
  preference_score numeric default 0,  
  created_at timestamptz default now()
);

-- level contents per hobby (1-5)
create table level_contents (
  id uuid primary key default gen_random_uuid(),
  hobby_id uuid references hobbies(id) on delete cascade,
  level int check(level between 1 and 5),
  title text,
  content text,
  caption text,
  image_url text,
  created_at timestamptz default now()
);

-- exercises: fill-in-the-blank style
create table exercises (
  id uuid primary key default gen_random_uuid(),
  hobby_id uuid references hobbies(id) on delete cascade,
  prompt text,        
  answer text,        
  tags text[],        
  difficulty int,    
  created_at timestamptz default now()
);

-- users completing exercises (attempts)
create table exercise_attempts (
  id uuid primary key default gen_random_uuid(),
  user_id uuid references users(id) on delete cascade,
  exercise_id uuid references exercises(id) on delete cascade,
  attempt_text text,
  correct boolean,
  score numeric default 0,
  created_at timestamptz default now()
);
