#!../../bin/linux-x86_64/si_ps_conv_fastcorrs

#- You may have to change si_ps_conv_fastcorrs to something else
#- everywhere it appears in this file

< envPaths

cd "${TOP}"

## Register all support components
dbLoadDatabase "dbd/si_ps_conv_fastcorrs.dbd"
si_ps_conv_fastcorrs_registerRecordDeviceDriver pdbbase

## Load record instances
dbLoadRecords("db/sector.db","SEC=$(SEC)")
dbLoadRecords("db/machine_params.db")

cd "${TOP}/iocBoot/${IOC}"
iocInit
