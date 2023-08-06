from time import sleep
from typing import Final, Type, TypeVar

from serial.serialposix import Serial
from tabulate import tabulate

CMD_RESET: Final = 0x44
CMD_STATUS: Final = 0x50
CMD_PURGE: Final = 0x51
CMD_DISPENSE: Final = 0x52
CMD_TEST_DISPENSE: Final = 0x53
CMD_LAST_STATUS: Final = 0x55
CMD_SENSOR_DIAGNOSTICS: Final = 0x58
CMD_SET_BILL_OPACITIES: Final = 0x5A
CMD_GET_BILL_OPACITIES: Final = 0x5B
CMD_SET_BILL_DISPENSE_ORDER: Final = 0x5C
CMD_GET_BILL_DISPENSE_ORDER: Final = 0x5D
CMD_SET_BILL_LENGTHS: Final = 0x5E
CMD_GET_BILL_LENGTHS: Final = 0x5F

NO_ERROR = 0x20

ACK_TIMEOUT = 0xF1
RESPONSE_TIMEOUT = 0xF2
UNKNOWN_ERROR = 0xFF

ERROR_CODES = {
    0x01: 'Bill Pick Up Error',
    0x02: 'Jam on the path between CHK Sensor and DVT Sensor',
    0x03: 'Jam on the path between DVT Sensor and EJT Sensor',
    0x04: 'Jam on the path between EJT Sensor and EXIT Sensor',
    0x05: 'A note Staying in EXIT Sensor',
    0x06: 'Ejecting the note suspected as rejected',
    0x07: 'Abnormal note management (Flow Processing Error Inside)',
    0x08: 'Abnormal note management (Flow Processing Error Inside)',
    0x09: 'Abnormal note management (Flow Processing Error Inside)',
    0x0A: 'Abnormal note management (Flow Processing Error Inside)',
    0x0B: 'Detecting notes on the path before start of pick-up',
    0x0C: 'Dispensing too many notes for one transaction (Default limit: 100 notes including the rejected)',
    0x0D: 'Rejecting too many notes for one transaction (Default limit: 10 notes)',
    0x0E: 'Abnormal termination during purge operation',
    0x20: 'Detecting sensor trouble or abnormal material before start',
    0x21: 'Detecting sensor trouble or abnormal material before start',
    0x22: 'Detecting trouble of solenoid operation before dispense',
    0x23: 'Detecting trouble in motor or slit sensor before dispense',
    0x24: 'Detecting no cassette requested to dispense bills',
    0x25: 'Detecting NEAREND status in the cassette requested to dispense (When NEAREND detection mode is turned on)',
    0x26: 'Detecting no reject tray before start or for operation',
    0x30: 'Recognizing abnormal command',
    0x31: 'Recognizing abnormal parameter on the command',
    ACK_TIMEOUT: 'ACK timed out',
    RESPONSE_TIMEOUT: 'Response timed out',
    UNKNOWN_ERROR: 'Unknown Error',
}


class CommandMessage:
    """
    Message protocol is dependent on Command and Response of message and
    has a little difference up to the function with specific format.

    BCC can be gotten through exclusive or (XOR) from the start of each message to ETX except BCC.
    """

    EOT: Final[int] = 0x04  # Start of Transmission.
    ID: Final[int] = 0x30  # Communications ID.
    STX: Final[int] = 0x02  # Start of Text.
    CMD: int  # Status Command.
    ...  # Command Parameter (Variable Length).
    ETX: Final[int] = 0x03  # End of Text.
    BCC: int  # Block Check Character.

    _response_size: int = 6

    def __init__(self, *_):
        self._compute_bcc()

    def _compute_bcc(self, *args: int):
        self.BCC = self.EOT
        for data in (self.ID, self.STX, self.CMD, *args, self.ETX):
            self.BCC = self.BCC ^ data

    def _bytes(self, *data: int):
        return ''.join(
            chr(d) for d in (self.EOT, self.ID, self.STX, self.CMD, *data, self.ETX, self.BCC,)
        ).encode('ascii')

    def bytes(self):
        return self._bytes()

    def response_size(self):
        return self._response_size


class ResponseMessage:
    SOH: Final[int] = 0x01  # Start of Header
    ID: Final[int] = 0x30  # Communications ID
    STX: Final[int] = 0x02  # Start of Text
    RSP: int  # Status Command
    ERROR: int  # Error Status for Operation
    ...  # Response Parameter (Variable Length)
    ETX: Final[int] = 0x03  # End of Text
    BCC: int  # Block Check Character

    _origin: tuple[int]

    def __init__(self, *response: int):
        self._origin = response
        self._compute_bcc()

    def _compute_bcc(self, *args: int):
        self.BCC = self.SOH
        for data in (self.ID, self.STX, self.RSP, *args, self.ETX):
            self.BCC = self.BCC ^ data

    def is_valid(self):
        return len(self._origin) > 0 and self.BCC == self._origin[-1]

    def __repr__(self) -> str:
        return tabulate(
            ((k, hex(v)) for k, v in self.__dict__.items() if type(v) == int),
            headers=('Name', 'Code'),
            colalign=('left', 'right'),
            tablefmt="pretty"
        )


class ResetCommand(CommandMessage):
    """
    The reset will cause the dispenser reset by software. Therefore, there is no response for this command.
    (Cf.) When RESET is transmitted, it would take 2 seconds for dispenser to initialize all status.
    Therefore, the next command would be sent after the initialization.
    """
    CMD = CMD_RESET
    _response_size = 0


class StatusCommand(CommandMessage):
    """This command shows the current sensor status and the configuration of cassette in the top position."""
    CMD = CMD_STATUS
    _response_size = 6 + 2 + 4 * 4


# DISP Description
# 0 Sensor DVTL is Blocked and Off.
# 1 Sensor DVTR is Blocked and Off.
# 2 Sensor EJT is Blocked and Off.
# 3 Sensor EXIT is Blocked and Off.
# 4 Sensor RJT is Blocked and Off.

class StatusResponse(ResponseMessage):
    RSP = CMD_STATUS
    ERROR: int  # Error Status for Operation
    DISP: int  # Status for Dispenser
    STAT1: int  # Status of Cassette in Top Pick Position
    TYPE1: int  # Type of Cassette in Top Pick Position 0x30: Cassette is removed. 0x31: Cassette exists.
    OPAC1: int  # Thickness Reference Value of Bills in Cassette in Top Pick Position. Value +0x20
    LENG1: int  # Length Reference Value of Bills in Cassette in Top Pick Position. Value +0x20
    STAT2: int  # Status of Cassette in Second Top Pick Position
    TYPE2: int  # Type of Cassette in the Second Top Pick Position. 0x30: Cassette is removed. 0x32: Cassette exists.
    OPAC2: int  # Thickness Reference Value of Bills in Cassette in the Second Top Pick Position. Value +0x20
    LENG2: int  # Length Reference Value of Bills in Cassette in the Second Top Pick Position. Value +0x20
    STAT3: int  # Status of Cassette in Third Top Pick Position
    TYPE3: int  # Type of Cassette in the Third Top Pick Position. 0x30: Cassette is removed. 0x33: Cassette exists.
    OPAC3: int  # Thickness Reference Value of Bills in Cassette in the Third Top Pick Position. Value +0x20
    LENG3: int  # Length Reference Value of Bills in Cassette in the Third Top Pick Position. Value +0x20
    STAT4: int  # Status of Cassette in Bottom Pick Position
    TYPE4: int  # Type of Cassette in Bottom Pick Position. 0x30: Cassette is removed. 0x34: Cassette exists.
    OPAC4: int  # Thickness Reference Value of Bills in Cassette in Bottom Pick Position. Value +0x20
    LENG4: int  # Length Reference Value of Bills in Cassette in Bottom Pick Position. Value +0x20

    def __init__(self, *response: int):
        (
            self.ERROR, self.DISP,
            self.STAT1, self.TYPE1, self.OPAC1, self.LENG1,
            self.STAT2, self.TYPE2, self.OPAC2, self.LENG2,
            self.STAT3, self.TYPE3, self.OPAC3, self.LENG3,
            self.STAT4, self.TYPE4, self.OPAC4, self.LENG4
        ) = response[4:-2]
        super().__init__(*response)

    def _compute_bcc(self, *_):
        super()._compute_bcc(
            self.ERROR, self.DISP,
            self.STAT1, self.TYPE1, self.OPAC1, self.LENG1,
            self.STAT2, self.TYPE2, self.OPAC2, self.LENG2,
            self.STAT3, self.TYPE3, self.OPAC3, self.LENG3,
            self.STAT4, self.TYPE4, self.OPAC4, self.LENG4
        )


class PurgeCommand(CommandMessage):
    """
    PURGE will cause the dispenser to purge the transport of all bills from four cassettes and
    to move the bills in the path to the reject tray. This command will not be required for normal operation.
    However, in case of abnormal termination such as sudden power-off by external cause,
    the command will be useful to remove the notes.
    A successful PURGE operation will move any bills in the transport to the reject tray but
    if the note would be left in the EXIT area, it may be dispensed.

    PURGE will perform the repetitive routine of FORWARD/BACKWARD FEED itself and cause the damage to notes.
    It will not recover errors completely by JAM or already terminated DISP (dispense) command.
    Therefore, it is recommended to use carefully.
    """
    CMD = CMD_PURGE
    _response_size = 6 + 2 + 3 * 4


class PurgeResponse(ResponseMessage):
    RSP = CMD_PURGE
    ERROR: int  # Error Status for Operation
    MISS: int = 0x30  # Reserved
    EXIT1: int  # Number of Items Dispensed from Top Pick Module. Count +0x20
    REJECT1: int  # Number of Items Reject Event from Top Pick Module. Count +0x20
    TYPE1: int  # Type of Cassette in Top Pick Position. 0x30: Cassette is removed. 0x31: Cassette exists.
    EXIT2: int  # Number of Items Dispensed from Top Pick Module. Count +0x20
    REJECT2: int  # Number of Items Reject Event from Top Pick Module. Count +0x20
    TYPE2: int  # Type of Cassette in Top Pick Position. 0x30: Cassette is removed. 0x32: Cassette exists.
    EXIT3: int  # Number of Items Dispensed from Top Pick Module. Count +0x20
    REJECT3: int  # Number of Items Reject Event from Top Pick Module. Count +0x20
    TYPE3: int  # Type of Cassette in Top Pick Position. 0x30: Cassette is removed. 0x33: Cassette exists.
    EXIT4: int  # Number of Items Dispensed from Top Pick Module. Count +0x20
    REJECT4: int  # Number of Items Reject Event from Top Pick Module. Count +0x20
    TYPE4: int  # Type of Cassette in Top Pick Position. 0x30: Cassette is removed. 0x34: Cassette exists.

    def __init__(self, *response: int):
        (
            self.ERROR, _,
            self.EXIT1, self.REJECT1, self.TYPE1,
            self.EXIT2, self.REJECT2, self.TYPE2,
            self.EXIT3, self.REJECT3, self.TYPE3,
            self.EXIT4, self.REJECT4, self.TYPE4
        ) = response[4:-2]
        super().__init__(*response)

    def _compute_bcc(self, *_):
        super()._compute_bcc(
            self.ERROR, self.MISS,
            self.EXIT1, self.REJECT1, self.TYPE1,
            self.EXIT2, self.REJECT2, self.TYPE2,
            self.EXIT3, self.REJECT3, self.TYPE3,
            self.EXIT4, self.REJECT4, self.TYPE4
        )


class DispenseCommand(CommandMessage):
    """
    The command will cause to dispenser the requested number of notes from the requested cassette.
    It will check thickness and length of notes, which are individually referred to the specified OPACITY and LENGTH,
    and then decide whether the notes are dispensed or rejected. During the process,
    other parameters such as the required distance between notes and
    the skew of notes will give influence on dispensing and rejecting.

    The requested dispensing number of notes at maximum should not be over 100 sheets.
    """
    CMD = CMD_DISPENSE
    QTY1: int = 0x20  # The number of bills to be dispensed from cassette type1 + 0x20
    QTY2: int = 0x20  # The number of bills to be dispensed from cassette type2 + 0x20
    QTY3: int = 0x20  # The number of bills to be dispensed from cassette type3 + 0x20
    QTY4: int = 0x20  # The number of bills to be dispensed from cassette type4 + 0x20
    TO1: int = 0x20  # If timeout value isn't used, then 0x20. Else if it's used, the value is 0x1c. Default: 0x20
    TO2: int = 0x20  # If timeout value isn't used, then 0x20. Else if it's used, the value is 0x30~39. Default: 0x20
    RSV: int = 0x20  # Reserved (9 bytes)
    _response_size = 6 + 2 + 3 * 4 + 9

    def __init__(self, *args):
        (self.QTY1, self.QTY2, self.QTY3, self.QTY4, self.TO1, self.TO2) = \
            (args + (self.QTY1, self.QTY2, self.QTY3, self.QTY4, self.TO1, self.TO2)[len(args):])[:6]
        super().__init__(*args)

    def _compute_bcc(self, *_):
        super()._compute_bcc(self.QTY1, self.QTY2, self.QTY3, self.QTY4, self.TO1, self.TO2, *[self.RSV] * 9)

    def _bytes(self, *_):
        return super()._bytes(self.QTY1, self.QTY2, self.QTY3, self.QTY4, self.TO1, self.TO2, *[self.RSV] * 9)


class DispenseResponse(ResponseMessage):
    RSP = CMD_DISPENSE
    ERROR: int  # Error Status for Operation
    MISS: int = 0x30  # Reserved
    EXIT1: int  # Number of Items Dispensed from Top Pick Module. Count +0x20
    REJECT1: int  # Number of Items Reject Event from Top Pick Module. Count +0x20
    TYPE1: int  # Type of Cassette in Top Pick Position. 0x30: Cassette is removed. 0x31: Cassette exists.
    EXIT2: int  # Number of Items Dispensed from Top Pick Module. Count +0x20
    REJECT2: int  # Number of Items Reject Event from Top Pick Module. Count +0x20
    TYPE2: int  # Type of Cassette in Top Pick Position. 0x30: Cassette is removed. 0x32: Cassette exists.
    EXIT3: int  # Number of Items Dispensed from Top Pick Module. Count +0x20
    REJECT3: int  # Number of Items Reject Event from Top Pick Module. Count +0x20
    TYPE3: int  # Type of Cassette in Top Pick Position. 0x30: Cassette is removed. 0x33: Cassette exists.
    EXIT4: int  # Number of Items Dispensed from Top Pick Module. Count +0x20
    REJECT4: int  # Number of Items Reject Event from Top Pick Module. Count +0x20
    TYPE4: int  # Type of Cassette in Top Pick Position. 0x30: Cassette is removed. 0x34: Cassette exists.
    RSV: int = 0x20  # Reserved (9 bytes)

    def __init__(self, *response: int):
        (
            self.ERROR, _,
            self.EXIT1, self.REJECT1, self.TYPE1,
            self.EXIT2, self.REJECT2, self.TYPE2,
            self.EXIT3, self.REJECT3, self.TYPE3,
            self.EXIT4, self.REJECT4, self.TYPE4,
        ) = response[4:-2 - 9]
        super().__init__(*response)

    def _compute_bcc(self, *_):
        super()._compute_bcc(
            self.ERROR, self.MISS,
            self.EXIT1, self.REJECT1, self.TYPE1,
            self.EXIT2, self.REJECT2, self.TYPE2,
            self.EXIT3, self.REJECT3, self.TYPE3,
            self.EXIT4, self.REJECT4, self.TYPE4,
            *[self.RSV] * 9
        )


class TestDispenseCommand(DispenseCommand):
    """
    The command will cause to reject the specified number of notes from the cassette to the reject tray.
    All the specified notes will move into the reject tray.

    The requested dispensing number of notes at maximum should not be over 100 sheets.
    """
    CMD = CMD_TEST_DISPENSE


class TestDispenseResponse(DispenseResponse):
    RSP = CMD_TEST_DISPENSE


class LastStatusCommand(CommandMessage):
    """
    The command will request to resend the results to the last operation commands
    such as PURGE, DISPENSE and TEST DISPENSE.
    Therefore, it is effective only when the prior operation was performed.
    """
    CMD = CMD_LAST_STATUS
    _response_size = 6 + 3 + 3 * 4


class LastStatusResponse(ResponseMessage):
    RSP = CMD_LAST_STATUS
    LAST_CMD: int  # Reserved
    ERROR: int  # Error Status for Operation
    MISS: int = 0x30  # Reserved
    EXIT1: int  # Number of Items Dispensed from Top Pick Module. Count +0x20
    REJECT1: int  # Number of Items Reject Event from Top Pick Module. Count +0x20
    TYPE1: int  # Type of Cassette in Top Pick Position. 0x30: Cassette is removed. 0x31: Cassette exists.
    EXIT2: int  # Number of Items Dispensed from Top Pick Module. Count +0x20
    REJECT2: int  # Number of Items Reject Event from Top Pick Module. Count +0x20
    TYPE2: int  # Type of Cassette in Top Pick Position. 0x30: Cassette is removed. 0x32: Cassette exists.
    EXIT3: int  # Number of Items Dispensed from Top Pick Module. Count +0x20
    REJECT3: int  # Number of Items Reject Event from Top Pick Module. Count +0x20
    TYPE3: int  # Type of Cassette in Top Pick Position. 0x30: Cassette is removed. 0x33: Cassette exists.
    EXIT4: int  # Number of Items Dispensed from Top Pick Module. Count +0x20
    REJECT4: int  # Number of Items Reject Event from Top Pick Module. Count +0x20
    TYPE4: int  # Type of Cassette in Top Pick Position. 0x30: Cassette is removed. 0x34: Cassette exists.

    def __init__(self, *response: int):
        (
            self.LAST_CMD, self.ERROR, _,
            self.EXIT1, self.REJECT1, self.TYPE1,
            self.EXIT2, self.REJECT2, self.TYPE2,
            self.EXIT3, self.REJECT3, self.TYPE3,
            self.EXIT4, self.REJECT4, self.TYPE4,
        ) = response[4:-2]
        super().__init__(*response)

    def _compute_bcc(self, *_):
        super()._compute_bcc(
            self.LAST_CMD, self.ERROR, self.MISS,
            self.EXIT1, self.REJECT1, self.TYPE1,
            self.EXIT2, self.REJECT2, self.TYPE2,
            self.EXIT3, self.REJECT3, self.TYPE3,
            self.EXIT4, self.REJECT4, self.TYPE4,
        )


class SensorDiagnosticsCommand(CommandMessage):
    """
    The command will cause to dispense 5 notes from the designated cassette as if “TEST DISPENSE” will do.
    The notes are moved to reject tray and the measured OPACITY, LENGTH and SOLENOID TIME of the last note is returned.
    """
    CMD = CMD_SENSOR_DIAGNOSTICS
    POS: int  # The Designated Cassette for Dispensing (0x31: Top, ... 0x34: Bottom)
    _response_size = 6 + 5

    def __init__(self, *args):
        super().__init__(*args)
        assert len(args) > 0
        assert args[0] in (0x31, 0x32, 0x33, 0x34)
        self.POS = args[0]

    def _compute_bcc(self, *_):
        super()._compute_bcc(self.POS)

    def _bytes(self, *_):
        return super()._bytes(self.POS)


class SensorDiagnosticsResponse(ResponseMessage):
    RSP = CMD_SENSOR_DIAGNOSTICS
    ERROR: int  # Error Status for Operation
    OPAC: int  # OPACITY of the Last Picked Bill. Value +0x20
    LENG: int  # LENGTH of the Last Picked Bill. Count +0x20
    DIVERT: int  # The Solenoid Operation Time for the Diverter Enable (Unit: ms). Time +0x20
    REJECT: int  # Number of Reject Event. 0x20~

    def __init__(self, *response: int):
        (self.ERROR, self.OPAC, self.LENG, self.DIVERT, self.REJECT) = response[4:-2]
        super().__init__(*response)

    def _compute_bcc(self, *_):
        super()._compute_bcc(self.ERROR, self.OPAC, self.LENG, self.DIVERT, self.REJECT)


class SetBillOpacitiesCommand(CommandMessage):
    """
    The command is used to save the reference value in order to detect double notes.
    Each opacity value can be saved from 0x00 to 0xFF. The value, 0x00 means to maintain current data.
    When the data is changed, it will be saved in the memory of EEPROM and then efficient for the next transaction.
    In case of power on/off, the value continues to be used.
    However, when the electricity trouble causes the saved data damaged (wrong check sum on EEPROM),
    the criterion is set to initial value again.
    Therefore, it is recommended for user to check the value of the saved value of OPACITY when it is turned on.
    """
    CMD = CMD_SET_BILL_OPACITIES
    OPAC1_HIGH: int  # The high hexadecimal digit for the opacity of bills in top cassette. 0x30~0x3F
    OPAC1_LOW: int  # The low hexadecimal digit for the opacity of bills in top cassette. 0x30~0x3F
    OPAC2_HIGH: int  # The high hexadecimal digit for the opacity of bills in second top cassette. 0x30~0x3F
    OPAC2_LOW: int  # The low hexadecimal digit for the opacity of bills in second top cassette. 0x30~0x3F
    OPAC3_HIGH: int  # The high hexadecimal digit for the opacity of bills in third top cassette. 0x30~0x3F
    OPAC3_LOW: int  # The low hexadecimal digit for the opacity of bills in third top cassette. 0x30~0x3F
    OPAC4_HIGH: int  # The high hexadecimal digit for the opacity of bills in bottom cassette. 0x30~0x3F
    OPAC4_LOW: int  # The low hexadecimal digit for the opacity of bills in bottom cassette. 0x30~0x3F
    _response_size = 6 + 1

    def __init__(self, *args):
        assert len(args) >= 8
        (
            self.OPAC1_HIGH, self.OPAC1_LOW, self.OPAC2_HIGH, self.OPAC2_LOW,
            self.OPAC3_HIGH, self.OPAC3_LOW, self.OPAC4_HIGH, self.OPAC4_LOW
        ) = args[:8]
        super().__init__(*args)

    def _compute_bcc(self, *_):
        super()._compute_bcc(
            self.OPAC1_HIGH, self.OPAC1_LOW, self.OPAC2_HIGH, self.OPAC2_LOW,
            self.OPAC3_HIGH, self.OPAC3_LOW, self.OPAC4_HIGH, self.OPAC4_LOW
        )

    def _bytes(self, *_):
        return super()._bytes(
            self.OPAC1_HIGH, self.OPAC1_LOW, self.OPAC2_HIGH, self.OPAC2_LOW,
            self.OPAC3_HIGH, self.OPAC3_LOW, self.OPAC4_HIGH, self.OPAC4_LOW
        )


class SetBillOpacitiesResponse(ResponseMessage):
    RSP = CMD_SET_BILL_OPACITIES
    ERROR: int  # Error Status for Operation

    def __init__(self, *response: int):
        (self.ERROR,) = response[4:-2]
        super().__init__(*response)

    def _compute_bcc(self, *_):
        super()._compute_bcc(self.ERROR)


class GetBillOpacitiesCommand(CommandMessage):
    """The command will get the OPACITY data from each cassette."""
    CMD = CMD_GET_BILL_OPACITIES
    _response_size = 6 + 1 + 2 * 4


class GetBillOpacitiesResponse(ResponseMessage):
    RSP = CMD_GET_BILL_OPACITIES
    ERROR: int  # Error Status for Operation
    OPAC1_HIGH: int  # The high hexadecimal digit for the opacity of bills in top cassette. 0x30~0x3F
    OPAC1_LOW: int  # The low hexadecimal digit for the opacity of bills in top cassette. 0x30~0x3F
    OPAC2_HIGH: int  # The high hexadecimal digit for the opacity of bills in second top cassette. 0x30~0x3F
    OPAC2_LOW: int  # The low hexadecimal digit for the opacity of bills in second top cassette. 0x30~0x3F
    OPAC3_HIGH: int  # The high hexadecimal digit for the opacity of bills in third top cassette. 0x30~0x3F
    OPAC3_LOW: int  # The low hexadecimal digit for the opacity of bills in third top cassette. 0x30~0x3F
    OPAC4_HIGH: int  # The high hexadecimal digit for the opacity of bills in bottom cassette. 0x30~0x3F
    OPAC4_LOW: int  # The low hexadecimal digit for the opacity of bills in bottom cassette. 0x30~0x3F

    def __init__(self, *response: int):
        (
            self.OPAC1_HIGH, self.OPAC1_LOW, self.OPAC2_HIGH, self.OPAC2_LOW,
            self.OPAC3_HIGH, self.OPAC3_LOW, self.OPAC4_HIGH, self.OPAC4_LOW
        ) = response[4:-2]
        super().__init__(*response)

    def _compute_bcc(self, *_):
        super()._compute_bcc(
            self.OPAC1_HIGH, self.OPAC1_LOW, self.OPAC2_HIGH, self.OPAC2_LOW,
            self.OPAC3_HIGH, self.OPAC3_LOW, self.OPAC4_HIGH, self.OPAC4_LOW
        )


class SetBillDispenseOrderCommand(CommandMessage):
    """
    The command will define the bill dispense order from multi-cassettes.
    The default order is to pick bills from top cassette first, then second cassette and so on.
    The invalid assignment of parameter will cause an error and not be saved.
    When the data is changed, it will be saved in the memory of EEPROM and then efficient for the next transaction.
    In case of power on/off, the value continues to be used. However,
    when the electricity trouble causes the saved data damaged (wrong check sum on EEPROM),
    the criterion is set to initial value again.
    Therefore, it is recommended for user to check the value of the saved bill dispenser order when it is turned on.
    """
    CMD = CMD_SET_BILL_DISPENSE_ORDER
    ORDER1: int  # The cassette location (type) that is first to be picked up. 0x31~0x34
    ORDER2: int  # The cassette location (type) that is second to be picked up. 0x31~0x34
    ORDER3: int  # The cassette location (type) that is third to be picked up. 0x31~0x34
    ORDER4: int  # The cassette location (type) that is last to be picked up. 0x31~0x34
    _response_size = 6 + 1

    def __init__(self, *args):
        assert len(args) >= 4
        assert all(v in (0x31, 0x32, 0x33, 0x34) for v in args[:4])
        (self.ORDER1, self.ORDER2, self.ORDER3, self.ORDER4) = args[:4]
        super().__init__(*args)

    def _compute_bcc(self, *_):
        super()._compute_bcc(self.ORDER1, self.ORDER2, self.ORDER3, self.ORDER4)

    def _bytes(self, *_):
        return super()._bytes(self.ORDER1, self.ORDER2, self.ORDER3, self.ORDER4)


class SetBillDispenseOrderResponse(ResponseMessage):
    RSP = CMD_SET_BILL_DISPENSE_ORDER
    ERROR: int  # Error Status for Operation

    def __init__(self, *response: int):
        (self.ERROR,) = response[4:-2]
        super().__init__(*response)

    def _compute_bcc(self, *_):
        super()._compute_bcc(self.ERROR)


class GetBillDispenseOrderCommand(CommandMessage):
    """The command will get the bill dispense order data."""
    CMD = CMD_GET_BILL_DISPENSE_ORDER
    _response_size = 6 + 4


class GetBillDispenseOrderResponse(ResponseMessage):
    RSP = CMD_GET_BILL_DISPENSE_ORDER
    ERROR: int  # Error Status for Operation
    ORDER1: int  # The cassette location (type) that is first to be picked up. 0x31~0x34
    ORDER2: int  # The cassette location (type) that is second to be picked up. 0x31~0x34
    ORDER3: int  # The cassette location (type) that is third to be picked up. 0x31~0x34
    ORDER4: int  # The cassette location (type) that is last to be picked up. 0x31~0x34

    def __init__(self, *response: int):
        (self.ORDER1, self.ORDER2, self.ORDER3, self.ORDER4) = response[4:-2]
        super().__init__(*response)

    def _compute_bcc(self, *_):
        super()._compute_bcc(self.ORDER1, self.ORDER2, self.ORDER3, self.ORDER4)


class SetBillLengthsCommand(CommandMessage):
    """
    The command is used to save the reference value in order to detect double notes.
    Each length value can be saved from 0x00 to 0xFF. The value, 0x00 means to maintain current data.
    When the data is changed, it will be saved in the memory of EEPROM and then efficient for the next transaction.
    In case of power on/off, the value continues to be used. However,
    when the electricity trouble causes the saved data damaged (wrong check sum on EEPROM),
    the criterion is set to initial value again.
    Therefore, it is recommended for user to check the value of the saved value of LENGTH when it is turned on.
    """
    CMD = CMD_SET_BILL_LENGTHS
    LENG1_HIGH: int  # The high hexadecimal digit for the length of bills in top cassette. 0x30~0x3F
    LENG1_LOW: int  # The low hexadecimal digit for the length of bills in top cassette. 0x30~0x3F
    LENG2_HIGH: int  # The high hexadecimal digit for the length of bills in second top cassette. 0x30~0x3F
    LENG2_LOW: int  # The low hexadecimal digit for the length of bills in second top cassette. 0x30~0x3F
    LENG3_HIGH: int  # The high hexadecimal digit for the length of bills in third top cassette. 0x30~0x3F
    LENG3_LOW: int  # The low hexadecimal digit for the length of bills in third top cassette. 0x30~0x3F
    LENG4_HIGH: int  # The high hexadecimal digit for the length of bills in bottom cassette. 0x30~0x3F
    LENG4_LOW: int  # The low hexadecimal digit for the length of bills in bottom cassette. 0x30~0x3F
    _response_size = 6 + 1

    def __init__(self, *args):
        assert len(args) >= 8
        (
            self.LENG1_HIGH, self.LENG1_LOW, self.LENG2_HIGH, self.LENG2_LOW,
            self.LENG3_HIGH, self.LENG3_LOW, self.LENG4_HIGH, self.LENG4_LOW
        ) = args[:8]
        super().__init__(*args)

    def _compute_bcc(self, *_):
        super()._compute_bcc(
            self.LENG1_HIGH, self.LENG1_LOW, self.LENG2_HIGH, self.LENG2_LOW,
            self.LENG3_HIGH, self.LENG3_LOW, self.LENG4_HIGH, self.LENG4_LOW
        )

    def _bytes(self, *_):
        return super()._bytes(
            self.LENG1_HIGH, self.LENG1_LOW, self.LENG2_HIGH, self.LENG2_LOW,
            self.LENG3_HIGH, self.LENG3_LOW, self.LENG4_HIGH, self.LENG4_LOW
        )


class SetBillLengthsResponse(ResponseMessage):
    RSP = CMD_SET_BILL_LENGTHS
    ERROR: int  # Error Status for Operation

    def __init__(self, *response: int):
        (self.ERROR,) = response[4:-2]
        super().__init__(*response)

    def _compute_bcc(self, *_):
        super()._compute_bcc(self.ERROR)


class GetBillLengthsCommand(CommandMessage):
    """The command will get to saved length data for each cassette."""
    CMD = CMD_GET_BILL_LENGTHS
    _response_size = 6 + 1 + 2 * 4


class GetBillLengthsResponse(ResponseMessage):
    RSP = CMD_GET_BILL_LENGTHS
    ERROR: int  # Error Status for Operation
    LENG1_HIGH: int  # The high hexadecimal digit for the opacity of bills in top cassette. 0x30~0x3F
    LENG1_LOW: int  # The low hexadecimal digit for the opacity of bills in top cassette. 0x30~0x3F
    LENG2_HIGH: int  # The high hexadecimal digit for the opacity of bills in second top cassette. 0x30~0x3F
    LENG2_LOW: int  # The low hexadecimal digit for the opacity of bills in second top cassette. 0x30~0x3F
    LENG3_HIGH: int  # The high hexadecimal digit for the opacity of bills in third top cassette. 0x30~0x3F
    LENG3_LOW: int  # The low hexadecimal digit for the opacity of bills in third top cassette. 0x30~0x3F
    LENG4_HIGH: int  # The high hexadecimal digit for the opacity of bills in bottom cassette. 0x30~0x3F
    LENG4_LOW: int  # The low hexadecimal digit for the opacity of bills in bottom cassette. 0x30~0x3F

    def __init__(self, *response: int):
        (
            self.LENG1_HIGH, self.LENG1_LOW, self.LENG2_HIGH, self.LENG2_LOW,
            self.LENG3_HIGH, self.OPAC3_LOW, self.OPAC4_HIGH, self.OPAC4_LOW
        ) = response[4:-2]
        super().__init__(*response)

    def _compute_bcc(self, *_):
        super()._compute_bcc(
            self.LENG1_HIGH, self.LENG1_LOW, self.LENG2_HIGH, self.LENG2_LOW,
            self.LENG3_HIGH, self.OPAC3_LOW, self.OPAC4_HIGH, self.OPAC4_LOW
        )


class PuloonException(Exception):
    code: int = 0x20
    message: str = ERROR_CODES[UNKNOWN_ERROR]
    response: ResponseMessage = None

    def __init__(self, code: int, message: str = '', response: ResponseMessage = None, *args: object):
        self.code = code
        self.message = message or ERROR_CODES.get(code) or ERROR_CODES[UNKNOWN_ERROR]
        self.response = response
        super().__init__(self.code, self.message, self.response, *args)

    def __repr__(self) -> str:
        _repr = f'{self.__class__.__name__}: {hex(self.code)} - {self.message}'
        if self.response:
            _repr += f'\n{repr(self.response)}'
        return _repr


C = TypeVar('C', bound=CommandMessage)
R = TypeVar('R', bound=ResponseMessage)


class PuloonLCDM4000:
    ack: Final = 0x06
    nak: Final = 0x15
    eot: Final = 0x04

    ack_delay = (0.000, 0.050)
    ack_timeout = (0.500, 0.550)
    response_delay = (0.000, 60.000)

    port: Serial

    def __init__(self, port: Serial):
        self.port = port

    def _run(self, cmd_class: Type[C], resp_class: Type[R], *args: int) -> R:
        cmd = cmd_class(*args)

        for _ in range(3):
            self.port.write(cmd.bytes())
            self.port.timeout = self.ack_timeout[1]

            ack = self.port.read(1)
            if len(ack) > 0 and self.ack == ack[0]:
                break
        else:
            raise PuloonException(ACK_TIMEOUT)

        for _ in range(3):
            self.port.timeout = self.response_delay[1]
            data = self.port.read(cmd.response_size())
            resp = resp_class(*data)
            if resp.is_valid():
                self.port.write(chr(self.ack).encode('ascii'))
                eot = self.port.read(1)
                if len(eot) > 0 and self.eot == eot[0]:
                    if resp.ERROR != NO_ERROR:
                        raise PuloonException(resp.ERROR - NO_ERROR, response=resp)
                    break
            self.port.write(chr(self.nak).encode('ascii'))
        else:
            raise PuloonException(RESPONSE_TIMEOUT)

        return resp

    def reset(self):
        cmd = ResetCommand()
        self.port.write(cmd.bytes())
        sleep(2)

    def status(self) -> StatusResponse:
        return self._run(StatusCommand, StatusResponse)

    def purge(self) -> PurgeResponse:
        return self._run(PurgeCommand, PurgeResponse)

    def dispense(self, qty1: int = 0, qty2: int = 0, qty3: int = 0, qty4: int = 0,
                 to1: int = 0x20, to2: int = 0x20) -> DispenseResponse:
        assert all(0 <= q <= 40 for q in (qty1, qty2, qty3, qty4)), "Quantity should be in range of 0 and 40"
        assert 0 < sum((qty1, qty2, qty3, qty4)) <= 40, "Quantity should be at least 1 and maximum 40 in total"
        args = [q + 0x20 for q in (qty1, qty2, qty3, qty4)]
        return self._run(DispenseCommand, DispenseResponse, *args, to1, to2)

    def test_dispense(self, qty1: int = 0, qty2: int = 0, qty3: int = 0, qty4: int = 0,
                      to1: bool = False, to2: int = 0) -> TestDispenseResponse:
        assert all(0 <= q <= 40 for q in (qty1, qty2, qty3, qty4)), "Quantity should be in range of 0 and 40"
        assert 0 < sum((qty1, qty2, qty3, qty4)) <= 40, "Quantity should be at least 1 and maximum 40 in total"
        assert 0 <= to2 <= 9, "Timeout should be in range of 0 and 9"
        return self._run(
            TestDispenseCommand,
            TestDispenseResponse,
            *(q + 0x20 for q in (qty1, qty2, qty3, qty4)),
            0x1C if to1 else 0x20,
            to2 + 0x30 if to1 else 0x20
        )

    def last_status(self) -> LastStatusResponse:
        return self._run(LastStatusCommand, LastStatusResponse)

    def sensor_diagnostics(self, pos: int = 1) -> SensorDiagnosticsResponse:
        assert 1 <= pos <= 4, "Dispenser has only 4 cassette"
        return self._run(SensorDiagnosticsCommand, SensorDiagnosticsResponse, pos + 0x30)

    def set_bill_opacities(self, opac1_high: int = 0x30, opac1_low: int = 0x30,
                           opac2_high: int = 0x30, opac2_low: int = 0x30,
                           opac3_high: int = 0x30, opac3_low: int = 0x30,
                           opac4_high: int = 0x30, opac4_low: int = 0x30) -> SetBillOpacitiesResponse:
        assert all(0x30 <= v <= 0x3F for v in (
            opac1_high, opac1_low, opac2_high, opac2_low,
            opac3_high, opac3_low, opac4_high, opac4_low
        )), "Opacity value should be in range of 0x31 and 0x34"
        return self._run(SetBillOpacitiesCommand, SetBillOpacitiesResponse,
                         opac1_high, opac1_low, opac2_high, opac2_low,
                         opac3_high, opac3_low, opac4_high, opac4_low)

    def get_bill_opacities(self) -> GetBillOpacitiesResponse:
        return self._run(GetBillOpacitiesCommand, GetBillOpacitiesResponse)

    def set_bill_dispense_order(self, order1: int = 0x31, order2: int = 0x31,
                                order3: int = 0x31, order4: int = 0x31) -> SetBillDispenseOrderResponse:
        assert all(0x31 <= v <= 0x34 for v in (order1, order2, order3, order4)), \
            "Order value should be in range of 0x31 and 0x34"
        assert len({order1, order2, order3, order4}) == 4, "Order values should be unique"
        return self._run(SetBillDispenseOrderCommand, SetBillDispenseOrderResponse,
                         order1, order2, order3, order4)

    def get_bill_dispense_order(self) -> GetBillDispenseOrderResponse:
        return self._run(GetBillDispenseOrderCommand, GetBillDispenseOrderResponse)

    def set_bill_lengths(self, leng1_high: int = 0x30, leng1_low: int = 0x30,
                         leng2_high: int = 0x30, leng2_low: int = 0x30,
                         leng3_high: int = 0x30, leng3_low: int = 0x30,
                         leng4_high: int = 0x30, leng4_low: int = 0x30) -> SetBillLengthsResponse:
        assert all(0x30 <= v <= 0x3F for v in (
            leng1_high, leng1_low, leng2_high, leng2_low,
            leng3_high, leng3_low, leng4_high, leng4_low
        )), "Length value should be in range of 0x31 and 0x34"
        return self._run(SetBillLengthsCommand, SetBillLengthsResponse,
                         leng1_high, leng1_low, leng2_high, leng2_low,
                         leng3_high, leng3_low, leng4_high, leng4_low)

    def get_bill_lengths(self) -> GetBillLengthsResponse:
        return self._run(GetBillLengthsCommand, GetBillLengthsResponse)
