from enum import Enum

# enum to denote the different types of error codes returned from the DB calls
class ErrorCodes(Enum):
    Duplicate = 1
    Unknown = 2
    NoError = 3
