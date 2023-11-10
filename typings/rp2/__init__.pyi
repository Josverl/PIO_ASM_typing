from typing import Any, Callable, ParamSpec, TypeVar
from _rp2 import *
from _typeshed import Incomplete

_PROG_DATA: Incomplete
_PROG_OFFSET_PIO0: Incomplete
_PROG_OFFSET_PIO1: Incomplete
_PROG_EXECCTRL: Incomplete
_PROG_SHIFTCTRL: Incomplete
_PROG_OUT_PINS: Incomplete
_PROG_SET_PINS: Incomplete
_PROG_SIDESET_PINS: Incomplete
_PROG_MAX_FIELDS: Incomplete

class PIOASMError(Exception): ...

class PIOASMEmit:
    labels: Incomplete
    prog: Incomplete
    wrap_used: bool
    sideset_count: int
    def __init__(
        self,
        *,
        out_init: Incomplete | None = ...,
        set_init: Incomplete | None = ...,
        sideset_init: Incomplete | None = ...,
        in_shiftdir: int = ...,
        out_shiftdir: int = ...,
        autopush: bool = ...,
        autopull: bool = ...,
        push_thresh: int = ...,
        pull_thresh: int = ...,
        fifo_join: int = ...,
    ) -> None: ...
    delay_max: int
    sideset_opt: Incomplete
    pass_: Incomplete
    num_instr: int
    num_sideset: int
    def start_pass(self, pass_) -> None: ...
    def __getitem__(self, key): ...
    def delay(self, delay): ...
    def side(self, value): 
        """\
            This is a modifier which can be applied to any instruction, and is used to control side-set pin values.
        value: the value (bits) to output on the side-set pins
        """
        ...
    def wrap_target(self) -> None: ...
    def wrap(self) -> None: ...
    def label(self, label) -> None: ...
    def word(self, instr, label: Incomplete | None = ...): ...
    def nop(self): ...
    def jmp(self, cond, label: Incomplete | None = ...): ...
    def wait(self, polarity, src, index): ...
    def in_(self, src, data): ...
    def out(self, dest, data): ...
    def push(self, value: int = ..., value2: int = ...): ...
    def pull(self, value: int = ..., value2: int = ...): ...
    def mov(self, dest, src): ...
    def irq(self, mod, index: Incomplete | None = ...): ...
    def set(self, dest, data): ...

_pio_funcs: Incomplete

T = TypeVar('T')
P = ParamSpec('P')

# def add_logging(f: Callable[P, T]) -> Callable[P, T]:
# # Complex but better
#     '''A type-safe decorator to add logging to a function.'''
#     def inner(*args: P.args, **kwargs: P.kwargs) -> T:
#         logging.info(f'{f.__name__} was called')
#         return f(*args, **kwargs)
#     return inner
# def asm_pio(func: Callable[P, T]) -> Callable[P, T]:
def asm_pio(**kwargs) -> Callable[..., PIOASMEmit]:
    """Assemble a PIO program.
    The following parameters control the initial state of the GPIO pins, as one of PIO.IN_LOW, PIO.IN_HIGH, PIO.OUT_LOW or PIO.OUT_HIGH. 
    If the program uses more than one pin, provide a tuple, e.g. out_init=(PIO.OUT_LOW, PIO.OUT_LOW).

        out_init configures the pins used for out() instructions.
        set_init configures the pins used for set() instructions. There can be at most 5.
        sideset_init configures the pins used side-setting. There can be at most 5.

    The following parameters are used by default, but can be overridden in StateMachine.init():
    in_shiftdir is the default direction the ISR will shift, either PIO.SHIFT_LEFT or PIO.SHIFT_RIGHT.
        out_shiftdir is the default direction the OSR will shift, either PIO.SHIFT_LEFT or PIO.SHIFT_RIGHT.
        push_thresh is the threshold in bits before auto-push or conditional re-pushing is triggered.
        pull_thresh is the threshold in bits before auto-pull or conditional re-pulling is triggered.

    The remaining parameters are:
        autopush configures whether auto-push is enabled.
        autopull configures whether auto-pull is enabled.
    fifo_join configures whether the 4-word TX and RX FIFOs should be combined into a single 8-word FIFO for one direction only. The options are PIO.JOIN_NONE, PIO.JOIN_RX and PIO.JOIN_TX.
"""
    ...

def asm_pio_encode(instr, sideset_count, sideset_opt: bool = ...): ...

# from .asm_pio import *