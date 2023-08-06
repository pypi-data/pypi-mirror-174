# Processo e sviluppo del software - Assignment 1

## Gruppo ITIS 

- 851813 - Brugora Michael
- 852095 - Locatelli Riccardo
- 851810 - Magni Marco

## Progetto

- https://gitlab.com/magni5/2022_assignment1_itis

## Presentazione

È stata realizzata una pipeline per il CI/CD di una semplice applicazione web per l'inserimento e la visualizzazione di una lista di utenze.

L'applicazione è stata sviluppata in Python, con l'utilizzo del framework Django. Si interfaccia con una base di dati PostgreSQL ed è pubblicata su Heroku.

## Analisi della pipeline

### Predisposizione

All'inizio della pipeline sono necessarie delle configurazioni al fine di predisporre la corretta esecuzione della pipeline. Queste comprendono la dichiarazione della versione di Python e dei vari percorsi per il caching.

In *before_script*, invece, sono definiti gli script da eseguire prima di ciascuna fase della pipeline. Nel nostro caso la configurazione dell'ambiente virtuale.

```bash
image: python:latest

variables:
  PIP_CACHE_DIR: "$CI_PROJECT_DIR/.cache/pip"

cache:
  paths:
    - .cache/pip
    - venv/

before_script:
  - pip install virtualenv
  - virtualenv venv
  - source venv/bin/activate
```

### Pipeline

Successivamente vengono definiti gli stage della pipeline. Per ciascuno di essi poi verrà eseguito un job, eccezion fatta per lo stage di *test* che prevederà *unit-test* e *integration-test*.

```bash
stages:
  - build
  - verify
  - test
  - package
  - release
  - deploy
```

### Build

Nella fase di build vengono installate nell'ambiente virtuale le dipendenze del progetto, indicate nel file *requirements.txt*.

Non è necessario compilare il progetto, essendo Python un linguaggio interpretato a runtime.

```bash
build:
  stage: build
  script:
    - pip install -r requirements.txt
```

### Verify

La fase di verify si occuppa di eseguire il linting del codice. Nello specifico questo viene fatto con *Prospector* e il tool *Bandit*. È stato deciso di poter accettare il fallimento di questo stage data la finalità didattica del progetto.

Vengono dunque scaricati i due strumenti e in seguito eseguito il linting, ignorando la directory *venv* e specificando l'utilizzo del framework Django.

```bash
verify:
  stage: verify
  allow_failure: true
  script:
    - pip install prospector bandit
    - prospector --uses django --with-tool bandit -i venv
```

### Unit test

Lo stage di test è diviso in due job, indipendenti tra loro.

Un primo job è quello dello unit test, che viene eseguito tramite i moduli di test integrati in Django.

```bash
unit-test:
  stage: test
  script:
    - python manage.py test --keepdb miaApplicazione.tests.unit
```

### Integration test

Parallelamente viene eseguito il test di integrazione con la base di dati, sempre utilizzando i moduli di test integrati in Django.

```bash
integration-test:
  stage: test
  script:
    - python manage.py test --keepdb miaApplicazione.tests.integration
```

### Package

Nello stage di package viene usato *Wheel* per creare *source archive* e *built distribution* e successivamente vene controllato quanto creato con *Twine*.

```bash
package:
  stage: package
  script:
    - pip install wheel twine
    - python setup.py sdist
    - python setup.py bdist_wheel
    - twine check dist/*
  artifacts:
    paths:
      - dist/*
```

### Release

La fase di release necessita del completamento e della riuscita di quella di package. Tramite *Twine* si occupa di caricare su *PyPI* i pacchetti generati nella fase precedente.

Quanto di caricato sarà poi consultabile, appunto, su [PyPI (mioProgetto)](https://pypi.org/project/mioProgetto/), e installabile tramite *pip* con il seguente comando.

```bash
pip install mioProgetto
```

```bash
release:
  stage: release
  needs: [package]
  script:
    - pip install twine
    - twine upload -u $PYPI_USERNAME -p $PYPI_PASSWORD --skip-existing dist/*
  artifacts:
    paths:
      - dist/*
```

### Deploy

Per ultima, sicuramente non per importanza, la fase di deploy. Viene installata la gemma di Ruby *dpl* e tramite essa viene effettuato il deploy vero e proprio dell'applicazione su [Heroku (gruppo-itis)](https://gruppo-itis.herokuapp.com/).

```bash
deploy:
  stage: deploy
  before_script:
    - apt-get update -qy
    - apt-get install -y ruby-dev
    - gem install dpl
  script:
    - dpl --provider=heroku --app=$HEROKU_APP_NAME --api-key=$HEROKU_PRODUCTION_KEY
```