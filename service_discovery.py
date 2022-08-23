#!/usr/bin/python3
import bluetooth_constants
import bluetooth_utils
import dbus
import sys
import time
import dbus.mainloop.glib
from gi.repository import GLib
mainloop = None


sys.path.insert(0, '.')
bus = None
device_interface = None


def signal_received(path, interfaces):
    print('received signal')
    print(f'path = {path}')
    print(f'interfaces = {interfaces}')
    print('---------------------------------')
    if bluetooth_constants.GATT_SERVICE_INTERFACE in interfaces:
        UUID = interfaces[bluetooth_constants.GATT_SERVICE_INTERFACE]['UUID']
        print(f'UUID = {UUID}')

        Device = interfaces[bluetooth_constants.GATT_SERVICE_INTERFACE]['Device']
        print(f'Device = {Device}')

        Primary = interfaces[bluetooth_constants.GATT_SERVICE_INTERFACE]['Primary']
        print(f'Primary = {Primary}')

        Includes = interfaces[bluetooth_constants.GATT_SERVICE_INTERFACE]['Includes']
        print(f'Includes = {Includes}')
    print('end')






def connect():
    global bus
    global device_interface

    try:
        device_interface.Connect()
    except Exception as e:
        print("Failed to connect")
        print(e.get_dbus_name())
        print(e.get_dbus_message())
        if("UnknownObject" in e.get_dbus_name()):
            print("Try scanning first to resolve this problem")
        return bluetooth_constants.RESULT_EXCEPTION

    else:
        print("Connected OK")
        return bluetooth_constants.RESULT_OK

if(len(sys.argv) != 2):
    print("usage: ./con_dis.py [bdaddr]")
    sys.exit(1)

dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

bdaddr = sys.argv[1]
bus = dbus.SystemBus()
adapter_path = bluetooth_constants.BLUEZ_NAMESPACE + bluetooth_constants.ADAPTER_NAME
device_path = bluetooth_utils.device_address_to_path(bdaddr, adapter_path)
device_proxy = bus.get_object(bluetooth_constants.BLUEZ_SERVICE_NAME, device_path)

iface_prop = dbus.Interface(device_proxy, bluetooth_constants.DBUS_PROPERTIES) #интерфейс чтобы посмотреть свойства
con = iface_prop.Get(bluetooth_constants.DEVICE_INTERFACE, 'Connected') #для Connected()

device_interface = dbus.Interface(device_proxy, bluetooth_constants.DEVICE_INTERFACE)#интерфейс для конкретного устройства

if con:
    print('device is always connected')
else:
    print("Connecting to " + bdaddr)
    res = connect()
    if res == bluetooth_constants.RESULT_OK:
        bus.add_signal_receiver(signal_received, dbus_interface = bluetooth_constants.DBUS_OM_IFACE, signal_name = "InterfacesAdded")
        mainloop = GLib.MainLoop()
        mainloop.run()


print('----exit---')

