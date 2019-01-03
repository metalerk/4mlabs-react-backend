###	Script just to use in local environments

start_env(){
	echo
	echo "    ### Startup script powered by <company/team> ###"
	echo
	echo "*** Setting development environment..."
	echo "*** Loading variables..."

	# Reads and loads environmental variables from the .env file
	export $(cat .env | xargs)

	echo "*** Starting development server..."
	echo
}

# From this point no questions, right ? >--(d ¬.¬)--<
echo
echo "         <company/team> Startup Script"
echo

if [ "$1" == "test" ]; then
	start_env
	python -m unittest discover

elif [ "$1" == "dev" ]; then
	start_env
	# Test dev mode (default port: 5000)
	python3 app.py

elif [ "$1" == "prod" ]; then
	start_env
	# Test prod mode
	gunicorn -w4 app:app -b 0.0.0.0:8080

else
	echo "Invalid option."
	echo
	echo "usage: ./start_dev.sh test|dev|prod"

fi
