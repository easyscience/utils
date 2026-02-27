---
icon: material/cog-box
---

# :material-cog-box: Installation & Setup

**EasyUtilities** is a cross-platform Python library compatible with
**Python 3.11** through **3.13**.

To install and set up EasyUtilities, we recommend using
[**Pixi**](https://pixi.prefix.dev), a modern package manager for
Windows, macOS, and Linux.

??? note "Main benefits of using Pixi"

    - **Ease of use**: Pixi simplifies the installation process, making it
      accessible even for users with limited experience in package management.
    - **Python version control**: Pixi allows specifying and managing different
      Python versions for each project, ensuring compatibility.
    - **Isolated environments**: Pixi creates isolated environments for each
      project, preventing conflicts between different package versions.
    - **PyPI and Conda support**: Pixi can install packages from both PyPI and
      Conda repositories, providing access to a wide range of libraries.

An alternative installation method using the traditional **pip** package
manager is also provided.

## Installing with Pixi <small>recommended</small> { #installing-with-pixi data-toc-label="Installing with Pixi" }

This section describes the simplest way to set up EasyUtilities using
**Pixi**.

#### Installing Pixi

- Install Pixi by following the instructions on the
  [official Pixi Installation Guide](https://pixi.prefix.dev/latest/installation).

#### Setting up EasyUtilities with Pixi

<!-- prettier-ignore-start -->

- Choose a project location (local drive recommended).

    ??? warning ":fontawesome-brands-windows: Windows + OneDrive"

        We **do not recommend creating a Pixi project inside OneDrive or other
        synced folders**.

        By default, Pixi creates the virtual environment inside the project
        directory (in `.pixi/`). On Windows, synced folders such as OneDrive
        may cause file‑system issues (e.g., path-length limitations or
        restricted link operations), which can lead to unexpected install
        errors or environments being recreated.

        Instead, create your project in a **local directory on your drive**
        where you have full write permissions.

<!-- prettier-ignore-end -->

- Initialize a new Pixi project and navigate into it:
  ```txt
  pixi init easyutilities
  cd easyutilities
  ```
- Set the Python version for the Pixi environment (e.g., 3.13):
  ```txt
  pixi add python=3.13
  ```
- Add EasyUtilities to the Pixi environment from PyPI:
  ```txt
  pixi add --pypi easyutilities
  ```
- Add a Pixi task to run EasyUtilities commands easily:
  ```txt
  pixi task add easyutilities "python -m easyutilities"
  ```

#### Updating Pixi and EasyUtilities

- To update all packages in the Pixi environment, including
  EasyUtilities:
  ```txt
  pixi update
  ```
- To update Pixi itself to the latest version:
  ```txt
  pixi self-update
  ```

#### Uninstalling Pixi

- Follow the
  [official Pixi Guide](https://pixi.prefix.dev/latest/installation/#uninstall).

## Classical Installation

This section describes how to install EasyUtilities using the
traditional method with **pip**. It is assumed that you are familiar
with Python package management and virtual environments.

### Environment Setup <small>optional</small> { #environment-setup data-toc-label="Environment Setup" }

We recommend using a **virtual environment** to isolate dependencies and
avoid conflicts with system-wide packages. If any issues arise, you can
simply delete and recreate the environment.

#### Creating and Activating a Virtual Environment:

<!-- prettier-ignore-start -->

- Create a new virtual environment:
  ```txt
  python3 -m venv venv
  ```
- Activate the environment:

    === ":material-apple: macOS"
        ```txt
        . venv/bin/activate
        ```
    === ":material-linux: Linux"
        ```txt
        . venv/bin/activate
        ```
    === ":fontawesome-brands-windows: Windows"
        ```txt
        . venv/Scripts/activate      # Windows with Unix-like shells
        .\venv\Scripts\activate.bat  # Windows with CMD
        .\venv\Scripts\activate.ps1  # Windows with PowerShell
        ```

- The terminal should now show `(venv)`, indicating that the virtual environment
  is active.

<!-- prettier-ignore-end -->

#### Deactivating and Removing the Virtual Environment:

<!-- prettier-ignore-start -->

- Exit the environment:
  ```txt
  deactivate
  ```
- If this environment is no longer needed, delete it:

    === ":material-apple: macOS"
        ```txt
        rm -rf venv
        ```
    === ":material-linux: Linux"
        ```txt
        rm -rf venv
        ```
    === ":fontawesome-brands-windows: Windows"
        ```txt
        rmdir /s /q venv
        ```

<!-- prettier-ignore-end -->

### Installing from PyPI { #from-pypi }

EasyUtilities is available on **PyPI (Python Package Index)** and can be
installed using `pip`. To do so, use the following command:

```txt
pip install easyutilities
```

To install a specific version of EasyUtilities, e.g., 1.0.3:

```txt
pip install 'easyutilities==1.0.3'
```

To upgrade to the latest version:

```txt
pip install --upgrade easyutilities
```

To upgrade to the latest version and force reinstallation of all
dependencies (useful if files are corrupted):

```txt
pip install --upgrade --force-reinstall easyutilities
```

To check the installed version:

```txt
pip show easyutilities
```

### Installing from GitHub <small>alternative</small> { #from-github data-toc-label="Installing from GitHub" }

Installing unreleased versions is generally not recommended but may be
useful for testing.

To install EasyUtilities from the `develop` branch of GitHub, for
example:

```txt
pip install git+https://github.com/easyscience/utils@develop
```

To include extra dependencies (e.g., dev):

```txt
pip install 'easyutilities[dev] @ git+https://github.com/easyscience/utils@develop'
```
