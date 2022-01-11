# ELG and GATE Cloud wrapper for ChemDataExtractor

This repository contains the configuration to build the ChemDataExtractor app for GATE Cloud.  The app is in two parts, an ELG-compatible service that does the actual Python NER, and a thin GATE application that uses the ELG client PR to call the tagger.


## Building the ELG Image


```
docker buildx build -t chemdataextractor:latest .
```

The image is also built automatically and pushed to `ghcr.io` when changes are pushed, see the "packages" section to the right for details.


### Updating Dependencies

To aid reproducability we use fixed versions for all dependencies. This includes both within
the conda environent and the python modules

```
conda lock -p linux-64 -f environment.yaml
```


```
docker run -it --rm --entrypoint /bin/bash ghcr.io/gatenlp/chemdataextractor:main
```

```
/env/bin/pip freeze -l | grep ==
```

## Building the GATE Cloud Pipeline

The GATE Cloud pipeline is then a thin wrapper which calls the ELG endpoint using the ELG client PR.  To build this, run `./gradlew cloudZip` in the `cloud-pipeline` directory and the zip file will be created under `build/distributions`.

## Licence

The code in this repository is licenced under the [MIT licence](LICENSE), as is [ChemDataExtractor](https://github.com/mcs07/ChemDataExtractor) itself.
