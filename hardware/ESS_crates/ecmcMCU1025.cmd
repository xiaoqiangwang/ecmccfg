############################################################
############# MCU1025:

#Configure EK1100 coupler terminal
${SCRIPTEXEC} ${ecmccfg_DIR}addSlave.cmd, "SLAVE_ID=0, HW_DESC=EK1100"

#Configure EL1018 digital input terminal
${SCRIPTEXEC} ${ecmccfg_DIR}addSlave.cmd, "SLAVE_ID=1, HW_DESC=EL1018"

#Configure EL2808 digital output terminal
${SCRIPTEXEC} ${ecmccfg_DIR}addSlave.cmd, "SLAVE_ID=2, HW_DESC=EL2808"

# Save the slave number for later
epicsEnvSet("ECMC_EC_SLAVE_NUM_DIG_OUT", "${ECMC_EC_SLAVE_NUM}")

#Configure EL5002 2-channel SSI encoder terminal, motor 1
${SCRIPTEXEC} ${ecmccfg_DIR}addSlave.cmd, "SLAVE_ID=3, HW_DESC=EL5002"

#Configure Baumer encoder for EL5002 2-channel SSI encoder terminal (Channel 1)
${SCRIPTEXEC} ${ecmccfg_DIR}applySlaveConfig.cmd "CONFIG=-Encoder-ch1-Baumer-BMMH30D1G24C1213P55"

#Configure Baumer encoder for EL5002 2-channel SSI encoder terminal (Channel 2)
${SCRIPTEXEC} ${ecmccfg_DIR}applySlaveConfig.cmd "CONFIG=-Encoder-ch2-Baumer-BMMH30D1G24C1213P55"

# Configure EL9505 Power supply terminal 5V
${SCRIPTEXEC} ${ecmccfg_DIR}addSlave.cmd, "SLAVE_ID=4, HW_DESC=EL9505"

# Configure EL1252 digital input terminal
${SCRIPTEXEC} ${ecmccfg_DIR}addSlave.cmd, "SLAVE_ID=5, HW_DESC=EL1252"

# Configure EL9410 Power supply with refresh of E-Bus.
${SCRIPTEXEC} ${ecmccfg_DIR}addSlave.cmd, "SLAVE_ID=6, HW_DESC=EL9410"

#Configure EL7037 stepper drive terminal, motor 1
${SCRIPTEXEC} ${ecmccfg_DIR}configureSlave.cmd, "SLAVE_ID=7, HW_DESC=EL7037, CONFIG=-Motor-Nanotec-ST4118L1804-B"

#Configure EL7037 stepper drive terminal, motor 2
${SCRIPTEXEC} ${ecmccfg_DIR}configureSlave.cmd, "SLAVE_ID=8, HW_DESC=EL7037, CONFIG=-Motor-Nanotec-ST4118L1804-B"

#Apply hardware configuration
ecmcConfigOrDie "Cfg.EcApplyConfig(1)"
