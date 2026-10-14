# INNOVERSE --- Campus Innovation Platform

INNOVERSE is a web-based campus innovation prototype designed to help
students turn ideas into projects, find collaborators, coordinate teams,
connect with mentors, track milestones, and manage funding requests and
project expenses.

This repository contains a single-page HTML/CSS/JavaScript frontend and
a lightweight Flask backend. The current implementation is intended for
hackathon demonstrations and local development, **not for production use
with real accounts, passwords, or financial records**.

## Table of contents

-   [Project goals](#project-goals)
-   [Features](#features)
-   [User roles](#user-roles)
-   [Technology stack](#technology-stack)
-   [Project structure](#project-structure)
-   [Requirements](#requirements)
-   [Run locally on Windows](#run-locally-on-windows)
-   [Backend API](#backend-api)
-   [Data storage and
    synchronization](#data-storage-and-synchronization)
-   [Typical workflow](#typical-workflow)
-   [Current limitations and security
    notes](#current-limitations-and-security-notes)
-   [Troubleshooting](#troubleshooting)
-   [Future improvements](#future-improvements)
-   [Contributing](#contributing)

## Project goals

Students may have useful technical skills and innovative ideas but
struggle to find teammates, evaluate ideas, access mentorship, and
organize project funding. INNOVERSE brings these activities into one
workspace and provides a basic workflow for tracking project development
and review.

The platform emphasizes collaboration, visible project progress, and
accountable human decisions. Any AI-style score or guidance shown by
this prototype is advisory; it does not replace a human review or
funding decision.

## Features

### Account and profile interface

-   Account registration and sign-in forms.
-   College/institution, ID, department, year, skills, and profile
    details.
-   Role selection for Student, Mentor/Faculty, and Administrator.
-   Password-recovery interface using a security question.
-   Local browser session state for the currently signed-in user.

> These are prototype account flows. The current backend is not a secure
> authentication service; see [Current limitations and security
> notes](#current-limitations-and-security-notes).

### Student workspace

-   Overview dashboard with project, team, funding, and milestone
    summaries.
-   Skill profile.
-   Project idea submission and project status tracking.
-   Collaborator discovery.
-   Team creation and team member displays.
-   Mentorship information and project mentor assignment.
-   Funding request and bill/expense interfaces.
-   Project milestones and progress tracking.

### Mentorship and review

-   Mentor profiles and availability indicators.
-   Project-to-mentor assignment interface.
-   Project review and selection workflow.
-   Review status options such as Submitted, In review, Selected, Needs
    changes, and Rejected.
-   Reviewer feedback and recommended budget fields.

### Funding and expense tracking

-   Funding request submission.
-   Requested and approved amount display.
-   Funding status tracking.
-   Bill/expense submission linked to a funding request.
-   Vendor, purchase date, description, amount, and receipt-reference
    fields.
-   Bill verification status and basic allocation/expense summaries.

The receipt field stores a reference or filename only; it does not
upload, store, or verify an actual receipt file.

### Administrator interface

-   Overview of registered demo accounts and pending work.
-   Project pipeline and project status controls.
-   Funding and bill review controls.
-   JSON data export and import tools.
-   Local demo-data reset option.

The role and permission checks in the frontend are suitable only for a
prototype. They are not server-enforced authorization.

### Additional interface features

-   Light and dark theme toggle.
-   Responsive layout for smaller screens.
-   AI Project Guide with rule-based guidance.
-   GitHub repository shortcut that saves a repository URL in the
    current browser and opens it.
-   Server synchronization indicator.
-   Browser-local fallback if the backend cannot be reached.

The GitHub shortcut is not an OAuth integration and does not grant the
app access to GitHub APIs or repositories.

## User roles

The current frontend includes these selectable roles:

  -----------------------------------------------------------------------
  Role                                Intended use in the prototype
  ----------------------------------- -----------------------------------
  **Student**                         Create project ideas, manage a
                                      skill profile, find collaborators,
                                      create teams, track milestones,
                                      request funding, and submit bills.

  **Mentor / Faculty**                View mentorship information,
                                      support projects, and access
                                      review-related interfaces available
                                      to mentors.

  **Administrator**                   Review project status, oversee
                                      funding and bill workflows, and
                                      access demo administration and data
                                      tools.
  -----------------------------------------------------------------------

The frontend hides the Reviews and Admin navigation sections from users
who are not recognized as a Mentor or Administrator. This is a UI-level
check only. The current backend does not independently authenticate
these roles or enforce record-level permissions.

## Technology stack

-   **HTML5** --- page structure.
-   **CSS** --- layout, responsive styling, and light/dark themes.
-   **Vanilla JavaScript** --- frontend rendering, form handling, and
    interactions.
-   **Python** --- backend language.
-   **Flask** --- local web server and JSON API.
-   **SQLite** --- persistent storage for the shared workspace snapshot.
-   **Browser `localStorage`** --- local cached workspace data, current
    browser session identifier, theme preference, and saved GitHub
    repository URL.

No frontend build step is required for the current single-file
implementation.

## Project structure

A typical project folder looks like this:

``` text
INNOVERSE/
├── index.html          # Frontend application
├── server.py           # Flask server and API
├── requirements.txt    # Python dependencies (Flask)
├── README.md           # Project documentation
└── innoverse.db        # Created by the backend at runtime
```

The SQLite database file is generated in the same directory as
`server.py` when the backend initializes. Do not commit a database
containing user data or test credentials to a public repository.

## Requirements

-   Windows, macOS, or Linux.
-   Python 3.10 or newer recommended.
-   `pip` available through Python.
-   A modern browser such as Chrome, Edge, or Firefox.
-   The project files listed above.

The backend dependency is Flask. The exact dependency list is maintained
in `requirements.txt`.

## Run locally on Windows

### 1. Open the project folder

Open the folder containing `index.html`, `server.py`, and
`requirements.txt` in VS Code.

### 2. Open the VS Code terminal

Choose **Terminal → New Terminal**. Confirm that the terminal is in the
project directory.

### 3. Install dependencies

``` powershell
python -m pip install -r requirements.txt
```

If the output says `Requirement already satisfied`, Flask is already
installed.

### 4. Start the server

``` powershell
python server.py
```

When Flask starts successfully, the terminal prints a local address,
commonly:

``` text
http://127.0.0.1:5000
```

Keep the terminal open while using the application.

### 5. Open INNOVERSE

Visit:

-   Application: <http://127.0.0.1:5000>
-   Health check: <http://127.0.0.1:5000/api/health>
-   Shared workspace state: <http://127.0.0.1:5000/api/state>

The health and state URLs are API endpoints; they display JSON rather
than the normal website.

### 6. Stop the server

Return to the terminal and press **Ctrl+C**.

### Run without Flask

Opening `index.html` directly with a `file://` URL may allow some
frontend elements to display, but the `/api/state` calls will not work
as intended. Run the application through Flask for the complete
prototype experience.

## Backend API

The provided backend implements the following routes.

### `GET /`

Serves `index.html` from the same directory as `server.py`.

**Typical use:** Open the application in a browser.

### `GET /api/health`

Returns a small JSON response indicating that the API is running and
using SQLite.

**Example response:**

``` json
{
  "ok": true,
  "service": "INNOVERSE",
  "database": "SQLite"
}
```

### `GET /api/state`

Returns the shared workspace snapshot as JSON. The snapshot contains
collections such as:

-   `users`
-   `ideas`
-   `teams`
-   `mentors`
-   `funding`
-   `bills`
-   `milestones`
-   `reviews`

The backend deliberately returns `currentUser` as `null`, because the
signed-in browser identity should not be shared as a workspace-wide
session. The response includes an `X-INNOVERSE-Updated-At` header and
disables caching.

### `PUT /api/state`

Accepts a JSON object containing workspace state and stores it in
SQLite.

-   Content type: `application/json`
-   Required top-level body type: JSON object.
-   The backend checks that known collection fields, when supplied, are
    arrays.
-   Requests larger than 5 MB are rejected.
-   The server sets `currentUser` to `null` before saving the shared
    snapshot.

**Example request body:**

``` json
{
  "users": [],
  "currentUser": null,
  "ideas": [],
  "teams": [],
  "mentors": [],
  "funding": [],
  "bills": [],
  "milestones": [],
  "reviews": []
}
```

**Example success response:**

``` json
{
  "ok": true,
  "updatedAt": "2026-01-01T00:00:00+00:00"
}
```

The timestamp above is an example, not a live value.

**Common errors:**

  -----------------------------------------------------------------------
  HTTP status                         Meaning
  ----------------------------------- -----------------------------------
  `400`                               The request body is not a JSON
                                      object or a supplied collection
                                      field has the wrong type.

  `413`                               The request body is too large.
  -----------------------------------------------------------------------

### Data model

The current backend stores the shared workspace in one SQLite table
named `app_state`, with one row (`id = 1`):

  Column         Purpose
  -------------- ---------------------------------------------------------
  `id`           Fixed row identifier for the single workspace snapshot.
  `payload`      JSON-serialized workspace state.
  `updated_at`   UTC timestamp for the latest saved snapshot.

This snapshot design is simple for a demo but is not a substitute for
normalized relational tables, user-specific access controls, or
concurrency-safe multi-user workflows.

## Data storage and synchronization

The current application uses both browser storage and a server database:

1.  The frontend keeps a local cached copy in browser `localStorage`
    under `innoverse_demo_v1`.
2.  When the app initializes, it requests `GET /api/state`.
3.  When frontend data changes, it saves locally and schedules a
    `PUT /api/state` request.
4.  If the API is unavailable, the frontend indicates that it is using
    local data.
5.  Theme preference is stored separately under `innoverse_theme`.
6.  The GitHub repository shortcut stores its URL under
    `innoverse_github_repo`.
7.  The signed-in user identifier remains in that browser's local cached
    state; it is not stored as the shared server login session.

**Important:** The backend currently stores one shared workspace
snapshot. It is not a multi-tenant database. Connected clients can
potentially read or overwrite shared workspace data. Concurrent updates
may overwrite one another.

`127.0.0.1` is accessible only on the same computer. Running the server
on a network interface or hosting it online does not make the prototype
secure.

## Typical workflow

1.  Start the Flask server.
2.  Open the application in the browser.
3.  Create a demo account or sign in.
4.  Complete the skill profile.
5.  Submit a project idea.
6.  Find collaborators and create a team.
7.  Track project milestones.
8.  Explore mentorship options.
9.  Submit a funding request.
10. After a request is marked approved in the demo workflow, add a bill
    and track its status.
11. Mentors or administrators can use the available review interfaces.
12. Export a JSON backup before resetting or replacing local demo data.

Actual financial transfers, file uploads, verified institutional
identity, email-based recovery, and live AI inference are not provided
by this prototype.

## Current limitations and security notes

**Do not deploy this version publicly with real user information.**

The current implementation is a hackathon/demo prototype and has
important limitations:

-   **No production authentication:** login and registration are
    implemented in frontend JavaScript and workspace data includes user
    records. The Flask API does not verify credentials or establish
    secure server-side user sessions.
-   **Passwords and security answers:** the prototype account flow
    stores these in its shared demo data. Do not use real passwords or
    real personal security answers.
-   **No server-enforced roles:** role checks in the frontend can be
    bypassed. The backend does not enforce Student, Mentor, or
    Administrator permissions.
-   **Shared workspace:** the API allows connected clients to retrieve
    and replace the shared state. Do not store private or sensitive data
    in it.
-   **No record-level access controls:** the backend does not isolate
    one user's projects, bills, or profile from another user.
-   **Prototype recovery flow:** security-question recovery is not
    equivalent to verified email-based password reset.
-   **No actual receipt upload:** the bill form records a reference
    string only.
-   **Rule-based AI guidance:** the AI Project Guide is local rule-based
    logic, not a connected AI model or external AI API.
-   **GitHub shortcut only:** entering a repository URL opens it and
    saves the URL locally; it does not connect through GitHub OAuth.
-   **No production deployment setup:** Flask's development server is
    for development only.
-   **Concurrency limitations:** a single shared JSON snapshot can lose
    updates when multiple clients save around the same time.
-   **No automated test suite is included** in the described project
    files.

### Before production deployment

At minimum, a production version should include:

-   Server-side registration and login.
-   Strong password hashing and secure session management.
-   Server-enforced authorization and role assignment by a trusted
    administrator.
-   Per-user and per-project access controls.
-   Strict schema validation and safe database transactions.
-   CSRF protection where applicable, secure cookies, HTTPS, and
    appropriate security headers.
-   Rate limiting and protections for login and account recovery.
-   Verified email or another secure account-recovery process.
-   A production WSGI server and managed hosting configuration.
-   Database backups, migrations, monitoring, and automated tests.
-   A review of privacy requirements before collecting student or
    institutional data.

Do not expose the development server directly to the internet as a
substitute for these controls.

## Troubleshooting

### `ModuleNotFoundError: No module named 'flask'`

Install the project dependencies:

``` powershell
python -m pip install -r requirements.txt
```

If you have multiple Python installations, run the command using the
same `python` command that you use to start `server.py`.

### `Address already in use`

Another process may already be using port `5000`. Stop the other Flask
process with `Ctrl+C`, or configure a different port consistently in the
server and your local URL.

### The website does not open

-   Confirm that `python server.py` is still running.
-   Open `http://127.0.0.1:5000` rather than opening `index.html`
    directly.
-   Check the terminal for Python errors.

### The health endpoint returns `404`

Check whether the `server.py` currently in your project defines
`/api/health`. The endpoint is present in the backend version documented
here, but your local file may differ if it was regenerated.

### The app says `Offline · local data`

The frontend could not complete its server-state request or save.
Confirm that the Flask server is running, refresh the page, and inspect
the terminal for errors.

### Data differs between browsers or devices

The app uses a single shared snapshot when the server is reachable, but
the current prototype has no conflict resolution. A browser with stale
cached state may overwrite newer shared data. Export a JSON backup
before testing across devices.

### The website loads but account behavior is unreliable

The account system is a demonstration flow, not a secure
server-authenticated account system. Avoid real credentials and do not
use it for sensitive information.

## Future improvements

Potential next steps for a production-oriented version:

1.  Replace the shared JSON snapshot with normalized database tables and
    migrations.
2.  Implement secure server-side authentication and session management.
3.  Enforce role and resource permissions on every protected API
    endpoint.
4.  Add project membership requests and explicit invitation acceptance.
5.  Add verified file uploads for bills and receipts.
6.  Add notifications and project activity history.
7.  Integrate a real AI service through a protected backend endpoint, if
    desired.
8.  Add GitHub OAuth only after configuring a secure OAuth application
    and callback flow.
9.  Add automated tests for routes, permissions, data validation, and
    frontend workflows.
10. Deploy with HTTPS, a production WSGI server, environment-based
    configuration, logging, and backups.

## Contributing

For hackathon development:

1.  Create a branch for your change.
2.  Keep frontend and backend API contracts consistent.
3.  Avoid committing `innoverse.db`, credentials, API keys, or private
    user data.
4.  Test the affected workflow locally.
5.  Document any new API route, database field, or setup requirement in
    this README.

## License

No license is specified in the current project files. Add a `LICENSE`
file before allowing others to reuse or redistribute the project.
