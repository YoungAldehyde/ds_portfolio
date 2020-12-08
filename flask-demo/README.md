# Flask

Example Flask application for demo purpose

## Installation

First, you need to clone this repo:

```bash
$ git clone 
```

Or:

```bash
$ git clone 
```

Then change into the `flask-demo` folder:

```bash
$ cd flask-demo
```

Now, we will need to create a virtual environment and install all the dependencies. We have two options available for now.

Use Pipenv:

```bash
$ pipenv install
$ pipenv shell
```

Or use pip + virtualenv:

```bash
$ virtualenv venv
$ . venv/bin/activate  # on Windows, use "venv\Scripts\activate" instead
$ pip install -r requirements.txt
```

## How to Run a Specific Example Application?

**Before run a specific example application, make sure you have activated the virtual enviroment:**

```bash
$ cd flask-demo
$ pipenv shell  # or ". venv/bin/activate" / "venv\Scripts\activate" (Windows)
```

For example, if you want to run the Hello application, just execute these commands:

```bash
$ cd hello
$ flask run
```

Similarly, you can run HTTP application like this:

```bash
$ cd http
$ flask run
```

The applications will always running on http://localhost:5000.

## Example Applications Menu

- Hello (`/hello`): Say hello with Flask.
- HTTP (`/http`): HTTP handing in Flask.
- Templates (`/templates`): Templating with Flask and Jinja2.
- Form (`/form`): Form handing with Flask-WTF (WTForms), File upload and integrating with Flask-CKEditor, Flask-Dropzone.
- Database (`/database`): Database with Flask-SQLAlchemy (SQLAlchemy).
- Email (`/email`): Email with Flask-Mail, SendGrid
- Assets (`/assets`): Assets profiling with Flask-Assets.
- Cache (`/cache`): Cache with Flask-Caching.