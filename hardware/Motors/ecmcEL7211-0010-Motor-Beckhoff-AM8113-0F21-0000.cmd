#-d /**
#-d   \brief hardware script for EL7211-0010-Motor-Beckhoff-AM8113-0F21-0000
#-d   \details Parametrization of EL7211 for motor Beckhoff AM8113-0F21-0000
#-d   \author Niko Kivel
#-d   \file
#-d   \note For important parameters see TwinCAT CoE startup list for the motor terminal configuration.
#-d */

#- 0x9009 0x0A Effective nominal voltage (mV)
#- --> 33900
ecmcConfigOrDie "Cfg.EcAddSdo(${ECMC_EC_SLAVE_NUM},0x8010,0x19,33900,4)"

#- 0x9009 0x07 Effective holding current (mA)
#- --> 4800
ecmcConfigOrDie "Cfg.EcAddSdo(${ECMC_EC_SLAVE_NUM},0x8011,0x11,4800,4)"
#- 0x9009 0x08 Effective rated current (mA)
#- --> 4650
ecmcConfigOrDie "Cfg.EcAddSdo(${ECMC_EC_SLAVE_NUM},0x8011,0x12,4650,4)"
#- 0x9009 0x06 Number of pole pair
#- --> 3
ecmcConfigOrDie "Cfg.EcAddSdo(${ECMC_EC_SLAVE_NUM},0x8011,0x13,3,1)"
#-
#- Commutation offset = -90 (reset by auto-configuration)
ecmcConfigOrDie "Cfg.EcAddSdo(${ECMC_EC_SLAVE_NUM},0x8011,0x15,-90,2)"

#- 0x9009 0x0E Torque constant (mNm/A)
#- --> 108
ecmcConfigOrDie "Cfg.EcAddSdo(${ECMC_EC_SLAVE_NUM},0x8011,0x16,108,4)"
#- 0x9009 0x14 Mass moment of inertia (g cm^2)
#- --> 94
ecmcConfigOrDie "Cfg.EcAddSdo(${ECMC_EC_SLAVE_NUM},0x8011,0x18,94,4)"
#- 0x9009 0x11 Inductance in the direction of flow (0.1 mH)
#- --> 9
ecmcConfigOrDie "Cfg.EcAddSdo(${ECMC_EC_SLAVE_NUM},0x8011,0x19,9,2)"
#- 0x9009 0x18 Thermal time constant of the motor (s)
#- --> 6000
ecmcConfigOrDie "Cfg.EcAddSdo(${ECMC_EC_SLAVE_NUM},0x8011,0x2d,6000,2)"

#- 0x9009 0x13 Maximum speed (rpm)
#- --> 10000 (reset by auto-configuration to 3885)
ecmcConfigOrDie "Cfg.EcAddSdo(${ECMC_EC_SLAVE_NUM},0x8011,0x1b,3885,4)"
#-
#- Current loop integral time = 5 (reset by auto-configuration to 5)
ecmcConfigOrDie "Cfg.EcAddSdo(${ECMC_EC_SLAVE_NUM},0x8010,0x12,5,2)"
#- Current loop proportianal gain = 106 (reset by auto-configuration to 106)
ecmcConfigOrDie "Cfg.EcAddSdo(${ECMC_EC_SLAVE_NUM},0x8010,0x13,106,2)"
#- Velocity loop integral time = 50 (reset by auto-configuration to 50)
ecmcConfigOrDie "Cfg.EcAddSdo(${ECMC_EC_SLAVE_NUM},0x8010,0x14,50,4)"
#- Velocity loop proportianal gain = 150 (reset by auto-configuration to 150)
ecmcConfigOrDie "Cfg.EcAddSdo(${ECMC_EC_SLAVE_NUM},0x8010,0x15,150,4)"

#- Index 9009 FB OCT Nameplate
#- 0x9009 0x01 Motor vendor
#- --> Beckhoff
#- 0x9009 0x02 Motor type
#- --> AM8113-xFx1
#- 0x9009 0x03 Serial number
#- --> 00316296
#- 0x9009 0x04 Order number
#- --> AM8113-0F21-0000
#- 0x9009 0x05 Type of motor
#- --> sync, rot
#- 0x9009 0x06 Number of pole pair
#- --> 3
#- 0x9009 0x07 Effective holding current (mA)
#- --> 4800
#- 0x9009 0x08 Effective rated current (mA)
#- --> 4650
#- 0x9009 0x09 Effective peak current (mA)
#- --> 18000
#- 0x9009 0x0A Effective nominal voltage (mV)
#- --> 33900
#- 0x9009 0x0B Maximum voltage (mV)
#- --> 96000
#- 0x9009 0x0C Maximum permissible voltage rise on the winding (kV/s)
#- --> 8000000
#- 0x9009 0x0D Maximum torque (nNm)
#- --> 205
#- 0x9009 0x0E Torque constant (mNm/A)
#- --> 108
#- 0x9009 0x0F Reverse voltage (mV/rpm)
#- --> 7
#- 0x9009 0x10 Coil resistance (mOhm)
#- --> 1450
#- 0x9009 0x11 Inductance in the direction of flow (0.1 mH)
#- --> 9
#- 0x9009 0x12 Inductance in the torque-forming direction (0.1 mH)
#- --> 9
#- 0x9009 0x13 Maximum speed (rpm)
#- --> 10000
#- 0x9009 0x14 Mass moment of inertia (g cm^2)
#- --> 94
#- 0x9009 0x15 Motor temperature warning threshold (0.1 °C)
#- --> 1200
#- 0x9009 0x16 Motor temperature error threshold (0.1 °C)
#- --> 1400
#- 0x9009 0x17 Time constant I2T model (s)
#- --> 531
#- 0x9009 0x18 Thermal time constant of the motor (s)
#- --> 6000
#- 0x9009 0x1B Brake type
#- --> holding brake
#- 0x9009 0x1C Minimum brake voltage (mV)
#- --> 21600
#- 0x9009 0x1D Maximum brake voltage (mV)
#- --> 25400
#- 0x9009 0x1E Minimum current for the monitoring of the brake (mA)
#- --> 181
#- 0x9009 0x1F Brake holding torque (mNm)
#- --> 600
#- 0x9009 0x20 Time until the brake is applied (ms)
#- --> 14
#- 0x9009 0x21 Time until the brake is released (ms)
#- --> 8
#- 0x9009 0x22 Reduced brake voltage (mV)
#- --> 0
#- 0x9009 0x23 Time from which the brake holds with reduced voltage (ms)
#- --> 3000
#- 0x9009 0x24 Temperature sensor connection
#- --> ---
