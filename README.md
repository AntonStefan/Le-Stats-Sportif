Anton Stefan,
331CC                      
                            Le Stats Sportif
                        

# Tema 1
Timp implementare:
~23 ore


Le Stats Sportif este un proiect pentru analiza datelor legate de activitati
sportive si de sanatate. Aplicatia are scopul implementarii concurente a taskurilor
utilizand o problema clasica (client - server), frameworkul Flask si aprofundarea lucrului
cu threaduri in Python.


Solutie aleasa:
Am optat sa folosesc ThreadPoolExecutor deoarece ofera o modalitate convenabila de
a gestiona sarcninile concurente intr-un mod simplu si eficient. Metoda submit furnizeaza
o interfata simpla si intuitiva pentru trimiterea si gestionarea saricinilor, permitand
obtinerea unui obiect 'Future'. Acest obiect poate fi folosit pentru a obtine rezultatul sau
pentru a verifica starea sarcinii.

Consider ca tema este una utila si de actualitate, cu o implementare eficienta.


Implementare:
Toate cerintele temei au fost atinse.


Detalii implementare:
Clasa 'ThreadPool' initializeaza un pool de fire de executie cu un numar specificat
de fire pe baza variabilei de mediu 'TP_NUM_OF_THREADS' sau a  concurentei hardware.
Initializam un dictionar job_results si cream un obiect de tip 'Lock' pentru a 
asigura accesul sincronizat la dictionarul de rezultate. Folosim submit pe 
ThreadPoolExecutor pentru a trimite o sarcina catre pool-ul de fire de executie
si a le gestiona concurent. Metoda creeaza un obiect 'Future' pentru 
sarcina trimisa si il adauga in job_results.


Endpointurile:
    - primesc datele cererii in format json si le inregistreaza in variabila 'data',
    inregistreaza o noua sarcina in 'ThreadPool' pentru a calcula pe datele primite,
    fara a astepta finalizarea sarcinii si in final returneaza un identificator de sarcina
    'job_id' catre client pentru a urmari starea si rezultatul sarcinii

Functii auxiliare:
    M-am folosit de pandas pentru usurinta

    /api/states_mean
    calculate_states_mean
    ia statele care au o anumita intrebare si le calculeaza media, sortandu-le in
    final crescator dupa medie 

    /api/state_mean
    calculate_state_mean
    ia statele care au o anumita intrebare si un stat si le calculeaza media, sortandu-le in
    final crescator dupa medie 

    /api/best
    calculate_best5
    ia cele mai bune 5 state ca medie dupa valoare in functie de o anumita intrebare, ordinea
    de sortare este determinata in functie de intrebare daca se afla in 
    self.questions_best_is_min sau self.questions_best_is_max din data_ingestor.py

    /api/worst5
    calculate_worst5
    ia cele mai proaste 5 state ca medie dupa valoare in functie de o anumita intrebare, ordinea
    de sortare este determinata in functie de intrebare daca se afla in 
    self.questions_best_is_min sau self.questions_best_is_max din data_ingestor.py

    /api/global/mean
    calculate_global_mean
    functie care calculeaza media valorilor din intregul set de date pentru o intrebare specifica

    /api/diff_from_mean
    calculate_diff_from_mean
    pentru o intrebare specifica calculeaza diferenta intre global_mean si state_mean

    /api/state_diff_from_mean
    calculate_state_diff_from_mean
    pentru o intrebare specifica si un stat calculeaza diferenta intre global_mean si state_mean

    /api/mean_by_category
    calculate_mean_by_category
    pentru o intrebare specifica calculeaza valoarea medie pentru fiecare segment
    Stratification1 din categoriile StratificationCategory1

    /api/state_mean_by_category
    calculate_state_mean_by_category
    pentru o intrebare specifica si un stat calculeaza valoarea medie pentru fiecare segment
    Stratification1 din categoriile StratificationCategory1

/api/jobs
aceasta ruta permite obtinerea tuturor job-urilor inregistrate in aplicatie
fie ele running sau done

/api/num_jobs
aceasta ruta ofera numarul total de sarcini ramase de procesat in aplicatie
printr-o diferenta intre toate joburile si joburile care sunt done


In final avem /api/graceful_shutdown

Folosind metoda shutdown() a obiectului webserver.tasks_runner, se trimite
o notificare ThreadPool-ului pentru a finaliza prelucrarea tuturor 
sarcinilor care sunt inca in asteptare. Am pus wait metodei shutdown()
pentru a se astepte finalizarea tuturor taskurilor ramase inainte 
de a opri efectiv executia firelor.


Unittests
Am creat si un folder pentru teste, anume unittests pentru verificarea metodelor de calcul.

Acesta contine: 
test.csv - mi-am definit eu o baza de date cu elementele minime pentru a putea testa metodele

calculus_routes.py - am adaugat toate metodele de calcul din aplicatia principala din routes.py
pentru a putea fi verificate si pentru a le separa de clasa de testare pentru o lizibilitate
mai buna

data_ingestor.py - folosit pentru incarcarea datelor din test.csv

TestWebserver.py - clasa de testare care pe baza anumitor inputuri testeaza sa de-a corect
outputul asteptat, daca outputul nu e cel asteptat o sa se termine cu assert. In aceasta clasa
am verificat validitatea tuturor metodelor de calcul.


Logging
In final am implementat fisiere de logging in __init__.py si in endopintul fiecarei functii
din routes.py. Am creat un obiect logger si am setat nivelul de inregistrare la INFO ceea 
ce inseamna ca doar mesajele de informare si erorile vor fi inregistrate. Am specificat
fisierul unde vor fi scrise si anume webserver.log, configurat RotatingFileHandler,
dimensiunea maxima a fisierului webserver.max_log_size, numarul maxim de fisiere de log
istorice webserver.backup_count, formatarea mesajelor (UTC/GMT) si am adaugat handler-ul
file_handler la loggerul webserver.logger.



