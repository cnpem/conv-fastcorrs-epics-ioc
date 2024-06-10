TOP=../..

include $(TOP)/configure/CONFIG
include $(PYDEVSUP)/configure/CONFIG_PY
#----------------------------------------
#  ADD MACRO DEFINITIONS AFTER THIS LINE
#=============================

#=============================
# Build the IOC application

PROD_IOC = si_ps_conv_fastcorrs
# si_ps_conv_fastcorrs.dbd will be created and installed
DBD += si_ps_conv_fastcorrs.dbd

# si_ps_conv_fastcorrs.dbd will be made up from these files:
si_ps_conv_fastcorrs_DBD += base.dbd

# Include dbd files from all support applications:
si_ps_conv_fastcorrs_DBD += pyDevSup.dbd

# Add all the support libraries needed by this IOC
#si_ps_conv_fastcorrs_LIBS += xxx

# si_ps_conv_fastcorrs_registerRecordDeviceDriver.cpp derives from si_ps_conv_fastcorrs.dbd
si_ps_conv_fastcorrs_SRCS += si_ps_conv_fastcorrs_registerRecordDeviceDriver.cpp

# Build the main IOC entry point on workstation OSs.
si_ps_conv_fastcorrs_SRCS_DEFAULT += si_ps_conv_fastcorrsMain.cpp
si_ps_conv_fastcorrs_SRCS_vxWorks += -nil-

# Add support from base/src/vxWorks if needed
#si_ps_conv_fastcorrs_OBJS_vxWorks += $(EPICS_BASE_BIN)/vxComLibrary

# Finally link to the EPICS Base libraries
si_ps_conv_fastcorrs_LIBS += pyDevSup$(PY_LD_VER)
si_ps_conv_fastcorrs_LIBS += $(EPICS_BASE_IOC_LIBS)

PY += curr2strn.py
PY += strn2curr.py
#===========================

include $(TOP)/configure/RULES
include $(PYDEVSUP)/configure/RULES_PY
#----------------------------------------
#  ADD RULES AFTER THIS LINE

