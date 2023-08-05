# declara

Programmatically fill out your Boreas declaration forms with Python.

See `example.py` for example use.

## Environment variables
This package requires the following environment variables to be set:

- `SMTP_HOST`
- `SMTP_USERNAME`
- `SMTP_PASSWORD`
- `SMTP_DEFAULT_RECIPIENT`

And these are optional:

- `SMTP_PORT` (default = `587`)
- `DECLARA_EMAIL_BODY_B64` (default = equal to base64-encoded `default_email_body.txt`)
- `DECLARA_EMAIL_SUBJECT` (default = `Declaratie`)
