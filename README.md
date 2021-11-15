# GATE Cloud based wrapper for ChemDataExtractor

This repository contains the configuration to build the ChemDataExtractor app for GATE Cloud.  The app is in two parts, an ELG-compatible service that does the actual Python NER, and a thin GATE application that uses the ELG client PR to call the tagger.


## Building the ELG Image

```
conda lock -p linux-64 -f environment.yaml
```

```
docker buildx build -t elg.docker.gate.ac.uk/chemdataextractor:latest .
```

## Building the GATE Cloud Pipeline

The GATE Cloud pipeline is then a thin wrapper which calls the ELG endpoint using the ELG client PR.  To build this, run `./gradlew cloudZip` in the `cloud-pipeline` directory and the zip file will be created under `build/distributions`.
