from machine import Pin
import rp2

from rp2 import PIO, StateMachine, asm_pio

# add type hints for the rp2.PIO Instructions
from typing_extensions import TYPE_CHECKING # type: ignore
if TYPE_CHECKING:
    from rp2.asm_pio import *
# -----------------------------------------------

@rp2.asm_pio(
    sideset_init=PIO.OUT_LOW,
    out_init=(PIO.OUT_LOW, PIO.OUT_LOW),
    out_shiftdir=PIO.SHIFT_LEFT,
    in_shiftdir=PIO.SHIFT_LEFT,
)
def spi():
    wrap_target()
    # Pull one byte from the TX FIFO and write it to the OSR
    pull(noblock, osr)
    # Set the chip select pin low
    set(pins, 0)
    # Push the ISR value to the RX FIFO
    push(noblock, isr)
    # Set the chip select pin high
    set(pins, 1)
    wrap()

