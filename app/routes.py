"""
Define Flask routes and API endpoints for the web application.
"""
from flask import request, jsonify
import pandas as pd
from app import webserver


# Example endpoint definition
@webserver.route('/api/post_endpoint', methods=['POST'])
def post_endpoint():
    if request.method == 'POST':
        # Assuming the request contains JSON data
        data = request.json
        print(f"got data in post {data}")

        # Process the received data
        # For demonstration purposes, just echoing back the received data
        response = {"message": "Received data successfully", "data": data}

        # Sending back a JSON response
        return jsonify(response)
    else:
        # Method Not Allowed
        return jsonify({"error": "Method not allowed"}), 405


@webserver.route('/api/get_results/<job_id>', methods=['GET'])
def get_response(job_id):
    print(f"JobID is {job_id}")

    # Check if job_id is valid

    # Check if job_id is done and return the result
    #    res = res_for(job_id)
    #    return jsonify({
    #        'status': 'done',
    #        'data': res
    #    })

    # Check if job_id is valid
    if job_id not in webserver.tasks_runner.job_results:
        return jsonify({"status": "error", "reason": "Invalid job_id"}), 400

    # Check if job_id is running and return the result
    if webserver.tasks_runner.job_results.get(job_id).done() is False:
        return jsonify({'status': 'running'}), 200

    result = webserver.tasks_runner.job_results.get(job_id).result()

    # If not, return done status
    return jsonify({"status": "done", "data": result}), 200


def calculate_states_mean(question):
    # Access the DataIngestor instance from the webserver
    ingestor = webserver.data_ingestor
    df = ingestor.df

    # Conversie valori Data_Value la numeric și eliminarea valorilor nevalide
    df['Data_Value'] = pd.to_numeric(df['Data_Value'], errors='coerce')

    # Filtrare date pentru întrebarea specifică și intervalul de ani dorit
    filtered_df = df[(df['YearStart'] >= 2011) & (df['YearStart'] <= 2022)
                     & (df['Question'] == question)]

    # Calcul medie pentru fiecare stat
    state_means = filtered_df.groupby('LocationDesc')['Data_Value'].mean()
    state_means = state_means.reset_index().sort_values(by='Data_Value')

    # Convertire rezultate în format dicționar pentru ușurința procesării
    sorted_states = state_means.to_dict(orient='records')

    # Numele statelor ca și chei și media valorilor ca și valori
    results_dict = {item['LocationDesc']: item['Data_Value'] for item in sorted_states}

    return results_dict



@webserver.route('/api/states_mean', methods=['POST'])
def states_mean_request():

    # Get request data
    data = request.json
    webserver.logger.info("Got request %s", data)
    print(f"Got request {data}")

    # Access job_counter from webserver
    job_id = f"job_id_{webserver.job_counter}"

    # Register job. Don't wait for task to finish
    task_runner = webserver.tasks_runner

    # Register the job to the ThreadPool without waiting for the task to finish
    task_runner.submit(calculate_states_mean, job_id, **data)

    # Increment job_id counter
    webserver.job_counter += 1

    # Log the job_id
    webserver.logger.info("Job ID: %s", job_id)

    # Return associated job_id
    return jsonify({"job_id": job_id}), 200



def calculate_state_mean(ingestor, question, state):

    # Filter data for the specified state and years between 2011 and 2022
    filtered_df = ingestor.df[(ingestor.df['Question'] == question)
                            & (ingestor.df['LocationDesc'] == state)
                            & (ingestor.df['YearStart'] >= 2011)
                            & (ingestor.df['YearStart'] <= 2022)]

    # Check if there are valid data values for the state
    if filtered_df.empty:
        return None

    # Calculate the mean of the Data_Value column for the specified state
    state_mean = filtered_df['Data_Value'].mean()

    return {state : state_mean}



@webserver.route('/api/state_mean', methods=['POST'])
def state_mean_request():

    # Get request data
    data = request.json
    webserver.logger.info("Got request %s", data)
    print(f"Got request {data}")

    # Extract state from the request data
    state = data.get('state')

    # Extract the question from the request data
    question = data.get('question', '')

    # Check if state is provided in the request
    if state is None:
        return jsonify({"error": "State not provided"}), 400

    # Generate a unique job ID
    job_id = f"job_id_{webserver.job_counter}"

    ingestor = webserver.data_ingestor

    # Register job. Don't wait for task to finish
    task_runner = webserver.tasks_runner
    task_runner.submit(calculate_state_mean, job_id, ingestor=ingestor,
                        question=question, state=state)

    # Increment job_id counter
    webserver.job_counter += 1

    # Log the job_id
    webserver.logger.info("Job ID: %s", job_id)

    # Return associated job_id
    return jsonify({"job_id": job_id}), 200



def calculate_best5(question):

    # Access the DataIngestor instance from the webserver
    ingestor = webserver.data_ingestor

    # Filter data for years between 2011 and 2022
    filtered_df = ingestor.df[(ingestor.df['Question'] == question)
                            & (ingestor.df['YearStart'] >= 2011)
                            & (ingestor.df['YearStart'] <= 2022)]

    # Group by state and calculate mean of Data_Value
    state_means = filtered_df.groupby('LocationDesc')['Data_Value'].mean().reset_index()

    # Sort states by mean value based on the question type
    # Determine the sorting order based on the question type
    if question in ingestor.questions_best_is_min:
        ascending_order = True
    elif question in ingestor.questions_best_is_max:
        ascending_order = False
    else:
        raise ValueError("Question not found in any list")
    state_means_sorted = state_means.sort_values(by='Data_Value', ascending=ascending_order)

    # Get the top 5 states with the highest mean values
    top5_states = state_means_sorted.head(5)

    # Convert DataFrame to a list of tuples (state, mean_value)
    result = top5_states.set_index('LocationDesc')['Data_Value'].to_dict()


    return result



@webserver.route('/api/best5', methods=['POST'])
def best5_request():

    # Get request data
    data = request.json
    webserver.logger.info("Got request %s", data)
    print(f"Got request {data}")

    # Generate a unique job ID
    job_id = f"job_id_{webserver.job_counter}"

    # Register job. Don't wait for task to finish
    task_runner = webserver.tasks_runner
    task_runner.submit(calculate_best5, job_id, **data)

    # Increment job_id counter
    webserver.job_counter += 1

    # Log the job_id
    webserver.logger.info("Job ID: %s", job_id)

    # Return associated job_id
    return jsonify({"job_id": job_id}), 200


def calculate_worst5(question):

    # Access the DataIngestor instance from the webserver
    ingestor = webserver.data_ingestor

    # Filter data for years between 2011 and 2022
    filtered_df = ingestor.df[(ingestor.df['Question'] == question)
                            & (ingestor.df['YearStart'] >= 2011)
                            & (ingestor.df['YearStart'] <= 2022)]

    # Group by state and calculate mean of Data_Value
    state_means = filtered_df.groupby('LocationDesc')['Data_Value'].mean().reset_index()

    # Sort states by mean value based on the question type
    # Determine the sorting order based on the question type
    if question in ingestor.questions_best_is_min:
        ascending_order = False
    elif question in ingestor.questions_best_is_max:
        ascending_order = True
    else:
        raise ValueError("Question not found in any list")
    state_means_sorted = state_means.sort_values(by='Data_Value', ascending=ascending_order)

    # Get the last 5 states with the highest or lowest mean values based on the question type
    worst5_states = state_means_sorted.head(5)

    # Convert DataFrame to a list of tuples (state, mean_value)
    result = worst5_states.set_index('LocationDesc')['Data_Value'].to_dict()

    return result


@webserver.route('/api/worst5', methods=['POST'])
def worst5_request():

    # Get request data
    data = request.json
    webserver.logger.info("Got request %s", data)
    print(f"Got request {data}")

    # Generate a unique job ID
    job_id = f"job_id_{webserver.job_counter}"

    # Register job. Don't wait for task to finish
    task_runner = webserver.tasks_runner
    task_runner.submit(calculate_worst5, job_id, **data)

    # Increment job_id counter
    webserver.job_counter += 1

    # Log the job_id
    webserver.logger.info("Job ID: %s", job_id)

    # Return associated job_id
    return jsonify({"job_id": job_id}), 200



def calculate_global_mean(question):

    # Access the DataIngestor instance from the webserver
    ingestor = webserver.data_ingestor

    # Filter data for the specified question
    filtered_df = ingestor.df[ingestor.df['Question'] == question]

    # Calculate the mean of Data_Value for the filtered data
    global_mean = filtered_df['Data_Value'].mean()

    # Return the global mean
    return {"global_mean" : global_mean}


@webserver.route('/api/global_mean', methods=['POST'])
def global_mean_request():

    # Get request data
    data = request.json
    webserver.logger.info("Got request %s", data)
    print(f"Got request {data}")

    # Generate a unique job ID
    job_id = f"job_id_{webserver.job_counter}"

    # Register job. Don't wait for task to finish
    task_runner = webserver.tasks_runner
    task_runner.submit(calculate_global_mean,job_id, **data)

    # Increment job_id counter
    webserver.job_counter += 1

    # Log the job_id
    webserver.logger.info("Job ID: %s", job_id)

    # Return associated job_id
    return jsonify({"job_id": job_id}), 200


def calculate_diff_from_mean(question):

    # Access the DataIngestor instance from the webserver
    ingestor = webserver.data_ingestor

    # Filter data for the specified question
    filtered_df = ingestor.df[ingestor.df['Question'] == question]

    # Calculate the global mean for the filtered data
    global_mean = filtered_df['Data_Value'].mean()

    # Group data by state and calculate mean for each state
    state_means = filtered_df.groupby('LocationDesc')['Data_Value'].mean()

    # Calculate the difference between global mean and state mean for each state
    diff_from_mean = global_mean - state_means

    # Convert the result to a dictionary for easier processing
    result = diff_from_mean.to_dict()

    return result


@webserver.route('/api/diff_from_mean', methods=['POST'])
def diff_from_mean_request():

    # Get request data
    data = request.json
    webserver.logger.info("Got request %s", data)
    print(f"Got request {data}")

    # Generate a unique job ID
    job_id = f"job_id_{webserver.job_counter}"

    # Register job. Don't wait for task to finish
    task_runner = webserver.tasks_runner
    task_runner.submit(calculate_diff_from_mean,job_id, **data)

    # Increment job_id counter
    webserver.job_counter += 1

    # Log the job_id
    webserver.logger.info("Job ID: %s", job_id)

    # Return associated job_id
    return jsonify({"job_id": job_id}), 200


def calculate_state_diff_from_mean(question, state):

    # Access the DataIngestor instance from the webserver
    ingestor = webserver.data_ingestor

    # Filtrăm datele pentru întrebarea specificată
    filtered_df = ingestor.df[ingestor.df['Question'] == question]

    # Calculăm media globală pentru toate datele filtrate, excluzând statul specific
    global_mean = filtered_df['Data_Value'].mean()

    # Filtrăm datele pentru statul specificat
    state_df = filtered_df[filtered_df['LocationDesc'] == state]
    state_mean = state_df['Data_Value'].mean()

    # Calculăm diferența dintre media statului și media globală
    diff_from_mean = global_mean - state_mean


    # Convert the result to a dictionary for easier processing
    result = {state: diff_from_mean}

    return result


@webserver.route('/api/state_diff_from_mean', methods=['POST'])
def state_diff_from_mean_request():

    # Get request data
    data = request.json
    webserver.logger.info("Got request %s", data)
    print(f"Got request {data}")

    # Generate a unique job ID
    job_id = f"job_id_{webserver.job_counter}"

    # Register job. Don't wait for task to finish
    task_runner = webserver.tasks_runner
    task_runner.submit(calculate_state_diff_from_mean, job_id, **data)

    # Increment job_id counter
    webserver.job_counter += 1

    # Log the job_id
    webserver.logger.info("Job ID: %s", job_id)

    # Return associated job_id
    return jsonify({"job_id": job_id}), 200


def calculate_mean_by_category(question):

    # Access the DataIngestor instance from the webserver
    ingestor = webserver.data_ingestor

    # Filter data for the specified question
    filtered_df = ingestor.df[ingestor.df['Question'] == question]

    # Group data by state, category, and segment, and calculate mean value for each group
    grouped_data = filtered_df.groupby(['LocationDesc',
                                        'StratificationCategory1',
                                        'Stratification1'])['Data_Value'].mean()

    result = {}
    # Iterate through each group in the grouped data
    for (state, category, segment), mean_value in grouped_data.items():
        # Construct the key as a string that represents the tuple
        key = f"('{state}', '{category}', '{segment}')"
        # Assign the mean value to the corresponding key in the result dictionary
        result[key] = mean_value

    # No need to store the result in the task runner with the associated job ID
    # Return the result dictionary directly
    return result


@webserver.route('/api/mean_by_category', methods=['POST'])
def mean_by_category_request():

    # Get request data
    data = request.json
    webserver.logger.info("Got request %s", data)
    print(f"Got request {data}")

    # Generate a unique job ID
    job_id = f"job_id_{webserver.job_counter}"

    # Register job. Don't wait for task to finish
    task_runner = webserver.tasks_runner
    task_runner.submit(calculate_mean_by_category, job_id, **data)

    # Increment job_id counter
    webserver.job_counter += 1

    # Log the job_id
    webserver.logger.info("Job ID: %s", job_id)

    # Return associated job_id
    return jsonify({"job_id": job_id}), 200



def calculate_state_mean_by_category(question, state):

    # Access the DataIngestor instance from the webserver
    ingestor = webserver.data_ingestor

    # Filter data for the specified question and state
    filtered_df = ingestor.df[(ingestor.df['Question'] == question)
                            & (ingestor.df['LocationDesc'] == state)]

    # Group data by category and segment, and calculate mean value for each group
    grouped_data = filtered_df.groupby(['StratificationCategory1',
                                        'Stratification1'])['Data_Value'].mean()

    # Convertirea datelor grupate într-un dicționar pentru procesare mai ușoară
    grouped_dict = grouped_data.to_dict()

    # Crearea unui nou dicționar cu statul ca cheie principală
    result = {state: {}}
    for (category, segment), value in grouped_dict.items():
        # Formatând cheia ca un string de tuplă pentru a se potrivi cu output-ul dorit
        result[state][f"('{category}', '{segment}')"] = value

    return result


@webserver.route('/api/state_mean_by_category', methods=['POST'])
def state_mean_by_category_request():

    # Get request data
    data = request.json
    webserver.logger.info("Got request %s", data)
    print(f"Got request {data}")

    # Generate a unique job ID
    job_id = f"job_id_{webserver.job_counter}"

    # Register job. Don't wait for task to finish
    task_runner = webserver.tasks_runner
    task_runner.submit(calculate_state_mean_by_category, job_id, **data)

    # Increment job_id counter
    webserver.job_counter += 1

    # Log the job_id
    webserver.logger.info("Job ID: %s", job_id)

    # Return associated job_id
    return jsonify({"job_id": job_id}), 200


@webserver.route('/api/graceful_shutdown', methods=['GET'])
def graceful_shutdown():

    # Notify the ThreadPool to finish processing all pending tasks
    webserver.tasks_runner.shutdown()

   # Log the initiation of graceful shutdown
    webserver.logger.info("Graceful shutdown initiated. No new requests will be accepted.")

    # Return a response indicating successful initiation of graceful shutdown
    return jsonify({"status": "Graceful shutdown initiated. No new requests will be accepted."}),200


@webserver.route('/api/jobs', methods=['GET'])
def get_jobs_status():

    # Get all job IDs and their corresponding statuses
    # Acquire the lock before accessing shared resources
    with webserver.tasks_runner.results_lock:
        # Get all job IDs and their corresponding statuses
        job_statuses = {job_id: "running" if future.running() else "done" for job_id, future in webserver.tasks_runner.job_results.items()}


    # Log the job statuses
    webserver.logger.info("Job statuses: %s", job_statuses)

    # Return the job IDs and their statuses as JSON response
    return jsonify({"status": "done", "data":
                    [{job_id: status} for job_id, status in job_statuses.items()]}), 200


@webserver.route('/api/num_jobs', methods=['GET'])
def get_num_jobs():

    # Calculate the number of remaining jobs to be processed
    num_jobs_remaining = len(webserver.tasks_runner.job_results) - sum(1 for future in webserver.tasks_runner.job_results.values() if future.done())

    # Log the number of remaining jobs
    webserver.logger.info("Number of remaining jobs: %d", num_jobs_remaining)

    # Return the number of remaining jobs as JSON response
    return jsonify({"num_jobs_remaining": num_jobs_remaining}), 200


# You can check localhost in your browser to see what this displays
@webserver.route('/')
@webserver.route('/index')
def index():
    routes = get_defined_routes()
    msg = f"Hello, World!\n Interact with the webserver using one of the defined routes:\n"

    # Display each route as a separate HTML <p> tag
    paragraphs = ""
    for route in routes:
        paragraphs += f"<p>{route}</p>"

    msg += paragraphs
    return msg

def get_defined_routes():
    routes = []
    for rule in webserver.url_map.iter_rules():
        methods = ', '.join(rule.methods)
        routes.append(f"Endpoint: \"{rule}\" Methods: \"{methods}\"")
    return routes
