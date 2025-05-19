# Understanding `pyproject.toml` and Managing Python Packages with Poetry

This document explains the `pyproject.toml` file, focusing on the provided example from the `openbb` project, and details how to build and install packages using Poetry.

## What is `pyproject.toml`?

`pyproject.toml` is a configuration file introduced in PEP 518. It's designed to be the central place for specifying Python project metadata, build system requirements, and tool configurations (like linters, formatters, and test runners). For projects using Poetry, `pyproject.toml` is the primary file that defines project dependencies, metadata, and build configurations, replacing older files like `setup.py`, `requirements.txt`, and `MANIFEST.in` for many use cases.

## Breakdown of the `openbb/pyproject.toml`

Let's examine the key sections of the provided `c:\workspace\github\OpenBB\openbb_platform\pyproject.toml`:

### 1. `[tool.poetry]`

This section contains general metadata about the project.

```toml
[tool.poetry]
name = "openbb"
version = "4.4.3"
description = "Investment research for everyone, anywhere."
authors = ["OpenBB Team <hello@openbb.co>"]
license = "AGPL-3.0-only"
readme = "README.md"
packages = [{ include = "openbb" }]
```

*   `name`: The name of the package as it would be published (e.g., on PyPI). Here, it's "openbb".
*   `version`: The current version of the package.
*   `description`: A short summary of the project.
*   `authors`: A list of authors.
*   `license`: The license under which the project is distributed.
*   `readme`: Specifies the file to be used as the long description for the package (often displayed on PyPI).
*   `packages`: Defines which Python packages are part of this project. `[{ include = "openbb" }]` means that the directory named `openbb` (relative to `pyproject.toml`) is the main package to be included.

### 2. `[tool.poetry.dependencies]`

This section lists all the packages that the `openbb` project depends on to run.

```toml
[tool.poetry.dependencies]
python = ">=3.9.21,<3.13"
openbb-core = "^1.4.3"
openbb-platform-api = "^1.1.5"

# Provider dependencies (mandatory)
openbb-benzinga = "^1.4.0"
# ... (other provider dependencies listed in the file) ...
openbb-yfinance = "^1.4.2"

# Data type specific dependencies (mandatory)
openbb-commodity = "^1.3.0"
# ... (other data type dependencies listed in the file) ...
openbb-regulators = "^1.4.1"

# Community dependencies (optional)
openbb-alpha-vantage = { version = "^1.4.0", optional = true }
# ... (other community dependencies listed in the file) ...
openbb-wsj = { version = "^1.4.0", optional = true }

openbb-charting = { version = "^2.3.2", optional = true }
# ... (other optional tool dependencies listed in the file) ...
openbb-technical = { version = "^1.4.2", optional = true }
```

*   `python`: Specifies the compatible Python versions for this project. `">=3.9.21,<3.13"` means Python 3.9.21 or newer, but less than Python 3.13.
*   **Mandatory Dependencies**:
    *   Packages like `openbb-core`, `openbb-platform-api`, and various `openbb-<provider>` (e.g., `openbb-benzinga`) and `openbb-<datatype>` (e.g., `openbb-commodity`) packages are listed directly with their version constraints (e.g., `^1.4.3` means "compatible with version 1.4.3", allowing updates to patch and minor versions but not major versions like 2.0.0). These are installed by default when you run `poetry install`.
*   **Optional Dependencies (Community Dependencies)**:
    *   Packages like `openbb-alpha-vantage` are marked with `optional = true`. This means they are not installed by default. They can be installed explicitly using "extras" (see next section). This is useful for dependencies that provide additional features but are not essential for the core functionality of the package.

### 3. `[tool.poetry.extras]`

This section defines "extras," which are named groups of optional dependencies. Installing an extra will install all the packages listed under it.

```toml
[tool.poetry.extras]
alpha_vantage = ["openbb-alpha-vantage"]
biztoc = ["openbb-biztoc"]
# ... (other individual extras listed in the file) ...
wsj = ["openbb-wsj"]

all = [
    "openbb-alpha-vantage",
    "openbb-biztoc",
    # ... (all optional dependencies listed again in the file) ...
    "openbb-wsj",
]
```

*   Individual extras like `alpha_vantage` map to one or more optional dependencies. For example, if a user wants to use Alpha Vantage features, they can install the `openbb` package with the `alpha_vantage` extra.
*   The `all` extra is a convenient way to install *all* defined optional dependencies at once.

### 4. `[build-system]`

This section specifies how the project should be built. It's defined by PEP 517 and PEP 518.

```toml
[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
```

*   `requires`: A list of packages needed to build your package. For Poetry projects, this is typically `poetry-core`.
*   `build-backend`: Specifies the Python object that build frontends (like `pip`) will use to execute the build.

## Building and Installing Packages with Poetry

Poetry is a tool for dependency management and packaging in Python. It helps you declare, manage, and install dependencies of Python projects, ensuring you have the right stack everywhere.

### Prerequisites

1.  **Install Poetry**: If you don't have Poetry installed, you can install it by following the official instructions at https://python-poetry.org/docs/#installation. A common way is:
    ```bash
    curl -sSL https://install.python-poetry.org | python3 -
    ```
    Or using pip:
    ```bash
    pip install poetry
    ```
    Ensure Poetry's `bin` directory is in your system's PATH.

### Installing Dependencies

Navigate to the root directory of your project (where `pyproject.toml` is located, i.e., `c:\workspace\github\OpenBB\openbb_platform\`) in your terminal.

1.  **Install all mandatory dependencies**:
    This command reads the `pyproject.toml` file, resolves the dependencies, installs them, and creates/updates a `poetry.lock` file. The `poetry.lock` file ensures deterministic builds by locking the exact versions of all dependencies.
    ```bash
    poetry install
    ```
    This will install `openbb-core`, `openbb-platform-api`, and all the provider and data-type specific `openbb-*` packages listed as mandatory. It will *not* install dependencies marked as `optional = true` by default.

2.  **Install with specific extras**:
    If you need functionality provided by optional dependencies, you can install them using the extras defined in `[tool.poetry.extras]`.
    For example, to install `openbb-alpha-vantage` and `openbb-charting`:
    ```bash
    poetry install --extras "alpha_vantage charting"
    ```
    Or using the `-E` shorthand:
    ```bash
    poetry install -E alpha_vantage -E charting
    ```

3.  **Install all mandatory and all optional dependencies**:
    To install all dependencies, including all those defined in the `all` extra:
    ```bash
    poetry install --extras "all"
    ```
    Or:
    ```bash
    poetry install -E all
    ```

4.  **Installing for development**:
    When you run `poetry install`, if you are in a virtual environment managed by Poetry (which it creates by default unless configured otherwise), the main package (`openbb` in this case) is installed in an "editable" mode. This means changes you make to the source code in the `openbb` directory are immediately reflected without needing to reinstall.

### Building the Package

To build your project into distributable formats (a source archive (sdist) and a wheel), run:

```bash
poetry build
```

This command will create a `dist/` directory in your project root and place the built files (e.g., `openbb-4.4.3-py3-none-any.whl` and `openbb-4.4.3.tar.gz`) into it. These files can then be published to PyPI or another package index, or installed directly using `pip`.

### Understanding "Sub-folder Ones" (Dependencies)

The request mentioned "including sub-folder ones." In the context of this `pyproject.toml` for the `openbb` package:

*   **Dependencies as Packages**: The various `openbb-core`, `openbb-benzinga`, `openbb-alpha-vantage`, etc., are treated as distinct Python packages. These can be thought of as the "sub-folder ones" in the sense that they are separate components (potentially developed in their own sub-folders within a larger project structure) that the main `openbb` package depends on.
*   **Development of Dependencies**: If these dependency packages (like `openbb-core`) are developed within a larger monorepo structure, each would typically have its own `pyproject.toml` file in its respective sub-folder. They would be built and potentially published (e.g., to PyPI or a private index) independently.
*   **Installation Process**: When you run `poetry install` for the main `openbb` package (using its `pyproject.toml`), Poetry resolves these dependencies based on their names and version specifications. It then downloads and installs them from the configured package sources (e.g., PyPI).
    *   If these dependencies were local path dependencies (e.g., defined as `openbb-core = {path = "../openbb-core", develop = true}` in `pyproject.toml`), Poetry would install them directly from that local path. However, the provided `pyproject.toml` lists them as regular dependencies, implying they are fetched from a package index.

So, `poetry install` (with or without extras) handles the installation of all declared dependencies for the `openbb` package. The `poetry build` command builds the `openbb` package itself, not its dependencies (those are assumed to be pre-built and available for installation from a package index or local path).

To summarize for the `openbb` project as defined by this `pyproject.toml`:
*   **To install everything needed to run `openbb` with all its features (including all optional dependencies)**: `poetry install -E all`
*   **To build the `openbb` package itself for distribution**: `poetry build`

This `pyproject.toml` effectively defines the `openbb` package and its universe of dependencies, both mandatory and optional. Poetry uses this file to manage that universe.