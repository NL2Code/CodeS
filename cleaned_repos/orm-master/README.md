# ORM

The `orm` package is an async ORM for Python, with support for Postgres,
MySQL, and SQLite. ORM is built with:

Because ORM is built on SQLAlchemy core, you can use Alembic to provide
database migrations.

## Quickstart

**Note**: Use `ipython` to try this from the console, since it supports `await`.

```python
import databases
import orm

database = databases.Database("sqlite:///db.sqlite")
models = orm.ModelRegistry(database=database)


class Note(orm.Model):
    tablename = "notes"
    registry = models
    fields = {
        "id": orm.Integer(primary_key=True),
        "text": orm.String(max_length=100),
        "completed": orm.Boolean(default=False),
    }

# Create the tables
await models.create_all()

await Note.objects.create(text="Buy the groceries.", completed=False)

note = await Note.objects.get(id=1)
print(note)
# Note(id=1)
```
