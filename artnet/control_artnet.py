"""(Very) Simple Implementation of Artnet.
Implementation for Artnet from https://github.com/cpvalente/stupidArtnet/tree/master/stupidArtnet

by you-wen ji, 2022 @fangal architectural @citacph
"""

import socket
from threading import Timer
import time
import math as m

class Artnet():
    """(Very) simple implementation of Artnet."""

    UDP_PORT = 6454#6454

    def __init__(self, target_ip='127.0.0.1', universe=0, packet_size=512, fps=30,
                 even_packet_size=True, broadcast=False):
        """Initializes Art-Net Client.

        Args:
        targetIP - IP of receiving device
        universe - universe to listen
        packet_size - amount of channels to transmit
        fps - transmition rate
        even_packet_size - Some receivers enforce even packets
        broadcast - whether to broadcast in local sub

        Returns:
        None

        """
        # Instance variables
        self.target_ip = target_ip
        self.sequence = 0
        self.physical = 0
        self.universe = universe
        self.subnet = 0
        self.net = 0
        self.packet_size = put_in_range(packet_size, 2, 512, even_packet_size)
        self.packet_header = bytearray()
        self.buffer = bytearray(self.packet_size)
        self.all = bytearray()

        self.make_even = even_packet_size

        self.is_simplified = True		# simplify use of universe, net and subnet

        # UDP SOCKET
        self.socket_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        if broadcast:
            self.socket_client.setsockopt(
                socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        # Timer
        self.fps = fps
        self.__clock = None

        self.make_header()

    def __del__(self):
        """Graceful shutdown."""
        self.stop()
        self.close()

    def __str__(self):
        """Printable object state."""
        state = "===================================\n"
        state += "Stupid Artnet initialized\n"
        state += "Target IP: {self.target_ip} : {self.UDP_PORT} \n"
        state += "Universe: {self.universe} \n"
        if not self.is_simplified:
            state += "Subnet: {self.subnet} \n"
            state += "Net: {self.net} \n"
        state += "Packet Size: {self.packet_size} \n"
        state += "==================================="

        return state

    def make_header(self):
        """Make packet header."""
        # 0 - id (7 x bytes + Null)
        self.packet_header = bytearray()
        self.packet_header.extend(bytearray('Art-Net', 'utf8')) #0-6
        self.packet_header.append(0x0) #7
        # 8 - opcode (2 x 8 low byte first)
        self.packet_header.append(0x00) 
        self.packet_header.append(0x50)  # ArtDmx data packet #8
        # 10 - prototocol version (2 x 8 high byte first)
        self.packet_header.append(0x0)
        self.packet_header.append(14)
        # 12 - sequence (int 8), NULL for not implemented
        self.packet_header.append(self.sequence)
        # 13 - physical port (int 8)
        self.packet_header.append(0x00)
        # 14 - universe, (2 x 8 low byte first)
        if self.is_simplified:
            # not quite correct but good enough for most cases:
            # the whole net subnet is simplified
            # by transforming a single uint16 into its 8 bit parts
            # you will most likely not see any differences in small networks
            msb, lsb = shift_this(self.universe)   # convert to MSB / LSB
            self.packet_header.append(lsb)
            self.packet_header.append(msb)
        # 14 - universe, subnet (2 x 4 bits each)
        # 15 - net (7 bit value)
        else:
            # as specified in Artnet 4 (remember to set the value manually after):
            # Bit 3  - 0 = Universe (1-16)
            # Bit 7  - 4 = Subnet (1-16)
            # Bit 14 - 8 = Net (1-128)
            # Bit 15     = 0
            # this means 16 * 16 * 128 = 32768 universes per port
            # a subnet is a group of 16 Universes
            # 16 subnets will make a net, there are 128 of them
            self.packet_header.append(self.subnet << 4 | self.universe)
            self.packet_header.append(self.net & 0xFF)
        # 16 - packet size (2 x 8 high byte first)
        msb, lsb = shift_this(self.packet_size)		# convert to MSB / LSB
        self.packet_header.append(msb)
        self.packet_header.append(lsb)

    def show(self):
        """Finally send data."""
        packet = bytearray()
        packet.extend(self.packet_header)
        packet.extend(self.buffer)
        

        p = packet.decode()
        try:
            self.socket_client.sendto(p, (self.target_ip, self.UDP_PORT))
        except socket.error as error:
            print("ERROR: Socket error with exception: {error}")
        finally:
            self.sequence = (self.sequence + 1) % 256

    def close(self):
        """Close UDP socket."""
        self.socket_client.close()

    # THREADING #

    def start(self):
        """Starts thread clock."""
        self.show()
        self.__clock = Timer((1000.0 / self.fps) / 1000.0, self.start)
        self.__clock.daemon = True
        self.__clock.start()

    def stop(self):
        """Stops thread clock."""
        if self.__clock is not None:
            self.__clock.cancel()

    # SETTERS - HEADER #

    def set_universe(self, universe):
        """Setter for universe (0 - 15 / 256).

        Mind if protocol has been simplified
        """
        # This is ugly, trying to keep interface easy
        # With simplified mode the universe will be split into two
        # values, (uni and sub) which is correct anyway. Net will always be 0
        if self.is_simplified:
            self.universe = put_in_range(universe, 0, 255, False)
        else:
            self.universe = put_in_range(universe, 0, 15, False)
        self.make_header()

    def set_subnet(self, sub):
        """Setter for subnet address (0 - 15).

        Set simplify to false to use
        """
        self.subnet = put_in_range(sub, 0, 15, False)
        self.make_header()

    def set_net(self, net):
        """Setter for net address (0 - 127).

        Set simplify to false to use
        """
        self.net = put_in_range(net, 0, 127, False)
        self.make_header()

    def set_packet_size(self, packet_size):
        """Setter for packet size (2 - 512, even only)."""
        self.packet_size = put_in_range(packet_size, 2, 512, self.make_even)
        self.make_header()

    # SETTERS - DATA #

    def clear(self):
        """Clear DMX buffer."""
        self.buffer = bytearray(self.packet_size)

    def set(self, value):
        """Set buffer."""
        if len(value) != self.packet_size:
            print("ERROR: packet does not match declared packet size")
            return
        self.buffer = value

    def set_16bit(self, address, value, high_first=False):
        """Set single 16bit value in DMX buffer."""
        if address > self.packet_size:
            print("ERROR: Address given greater than defined packet size")
            return
        if address < 1 or address > 512 - 1:
            print("ERROR: Address out of range")
            return
        value = put_in_range(value, 0, 65535, False)

        # Check for endianess
        if high_first:
            self.buffer[address - 1] = (value >> 8) & 0xFF  # high
            self.buffer[address] = (value) & 0xFF 			# low
        else:
            self.buffer[address - 1] = (value) & 0xFF				# low
            self.buffer[address] = (value >> 8) & 0xFF  # high

    def set_single_value(self, address, value):
        """Set single value in DMX buffer."""
        if address > self.packet_size:
            print("ERROR: Address given greater than defined packet size")
            return
        if address < 1 or address > 512:
            print("ERROR: Address out of range")
            return
        self.buffer[address - 1] = put_in_range(value, 0, 255, False)

    def set_single_rem(self, address, value):
        """Set single value while blacking out others."""
        if address > self.packet_size:
            print("ERROR: Address given greater than defined packet size")
            return
        if address < 1 or address > 512:
            print("ERROR: Address out of range")
            return
        self.clear()
        self.buffer[address - 1] = put_in_range(value, 0, 255, False)

    def set_rgb(self, address, red, green, blue):
        """Set RGB from start address."""
        if address > self.packet_size:
            print("ERROR: Address given greater than defined packet size")
            return
        if address < 1 or address > 510:
            print("ERROR: Address out of range")
            return

        self.buffer[address - 1] = put_in_range(red, 0, 255, False)
        self.buffer[address] = put_in_range(green, 0, 255, False)
        self.buffer[address + 1] = put_in_range(blue, 0, 255, False)

    def set_address_color(self, address, red, blue, green):
        """Set address color"""
        if(address * 3 > self.packet_size or address < 0):
            print("ERROR: num is greater than the 512 or lower than 0")
            return
        """the color BRG not RGB"""
        self.buffer[address*3+2] = put_in_range(blue, 0, 255, False)
        self.buffer[address*3+1] = put_in_range(red, 0, 255, False)
        self.buffer[address*3] = put_in_range(green, 0, 255, False)
    # AUX Function #

    def send(self, packet):
        """Set buffer and send straightaway.

        Args:
        array - integer array to send
        """
        self.set(packet)
        self.show()

    def set_simplified(self, simplify):
        """Builds Header accordingly.

        True - Header sends 16 bit universe value (OK but incorrect)
        False - Headers sends Universe - Net and Subnet values as protocol
        It is recommended that you set these values with .set_net() and set_physical
        """
        # avoid remaking header if there are no changes
        if simplify == self.is_simplified:
            return
        self.is_simplified = simplify
        self.make_header()

    def see_header(self):
        """Show header values."""
        print(self.packet_header)

    def see_buffer(self):
        """Show buffer values."""
        print(self.buffer)

    def blackout(self):
        """Sends 0's all across."""
        self.clear()
        self.show()

    def flash_all(self, delay=None):
        """Sends 255's all across."""
        self.set([255] * self.packet_size)
        self.show()
        # Blackout after delay
        if delay:
            time.sleep(delay)
            self.blackout()

def shift_this(number, high_first=True):
    """Utility method: extracts MSB and LSB from number.

    Args:
    number - number to shift
    high_first - MSB or LSB first (true / false)

    Returns:
    (high, low) - tuple with shifted values

    """
    low = (number & 0xFF)
    high = ((number >> 8) & 0xFF)
    if high_first:
        return((high, low))
    return((low, high))

def clamp(number, min_val, max_val):
    """Utility method: sets number in defined range.

    Args:
    number - number to use
    range_min - lowest possible number
    range_max - highest possible number

    Returns:
    number - number in correct range
    """
    return max(min_val, min(number, max_val))

def set_even(number):
    """Utility method: ensures number is even by adding.

    Args:
    number - number to make even

    Returns:
    number - even number
    """
    if number % 2 != 0:
        number += 1
    return number

def put_in_range(number, range_min, range_max, make_even=True):
    """Utility method: sets number in defined range.
    DEPRECATED: this will be removed from the library

    Args:
    number - number to use
    range_min - lowest possible number
    range_max - highest possible number
    make_even - should number be made even

    Returns:
    number - number in correct range

    """
    number = clamp(number, range_min, range_max)
    if make_even:
        number = set_even(number)
    return number

def make_address_mask(universe, sub=0, net=0, is_simplified=True):
    """Returns the address bytes for a given universe, subnet and net.

    Args:
    universe - Universe to listen
    sub - Subnet to listen
    net - Net to listen
    is_simplified - Whether to use nets and subnet or universe only,
    see User Guide page 5 (Universe Addressing)

    Returns:
    bytes - byte mask for given address

    """
    address_mask = bytearray()

    if is_simplified:
        # Ensure data is in right range
        universe = clamp(universe, 0, 32767)

        # Make mask
        msb, lsb = shift_this(universe)  # convert to MSB / LSB
        address_mask.append(lsb)
        address_mask.append(msb)
    else:
        # Ensure data is in right range
        universe = clamp(universe, 0, 15)
        sub = clamp(sub, 0, 15)
        net = clamp(net, 0, 127)

        # Make mask
        address_mask.append(sub << 4 | universe)
        address_mask.append(net & 0xFF)

    return address_mask

"""
==================================================
main from below
==================================================
"""

target_ip = '192.168.2.1'		# the defaut of super sweet
universe = 0 					# the port number
packet_size = 512				

kagome = Artnet(target_ip, universe, packet_size, 20, True, True)

packet = bytearray(packet_size)		# create packet for Artnet
kagome.buffer = packet

for i in range(len(addr)):
    kagome.set_address_color(addr[i],colors[i].R,colors[i].G,colors[i].B)

kagome.start()
time.sleep(0.01)
kagome.stop()
del kagome