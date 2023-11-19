#type: ignore
"""
Test to see if / how the decorator internal functions are seen/used by the type-checking tools
Answer: they are not seen :-( 
"""
class PIOASMEmit:
    def __init__(self) -> None:
        self.labels = {}
        self.prog = []
        self.wrap_used = False
        self.pins = 0
    def nop(self) -> None:
        self.prog.append(0)
    


def pio_asm_nop() -> None: 
    print("NOP")

def jos_pio_old(**kw):

    emit = PIOASMEmit(**kw)
    def decorator(f):
        def nop(self) -> None: ...
        f(emit)
        return emit
    return decorator

def jos_pio(set_init=3):
    def wrap(f):
        print ("Inside wrap()")
        def wrapped_f(*args):
            print ("Inside wrapped_f()")
            print ("Decorator arguments:", set_init)
            f.__globals__["nop"] = pio_asm_nop
            f(*args)
            print ("After f(*args)")
        return wrapped_f
    return wrap

@jos_pio(set_init=0)
def blink_1hz():
    # Cycles: 1 + 1 + 6 + 32 * (30 + 1) = 1000
    # irq(rel(0))
    nop()
    