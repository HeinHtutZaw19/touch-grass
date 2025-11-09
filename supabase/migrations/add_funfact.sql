-- fun fact for hobbies
create table if not exists fun_facts (
  id uuid primary key default gen_random_uuid(),
  hobbies_id uuid references hobbies(id) on delete cascade,
  text text not null,
  created_at timestamptz default now(),
  unique (hobbies_id, text)
);

-- helpful index
create index if not exists idx_fun_facts_hobbies on fun_facts(hobbies_id);
