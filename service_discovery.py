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


def interfaces_added_sig_rcvd(path, interfaces):
    print('received signal')
    if bluetooth_constants.GATT_SERVICE_INTERFACE in interfaces:
        properties = interfaces[bluetooth_constants.GATT_SERVICE_INTERFACE]
        print("----------------------------------------------------------")
        print(f'service path: {path}')
        if 'UUID' in properties:
            uuid = properties['UUID']
            print("service UUID: ", bluetooth_utils.dbus_to_python(uuid))
            print("service name: ", bluetooth_utils.get_name_from_uuid(uuid))
        return

    if bluetooth_constants.GATT_CHARACTERISTIC_INTERFACE in interfaces:
        properties = interfaces[bluetooth_constants.GATT_CHARACTERISTIC_INTERFACE]
        print(f'characteristic path: {path}')
        if 'UUID' in properties:
            uuid = properties['UUID']
            print(" CHR UUID: ", bluetooth_utils.dbus_to_python(uuid))
            print(" CHR name: ", bluetooth_utils.get_name_from_uuid(uuid))
            flags = ""
            for flag in properties['Flags']:
                flags = flags + flag + ","
            print(" CHR flags : ", flags)
        return








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
        bus.add_signal_receiver(interfaces_added_sig_rcvd, dbus_interface = bluetooth_constants.DBUS_OM_IFACE, signal_name = "InterfacesAdded")
        mainloop = GLib.MainLoop()
        mainloop.run()


print('----exit---')

