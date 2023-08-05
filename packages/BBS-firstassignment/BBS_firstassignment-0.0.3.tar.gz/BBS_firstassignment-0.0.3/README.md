# Processo e Sviluppo del Software - 1st Assignment

## Gruppo

BSS Group

&bull; <u>817 &nbsp;052</u> &emsp; Balde Muhammad Yassin      <br>
&bull; <u>856 450</u> &emsp; Bianchi Edoardo             <br>
&bull; <u>903 586</u> &emsp; Sala Niccolò                <br>

## Repository

https://gitlab.com/unimib-community/2022_assignment1_bbsgroup/-/tree/main

## Applicazione

Il codice realizzato e caricato per lo svolgimento dell’assignment descrive una semplice applicazione in Python che si interfaccia ad un’API - url: https://www.fishwatch.gov/api/species - incaricata di fornire informazioni su diverse specie di pesci.

## Pipeline

### 1. Image
Con "image" viene installata un'immagine di Docker contenente l'ultima versione di Python.

### 2. Variables
Con “variables” definiamo le variabili che utilizzeremo e richiameremo all'interno della pipeline.

### 3. Cache
La cache serve a ridurre il tempo di attesa per il download e la build. Infatti, quando viene gestita una richiesta HTTP, si verifica prima che la cache abbia memorizzata una risposta idonea e non scaduta da poter utilizzare. Solo nel caso in cui la ricerca non dovesse dare esito positivo si procede con il download del contenuto richiesto.
Con "paths" indichiamo i percorsi in cui è memorizzata la cache.

### 4. Stages
Attraverso “stages” definiamo quali sono le fasi della nostra pipeline. Possiamo quindi identificare Build, Verify, Unit-test, Integration-test, Package, Release e Deploy.

### 4.1 Build
La fase di Build consiste nella risoluzione delle dipendenze e nella compilazione del codice. L'installazione delle dipendenze è esplicitata con il comando "pip install requests" che importa ed esegue un modulo per l'invio di richieste HTTP.

### 4.2 Verify
Nel Verify-job verifichiamo la correttezza e la sicurezza del codice tramite Prospector e Bandit. Nel before_script installiamo le dipendenze ed eseguiamo l’attivazione di Bandit. Nel file “bandit.yaml” richiamato nello script esplicitiamo la volontà di non valutare le asserzioni usate nei file di test come warning, in quanto non creino problemi di correttezza o sicurezza per il nostro programma.

### 4.3 Unit-test
Nella fase di Unit-test vengono fatti test sui singoli moduli del programma. Il before_script di questa fase ha il compito di installare le dipendenze necessarie, ovvero "requests" e "pytest". Dunque, con il comando “pytest” eseguiamo tutti i file di test creati (nel nostro caso solo “test_unit.py”).

### 4.4 Integration-test
Presto disponibile.

### 4.5 Package
Per la creazione del pacchetto usiamo Wheel e Setuptools. Nello script eseguiamo il file “setup.py”, ossia il file che definisce metadati, dipendenze e contenuti del nostro pacchetto.  

### 4.6 Release
Con Twine gestiamo il rilascio dell’applicazione. Nel before_script installiamo “build” e “twine”. Quindi, tramite il comando “twine upload -r testpy” verifichiamo la correttezza del pacchetto e con il secondo comando di upload concretizziamo la pubblicazione del pacchetto su PyPi. 

### 4.7 Deploy
Presto disponibile.
