import pandas as pd


# Define the calculate_state_mean function here
def calculate_state_mean(ingestor, question, state):

    # Filter data for the specified state and years between 2011 and 2022
    filtered_df = ingestor.df[(ingestor.df['Question'] == question) & (ingestor.df['LocationDesc'] == state) & (ingestor.df['YearStart'] >= 2011) & (ingestor.df['YearStart'] <= 2022)]

    # Check if there are valid data values for the state
    if filtered_df.empty:
        return f"No data available for {state} and {question}"  # Return a message instead of None

    # Check if there are valid data values for the state
    if filtered_df.empty:
        return None

    # Calculate the mean of the Data_Value column for the specified state
    state_mean = filtered_df['Data_Value'].mean()

    return {state : state_mean}


def calculate_states_mean(ingestor, question):

    # Convert request data to a DataFrame
    df = ingestor.df

    # Conversie valori Data_Value la numeric și eliminarea valorilor nevalide
    df['Data_Value'] = pd.to_numeric(df['Data_Value'], errors='coerce')

    # Filtrare date pentru întrebarea specifică și intervalul de ani dorit
    filtered_df = df[(df['YearStart'] >= 2011) & (df['YearStart'] <= 2022) & (df['Question'] == question)]

    # Calcul medie pentru fiecare stat
    state_means = filtered_df.groupby('LocationDesc')['Data_Value'].mean().reset_index().sort_values(by='Data_Value')

    # Convertire rezultate în format dicționar pentru ușurința procesării
    sorted_states = state_means.to_dict(orient='records')

    # Transformarea într-un singur dicționar cu numele statelor ca și chei și media valorilor ca și valori
    results_dict = {item['LocationDesc']: item['Data_Value'] for item in sorted_states}

    return results_dict



def calculate_best5(ingestor, question):

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


def calculate_worst5(ingestor, question):    
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


def calculate_global_mean(ingestor, question):

    # Filter data for the specified question
    filtered_df = ingestor.df[ingestor.df['Question'] == question]

    # Calculate the mean of Data_Value for the filtered data
    global_mean = filtered_df['Data_Value'].mean()

    # Return the global mean
    return {"global_mean" : global_mean}


def calculate_diff_from_mean(ingestor, question):

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


def calculate_state_diff_from_mean(ingestor, question, state):

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


def calculate_mean_by_category(ingestor, question):

    # Filter data for the specified question
    filtered_df = ingestor.df[ingestor.df['Question'] == question]

    # Group data by state, category, and segment, and calculate mean value for each group
    grouped_data = filtered_df.groupby(['LocationDesc', 'StratificationCategory1', 'Stratification1'])['Data_Value'].mean()

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


def calculate_state_mean_by_category(ingestor, question, state):

    # Filter data for the specified question and state
    filtered_df = ingestor.df[(ingestor.df['Question'] == question)
                            & (ingestor.df['LocationDesc'] == state)]

    # Group data by category and segment, and calculate mean value for each group
    grouped_data = filtered_df.groupby(['StratificationCategory1', 'Stratification1'])['Data_Value'].mean()

    # Convertirea datelor grupate într-un dicționar pentru procesare mai ușoară
    grouped_dict = grouped_data.to_dict()

    # Crearea unui nou dicționar cu statul ca cheie principală
    result = {state: {}}
    for (category, segment), value in grouped_dict.items():
        # Formatând cheia ca un string de tuplă pentru a se potrivi cu output-ul dorit
        result[state][f"('{category}', '{segment}')"] = value

    return result