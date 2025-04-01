# EPICS IOC for fast correctors current to kick conversion

[![Continuous Integration
Status](https://github.com/cnpem/conv-fastcorrs-epics-ioc/actions/workflows/build.yml/badge.svg)](https://github.com/cnpem/conv-fastcorrs-epics-ioc/actions)

This repository contains the EPICS Input/Output Controller (IOC) used at LNLS
for converting current to kicks, based on
[pyDevSup](http://mdavidsaver.github.io/pyDevSup/index.html) support module and
[siriuspy](https://github.com/lnls-sirius/dev-packages/tree/master/siriuspy)
conversion library.

## Running the IOC

You can use the following command to run it in the background using the default
start-up script from
[epics-in-docker](https://github.com/cnpem/epics-in-docker). First, define the
variable `SEC_LIST` with the list of storage ring sectors to handle on this IOC
instance.

```bash
SEC_LIST={section_list} docker compose up -d
```

## Building the IOC image

You can build the IOC with the following command:

```bash
docker compose build
```
