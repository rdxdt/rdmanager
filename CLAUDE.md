# About this project
This is a Flask app built for managing remote access id and passwords.
It uses bootstrap from a CDN.

# Directory Structure
- `app.py` : App entrypoint.
- `.env`: Configuration file 
- `.venv/` : Current python virtual environment.
- `rdmanager/`: Modules and templates, config.py(app configuration) and models.py(SQLAlchemy models).
- `rdmanager/static`: Static files such as css files(`css` subdirectory), image files(`img` subdirectory) and js files(`js` subdirectory).
- `rdmanager/errors`: Special module for error handling.
- `rdmanager/main`: Module for handling the login, logout, password recovery, and home page.
- `rdmanager/users`: Module for handling the user credentials.
- `rdmanager/clients`: Module for handling the creation of clients and it's terminals.
- `templates`: Directory containing the templates in subdirectories for each module. 

# Project rules
- The bootstrap should be loaded from it's cdn
- The project has a main.html template that serves as an outer shell, containing the header with the navigation menu and a footer and the modules content should expand it's "inside"
- Every python source code should have comments in english explaining each logical block of the functions, tuples, classes and etc... and every code in python should be clean, keep it simple and idiomatic, and following the black formatter style.
- Every html template should either load content from the bootstrap cdn or load custom css from a style.css placed in the static directory, never inline css styles in the template itself, also javascript functions should be in a js file when applicable to be reused whenever it's possible.
- Besides the login route, and password reset related routes, every route should have the decorator @login_required

# Editing Hygiene
- Change only what is required.
- Prefer the smallest valid diff.
- Do not refactor unrelated code.
- Do not make formatting-only changes.
- Keep naming/style consistent with nearby code.

# Comment rules
- Avoid comments unless they explain a non-obvious reason, constraint, or workaround.
- Never restate what the code does; prefer clearer code instead.
- If the code is self-explanatory, add no comment.
