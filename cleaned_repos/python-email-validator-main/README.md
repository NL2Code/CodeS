email-validator: Validate Email Addresses
=========================================

A robust email address syntax and deliverability validation library for

This library validates that a string is of the form `name@example.com`
and optionally checks that the domain name is set up to receive email.
This is the sort of validation you would want when you are identifying
users by their email address like on a registration/login form (but not
necessarily for composing an email message, see below).

Key features:

* Checks that an email address has the correct syntax --- good for
  registration/login forms or other uses related to identifying users.
* Gives friendly English error messages when validation fails that you
  can display to end-users.
* Checks deliverability (optional): Does the domain name resolve?
  (You can override the default DNS resolver to add query caching.)
* Supports internationalized domain names and internationalized local parts.
* Rejects addresses with unsafe Unicode characters, obsolete email address
  syntax that you'd find unexpected, special use domain names like
  `@localhost`, and domains without a dot by default. This is an
  opinionated library!
* Normalizes email addresses (important for internationalized
  and quoted-string addresses! see below).
* Python type annotations are used.

Quick Start
-----------

If you're validating a user's email address before creating a user
account in your application, you might do this:

```python
from email_validator import validate_email, EmailNotValidError

email = "my+address@example.org"

try:

  # Check that the email address is valid. Turn on check_deliverability
  # for first-time validations like on account creation pages (but not
  # login pages).
  emailinfo = validate_email(email, check_deliverability=False)

  # After this point, use only the normalized form of the email address,
  # especially before going to a database query.
  email = emailinfo.normalized

except EmailNotValidError as e:

  # The exception message is human-readable explanation of why it's
  # not a valid (or deliverable) email address.
  print(str(e))
```

This validates the address and gives you its normalized form. You should
**put the normalized form in your database** and always normalize before
checking if an address is in your database. When using this in a login form,
set `check_deliverability` to `False` to avoid unnecessary DNS queries.
