CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE IF NOT EXISTS public.students (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    auth_user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    course TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    CONSTRAINT unique_auth_user UNIQUE (auth_user_id),
    CONSTRAINT unique_student_email UNIQUE (email)
);

CREATE TABLE IF NOT EXISTS public.tasks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    student_id UUID NOT NULL REFERENCES public.students(id) ON DELETE CASCADE,
    title TEXT NOT NULL,
    subject TEXT NOT NULL,
    deadline DATE NOT NULL,
    priority TEXT NOT NULL CHECK (priority IN ('Low', 'Medium', 'High')),
    completed BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS public.focus_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    student_id UUID NOT NULL REFERENCES public.students(id) ON DELETE CASCADE,
    task_id UUID REFERENCES public.tasks(id) ON DELETE SET NULL,
    duration INTEGER NOT NULL,
    session_date DATE NOT NULL DEFAULT CURRENT_DATE,
    completed BOOLEAN NOT NULL DEFAULT TRUE,
    subject TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS public.subtasks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    task_id UUID NOT NULL REFERENCES public.tasks(id) ON DELETE CASCADE,
    student_id UUID NOT NULL REFERENCES public.students(id) ON DELETE CASCADE,
    title TEXT NOT NULL,
    completed BOOLEAN NOT NULL DEFAULT FALSE,
    position INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

ALTER TABLE public.students ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.tasks ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.focus_sessions ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.subtasks ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Students can view own profile"
ON public.students
FOR SELECT
USING (auth.uid() = auth_user_id);

CREATE POLICY "Students can insert own profile"
ON public.students
FOR INSERT
WITH CHECK (auth.uid() = auth_user_id);

CREATE POLICY "Students can update own profile"
ON public.students
FOR UPDATE
USING (auth.uid() = auth_user_id)
WITH CHECK (auth.uid() = auth_user_id);

CREATE POLICY "Students can delete own profile"
ON public.students
FOR DELETE
USING (auth.uid() = auth_user_id);

CREATE POLICY "Students can view own tasks"
ON public.tasks
FOR SELECT
USING (
    student_id IN (
        SELECT id FROM public.students WHERE auth_user_id = auth.uid()
    )
);

CREATE POLICY "Students can insert own tasks"
ON public.tasks
FOR INSERT
WITH CHECK (
    student_id IN (
        SELECT id FROM public.students WHERE auth_user_id = auth.uid()
    )
);

CREATE POLICY "Students can update own tasks"
ON public.tasks
FOR UPDATE
USING (
    student_id IN (
        SELECT id FROM public.students WHERE auth_user_id = auth.uid()
    )
)
WITH CHECK (
    student_id IN (
        SELECT id FROM public.students WHERE auth_user_id = auth.uid()
    )
);

CREATE POLICY "Students can delete own tasks"
ON public.tasks
FOR DELETE
USING (
    student_id IN (
        SELECT id FROM public.students WHERE auth_user_id = auth.uid()
    )
);

CREATE POLICY "Students can view own focus sessions"
ON public.focus_sessions
FOR SELECT
USING (
    student_id IN (
        SELECT id FROM public.students WHERE auth_user_id = auth.uid()
    )
);

CREATE POLICY "Students can insert own focus sessions"
ON public.focus_sessions
FOR INSERT
WITH CHECK (
    student_id IN (
        SELECT id FROM public.students WHERE auth_user_id = auth.uid()
    )
);

CREATE POLICY "Students can update own focus sessions"
ON public.focus_sessions
FOR UPDATE
USING (
    student_id IN (
        SELECT id FROM public.students WHERE auth_user_id = auth.uid()
    )
)
WITH CHECK (
    student_id IN (
        SELECT id FROM public.students WHERE auth_user_id = auth.uid()
    )
);

CREATE POLICY "Students can delete own focus sessions"
ON public.focus_sessions
FOR DELETE
USING (
    student_id IN (
        SELECT id FROM public.students WHERE auth_user_id = auth.uid()
    )
);

CREATE POLICY "Students can view own subtasks"
ON public.subtasks
FOR SELECT
USING (
    student_id IN (
        SELECT id FROM public.students WHERE auth_user_id = auth.uid()
    )
);

CREATE POLICY "Students can insert own subtasks"
ON public.subtasks
FOR INSERT
WITH CHECK (
    student_id IN (
        SELECT id FROM public.students WHERE auth_user_id = auth.uid()
    )
);

CREATE POLICY "Students can update own subtasks"
ON public.subtasks
FOR UPDATE
USING (
    student_id IN (
        SELECT id FROM public.students WHERE auth_user_id = auth.uid()
    )
)
WITH CHECK (
    student_id IN (
        SELECT id FROM public.students WHERE auth_user_id = auth.uid()
    )
);

CREATE POLICY "Students can delete own subtasks"
ON public.subtasks
FOR DELETE
USING (
    student_id IN (
        SELECT id FROM public.students WHERE auth_user_id = auth.uid()
    )
);

CREATE INDEX IF NOT EXISTS idx_students_auth_user_id ON public.students(auth_user_id);
CREATE INDEX IF NOT EXISTS idx_tasks_student_id ON public.tasks(student_id);
CREATE INDEX IF NOT EXISTS idx_tasks_deadline ON public.tasks(deadline);
CREATE INDEX IF NOT EXISTS idx_focus_sessions_student_id ON public.focus_sessions(student_id);
CREATE INDEX IF NOT EXISTS idx_focus_sessions_session_date ON public.focus_sessions(session_date);
CREATE INDEX IF NOT EXISTS idx_subtasks_task_id ON public.subtasks(task_id);
CREATE INDEX IF NOT EXISTS idx_subtasks_student_id ON public.subtasks(student_id);
