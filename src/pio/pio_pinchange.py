# Example using PIO to wait for a pin change and raise an IRQ.
#
# Demonstrates:
#   - PIO wrapping
#   - PIO wait instruction, waiting on an input pin
#   - PIO irq instruction, in blocking mode with relative IRQ number
#   - setting the in_base pin for a StateMachine
#   - setting an irq handler for a StateMachine
#   - instantiating 2x StateMachine's with the same program and different pins

import time

import rp2
from machine import Pin

# -----------------------------------------------
# add type hints for the rp2.PIO Instructions
from typing_extensions import TYPE_CHECKING  # type: ignore

if TYPE_CHECKING:
    from rp2.asm_pio import *
# -----------------------------------------------

@rp2.asm_pio()
def wait_pin_low():
    wrap_target()

    wait(0, pin, 0)
    irq(block, rel(0))
    wait(1, pin, 0)

    wrap()


def handler(sm):
    # Print a (wrapping) timestamp, and the state machine object.
    print(time.ticks_ms(), sm)


# Instantiate StateMachine(0) with wait_pin_low program on Pin(16).
pin16 = Pin(16, Pin.IN, Pin.PULL_UP)
sm0 = rp2.StateMachine(0, wait_pin_low, in_base=pin16)
sm0.irq(handler)

# Instantiate StateMachine(1) with wait_pin_low program on Pin(17).
pin17 = Pin(17, Pin.IN, Pin.PULL_UP)
sm1 = rp2.StateMachine(1, wait_pin_low, in_base=pin17)
sm1.irq(handler)

# Start the StateMachine's running.
sm0.active(1)
sm1.active(1)

# Now, when Pin(16) or Pin(17) is pulled low a message will be printed to the REPL.
