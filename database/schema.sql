-- Run this once in the Supabase SQL Editor to create Planly's tables.

create table if not exists students (
    id uuid primary key default gen_random_uuid(),
    auth_user_id uuid unique not null references auth.users (id) on delete cascade,
    name text not null,
    email text unique not null,
    course text not null,
    created_at timestamptz default now()
);

create table if not exists tasks (
    id uuid primary key default gen_random_uuid(),
    student_id uuid not null references students (id) on delete cascade,
    title text not null,
    subject text not null,
    deadline date not null,
    priority text not null default 'Medium' check (priority in ('Low', 'Medium', 'High')),
    completed boolean not null default false,
    created_at timestamptz default now()
);

-- Row Level Security: each student can only see and change their own data.
alter table students enable row level security;
alter table tasks enable row level security;

create policy "Students manage own profile" on students
    for all using (auth.uid() = auth_user_id) with check (auth.uid() = auth_user_id);

create policy "Students manage own tasks" on tasks
    for all using (
        student_id in (select id from students where auth_user_id = auth.uid())
    ) with check (
        student_id in (select id from students where auth_user_id = auth.uid())
    );
