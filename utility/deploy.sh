#!/usr/bin/env bash
# Deployment script for the CodeDevils website. The script is designed
# to run at the end of a Travis CI script as a deploy artifact.
#
# Author: Kevin Shelley (kevin.shelley@pm.me)
# Copyright: CodeDevils 2020
################################################################

# environment variables
RUN_VENV="True"
DEBUG="ON"
ENV="prod"
PYTHON_VERSION="python3.8"
RESTART="True"

ENV_PROD="codedevils.org"
ENV_DEV="qa.codedevils.org"
VENV_NAME=ENV_PROD
BASE_PATH="/home/codedevils_admin/"

# color!
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

################################################################
# prints the help information for the -h command
################################################################
echo_help() {
echo -e "Usage: ./bin/deploy.sh [OPTIONS]"
echo -e "           [-h | --help][-e | --settings-env <prod|dev>][-nr | --no-restart]"
echo -e "           [-d | --debug <on|off>][-v | --virtualenv][-dev]"
echo -e "           [-V | --virtualenv-name <name>][-p | --python-version <python#.#>]"
echo -e ""
echo -e "Deploys the project to the DreamHost server. This script is designed to be used as"
echo -e "part of the deploy mechanism at the end of a successful Travis CI build. It is not"
echo -e "designed to run standalone (however it probably can)"
echo -e ""
echo -e " -h, --help            Display this help and exit."
echo -e " -e, --settings-env    Set the settings to be modified for either prod or dev."
echo -e " -d, --debug           Turn off console messages by setting this flag to 'off'"
echo -e " -dev                  Run the development environment deployment"
echo -e " -nr, --no-restart     Turns off automatically restarting the Passenger service, and therefore"
echo -e "                       updating the website. This will require a manual restart after."
echo -e " -v, --virtualenv      Flag that turns off sourcing the virtual environment automatically."
echo -e " -V, --virtualenv-name The name of the virtual environment folder. By default"
echo -e "                       the folder is named ${VENV_NAME}."
echo -e " -p, --python-version  The version of Python installed in the virtual environment."
echo -e "                       The name should not be changed from the default ${PYTHON_VERSION} unless the"
echo -e "                       script is being run as part of a CI test."
echo -e ""
echo -e "For more information on defaults, see below."
echo -e ""
echo -e "======= Default ======="
echo -e "Category       Value"
echo -e "--------       -----"
echo -e "Run venv       ${RUN_VENV}"
echo -e "Debug          ${DEBUG}"
echo -e "Environment    ${ENV}"
echo -e "Python Version ${PYTHON_VERSION}"
echo -e "Restart Server ${RESTART}"
echo -e ""
}

################################################################
# prints a debug message if DEBUG is set to True
################################################################
debug() {
if [[ "$DEBUG" == "ON" ]]; then
    echo -e "$1"
fi
}

################################################################
# prints a debug message if DEBUG is set to True
################################################################
deployment_failed() {
echo -e "Deployment failed"
exit 1
}

################################################################
# Prints the completion message with instructions on how to
# restart the server if the user chooses manually not to restart
################################################################
complete_installation() {
if [[ ${RESTART} == "True" ]]; then
    echo -e "Installation complete! Visit https://${VENV_NAME} to view the updated website!"
else
    echo -e "Installation complete! Only thing left to do is restart Passenger"
    echo -e "on the server. To do so, log into the server and run the commands:"
    echo -e "\tcd ${BASE_PATH}${VENV_NAME}"
    echo -e "\tmkdir -p tmp"
    echo -e "touch tmp/restart.txt"
fi
exit 0
}

################################################################
# activates the virtual environment
################################################################
activate() {
source /home/codedevils_admin/.envs/${VENV_NAME}/bin/activate
debug "Virtual environment ${VENV_NAME} activated"
}

################################################################
# takes a package as a parameters and checks if it has already
# been installed
################################################################
package_installed() {
if [[ -x "$(command -v $1)" ]]; then
    echo "Installed"
else
    echo "Not installed"
fi
}

################################################################
# Parses arguments
################################################################

while [[ "$1" != "" ]]; do
    case $1 in
        -e | --settings-env )   shift
                                if [[ "$1" != "prod" ]]; then
                                    ENV="dev"
                                fi
                                ;;
        -d | --debug )          shift
                                if [[ "$1" != "on" ]]; then
                                    DEBUG_ON="$1"
                                fi
                                ;;
        -v | --virtualenv )     RUN_VENV="False"
                                ;;
        -dev )                  VENV_NAME=ENV_DEV
                                ;;
        -V | --virtualenv-name) shift
                                VENV_NAME="$1"
                                ;;
        -p | --python-version ) shift
                                PYTHON_VERSION="$1"
                                ;;
        -h | --help )           shift
                                echo_help
                                exit
                                ;;
        * )                     echo -e "${RED}Invalid tag. Use the -h or --help tag for usage info.${NC}"
                                exit 1
    esac
    shift
done

#===============================================================

# update environment
if [[ ${ENV} == "dev" ]]; then
    VENV_NAME=ENV_DEV
fi

# change to the 

# 4 - if the user specified, install and run the virtual environment
if [[ ${RUN_VENV} == "True" ]]; then
    activate
fi

# change to the working directory
cd "${BASE_PATH}${VENV_NAME}"

PROJECT_UPDATED="True"
git pull || PROJECT_UPDATED="False"
if [[ ${PROJECT_UPDATED} == "False" ]]; then
    debug "${RED}Git failed to update the project. Check the git credentials on the server.${NC}"
    exit 1
fi

# install the logs directory just in case it doesn't get installed
LOGS_CREATED="True"
debug "Creating log directory"
mkdir -p logs/ || LOGS_CREATED="False"
if [[ ${LOGS_CREATED} == "False" ]]; then
    debug "${YELLOW}Log folder already exists.${NC}"
fi

# install project dependencies
INSTALLED_DEPENDENCIES="True"
debug "Using pip to install project dependencies"
pip3 install -r requirements.txt || INSTALLED_DEPENDENCIES="False"
if [[ ${INSTALLED_DEPENDENCIES} == "False" ]]; then
    debug "${RED}Failed to install one or more dependencies. Review the failed installs, fix the issue and try again.${NC}"
    exit 1
fi

# make database migrations (if applicable)
FAILED_MAKE_MIGRATIONS="False"
debug "Creating model migration templates"
./manage.py makemigrations || FAILED_MAKE_MIGRATIONS="True"
if [[ ${FAILED_MAKE_MIGRATIONS} == "True" ]]; then
    debug "${RED}Failed to make database migrations. Please ensure your database credentials in settings.py are correct.${NC}"
    exit 1
fi
debug "Migration files created. Running database migration..."

# migrate database
FAILED_MIGRATE="False"
./manage.py migrate || FAILED_MIGRATE="True"
debug "Migrating templated models to database"
if [[ ${FAILED_MIGRATE} == "True" ]]; then
    debug "${RED}Failed to migrate databases. Please ensure that the database server is online and no other users are accessing it.${NC}"
    exit 1
fi

# restart passenger
# this block is also where the installation completes
if [[ ${RESTART} == "True" ]]; then
    RESTARTED_PASSENGER="True"
    debug "Restarting Passenger"
    mkdir -p tmp
    touch tmp/restart.txt || RESTARTED_PASSENGER="False"
    if [[ ${RESTARTED_PASSENGER} == "False" ]]; then
        debug "${RED}Passenger failed to restart.${NC}"
        exit 1
    fi
fi

# completed installation
complete_installation
