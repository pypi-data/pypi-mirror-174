from pathlib import Path
from typing import Optional

import typer
from serial import Serial, SerialException

from puloon import __app_name__, __version__
from .lcdm4000 import PuloonException, PuloonLCDM4000

app = typer.Typer()


def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"{__app_name__} v{__version__}")
        raise typer.Exit()


# noinspection PyUnusedLocal
@app.callback()
def main(
        version: Optional[bool] = typer.Option(
            None,
            "--version",
            "-v",
            help="Show the application's version and exit.",
            callback=_version_callback,
            is_eager=True,
        )
) -> None:
    return


class PuloonExceptionHandler:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val: tuple, exc_tb):
        if exc_type and issubclass(exc_type, PuloonException):
            typer.echo(repr(exc_val))
            raise typer.Abort()
        if exc_type and issubclass(exc_type, (AssertionError, SerialException, PuloonException)):
            typer.echo(exc_val)
            raise typer.Abort()


@app.command(name='reset')
def _reset():
    ...


PortArg = typer.Argument(
    ...,
    exists=True,
    dir_okay=False,
    help="Serial port path",
)


@app.command(name='status')
def _status(port: Path = PortArg) -> None:
    with PuloonExceptionHandler():
        with Serial(str(port.resolve())) as serial:
            puloon = PuloonLCDM4000(serial)
            typer.echo(puloon.status())


@app.command(name='purge')
def _purge(port: Path = PortArg) -> None:
    with PuloonExceptionHandler():
        with Serial(str(port.resolve())) as serial:
            puloon = PuloonLCDM4000(serial)
            typer.echo(puloon.purge())


@app.command(name='dispense')
def _dispense():
    ...


@app.command(name='test-dispense')
def _test_dispense(
        qty1: int = typer.Option(
            0, "--qty1", "-q1", min=0, max=40, help="The number of bills to be dispensed from cassette type1"
        ),
        qty2: int = typer.Option(
            0, "--qty2", "-q2", min=0, max=40, help="The number of bills to be dispensed from cassette type2"
        ),
        qty3: int = typer.Option(
            0, "--qty3", "-q3", min=0, max=40, help="The number of bills to be dispensed from cassette type3"
        ),
        qty4: int = typer.Option(
            0, "--qty4", "-q4", min=0, max=40, help="The number of bills to be dispensed from cassette type4"
        ),
        to1: bool = typer.Option(
            False, "--to1", "-t1", help="If timeout value is used"
        ),
        to2: int = typer.Option(
            0, "--to2", "-t2", min=0, max=9, help="If  timeout value used, the value is 0~9"
        ),
        port: Path = PortArg,
) -> None:
    if sum((qty1, qty2, qty3, qty4)) == 0:
        raise typer.Exit()
    with PuloonExceptionHandler():
        with Serial(str(port.resolve())) as serial:
            puloon = PuloonLCDM4000(serial)
            typer.echo(puloon.test_dispense(qty1, qty2, qty3, qty4, to1, to2))


@app.command(name='last-status')
def _last_status():
    ...


@app.command(name='sensor-diagnostics')
def _sensor_diagnostics():
    ...


@app.command(name='set-bill-opacities')
def _set_bill_opacities():
    ...


@app.command(name='get-bill-opacities')
def _get_bill_opacities():
    ...


@app.command(name='set-bill-dispense-order')
def _set_bill_dispense_order():
    ...


@app.command(name='get-bill-dispense-order')
def _get_bill_dispense_order():
    ...


@app.command(name='set-bill-lengths')
def _set_bill_lengths():
    ...


@app.command(name='get-bill-lengths')
def _get_bill_lengths():
    ...
