from enum import Enum

class Parameters(Enum, str):
    LOWER_RATE_LIMIT = "lowerRateLimit"
    UPPER_RATE_LIMIT = "upperRateLimit"
    ATRIAL_AMPLITUDE = "atrialAmplitude"
    ATRIAL_PULSE_WIDTH = "atrialPulseWidth"
    ATRIAL_REFACTORY_PERIOD = "atrialRefractoryPeriod"
    VENTRICULAR_AMPLITUDE = "ventricularAmplitude"
    VENTRICULAR_PULSE_WIDTH = "ventricularPulseWidth"
    VENTRICULAR_REFACTORY_PERIOD = "ventricularRefractoryPeriod"

# Pacing Modes

class PacingModes(Enum, list[Parameters]):
       '''
       _XXX = [Parameters.LOWER_RATE_LIMIT,\
              Parameters.UPPER_RATE_LIMIT,\
       ]

       AOO = _XXX.extend([
                       ])

       AAI = AOO.extend([
                       ])

       VOO = [Parameters.LOWER_RATE_LIMIT,\
              Parameters.UPPER_RATE_LIMIT,\
       ]

       VVI = [Parameters.LOWER_RATE_LIMIT,\
              Parameters.UPPER_RATE_LIMIT,\
       ]
       '''