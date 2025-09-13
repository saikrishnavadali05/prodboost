# prodboost
This repository contains a modular Django application that manages tasks with progress bars and a lightweight API + template UI.

Progress bars feel satisfying because they tap into both psychology and human perception. A few reasons why they feel so good:

1. **Visual feedback & certainty** – Humans don’t like uncertainty. A progress bar tells us *something is happening* and gives us a sense of control because we can see how far along the task is.

2. **Completion bias** – Our brains love finishing things. Seeing the bar move closer to 100% gives us little dopamine hits, encouraging us to stick around until it’s done.

3. **Chunking the task** – A big, invisible process feels overwhelming. A progress bar breaks it into smaller, manageable steps. Instead of "waiting forever," we see it as "just 20% more."

4. **Illusion of speed** – Even if the task takes the same amount of time, watching progress makes it *feel* faster. It turns passive waiting into an engaging experience.

5. **Goal gradient effect** – The closer we get to completion, the more motivated we feel. That’s why the last 10% of a progress bar feels extra exciting.

It’s basically a neat trick that turns *waiting* (something people hate) into a mini journey of *achievement*.


# How to run (local dev)

1. create virtualenv: `python -m venv .venv && source .venv/bin/activate` (or on Windows `.venv\Scripts\activate`).
2. `pip install -r requirements.txt`
3. `python manage.py migrate`
4. `python manage.py runserver`
5. Visit http://127.0.0.1:8000/

# Next improvements (ideas)

- Add authentication + per-user tasks (link Task to `settings.AUTH_USER_MODEL`).
- Add websockets (Django Channels) for real-time progress updates across sessions.
- Add analytics (daily/weekly completed tasks) and gamification (streaks, badges).
- Integrate a simple Pomodoro timer and tie progress to pomodoro sessions.

# Key design choices

- Keep business logic out of views: `services.py` holds task-related operations (create, update progress, compute percent).
- Provide both server-rendered templates and a tiny JSON API (in `api.py`) so you can later plug a SPA.
- Use class-based views for clarity and easy extension.
- Minimal JS (fetch) to update progress bars without pulling in heavy frontend frameworks.