#!/bin/sh

# Script will exit if exit code is not 0.
set -e

# Define colors for log.
_info()    { echo "\033[1m[INFO]\033[0m $1" ; }
_ok()      { echo "\033[32m[OK]\033[0m $1" ; }
_error()   { echo "\033[31m[ERROR]\033[0m $1" ; }
_warn()   { echo "\033[33m[WARN]\033[0m $1" ; }
_logo()   { echo "\033[1m $1\033[0m" ; }


# Header
echo ""
echo ""
_logo "  █▌     ▀▀▀▀▀▀ ║█    ╫█ ▐█µ   ▐█  ▄██▀▀██▌  ██     ▀└ █▌   ╒█▌ █µ      █▌  "
_logo " ▐█             ███▌  ██ ████  ██ ██     ╟█ ▐█     ▐█ ║█    ╫█ ║██▌  ╓███   "
_logo " ██     ▀▀▀▀▀▀ ╒█Γ└██▓█  █▌ ██▓█▌▐█      ██ ██     ██ ██       ██ ███▀ ██   "
_logo "┌▀             ██   ▀██ ║█   ╙██ └██   ╓██  █▌    ╒█▌ ██   ██ ╒█▌  ╙  ╒█Γ   "
_logo " -▀▀▀▀ ╝▀▀▀▀▀▀ ▀▀     ▀ ▀▀     ▀   ▀▀█▀▀   ╘▀▀▀▀▀ ╝▀   ▀██▀   ╝▀      ╝▀    "
_logo " "
_logo "             P Y T H O N    B  U  I  L  D     S  C  R  I  P  T              "
_logo " -------------------------------------------------------------------------  "
echo ""
echo ""

# Check if Python 3 is installed and install it if not.
_info "Checking and installing requirements ..."
if test ! "$(which python3)"; then
    _info "Python 3 is not installed! Installing with Homebrew ..."
    /bin/bash -c \
    "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"
    brew update
    brew install python3
else
    _ok "Python 3 is installed."
fi

# Creating dist folder.
mkdir -p dist/

# Delete the content of dist folder (to remove old .app builds).
_info "Deleting old builds in /dist folder."
rm -Rf dist/*

# Check if venv is created and do so if not.
if ! [ -d "./venv" ] ; then
    _info "Creating virtual environment, so we do not pollute the system."
    python3 -m venv venv
else
    _ok "Looks like a virtual environment is already created."
fi

# Activate virtual environment, update and install requirements.
_info "Installing and updating requirements."
source venv/bin/activate
pip install --upgrade pip
python -m pip install pip-tools
python -m pip install build twine    
pip install -r requirements.txt

# Save name of the package.
package_directory=$(find src -mindepth 2 -maxdepth 2 -type f -name '__init__.py' -exec dirname {} \;)
package_name=$(basename "$package_directory")

# Get the version of the package from __init__.py file.
version=$(grep '__version__ =' "$package_directory/__init__.py" | sed -E 's/^.*"([^"]+)".*$/\1/')

# Override the version variable of setup.cfg with the version number of __init__.py.
tmpfile=$(mktemp)
sed "s/^version =.*/version = $version/" setup.cfg > "$tmpfile"
mv "$tmpfile" setup.cfg
_ok "Updated the version variable in 'setup.cfg' to $version"

# Build dist and verify.
_info "Building the distribution files. This can take a while ..."
if python -m build
then
    twine check dist/*
    _ok "BUILD FINISHED!"
else
    _error "BUILD FAILED!"
    exit 1
fi

# Upload build to PyPI. Credentials are in '~.pypirc'.
_info "Uploading built package to PyPI index."
if twine upload -r pypi dist/*
then
    _ok "UPLOAD FINISHED!"
else
    _error "UPLOAD FAILED!"
fi

# Generate sha256 hash files.
_info "Generating sha256 checksum files..."
cd dist || exit
for file in *; do
    if [ -f "$file" ]; then
        shasum -a 256 "$file" > "$file.sha256"
    fi
done

# Validate sha256 checksums.
if sha256sum -c *.sha256; then
    _ok "Checksums are valid."
    _ok "BUILD AND UPLOAD COMPLETED!"
else
    _error "Checksums are not valid."
fi

# Cleanup egg files.
cd .. || exit
rm -rf "src/${package_name}.egg-info"

# Exit out of virtual environment.
deactivate

_info "Exiting ..."
exit 0

