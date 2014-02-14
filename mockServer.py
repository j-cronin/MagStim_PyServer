from mock import patch
import server

# Mock out the serial port
with patch('serial.Serial') as mockedSerialPort:
    server.do_main()
