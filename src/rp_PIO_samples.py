import time
from machine import Pin
import rp2


# -----------------------------------------------
# add type hints for the rp2.PIO Instructions
from typing_extensions import TYPE_CHECKING  # type: ignore

if TYPE_CHECKING:
    from rp2.asm_pio import *
# -----------------------------------------------
@rp2.asm_pio(set_init=rp2.PIO.OUT_LOW)
def blink_1hz():
    # Cycles: 1 + 1 + 6 + 32 * (30 + 1) = 1000
    irq(rel(0))
    set(pins, 1)
    set(x, 31) [5]
    label("delay_high")
    nop() [29]
    jmp(x_dec, "delay_high")

    # Cycles: 1 + 7 + 32 * (30 + 1) = 1000
    set(pins, 0)
    set(x, 31) [6]
    label("delay_low")
    nop() [29]
    jmp(x_dec, "delay_low")


@rp2.asm_pio()
def wait_pin_low():
    wrap_target()

    wait(0, pin, 0)
    irq(block, rel(0))
    wait(1, pin, 0)

    wrap()


# Example of using PIO for PWM, and fading the brightness of an LED

from machine import Pin
from rp2 import PIO, StateMachine, asm_pio
from time import sleep


@asm_pio(sideset_init=PIO.OUT_LOW)
def pwm_prog():
    pull(noblock) .side(0)
    mov(x, osr) # Keep most recent pull data stashed in X, for recycling by noblock
    mov(y, isr) # ISR must be preloaded with PWM count max
    label("pwmloop")
    jmp(x_not_y, "skip")
    nop()         .side(1)
    label("skip")
    jmp(y_dec, "pwmloop")


class PIOPWM:
    def __init__(self, sm_id, pin, max_count, count_freq):
        self._sm = StateMachine(sm_id, pwm_prog, freq=2 * count_freq, sideset_base=Pin(pin))
        # Use exec() to load max count into ISR
        self._sm.put(max_count)
        self._sm.exec("pull()")
        self._sm.exec("mov(isr, osr)")
        self._sm.active(1)
        self._max_count = max_count

    def set(self, value):
        # Minimum value is -1 (completely turn off), 0 actually still produces narrow pulse
        value = max(value, -1)
        value = min(value, self._max_count)
        self._sm.put(value)


# Pin 25 on Pico boards
pwm = PIOPWM(0, 25, max_count=(1 << 16) - 1, count_freq=10_000_000)

while True:
    for i in range(256):
        pwm.set(i ** 2)
        sleep(0.01)
    break


# Create the StateMachine with the blink_1hz program, outputting on Pin(25).
sm = rp2.StateMachine(0, blink_1hz, freq=2000, set_base=Pin(25))

# Set the IRQ handler to print the millisecond timestamp.
sm.irq(lambda p: print(time.ticks_ms())) # type: ignore

# Start the StateMachine.
sm.active(1)