# csvs-to-sqlite

Convert CSV files into a SQLite database. Browse and publish that SQLite database with Datasette.

Basic usage:

    csvs-to-sqlite myfile.csv mydatabase.db

This will create a new SQLite database called `mydatabase.db` containing a
single table, `myfile`, containing the CSV content.

You can provide multiple CSV files:

    csvs-to-sqlite one.csv two.csv bundle.db

The `bundle.db` database will contain two tables, `one` and `two`.

This means you can use wildcards:

    csvs-to-sqlite ~/Downloads/*.csv my-downloads.db

If you pass a path to one or more directories, the script will recursively
search those directories for CSV files and create tables for each one.

    csvs-to-sqlite ~/path/to/directory all-my-csvs.db