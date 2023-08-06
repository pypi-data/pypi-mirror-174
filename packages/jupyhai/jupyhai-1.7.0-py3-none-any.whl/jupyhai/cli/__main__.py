import argparse
import platform
from typing import Optional


def determine_symlink_mode(symlink_arg: Optional[str]) -> bool:
    if symlink_arg == 'yes':
        return True
    elif symlink_arg == 'no':
        return False
    # When in auto mode, use symlinks when not on Windows
    return platform.system() != 'Windows'


def main() -> None:
    ap = argparse.ArgumentParser()
    sp = ap.add_subparsers(dest='action')
    install_sp = sp.add_parser('install')
    install_sp.add_argument('--symlink', choices=('auto', 'yes', 'no'), default='auto')
    args = ap.parse_args()
    if args.action == 'install':
        if not do_install(symlink_mode=determine_symlink_mode(args.symlink)):
            raise RuntimeError("Nothing was installed.")
    else:
        print("Use 'jupyhai install' to install the notebook extension.")


def do_labextension_install() -> bool:
    try:
        from jupyterlab import labextensions
        print("Installing Jupyhai lab extension...")
        labextensions.enable_extension('jupyhai')
        print("Jupyhai lab extension installed successfully.")
        return True
    except ImportError:
        print("Jupyterlab not found, skipping Jupyhai lab extension installation.")
    return False


def do_nbextension_install(symlink_mode) -> bool:
    try:
        from notebook import nbextensions, serverextensions
        print(
            "Installing Jupyhai notebook extension ({using_symlinks})...".format(
                using_symlinks=(
                    "using symlinks" if symlink_mode else "without symlinks"
                ),
            )
        )
        serverextensions.toggle_serverextension_python('jupyhai', enabled=True)
        nbextensions.install_nbextension_python(
            'jupyhai', symlink=symlink_mode, user=True
        )
        nbextensions.enable_nbextension_python('jupyhai')
        print("Jupyhai notebook extension installed successfully.")
        return True
    except ImportError:
        print("Notebook not found, skipping Jupyhai notebook extension installation.")
    return False


def do_server_extension_install() -> bool:
    try:
        from jupyter_server.extension.serverextension import (
            toggle_server_extension_python,
        )
        print("Installing Jupyhai jupyter_server extension...")
        toggle_server_extension_python('jupyhai', enabled=True)
        print("Jupyhai notebook extension installed successfully.")
        return True
    except ImportError:
        print("jupyter_server not found, skipping Jupyhai jupyter_server extension installation.")
    return False


def do_install(symlink_mode) -> bool:
    did_install = False
    if do_labextension_install():
        did_install = True
    if do_nbextension_install(symlink_mode):
        did_install = True
    if do_server_extension_install():
        did_install = True
    return did_install


if __name__ == "__main__":
    main()
