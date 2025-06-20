# Hostname Discovery project

This file contains the instructions and steps to install the system depencies and run the system

# System dependcies

django + sqlite3
celery (async tasks)
RabbitMQ (Broker)
pika (RabbitMQ client)
dnspython (DNS record A lookup)
black, ruff (PEP8 guidlines and formatting)

### Install RabbitMQ

1. Install Erlang (RabbitMQ dependency)
   Go to the Erlang Downloads page, download the latest verion to your os.
   Run the installer and follow the steps.
2. Install RabbitMQ
   Go to the RabbitMQ Downloads page.

   Download the latest RabbitMQ installer for your OS
   Run the installer and follow the steps.
3. Start RabbitMQ
   Open terminal and run:

   ```
   net start RabbitMQ
   ```

   Should see logs indicating RabbitMQ is running.

   By default, RabbitMQ runs on localhost:5672.
4. Enable RabbitMQ Management Plugin
   This gives a nice web UI at http://localhost:15672:

   ```
   rabbitmq-plugins.bat enable rabbitmq_management
   ```

   Access the UI with default credentials: guest / guest.

### Create virtual environment

```
python -m venv <venv_name>
source <venv_name>/Scripts/activate
```

then install the requirements:

```
pip install -r requirments.txt
```

## Run the system

Create superuser to manage django system admin and see your models

```
python manage.py createsuperuser
```

Choose your username and password
From the project directory, Start Django Development Server

```
python manage.py runserver
```

The API will be available at http://localhost:8000/hostname.

Start Celery Worker, in a new terminal:

```
celery -A hostname_discovery worker --loglevel=info
```

This will process tasks triggered by both entry points.
Note: this is a tricky point as sometimes on windows os this raises a permission error, to fix run the following command instead

```
celery -A hostname_discovery worker --pool=solo --loglevel=info
```

Start the Broker Listener, In a new terminal:

```
python -m active_discovery.consumer
```

This will listen to the hostname queue for incoming messages.

## Test Both Entrypoints

Test the HTTP API Endpoint
Use curl (from terminal) or Postman for example:

```
curl -X POST http://localhost:8000/hostname \
  -H "Content-Type: application/json" \
  -d '{"hostname": "www.youtube.com", "source": "API"}'
```

Should get a response like:
{"status": "queued", "hostname": "www.youtube.com"}

From RabbitMQ plugin can publish a message to hostname queue.

The Celery worker will save the data received from any of the 2 entry points to the DB, process the DNS lookup and if successful, publish the result to the dns_record_discovered queue.

The messages on hostname and dns_record_discovered queues can be viewed also from RabbitMQ plugin.

From python admin panel you can view the records added to the database.

Included system_snapshots folder for examples demonsteration.
