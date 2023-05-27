# WebSite-Blog

The site is more for people who want users to be able to comment on their blog and admins to create posts

---
### Basic functionality
- Main routes: search posts, contact form, statistics site, sign-up, sign-in

- Admin panel: Create and edit posts, create lists and edit users `(To access the admin panel, the account status in the is_admin field must be == True)`

- Profiles users: my profile, settings, history comments, save posts, like posts, request post edits

- Category News, post information



---
### Installation

1. Clone repository: `git clone https://github.com/mykyttem/WebSite-Blog.git`

2. Install Dependencies: `pip install -r requirements.txt`

3. Start app.py file: `python app.py`

---
### Tests
The "pytest" library is used to test the project.
Commands for test

`During tests, it is better to delete the existing database located in the "instance" folder`

- `pytest` 
- `pytest -s` (tests with a printout to the console)

---
### Recommendations

- The project has one category for `news` posts, you can add more if you wish.

- `Hard-coded data to create an admin account in file app.py`