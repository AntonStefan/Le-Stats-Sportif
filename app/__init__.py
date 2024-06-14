"""
This script initializes a Flask web server and configures logging for the server.

The Flask web server is set up with a ThreadPool to handle concurrent tasks.
A DataIngestor instance is created to handle data ingestion from a CSV file.
The web server maintains a job counter and a dictionary to store job results.
"""
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask
from app.data_ingestor import DataIngestor
from app.task_runner import ThreadPool


webserver = Flask(__name__)
webserver.tasks_runner = ThreadPool()

#webserver.task_runner.start()

webserver.data_ingestor = DataIngestor("./nutrition_activity_obesity_usa_subset.csv")

webserver.job_counter = 1

webserver.job_results = {}


# Creăm un obiect logger
webserver.logger = logging.getLogger('webserver_logger')
webserver.logger.setLevel(logging.INFO)

# Configurăm RotatingFileHandler pentru a scrie în fișierul "webserver.log"
webserver.log_file = "webserver.log"

# Dimensiunea maximă a fișierului de log în bytes (100 MB = 100 * (1024 * 1024 bytes))
webserver.max_log_size = 100 * 1024 * 1024

# Numărul maxim de fișiere de log istorice
webserver.backup_count = 5

# Creăm un RotatingFileHandler
file_handler = RotatingFileHandler(webserver.log_file,
                                maxBytes=webserver.max_log_size,
                                backupCount=webserver.backup_count
                                )

# Configurăm formatarea mesajelor de logging
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S')
file_handler.setFormatter(formatter)

# Adăugăm handler-ul la logger
webserver.logger.addHandler(file_handler)

from app import routes
