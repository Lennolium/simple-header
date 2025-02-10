#!/bin/bash

# Script will exit if exit code is not 0.
set -e

# Define colors for log.
_info()    { printf " \033[1m[INFO]\033[0m $1 " ; }
_ok()      { printf " \033[1m\033[32m[OK]\033[0m $1 " ; }
_error()   { printf " \033[1m\033[31m[ERROR]\033[0m $1 " ; }
_logo()    { printf " \033[1m $1\033[0m \n" ; }
_success()    { printf "\033[0m\033[32mSUCCESS\033[0m \n" ; }
_warn()    { printf "\033[1m\033[33mWARNING\033[0m \n" ; }
_failed()    { printf "\033[1m\033[31mFAILED\033[0m \n" ; exit 1; }


# Define rainbow colors
RB_RED=$(printf '\033[1;38;5;196m')
RB_ORANGE=$(printf '\033[1;38;5;202m')
RB_YELLOW=$(printf '\033[1;38;5;226m')
RB_GREYEL=$(printf '\033[1;38;5;184m')
RB_GREEN=$(printf '\033[1;38;5;082m')
RB_BLUGRE=$(printf '\033[1;38;5;033m')
RB_BLUE=$(printf '\033[1;38;5;021m')
RB_INDIGO=$(printf '\033[1;38;5;093m')
RB_VIOLET=$(printf '\033[1;38;5;163m')
RB_RESET=$(printf '\033[0m')


# Get os and architecture.
case $(uname -s) in
    Linux) os="Linux" ;;
    Darwin) os="macOS" ;;
    CYGWIN*|MINGW*|MSYS*) os="Windows" ;;
    *) os="Unknown" ;;
esac

case $(uname -m) in
    x86_64) arch="x64" ;;
    arm64) arch="arm64" ;;
    arm32) arch="arm32" ;;
    *) arch="Unknown" ;;
esac


# Save name and version of the package from __init__.py in src folder.
package_directory=$(find src -mindepth 2 -maxdepth 2 -type f -name '__init__.py' -exec dirname {} \;)
package_name=$(basename "$package_directory")  # e.g. my_package
package_name_github=${package_name//_/-}  # e.g. my-package
version=$(grep '__version__ =' "$package_directory/__init__.py" | sed -E 's/^.*"([^"]+)".*$/\1/')

# Get the minimum required Python version from setup.cfg.
min_py_version="python$(grep 'python_requires' setup.cfg | sed -E 's/^.*>=//')"
min_py_version_num="${min_py_version:6}"

if which "${min_py_version}" &> /dev/null; then
    py_inst="$("$min_py_version" --version)"
else
    py_inst="$(python3 --version)"
fi


# Header.
_logo "--------------------------------------------------------------------------  \n"
printf "\n"
printf "\n"
printf "  %s  █▌  %s   ▀▀▀▀▀▀%s ║█    ╫█%s ▐█µ   ▐█%s  ▄██▀▀██▌%s  ██  %s   ▀└%s █▌   ╒█▌%s █µ      █▌%s  \n" $RB_RED $RB_ORANGE $RB_YELLOW $RB_GREYEL $RB_GREEN $RB_BLUGRE $RB_BLUE $RB_INDIGO $RB_VIOLET $RB_RESET
printf "  %s ▐█   %s         %s ███▌  ██%s ████  ██%s ██     ╟█%s ▐█   %s  ▐█%s ║█    ╫█%s ║██▌  ╓███ %s  \n" $RB_RED $RB_ORANGE $RB_YELLOW $RB_GREYEL $RB_GREEN $RB_BLUGRE $RB_BLUE $RB_INDIGO $RB_VIOLET $RB_RESET
printf "  %s ██   %s  ▀▀▀▀▀▀%s ╒█Γ└██▓█%s  █▌ ██▓█▌%s▐█      ██%s ██   %s  ██%s ██    █▌%s ██ ███▀ ██ %s  \n" $RB_RED $RB_ORANGE $RB_YELLOW $RB_GREYEL $RB_GREEN $RB_BLUGRE $RB_BLUE $RB_INDIGO $RB_VIOLET $RB_RESET
printf "  %s┌▀    %s        %s ██   ▀██%s ║█   ╙██%s └██   ╓██%s  █▌   %s ╒█▌%s ██   ██%s ╒█▌  ╙  ╒█Γ %s  \n" $RB_RED $RB_ORANGE $RB_YELLOW $RB_GREYEL $RB_GREEN $RB_BLUGRE $RB_BLUE $RB_INDIGO $RB_VIOLET $RB_RESET
printf "  %s -▀▀▀▀%s ╝▀▀▀▀▀▀%s ▀▀     ▀%s ▀▀     ▀%s   ▀▀█▀▀ %s  ╘▀▀▀▀▀%s ╝▀ %s  ▀██▀  %s ╝▀      ╝▀  %s  \n" $RB_RED $RB_ORANGE $RB_YELLOW $RB_GREYEL $RB_GREEN $RB_BLUGRE $RB_BLUE $RB_INDIGO $RB_VIOLET $RB_RESET
_logo " "
_logo "             P Y T H O N    B  U  I  L  D     S  C  R  I  P  T              \n"
printf "\n"


# General information.
_logo "S y s t e m   I n f o r m a t i o n :"
_logo "-------------------------------------"
_logo "Hostname: $(hostname)"
_logo "Operating System: $os"
_logo "Architecture: $arch"
_logo "Shell: $SHELL"
_logo "Python version: $py_inst"
_logo "PWD: $(pwd)"
_logo "Log file location: ./trace.log"
_logo "Execution time: $(date +'%y/%m/%d %H:%M:%S')"
_logo "-------------------------------------------------------------------------- \n\n"


# Confirm we are on the dev branch.
current_branch=$(git rev-parse --abbrev-ref HEAD)
_info "Confirming we are on the dev branch ..."
if [ "$current_branch" != "dev" ]; then
    _failed
else
    _success
fi


# Check if Python 3 is installed and install it if not.
_info "Checking and installing system dependencies (${min_py_version}) ..."
if test ! "$(which "${min_py_version}")" && test $os = "Linux"; then
    _warn
    _info "P${min_py_version:1} is not installed! Installing with apt-get ..."
    sudo apt-get update 2>&1 | tee -a trace.log
    sudo apt-get install "${min_py_version}" 2>&1 | tee -a trace.log && _success || _failed
    sudo apt-get install "${min_py_version}"-venv 2>&1 | tee -a trace.log && _success || _failed
elif test ! "$(which "${min_py_version}")" && test $os = "macOS";
then
    _warn
    _info "P${min_py_version:1} is not installed! Installing with Homebrew ..."
    /bin/bash -c \
    "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)" 2>&1 | tee -a trace.log
    brew update 2>&1 | tee -a trace.log
    brew install "${min_py_version}" 2>&1 | tee -a trace.log && _success || _failed
elif test ! "$(which "${min_py_version}")" && test $os = "Windows";
then
    _warn
    _info "P${min_py_version:1} is not installed! Installing with Chocolatey ..."
    if ! command -v choco &> /dev/null; then
        _info "\nDownloading and installing Chocolatey ..."
        powershell -Command "Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))"
    fi
    choco install "${min_py_version}" 2>&1 | tee -a trace.log && _success || _failed
else
    _success
fi


# Creating dist folder and delete the content of it (to remove old .app builds).
_info "Deleting old builds and logs ..."
rm -f ./trace.log
mkdir -p ./dist/
rm -Rf ./dist/* && _success || _failed


# Create temporary build venv and delete old venv.
_info "Creating temporary virtual environment ..."
if [ -d "./.buildvenv" ] ; then
    rm -r -f ./.buildvenv
fi
${min_py_version} -m venv .buildvenv >> trace.log 2>&1 && _success || _failed


# Activate virtual environment, update and install requirements.
_info "Installing and updating requirements ..."
source ./.buildvenv/bin/activate >> trace.log 2>&1
${min_py_version} -m pip install --upgrade pip >> trace.log 2>&1
${min_py_version} -m pip install pip-tools >> trace.log 2>&1
${min_py_version} -m pip install -r requirements-dev.txt >> trace.log 2>&1 && _success || _failed


# Running tests, but first check if tests folder exists.
if [ ! -d "./tests" ]; then
    _info "No tests folder found. Skipping tests ..."; _warn
else
    _info "Running unit tests now ..."
    cd src || exit
    ${min_py_version} -m unittest discover -s ../tests >> ../trace.log 2>&1 && _success || _failed
    cd .. || exit
fi

# Override the version variable of setup.cfg with the version number of __init__.py.
_info "Updating the version in 'setup.cfg' and 'README.md' to $version ..."
tmpfile=$(mktemp)
sed "s/^version =.*/version = $version/" setup.cfg > "$tmpfile"
mv "$tmpfile" setup.cfg
tmpfile=$(mktemp)
sed "s|https://img.shields.io/badge/Version-.*-brightgreen|https://img.shields.io/badge/Version-$version-brightgreen|" README.md > "$tmpfile"
mv "$tmpfile" README.md && _success || _failed


# Build dist and verify.
_info "Building the distribution files. This can take a while ..."
${min_py_version} -m build >> trace.log 2>&1 && _success || _failed
_info "Verifying the distribution files ...\n"
twine check ./dist/*.tar.gz ./dist/*.whl


# Generate sha256 hash files.
_info "Generating SHA256 checksum files..."
cd ./dist || exit
for file in *; do
    if [ -f "$file" ]; then
        shasum -a 256 "$file" > "$file.sha256"
    fi
done
if [ $? -eq 0 ]; then _success; else _failed; fi

_info "Validating the checksum files ...\n"
for file in *.sha256; do
    if sha256sum -c "$file" >> ../trace.log 2>&1; then
        printf " Checking $file: \033[0m\033[32mPASSED\033[0m \n"
    else
        printf " Checking $file: \033[1m\033[31mNOT PASSED\033[0m \n" && _failed
    fi
done
cd .. || exit


# Upload build to PyPI. Credentials are in '~.pypirc'.
_info "Uploading to the built package PyPI ...\n"
twine upload --repository pypi ./dist/*.tar.gz ./dist/*.whl && _success || _failed


# Exit out of virtual environment, cleanup egg files and delete venv.
_info "Intermission clean up ..."
deactivate
sleep 2
rm -rf ./.buildvenv
rm -rf "./src/${package_name}.egg-info" && _success || _failed


# Reflect all changes to git, commit and push to dev branch on GitHub.
_info "Adding all files to git ..."
git add .github >> trace.log 2>&1
git add -A >> trace.log 2>&1 && _success || _failed
_info "Creating tag: 'v$version' ..."
git tag "v$version" >> trace.log 2>&1 && _success || _failed
_info "Committing with message: 'v$version' ..."
git commit -m "v$version" >> trace.log 2>&1 && _success || _failed
_info "Pushing to GitHub (dev) ..."
if git push origin dev --tags >> trace.log 2>&1;
then
  _success;
else
    _warn
    _info "Push failed. Forcing push now to dev branch ..."
    git push origin dev --tags --force >> trace.log 2>&1 && _success || _failed;
fi


# Creating pull request to main branch.
_info "Creating a pull request to merge dev into main ..."
pr_title="Merge dev into main $(date +'%Y%m%d%H%M%S')"
gh pr create --base main --head dev --title "$pr_title" --body "Automated pull request to merge dev into main." >> trace.log 2>&1 && _success || _failed


# Approve the pull request (permissions required).
_info "Approving the pull request ..."
pr_number=$(gh pr list | grep "$pr_title" | awk '{print $1}')
gh pr merge "$pr_number" --merge --admin >> trace.log 2>&1 && _success || _failed


# Create a new GitHub release and upload dist files.
_info "Creating a new GitHub release and uploading distribution files ..."
cp .github/RELEASE_NOTES_TEMPLATE.md temp.md
sed -i '' "s/\$VERSION_NUMBER/$version/g" temp.md
sed -i '' "s/\$PACKAGE_NAME/$package_name_github/g" temp.md
gh release create "v$version" ./dist/* --title "v$version" --notes-file temp.md --target main >> trace.log 2>&1 && _success || _failed


_info "FINISHED! Cleaning up ..."
rm temp.md
sleep 1 && _success || _failed


_info "Exiting ..."
sleep 1
echo "Bye!"
exit 0
