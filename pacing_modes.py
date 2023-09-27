from enum import Enum

class Parameters(str, Enum):
    LOWER_RATE_LIMIT = "lowerRateLimit"
    UPPER_RATE_LIMIT = "upperRateLimit"
    ATRIAL_AMPLITUDE = "atrialAmplitude"
    ATRIAL_PULSE_WIDTH = "atrialPulseWidth"
    ATRIAL_REFACTORY_PERIOD = "atrialRefractoryPeriod"
    ATRIAL_SENSITIVITY = "atrialSensitivity"
    VENTRICULAR_AMPLITUDE = "ventricularAmplitude"
    VENTRICULAR_PULSE_WIDTH = "ventricularPulseWidth"
    VENTRICULAR_REFACTORY_PERIOD = "ventricularRefractoryPeriod"
    VENTRICULAR_SENSITIVITY = "ventricularSensitivity"
    PVARP = "PVARP"
    HYSTERESIS = "hysteresis"
    RATE_SMOOTHING = "rateSmoothing"

# Pacing Modes

class PacingModes(list[Parameters], Enum):

       AOO = [
              Parameters.LOWER_RATE_LIMIT,\
              Parameters.UPPER_RATE_LIMIT,\
              Parameters.ATRIAL_AMPLITUDE,\
              Parameters.ATRIAL_PULSE_WIDTH, \
       ]

       AAI = [
             Parameters.LOWER_RATE_LIMIT,\
              Parameters.UPPER_RATE_LIMIT,\
              Parameters.ATRIAL_AMPLITUDE,\
              Parameters.ATRIAL_PULSE_WIDTH,\
              Parameters.ATRIAL_SENSITIVITY,\
              Parameters.ATRIAL_REFACTORY_PERIOD,\
              Parameters.PVARP,\
              Parameters.HYSTERESIS,\
              Parameters.RATE_SMOOTHING \
       ]

       VOO = [
              Parameters.LOWER_RATE_LIMIT,\
              Parameters.UPPER_RATE_LIMIT,\
              Parameters.VENTRICULAR_AMPLITUDE,\
              Parameters.VENTRICULAR_PULSE_WIDTH \
       ]

       VVI = [
             Parameters.LOWER_RATE_LIMIT,\
              Parameters.UPPER_RATE_LIMIT,\
              Parameters.VENTRICULAR_AMPLITUDE,\
              Parameters.VENTRICULAR_PULSE_WIDTH,\
              Parameters.VENTRICULAR_SENSITIVITY,\
              Parameters.VENTRICULAR_REFACTORY_PERIOD,\
              Parameters.HYSTERESIS,\
              Parameters.RATE_SMOOTHING \
       ]
       