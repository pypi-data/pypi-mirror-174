# Componenti del gruppo NERV:

* Giannaccari Mattia - Matricola 869877
* Dedò Shana - Matricola 851660


# pyWall
pyWall è una semplice chat di gruppo a linea di comando realizzata allo scopo di implementare la pipeline per il primo assignment del corso di processo e sviluppo del software.

La repository del progetto è [https://gitlab.com/nerv8/2022_assignment1_pywall](https://gitlab.com/nerv8/2022_assignment1_pywall)

# Avanzamento

* ~~Implementazione del codice server side~~
* ~~Implementazione del codice client side~~
* ~~Implementazione dei test~~
* Formalizzazione della pipeline
* ~Documentazione~

# Pipeline

### Build 
Nella fase di **build** vengono installate le librerie necessarie, se presenti. Per far ciò viene utilizzato il file `requirements.txt`, il quale contiene il nome di ciascuna libreria e la versione da installare.

```python
build-job:
  stage: build
  script:
    - pip install -r requirements.txt
```

### Verify
Nella fase di **verify** vengono eseguiti due revisori di codice: `prospector` e `bandit`. Il primo controlla la correttezza della struttura del codice, mentre il secondo verifica la presenza di potenziali errori di sicurezza.

```python
verity-prospector-job:
  stage: verify
  script:
    - python3 -m prospector ./pyWall_client.py --no-autodetect
    - python3 -m prospector ./pyWall_client_functions.py --no-autodetect
    - python3 -m prospector ./pyWall_server.py --no-autodetect

verify-bandit-job:
  stage: verify
  script:
    - bandit -r ./pyWall_server.py
    - bandit -r ./pyWall_client.py
    - bandit -r ./pyWall_client_functions.py
```

### Test
Durante la fase di **test** vengono eseguiti gli **unit** e gli **integration** test, i primi per testare i singoli componenti mentre i secondi per valutare il sistema complessivamente, ovvero controllando il funzionemto delle componenti mentre interagiscono tra di loro. Per fare ciò si fa uso di `pytest`.

```python
unit-test-job:
  stage: test
  script:
    - nohup python3 ./pyWall_server.py &
    - pytest ./tests/unit/test_server_endpoint.py
    - pytest ./tests/unit/test_client_request.py

lint-test-job:
  stage: test
  script:
    - nohup python3 ./pyWall_server.py &
    - pytest ./tests/integration/test_server_client_comm.py
```

### Package 
Nella fase di **package** viene generato il pacchetto da rilasciare. 

```python
package-job:
  stage: package
  script:
 
```

### Release
Nella fase di **release** viene rilasciata l'applicazione.

```python
release-job:
  stage: release
  script:
```

### Deploy
Nella fase di **deploy** viene utilizzato `...` per distribuire l'applicazione.

```python
deploy-job:
  stage: deploy
  script:
```
