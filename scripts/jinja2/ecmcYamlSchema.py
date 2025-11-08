supportedAxisTypes = {
    '0': 0,
    'debug': 0,
    '1': 1,
    'j': 1,
    'joint': 1,
    'physical': 1,
    'motor': 1,
    'real': 1,
    '2': 2,
    'e': 2,
    'ee': 2,
    'end_effector': 2,
    'endeffector': 2,
    'virtual': 2,
}


class Schema:
    axisSchemaDict = {
        0: None,
        1: ['var',
            'axis',
            'epics',
            'encoder',
            'drive',
            'controller',
            'trajectory',
            'input',
            'axisPlc',
            'homing',
            'softlimits',
            'monitoring',
            'meta'],
        2: ['var',
            'axis',
            'epics',
            'encoder',
            'trajectory',
            'input',
            'axisPlc',
            'homing',
            'softlimits',
            'monitoring',
            'meta']
    }

    """
    schema for PLCs
    WARNING: The PLC schema _must_ be the FIRST entry of the list!!!
    """
    plcSchemaDict = {
        0: None,
        1: ['plc'],
        2: ['axisPlc', 'axis', 'encoder', 'trajectory', 'var']
    }

    encSchemaDict = {
        0: ['encoder']
    }

    def get_schema(self, keys):
        _type = type(keys)
        if _type is list:
            return {key: self.grandSchema[key] for key in keys}
        elif _type is str:
            return {keys: self.grandSchema[keys]}
        else:
            raise NotImplementedError(f'unsupported input type >>{_type}<<')

    metaSchema = {
        'type': 'dict',
        'default': {},
        'schema': {
            'author': {'type': 'string'},
            'facility': {'type': 'string', 'default': 'SLS 2.0'},
            'device': {'type': 'string'},
            'date': {'type': 'string'},
            'md5': {'type': 'string'},
        }
    }

    plcVeloFilterSchema = {
        'type': 'dict',
        'required': False,
        'default': {},
        'schema': {
            'trajectory': {
                'type': 'dict',
                'schema': {
                    'enable': {'required': False, 'type': 'boolean'},
                    'size': {'required': False, 'type': 'integer'}
                }
            },
            'encoder': {
                'type': 'dict',
                'schema': {
                    'enable': {'required': False, 'type': 'boolean'},
                    'size': {'required': False, 'type': 'integer'}
                }
            }
        }
    }

    filterSchema = {
        'type': 'dict',
        'required': False,
        'default': {},
        'schema': {
            'velocity': {
                'type': 'dict',
                'schema': {
                    'enable': {'required': False, 'type': 'boolean'},
                    'size': {'required': False, 'type': 'integer'}
                }
            },
            'trajectory': {
                'type': 'dict',
                'schema': {
                    'enable': {'required': False, 'type': 'boolean'},
                    'size': {'required': False, 'type': 'integer'}
                }
            },
            'position': {
                'type': 'dict',
                'schema': {
                    'enable': {'required': False, 'type': 'boolean'},
                    'size': {'required': False, 'type': 'integer'}
                }
            }
        }
    }

    homingSchema = {
        'type': 'dict',
        'required': False,
        'schema': {
            'type': {'type': 'integer', 'allowed': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 15, 21, 22, 25, 26]},
            'position': {'oneof': [
                {'type': 'float'},
                {'type': 'string', 'regex': '^\$(\{|\()\w*(=\d*(\.\d*)?)?(\}|\))$'}
            ]
            },
            'postMoveEnable': {'type': 'boolean', 'dependencies': ['postMovePosition']},
            'postMovePosition': {'oneof': [
                {'type': 'float'},
                {'type': 'string', 'regex': '^\$(\{|\()\w*(=\d*(\.\d*)?)?(\}|\))$'}
            ]
            },
            'latchCount': {'type': 'integer', 'min': 0},
            'velocity': {
                'type': 'dict',
                'schema': {
                    'to': {'type': 'float'},
                    'from': {'type': 'float'},
                }
            },
            'acceleration': {'type': 'float'},
            'deceleration': {'type': 'float'},
            'timeout': {'type': 'integer'},
            'refToEncIDAtStartup': {'type': 'integer', 'default': -1},
            'refAtHome': {'type': 'integer', 'default': 0},
            'tolToPrim': {'type': 'float', 'default': 0},
            'trigg': {'type': 'string'},
            'ready': {'type': 'string'},
        }
    }

    axisSchema = {
        'type': 'dict',
        'required': True,
        'schema': {
            'id': {'oneof': [
                {'type': 'integer'},
                {'type': 'string', 'regex': '^\$(\{|\()\w*(=\d*)?(\}|\))$'}
            ],
            'description': 'unique axis identifier'
            },
            'type': {'type': 'integer', 'default': 'joint',
                     'coerce': lambda v: supportedAxisTypes[str(v).lower().replace(" ", "")]},
            'mode': {'type': 'string', 'default': 'CSV', 'allowed': ['CSV', 'CSP', 'CSP_PC'], 'coerce': lambda v: v.upper()},
            'parameters': {'type': 'string'},
            'healthOutput': {'type': 'string'},
            'feedSwitchesOutput': {'type': 'string',
                'description': 'EtherCAT entry to control feed switches'},
            'feedSwitchesValue': {'type': 'integer',
                'description': 'Value to enable feed switches'},
            'group': {'type': 'string',
                'description': 'Add axis to group (group will be created if not exists), group id will be stored in GRP<axis.group>_ID for later use.'},
            'tweakDist': {'type': 'float', 'default': 1.0,
                'description': 'Tweak value (both ecmc interface and motor record tweak value)'},
            'autoEnable': {'type': 'dict', 'schema': {
                'enableTimeout': {'type': 'float', 'default': -1.0,
                    'description': 'If defined, ecmc tries to auto-enable for a maximum enableTimeout seconds.'},
                'disableTimeout': {'type': 'float','default': -1.0,
                    'description': 'If defined, ecmc disables axis after idle (non busy) in disableTime seconds.'},
                'atStartup': {'type': 'boolean','default': False,
                    'description': 'Auto enable axis at ioc start.'}
                },
                'description': 'ecmc auto enable of axis (Please use this instead of motor record version..)'
            },
            'autoMode': {'type': 'dict','schema': {
                'modeSet': {'type': 'string',
                    'description': 'Ethercat entry drive mode write (set CSV,CSP,homing)'},
                'modeAct': {'type': 'string',
                    'description': 'Ethercat entry drive mode reading (set CSV,CSP,homing)'},
                'modeCmdMotion': {'type': 'integer',
                    'description': 'Drive mode value for normal motion (written to axis.autoMode.modeSet when normal motion)'},
                'modeCmdHome': {'type': 'integer',
                    'description': 'Drive mode value for when homing (written to axis.drvMode.modeSet when homing)'},
                },
                'description': 'Switch drive modes automaticaly for normal motion and homing (smaract for instance)'
            },
            'features': {'type': 'dict', 'schema': {
                'disableOnReset': {'type': 'boolean',
                    'description': '???'},
                'alarmAtHardLimits': {'type': 'boolean',
                    'description': '???'},
                'blockCom': {'type': 'boolean',
                    'description': 'Block communication to axis'},
                'allowSrcChangeWhenEnabled': {'type': 'boolean',
                    'description': 'Allow traj/enc source change when axis is enabled'},
                'allowedFunctions': {'type': 'dict', 'schema': {
                    'positioning': {'type': 'boolean',
                        'description': 'Allow positioning'},
                    'constantVelocity': {'type': 'boolean',
                        'description': 'Allow constant velocity'},
                    'homing': {'type': 'boolean',
                        'description': 'Allow homing'}
                }}
            }}
        }
    }

    varSchema = {
        'type': 'dict',
        'required': False
    }

    epicsSchema = {
        'type': 'dict',
        'required': False,
        'default': {'name': 'axis'},
        'schema': {
            'name': {'default': 'axis',
                'description': 'Axis name'},
            'precision': {'type': 'integer', 'min': 0, 'default': 3,
                'description': 'Decimal count'},
            'unit': {'type': 'string', 'default': 'mm',
                'description': 'Unit'},
            'motorRecord': {
                'type': 'dict',
                'default': {'enable': True},
                'schema': {
                    'enable': {'type': 'boolean', 'default': True,
                        'description': 'Load motor record'},
                    'fieldInit': {'type': 'string',
                        'description': 'Additional motor record field initializations'},
                    'description': {'type': 'string',
                        'description': 'Motor record DESC field'},
                    'pvt': {
                        'type': 'dict',
                        'schema': {
                        'npoints': {'default': 0,
                            'description': '???'},
                        'nreadback': {'default': 0,
                            'description': '???'},
                        }
                    },
                    'syncSoftLimits': {'type': 'boolean', 'default': False,
                        'description': 'Sync softlimits between motor and ecmc'},
                }
            }
        }
    }

    driveSchema = {
        'type': 'dict',
        'required': True,
        'schema': {
            'numerator': {'type': 'float', 'default': 0,
                'description': 'Fastest speed in engineering units'},
            'denominator': {'type': 'integer', 'default': 1, 'min': 1,
                'description': 'I/O range for ECMC_EC_ALIAS_DRV_VELO_SET'},
            'type': {'type': 'integer', 'default': 0, 'allowed': [0, 1],
                'description': 'Stepper: 0. DS402: 1 (DS402 = servos and advanced stepper drives)'},
            'setpoint': {'required': True, 'type': 'string',
                'description': 'Velocity setpoint if CSV. Position setpoint if CSP.'},
            'control': {'required': True, 'type': 'string',
                'description': 'EtherCAT entry for control word'},
            'status': {'type': 'string',
                'description': 'EtherCAT entry for status word'},
            'reduceTorqueEnable': {'type': 'boolean', 'dependencies': ['control', 'reduceTorque'],
                'description': 'Enable reduce torque functionality'},
            'reduceTorque': {'type': 'integer', 'min': 0, 'dependencies': ['control', 'reduceTorqueEnable'],
                'description': 'Reduce torque bit in drive control word'},
            'enable': {'type': 'integer', 'min': 0, 'dependencies': ['control'],
                'description': 'Enable bit index in control word (not used if DS402)'},
            'enabled': {'type': 'integer', 'min': 0, 'dependencies': ['status'],
                'description': 'Enabled bit index in status word (not used if DS402)'},
            'brake': {
                'type': 'dict',
                'schema': {
                    'enable': {'required': True, 'type': 'boolean',
                        'description': 'Enable brake control'},
                    'output': {'required': True, 'type': 'string',
                        'description': 'EtherCAT entry to control brake'},
                    'openDelay': {'type': 'integer', 'min': 0, 'default': 0,
                        'description': 'number of cycles to wait after enable to disengage the brake'},
                    'closeAhead': {'type': 'integer', 'min': 0, 'default': 0,
                        'description': 'number of cycles to wait after the brake was engaged'},
                }
            },
            'warning': {'type': 'integer', 'min': 0, 'dependencies': ['status'],
                'description': 'status word bit for drive warning'},
            'reset': {'type': 'integer', 'min': 0, 'dependencies': ['control'],
                'description': 'control word bit to reset the drive'},
            'error': {'type': 'list', 'maxlength': 3, 'schema': {'anyof_type': ['integer', 'string']}, 'dependencies': ['status'],
                'description': 'list of status bits for drive errors'},
        }
    }

    encoderSchema = {
        'type': 'dict',
        'required': True,
        'schema': {
            'source': {'type': 'integer', 'allowed': [0, 1], 'default': 0,
                'description': '0 = Encoder value from etehrcat hardware, 1 = Encoder value from PLC'},
            'numerator': {'oneof': [
                {'type': 'float'},
                {'type': 'string', 'regex': '^\$(\{|\()\w*(=\d*(\.\d*)?)?(\}|\))$'}
                ], 'default': 0.0,
                'description': 'Scaling numerator'
            },
            'denominator': {'type': 'integer', 'default': 1, 'min': 1,
                'description': 'Scaling denominator'},
            'type': {'type': 'integer', 'allowed': [0, 1], 'default': 0,
                'description': 'Type: 0=Incremental, 1=Absolute'},
            'mask': {'type': 'string',
                'description': '???'},
            'bits': {'type': 'integer', 'min': 0, 'max': 64, 'default': 16,
                'description': 'Total bit count of encoder raw data'},
            'absBits': {'type': 'integer', 'min': 0, 'max': 64, 'default': 25,
                'description': 'Absolute bit count (for absolute encoders) always least significant part of "bits"'},
            'absOffset': {'oneof': [
                {'type': 'float'},
                {'type': 'string', 'regex': '^\$(\{|\()\w*(=\d*(\.\d*)?)?(\}|\))$'}
                ], 'default': 0.0,
                'description': 'Encoder offset in engineering units (for absolute encoders)'
            },
            'lookuptable': {
                'type': 'dict',
                'schema': {
                    'filename': {'required': True, 'type': 'string',
                        'description': 'Load correction lockuptable file (default enabled if loaded)'},
                    'range': {'type': 'float',
                        'description': '???'},
                    'scale': {'type': 'float',
                        'description': '???'},
                    'enable': {'type': 'boolean',
                        'description': 'Enable lookup table correction'}
                }
            },
            'unit': {'type': 'string',
                'description': 'Unit'},
            'delayComp': {
                'type': 'dict',
                'schema': {
                    'time': {'required': True, 'type': 'float',
                        'description': 'Delay time between set and act [cycles]'},
                    'enable': {'type': 'boolean',
                        'description': 'enable (defaults to 1 if not set)'},
                },
                'description': 'Delay compensation for time between application of setpoint to reading of encoder (normally atleast 1 cycle)'
            },
            'desc': {'type': 'string'},
            'position': {'type': 'string',
                'description': 'Ethercat entry for actual position input'},
            'control': {'type': 'string',
                'description': 'EtherCAT entry for encoder control word'},
            'status': {'type': 'string',
                'description': 'EtherCAT entry for encoder status word'},
            'warning': {'type': 'integer', 'min': 0, 'dependencies': ['status'],
                'description': 'Status word bit for encoder warning'},
            'ready': {'type': 'integer', 'min': 0, 'dependencies': ['status'],
                'description': 'Status word bit for encoder ready'},
            'reset': {'type': 'integer', 'min': 0, 'dependencies': ['control'],
                'description': 'Control word bit to reset the encoder'},
            'error': {'type': 'list', 'maxlength': 3, 'schema': {'anyof_type': ['integer', 'string']}, 'dependencies': ['status'],
                'description': 'List of status bits for encoder errors'},
            'filter': filterSchema,
            'latch': {
                'type': 'dict',
                'schema': {
                    'position': {'required': True, 'type': 'string',
                        'description': '???'},
                    'control': {'type': 'integer', 'default': 0,
                        'description': 'Control word bit to arm latch. Used for some homing seqs'},
                    'armCmd': {'type': 'integer', 'default': 1,
                        'description': 'Value in dec to arm latch/touch probe'},
                    'armBits': {'type': 'integer', 'default': 1,
                        'description': 'Bit size of encoder.latch.armCmd'},
                    'status': {'type': 'integer', 'default': 0},
                }
            },
            'primary': {'type': ['boolean', 'integer'],
                'description': 'Use this encoder as primary (for control)'},
            'homing': homingSchema,
            'useAsCSPDrvEnc': {'type': ['boolean', 'integer' ],
                'description': 'Use this encoder as CSP drive encoder (ecmc controller enabled in CSP)'},
        }
    }

    controllerSchema = {
        'type': 'dict',
        'required': False,
        'default': {'controller': {'Kp': 1}},
        'schema': {
            'Kp': {'type': 'float', 'default': 1., 'min': 0},
            'Ki': {'type': 'float', 'default': 0., 'min': 0},
            'Kd': {'type': 'float', 'default': 0., 'min': 0},
            'Kff': {'type': 'float', 'default': 1., 'min': 0},
            'inner': {
                'type': 'dict',
                'required': False,
                'schema': {
                    'Kp': {'type': 'float', 'default': 1., 'min': 0},
                    'Ki': {'type': 'float', 'default': 0., 'min': 0},
                    'Kd': {'type': 'float', 'default': 0., 'min': 0},
                    'tol': {'type': 'float', 'default': 0., 'min': 0},
                }
            },
            'limits': {
                'type': 'dict',
                'required': False,
                'schema': {
                    'minOutput': {'type': 'float'},
                    'maxOutput': {'type': 'float'},
                    'minIntegral': {'type': 'float'},
                    'maxIntegral': {'type': 'float'},
                }
            },
            'deadband': {
                'type': 'dict',
                'required': False,
                'schema': {
                    'tol': {'type': 'float', 'min': 0},
                    'time': {'type': 'integer', 'min': 0},
                }
            },
        }
    }

    trajectorySchema = {
        'type': 'dict',
        'required': True,
        'schema': {
            'source': {'type': 'integer', 'default': 0, 'allowed': [0, 1]},
            'type': {'type': 'integer', 'default': 0, 'allowed': [0, 1]},
            'axis': {
                'required': True,
                'type': 'dict',
                'schema': {
                    'velocity': {'required': True, 'type': 'float'},
                    'acceleration': {'required': True, 'type': 'float'},
                    'jerk': {'type': 'float'},
                    'deceleration': {'type': 'float'},
                    'emergencyDeceleration': {'type': 'float'}
                }
            },
            'jog': {
                'type': 'dict',
                'schema': {
                    'velocity': {'type': 'float'},
                    'acceleration': {'type': 'float'},
                }
            },
            'modulo': {
                'type': 'dict',
                'schema': {
                    'range': {'type': 'float', 'default': 0.},
                    'type': {'type': 'integer', 'default': 0, 'allowed': [0, 1, 2, 3]}
                }
            },
        }
    }

    inputSchema = {
        'type': 'dict',
        'required': True,
        'schema': {
            'limit': {
                'type': 'dict',
                'required': True,
                'schema': {
                    'forward': {'required': True, 'type': 'string'},
                    'forwardPolarity': {'type': 'integer', 'allowed': [0, 1]},
                    'backward': {'required': True, 'type': 'string'},
                    'backwardPolarity': {'type': 'integer', 'allowed': [0, 1]},
                    'latchInput': {'type': 'boolean'}
                }
            },
            'home': {'required': False, 'type': 'string'},
            'homePolarity': {'type': 'integer', 'allowed': [0, 1]},
            'interlock': {'required': False, 'type': 'string'},
            'interlockPolarity': {'type': 'integer', 'allowed': [0, 1]},
            'analog': {
                'type': 'dict',
                'required': False,
                'schema': {
                    'interlock': {'required': False, 'type': 'string'},
                    'rawLimit': {'required': False, 'type': 'float'},
                    'interlockPolarity': {'required': False, 'type': 'integer', 'allowed': [0, 1]},
                    'enable': {'required': False, 'type': 'boolean'},
                }
            },
        }
    }

    axisPlcSchema = {
        'type': 'dict',
        'required': False,
        'schema': {
            'enable': {'required': True, 'type': 'boolean'},
            'externalCommands': {'type': 'boolean'},
            'filter': filterSchema,
            'velocity_filter': plcVeloFilterSchema,
            'file': {'type': 'string'},
            'macros': {'type': 'string'},
            'code': {'type': 'list', 'schema': {'type': 'string'}},
        }
    }

    plcSchema = {
        'type': 'dict',
        'required': True,
        'schema': {
            'id': {'required': True, 'type': 'integer'},
            'enable': {'type': 'boolean'},
            'rateMilliseconds': {'type': 'integer'},
            'file': {'type': 'string'},
            'macros': {'type': 'string'},
            'code': {'type': 'list', 'schema': {'type': 'string'}},
        }
    }

    softlimitsSchema = {
        'type': 'dict',
        'required': False,
        'default': {'enable': False},
        'schema': {
            'enable': {'required': False, 'type': 'boolean'},
            'forwardEnable': {'type': 'boolean', 'dependencies': ['forward', 'enable']},
            'forward': {'type': 'float', 'dependencies': ['forwardEnable']},
            'backwardEnable': {'type': 'boolean', 'dependencies': ['backward', 'enable']},
            'backward': {'type': 'float', 'dependencies': ['backwardEnable']},
        }
    }

    monitoringSchema = {
        'type': 'dict',
        'required': False,
        'schema': {
            'lag': {
                'type': 'dict',
                'required': False,
                'default': {'enable': False, 'tolerance': 0.0, 'time': 100},
                'schema': {
                    'enable': {'required': True, 'type': 'boolean', 'dependencies': ['tolerance', 'time']},
                    'tolerance': {'type': 'float', 'min': 0.0},
                    'time': {'type': 'integer', 'min': 0},
                }
            },
            'target': {
                'type': 'dict',
                'required': False,
                'schema': {
                    'enable': {'required': True, 'type': 'boolean', 'dependencies': ['tolerance', 'time']},
                    'tolerance': {'type': 'float', 'min': 0.0},
                    'time': {'type': 'integer', 'min': 0},
                }
            },
            'velocity': {
                'type': 'dict',
                'required': False,
                'schema': {
                    'enable': {'required': True, 'type': 'boolean', 'dependencies': ['max', 'time']},
                    'max': {'type': 'float', 'min': 0.0},
                    'time': {
                        'type': 'dict',
                        'schema': {
                            'trajectory': {'required': True, 'type': 'integer', 'min': 0},
                            'drive': {'type': 'integer', 'min': 0},
                        }
                    },
                }
            },
            'velocityDifference': {
                'type': 'dict',
                'required': False,
                'schema': {
                    'enable': {'required': True, 'type': 'boolean', 'dependencies': ['max', 'time']},
                    'max': {'type': 'float', 'min': 0.0},
                    'time': {
                        'type': 'dict',
                        'schema': {
                            'trajectory': {'required': True, 'type': 'integer', 'min': 0},
                            'drive': {'type': 'integer', 'min': 0},
                        }
                    },
                }
            },
            'stall': {
                'type': 'dict',
                'required': False,
                'schema': {
                    'enable': {'type': 'boolean'},
                    'time': {
                        'type': 'dict',
                        'schema': {
                            'timeout': {'type': 'integer', 'min': 0},
                            'factor': {'type': 'float', 'min': 0},
                        }
                    },
                }
            },
        }
    }

    grandSchema = {
        'var': varSchema,
        'axis': axisSchema,
        'epics': epicsSchema,
        'encoder': encoderSchema,
        'drive': driveSchema,
        'controller': controllerSchema,
        'trajectory': trajectorySchema,
        'input': inputSchema,
        'axisPlc': axisPlcSchema,
        'plc': plcSchema,
        'homing': homingSchema,
        'softlimits': softlimitsSchema,
        'monitoring': monitoringSchema,
        'meta': metaSchema
    }
