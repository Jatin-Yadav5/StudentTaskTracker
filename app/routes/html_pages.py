"""HTML page builders for the web UI."""

import html

from app.schemas.task import Task

_STYLES = """
  * { box-sizing: border-box; }
  body {
    font-family: system-ui, -apple-system, "Segoe UI", Roboto, sans-serif;
    margin: 0;
    min-height: 100vh;
    background: linear-gradient(160deg, #0f2744 0%, #1e4d7b 45%, #3d7ab5 100%);
    color: #1a2332;
  }
  .wrap { max-width: 720px; margin: 0 auto; padding: 2rem 1.25rem 3rem; }
  header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 1rem;
    margin-bottom: 1.5rem;
    flex-wrap: wrap;
  }
  .logo {
    color: #fff;
    font-size: 1.35rem;
    font-weight: 700;
    text-decoration: none;
  }
  nav { display: flex; gap: 0.5rem; flex-wrap: wrap; }
  nav a {
    color: #e8f1fa;
    text-decoration: none;
    padding: 0.45rem 0.9rem;
    border-radius: 8px;
    font-size: 0.9rem;
    font-weight: 600;
    background: rgba(255,255,255,0.12);
  }
  nav a:hover { background: rgba(255,255,255,0.22); }
  nav a.active { background: #fff; color: #1e4d7b; }
  .panel {
    background: #fff;
    border-radius: 14px;
    padding: 1.5rem 1.75rem;
    box-shadow: 0 12px 40px rgba(0,0,0,0.2);
    margin-bottom: 1.25rem;
  }
  h1 { margin: 0 0 0.35rem; font-size: 1.6rem; color: #0f2744; }
  h2 { margin: 0 0 1rem; font-size: 1.1rem; color: #334155; font-weight: 600; }
  .muted { color: #64748b; margin: 0 0 1.25rem; line-height: 1.5; }
  .stats {
    display: flex;
    gap: 1rem;
    margin-bottom: 1.25rem;
    flex-wrap: wrap;
  }
  .stat {
    flex: 1;
    min-width: 100px;
    background: #f1f5f9;
    border-radius: 10px;
    padding: 0.75rem 1rem;
    text-align: center;
  }
  .stat strong { display: block; font-size: 1.5rem; color: #1e4d7b; }
  .stat span { font-size: 0.8rem; color: #64748b; text-transform: uppercase; letter-spacing: 0.04em; }
  label { display: block; font-weight: 600; font-size: 0.9rem; margin-bottom: 0.35rem; color: #334155; }
  input[type="text"], textarea {
    width: 100%;
    padding: 0.65rem 0.85rem;
    border: 1px solid #cbd5e1;
    border-radius: 8px;
    font-size: 1rem;
    margin-bottom: 1rem;
  }
  input:focus, textarea:focus {
    outline: none;
    border-color: #3d7ab5;
    box-shadow: 0 0 0 3px rgba(61,122,181,0.2);
  }
  .btn {
    display: inline-block;
    padding: 0.6rem 1.1rem;
    border: none;
    border-radius: 8px;
    font-size: 0.9rem;
    font-weight: 600;
    cursor: pointer;
    text-decoration: none;
    font-family: inherit;
  }
  .btn-primary { background: #1e4d7b; color: #fff; }
  .btn-primary:hover { background: #0f2744; }
  .btn-success { background: #15803d; color: #fff; }
  .btn-danger { background: #b91c1c; color: #fff; }
  .btn-ghost { background: #e2e8f0; color: #334155; }
  .task-list { list-style: none; padding: 0; margin: 0; }
  .task-item {
    border: 1px solid #e2e8f0;
    border-radius: 10px;
    padding: 1rem 1.1rem;
    margin-bottom: 0.75rem;
    display: flex;
    flex-wrap: wrap;
    align-items: flex-start;
    justify-content: space-between;
    gap: 0.75rem;
  }
  .task-item.done { background: #f0fdf4; border-color: #bbf7d0; }
  .task-item.done .task-title { text-decoration: line-through; color: #64748b; }
  .task-title { font-weight: 700; font-size: 1.05rem; margin: 0 0 0.25rem; }
  .task-desc { margin: 0; color: #64748b; font-size: 0.9rem; }
  .task-meta { font-size: 0.8rem; color: #94a3b8; margin-top: 0.35rem; }
  .badge {
    display: inline-block;
    font-size: 0.75rem;
    font-weight: 700;
    padding: 0.2rem 0.5rem;
    border-radius: 6px;
    text-transform: uppercase;
  }
  .badge-pending { background: #fef3c7; color: #92400e; }
  .badge-done { background: #dcfce7; color: #166534; }
  .task-actions { display: flex; gap: 0.5rem; flex-wrap: wrap; align-items: center; }
  .empty {
    text-align: center;
    padding: 2rem 1rem;
    color: #64748b;
  }
  .flash {
    background: #dbeafe;
    color: #1e40af;
    padding: 0.75rem 1rem;
    border-radius: 8px;
    margin-bottom: 1rem;
    font-weight: 500;
  }
  .hero-btns { display: flex; gap: 0.75rem; flex-wrap: wrap; margin-top: 1.5rem; }
  .features { display: grid; gap: 0.75rem; margin-top: 1rem; }
  .feature {
    padding: 0.85rem 1rem;
    background: #f8fafc;
    border-radius: 8px;
    border-left: 4px solid #3d7ab5;
  }
  .feature strong { color: #0f2744; }
"""

_DOCS_NAV_STYLE = """
  .docs-nav {
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 0.75rem;
    padding: 0.75rem 1.5rem;
    background: linear-gradient(160deg, #0f2744 0%, #1e4d7b 100%);
    font-family: system-ui, -apple-system, "Segoe UI", Roboto, sans-serif;
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.2);
    margin: 0;
  }
  .docs-nav .logo {
    color: #fff;
    font-weight: 700;
    text-decoration: none;
    font-size: 1.1rem;
  }
  .docs-nav nav {
    display: flex;
    gap: 0.5rem;
    flex-wrap: wrap;
  }
  .docs-nav nav a {
    color: #e8f1fa;
    text-decoration: none;
    padding: 0.45rem 0.9rem;
    border-radius: 8px;
    font-size: 0.9rem;
    font-weight: 600;
    background: rgba(255, 255, 255, 0.12);
  }
  .docs-nav nav a:hover {
    background: rgba(255, 255, 255, 0.22);
  }
  .docs-nav nav a.active {
    background: #fff;
    color: #1e4d7b;
  }
"""


def _layout(title: str, active: str, body: str) -> str:
    home_cls = "active" if active == "home" else ""
    tasks_cls = "active" if active == "tasks" else ""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{html.escape(title)}</title>
  <style>{_STYLES}</style>
</head>
<body>
  <div class="wrap">
    <header>
      <a class="logo" href="/">Student Task Tracker</a>
      <nav>
        <a class="{home_cls}" href="/">Home</a>
        <a class="{tasks_cls}" href="/tasks">My Tasks</a>
        <a href="/docs">API Docs</a>
      </nav>
    </header>
    {body}
  </div>
</body>
</html>"""


def render_home() -> str:
    """Build the home page HTML."""
    body = """
    <div class="panel">
      <h1>Stay on top of your schoolwork</h1>
      <p class="muted">Add assignments, mark them done when you finish, and remove tasks you no longer need. Everything is saved in memory while the server runs.</p>
      <div class="features">
        <div class="feature"><strong>Add tasks</strong> — title and optional notes for each assignment.</div>
        <div class="feature"><strong>Track progress</strong> — see pending vs completed at a glance.</div>
        <div class="feature"><strong>Stay organized</strong> — complete or delete tasks from one page.</div>
      </div>
      <div class="hero-btns">
        <a class="btn btn-primary" href="/tasks">Go to My Tasks</a>
        <a class="btn btn-ghost" href="/docs">Developer API</a>
      </div>
    </div>
    """
    return _layout("Home — Student Task Tracker", "home", body)


def render_tasks_page(tasks: list[Task], message: str | None = None) -> str:
    """Build the task list / manage page HTML."""
    pending = sum(1 for t in tasks if not t.completed)
    done = sum(1 for t in tasks if t.completed)
    flash = f'<div class="flash">{html.escape(message)}</div>' if message else ""

    if tasks:
        items = []
        for task in tasks:
            title = html.escape(task.title)
            desc = html.escape(task.description or "")
            desc_html = f'<p class="task-desc">{desc}</p>' if task.description else ""
            status = "done" if task.completed else ""
            badge = (
                '<span class="badge badge-done">Done</span>'
                if task.completed
                else '<span class="badge badge-pending">Pending</span>'
            )
            if not task.completed:
                actions = f"""
                <div class="task-actions">
                  <form method="post" action="/tasks/{task.id}/complete" style="margin:0">
                    <button type="submit" class="btn btn-success">Complete</button>
                  </form>
                  <form method="post" action="/tasks/{task.id}/delete" style="margin:0"
                        onsubmit="return confirm('Delete this task?');">
                    <button type="submit" class="btn btn-danger">Delete</button>
                  </form>
                </div>
                """
            else:
                actions = f"""
                <div class="task-actions">
                  <form method="post" action="/tasks/{task.id}/delete" style="margin:0"
                        onsubmit="return confirm('Delete this task?');">
                    <button type="submit" class="btn btn-danger">Delete</button>
                  </form>
                </div>
                """
            items.append(f"""
            <li class="task-item {status}">
              <div>
                <p class="task-title">{title} {badge}</p>
                {desc_html}
                <p class="task-meta">Task #{task.id}</p>
              </div>
              {actions}
            </li>
            """)
        list_html = f'<ul class="task-list">{"".join(items)}</ul>'
    else:
        list_html = '<div class="empty"><p>No tasks yet. Add your first assignment below.</p></div>'

    body = f"""
    {flash}
    <div class="stats">
      <div class="stat"><strong>{pending}</strong><span>Pending</span></div>
      <div class="stat"><strong>{done}</strong><span>Completed</span></div>
      <div class="stat"><strong>{len(tasks)}</strong><span>Total</span></div>
    </div>
    <div class="panel">
      <h2>Add a new task</h2>
      <form method="post" action="/tasks/create">
        <label for="title">Title *</label>
        <input type="text" id="title" name="title" required maxlength="200"
               placeholder="e.g. Math homework — Chapter 5" />
        <label for="description">Description (optional)</label>
        <textarea id="description" name="description" rows="2" maxlength="500"
                  placeholder="Due date, room number, extra notes…"></textarea>
        <button type="submit" class="btn btn-primary">Add task</button>
      </form>
    </div>
    <div class="panel">
      <h2>Your tasks</h2>
      {list_html}
    </div>
    """
    return _layout("My Tasks — Student Task Tracker", "tasks", body)


def docs_nav_bar(active: str) -> str:
    """Navigation bar HTML for Swagger / ReDoc pages."""
    links = [
        ("home", "/", "Home"),
        ("tasks", "/tasks", "My Tasks"),
        ("docs", "/docs", "API Docs"),
        ("redoc", "/redoc", "ReDoc"),
    ]
    link_html = "".join(
        f'<a href="{href}" class="{"active" if key == active else ""}">{label}</a>'
        for key, href, label in links
    )
    return f"""<header class="docs-nav">
  <a class="logo" href="/">Student Task Tracker</a>
  <nav>{link_html}</nav>
</header>"""


def inject_docs_nav(page_html: str, active: str) -> str:
    """Add shared navigation and styles to API documentation pages."""
    style_block = f"<style>{_DOCS_NAV_STYLE}</style>"
    bar = docs_nav_bar(active)
    if "</head>" in page_html:
        page_html = page_html.replace("</head>", f"{style_block}\n</head>", 1)
    if "<body>" in page_html:
        page_html = page_html.replace("<body>", f"<body>\n{bar}", 1)
    return page_html
