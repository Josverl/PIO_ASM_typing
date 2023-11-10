import time

import machine
import uctypes
from micropython import const


class DMA:
    DMA_BASE = 0x50000000
    CH_ABORT = const(0x50000444)

    EN:int = const(0x01 << 0) #type: ignore

    HIGH_PRIORITY:int = const(0x01 << 1) #type: ignore
    INCR_READ:int = const(0x01 << 4) #type: ignore
    INCR_WRITE:int = const(0x01 << 5) #type: ignore
    IRQ_QUIET:int = const(0x01 << 21) #type: ignore
    BUSY:int = const(0x01 << 24) #type: ignore

    SIZE_BYTE:int = const(0x00 << 2)  #type: ignore
    SIZE_HALFWORD:int = const(0x01 << 2) #type: ignore
    SIZE_WORD:int = const(0x02 << 2) # type: ignore

    DREQ_PIO0_TX0:int = const(0x00 << 15) #type: ignore
    DREQ_PIO0_TX1:int = const(0x01 << 15) #type: ignore
    DREQ_PIO0_TX2:int = const(0x02 << 15) #type: ignore
    DREQ_PIO0_TX3:int = const(0x03 << 15) #type: ignore
    DREQ_PIO0_RX0:int = const(0x04 << 15) #type: ignore
    DREQ_PIO0_RX1:int = const(0x05 << 15) #type: ignore
    DREQ_PIO0_RX2:int = const(0x06 << 15) #type: ignore
    DREQ_PIO0_RX3:int = const(0x07 << 15) #type: ignore
    DREQ_PIO1_TX0:int = const(0x08 << 15) #type: ignore
    DREQ_PIO1_TX1:int = const(0x09 << 15) #type: ignore
    DREQ_PIO1_TX2:int = const(0x0A << 15) #type: ignore
    DREQ_PIO1_TX3:int = const(0x0B << 15) #type: ignore
    DREQ_PIO1_RX0:int = const(0x0C << 15) #type: ignore
    DREQ_PIO1_RX1:int = const(0x0D << 15) #type: ignore
    DREQ_PIO1_RX2:int = const(0x0E << 15) #type: ignore
    DREQ_PIO1_RX3:int = const(0x0F << 15) #type: ignore
    DREQ_SPI0_TX:int = const(0x10 << 15) #type: ignore
    DREQ_SPI0_RX:int = const(0x11 << 15) #type: ignore
    DREQ_SPI1_TX:int = const(0x12 << 15) #type: ignore
    DREQ_SPI1_RX:int = const(0x13 << 15) #type: ignore
    DREQ_UART0_TX:int = const(0x14 << 15) #type: ignore
    DREQ_UART0_RX:int = const(0x15 << 15) #type: ignore
    DREQ_UART1_TX:int = const(0x16 << 15) #type: ignore
    DREQ_UART1_RX:int = const(0x17 << 15) #type: ignore
    DREQ_PWM_WRAP0:int = const(0x18 << 15) #type: ignore
    DREQ_PWM_WRAP1:int = const(0x19 << 15) #type: ignore
    DREQ_PWM_WRAP2:int = const(0x1A << 15) #type: ignore
    DREQ_PWM_WRAP3:int = const(0x1B << 15) #type: ignore
    DREQ_PWM_WRAP4:int = const(0x1C << 15) #type: ignore
    DREQ_PWM_WRAP5:int = const(0x1D << 15) #type: ignore
    DREQ_PWM_WRAP6:int = const(0x1E << 15) #type: ignore
    DREQ_PWM_WRAP7:int = const(0x1F << 15) #type: ignore
    DREQ_I2C0_TX:int = const(0x20 << 15) #type: ignore
    DREQ_I2C0_RX:int = const(0x21 << 15) #type: ignore
    DREQ_I2C1_TX:int = const(0x22 << 15) #type: ignore
    DREQ_I2C1_RX:int = const(0x23 << 15) #type: ignore
    DREQ_ADC:int = const(0x24 << 15) #type: ignore
    DREQ_XIP_STREAM:int = const(0x25 << 15) #type: ignore
    DREQ_XIP_SSITX:int = const(0x26 << 15) #type: ignore
    DREQ_XIP_SSIRX:int = const(0x27 << 15) #type: ignore
    TREQ_TMR0:int = const(0x3B << 15) #type: ignore
    TREQ_TMR1:int = const(0x3C << 15) #type: ignore
    TREQ_TMR2:int = const(0x3D << 15) #type: ignore
    TREQ_TMR3:int = const(0x3E << 15) #type: ignore
    TREQ_PERMANENT:int = const(0x3F << 15) #type: ignore

    def __init__(self, channelNumber):
        self.channel = channelNumber
        channelOffset = channelNumber * 0x40
        self.READ_ADDR = DMA.DMA_BASE + 0x00 + channelOffset
        self.WRITE_ADDR = DMA.DMA_BASE + 0x04 + channelOffset
        self.TRANS_COUNT = DMA.DMA_BASE + 0x08 + channelOffset
        self.CTRL_TRIG = DMA.DMA_BASE + 0x0C + channelOffset
        self.AL1_CTRL = DMA.DMA_BASE + 0x10 + channelOffset

    def config(
        self,
        *,
        read_addr,
        write_addr,
        trans_count,
        read_inc:bool,
        write_inc:bool,
        treq_sel=-1,
        chain_to=-1,
        data_size=0
    ):
        """
        Configure the DMA channel.

        - read_addr : Read address
        - write_addr : Write address
        - trans_count : Transfer count
        - read_inc:bool Increment read address 
        - write_inc:bool Increment write address
        - treq_sel : Transfer Request signal is selected by treq_sel. If treq_sel is -1, then the channel is permanently enabled.
        - chain_to : Chain to the given channel number. If chain_to is -1, then the channel is not chained.
        - data_size : Data size. 0=byte, 1=halfword, 2=word
        """
        if chain_to == -1:
            chain_to = self.channel
        if treq_sel == -1:
            treq_sel = DMA.TREQ_PERMANENT
        machine.mem32[self.CTRL_TRIG] = 0
        machine.mem32[self.READ_ADDR] = read_addr
        machine.mem32[self.WRITE_ADDR] = write_addr
        machine.mem32[self.TRANS_COUNT] = trans_count
        ctrl = DMA.INCR_READ if read_inc else 0
        if write_inc:
            ctrl |= DMA.INCR_WRITE
        machine.mem32[self.CTRL_TRIG] = (
            ctrl | (chain_to << 11) | treq_sel | DMA.IRQ_QUIET | data_size
        )

    def enable(self):
        machine.mem32[self.CTRL_TRIG] |= DMA.EN

    def enable_notrigger(self):
        machine.mem32[self.AL1_CTRL] |= DMA.EN

    def disable(self):
        machine.mem32[self.CTRL_TRIG] = 0

    @staticmethod
    def abort_all():
        machine.mem32[DMA.CH_ABORT] = 0xFFFF
        time.sleep(0.1)
        machine.mem32[DMA.CH_ABORT] = 0

    def is_busy(self):
        return bool(machine.mem32[self.CTRL_TRIG] & DMA.BUSY)
