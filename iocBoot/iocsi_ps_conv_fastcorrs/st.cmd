#!../../bin/linux-x86_64/si_ps_conv_fastcorrs

< envPaths
cd "${TOP}"

## Register all support components
dbLoadDatabase "dbd/si_ps_conv_fastcorrs.dbd"
si_ps_conv_fastcorrs_registerRecordDeviceDriver pdbbase

## Load record instances
on error break
system("./generate_crate_substitutions.py")
dbLoadTemplate("db/crates.substitutions")
dbLoadRecords("db/machine_params.db")

cd "${TOP}/iocBoot/${IOC}"
iocInit
