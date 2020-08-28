#!/bin/bash
function export_keys {
    export SECRET_KEY=''
    export DB_NAME=''
    export USER=''
    export PASSWORD=''
}

function run_postgresql {
    output=$(systemctl status postgresql.service | grep running)

    if [ -z "$output" ]
    then
        echo 'Starting Postgresql...'
        sudo systemctl start postgresql
    else
	    echo 'Postgresql is already running'
    fi
}

function setup_shell {
    python -m venv venv
    source ./venv/bin/activate
    pip install -r requirements.txt
}

function main {
    error_msg="Not valid script parameters!"

    if [ -z $1 ] || [ -z $2 ]
    then
        echo $error_msg
    else
	case $1 in
	    -dev) param="$2"
	        echo "Starting in DEV mode on $param ..."
            source ./venv/bin/activate
            export_keys
            run_postgresql
	       	./manage.py runserver $2 --settings=my_knowledge_base.settings.dev ;;
	    -prod) param="$2"
            echo "Starting in PRODUCTION mode on $param ..."
            setup_shell
            export_keys
            run_postgresql
            ./manage.py makemigrations
            ./manage.py collectstatic
            ./manage.py migrate
            ./manage.py runserver $2 --settings=my_knowledge_base.settings.prod ;;
	    *) echo "Not valid option" ;;
	esac
    fi
}

main $1 $2

