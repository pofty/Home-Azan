
import socket


def bluetooth():

# Create a Bluetooth socket
    sock = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)

    # Set the Bluetooth address and port of the device you want to connect to

    device_address = '20:15:02:00:01:7D' # Replace with the actual Bluetooth address
    port = 1  # Replace with the actual RFCOMM port

    # Connect to the Bluetooth device
    sock.connect((device_address, port))

