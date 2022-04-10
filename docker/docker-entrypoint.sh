#!/bin/bash

# http://linuxcommand.org/lc3_man_pages/seth.html 
set -eo pipefail

shopt -s nullglob

# check to see if this file is being run or sourced from another script
_is_sourced() {
	# https://unix.stackexchange.com/a/215279
	[ "${#FUNCNAME[@]}" -ge 2 ] \
		&& [ "${FUNCNAME[0]}" = '_is_sourced' ] \
		&& [ "${FUNCNAME[1]}" = 'source' ]

}

# logging functions
log_log() {
	local type="$1"; shift
	printf '%s [%s] [Entrypoint]: %s\n' "$(date --rfc-3339=seconds)" "$type" "$*"
}
log_note() {
	log_log Note "$@"
}
log_error() {
	log_log Error "$@"
}

# usage: file_env VAR [DEFAULT]
#    ie: file_env 'XYZ_DB_PASSWORD' 'example'
# (will allow for "$XYZ_DB_PASSWORD_FILE" to fill in the value of
#  "$XYZ_DB_PASSWORD" from a file, especially for Docker's secrets feature)
file_env() {
  local var="$1"
  local fileVar="${var}_FILE"
  local def="${2:-}"
  if [ "${!var:-}" ] && [ "${!fileVar:-}" ]; then
    log_error "both $var and $fileVar are set (but are exclusive)"
    exit 1
  fi
  local val="$def"
  if [ "${!var:-}" ]; then
    val="${!var}"
  elif [ "${!fileVar:-}" ]; then
    val="$(< "${!fileVar}")"
  fi
  export "$var"="$val"
  unset "$fileVar"
}

# Loads various settings that are used elsewhere in the script
# This should be called before any other functions
docker_setup_env() {
	file_env 'DB_NAME'
	file_env 'DB_USER'
	file_env 'DB_PASSWORD'
	file_env 'DB_HOST'
	file_env 'DB_PORT'

	file_env 'GHASEDAK_API_KEY'
	file_env 'SECRET_KEY'
}

_migrate() {
	log_note "Migrating apps to the database"
	python "$PWD/manage.py" migrate --noinput >&1 2>&2
}

_makemigration() {
	log_note "Making migratiions"
	python "$PWD/manage.py" makemigrations --noinput >&1 2>&2
}

_main() {
  # load env
  docker_setup_env

  if [ "$1" = "--makemigrations" ]; then
		shift
    _makemigration
	fi

	if [ "$1" = "--migrate" ]; then
		shift
		_migrate
  fi


	log_note "Executing $@"
    exec "$@" >&1
}

# If we are sourced from elsewhere, don't perform any further actions
if ! _is_sourced; then
	_main "$@"
fi
