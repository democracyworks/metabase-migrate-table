# Metabase Card Table Update Script

This script updates Metabase cards to use a new table, replacing occurrences of an old table name with a new one and updating field IDs accordingly.
It's useful when migrating or renaming tables within your Metabase instance.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
  - [Command-Line Arguments](#command-line-arguments)
  - [Examples](#examples)
- [Development and Debugging](#development-and-debugging)
- [Resources](#resources)

---

## Prerequisites

- **Python 3.12** or higher.
- [`uv`](https://docs.astral.sh/uv/) for dependency and environment management.
- Metabase API access.

## Installation

1. **Clone the Repository**

   ```bash
   git clone git@github.com:untitled-data-company/metabase-migrate-table.git
   cd metabase-migrate-table
   ```

2. **Install Dependencies**

   Sync the project dependencies with `uv`.
   This creates and manages the virtual environment automatically.
   Dependencies are declared in `pyproject.toml` and pinned in `uv.lock`.

   ```bash
   uv sync
   ```

3. **Credentials**

   Set environment variables before running scripts:

   ```bash
   export METABASE_API_KEY="..."
   export METABASE_BASE_URL="https://your-metabase-host/api"
   ```

   `METABASE_BASE_URL` must include `/api`.

## Usage

The script is executed via the command line and requires specific arguments to function correctly.

> **IMPORTANT:** In case a card is modified by this script independently from the dashboard containing it, it is possible that the dashboard filters associated with the dashcard will be disconnected and the dashcard will be unable to retrieve data.
>
> This can be fixed by opening the dashboard, reconnecting the filters, and saving it.
> For some Metabase internal reasons, changes will not be visible before saving the dashboard.

### Command-Line Arguments

- `-o`, `--old_table` **(required)**:  
  The name of the old table to be replaced.  
  *Example*: `'old_schema.old_table'`

- `-n`, `--new_table` **(required)**:  
  The name of the new table that will replace the old one.  
  *Example*: `'new_schema.new_table'`

- `-l`, `--list`:
  List all the cards/questions and dashboards depending on the old table.

- `-a`, `--all`:
  Migrate all the cards and dashboards depending on the old table.

- `-c`, `--card_ids`:  
  One or more Metabase card IDs to update.
  Provide multiple IDs separated by spaces.
  *Example*: `10717 12345 67890`

- `-d`, `--dashboard_ids`:  
  One or more Metabase dashboard IDs to update.
  Provide multiple IDs separated by spaces.
  *Example*: `10717 12345 67890`

- `-r`, `--renamed_columns`:
  Pass a JSON object with `old:new` column names to handle renamed columns.
  *Example*: `{"insurance_category_label":"insurance_category"}`

`-a`, `-c`, and `-d` are mutually exclusive.

### Basic Command Structure

```bash
uv run main.py -o OLD_TABLE_NAME -n NEW_TABLE_NAME [-l] [-a] [-c CARD_ID [CARD_ID ...]] [-d DASHBOARD_ID [DASHBOARD_ID ...]] [-r '{"old_name":"new_name"}']
```

## Examples

### Example 1: List objects associated with a table

```bash
uv run main.py \
  -o old_schema.old_table \
  -n new_schema.new_table \
  -l
```

### Example 2: Update a single card

Update card with ID `10717`, replacing `'old_schema.old_table'` with `'new_schema.new_table'`:

```bash
uv run main.py \
  -o old_schema.old_table \
  -n new_schema.new_table \
  -c 10717
```

### Example 3: Update multiple cards

Update cards with IDs `10717`, `12345`, and `67890`:

```bash
uv run main.py \
  -o old_schema.old_table \
  -n new_schema.new_table \
  -c 10717 12345 67890
```

### Example 4: Migrate dashboards and cards associated with a table

To migrate all objects associated with a given table in one go:

```bash
uv run main.py \
  -o old_schema.old_table \
  -n new_schema.new_table \
  -a
```

### Example 5: Rename columns

In case the new table contains columns with names different from the old one, you can pass a JSON string with pairs like `"old_column_name":"new_column_name"`:

```bash
uv run main.py \
  -o old_schema.old_table \
  -n new_schema.new_table \
  -a \
  -r '{"successful_connections":"successful_connections_new"}'
```

## Development and Debugging

For development or debugging purposes, default arguments can be set within the script.
When running the script without command-line arguments in a debugging environment (for example, an IDE like VSCode), it will use these default values.

### Setting Default Arguments

In the script, locate the `default_arguments` dictionary:

```python
# Use it for development or debugging purposes
default_arguments = {
    "old": "old_schema.old_table",
    "new": "new_schema.new_table",
    "all": False,
    "card_ids": "10717 10733",
    "dashboard_ids": None,
    "renamed_columns": '{"insurance_category_label":"insurance_category"}',
}
```

Set the desired default values for `old`, `new`, and the other parameters.

## Resources

- [Metabase API references](docs/metabase-api-references.md)
