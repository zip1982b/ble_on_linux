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
device_path = None
found_dis = False
found_mn = False
dis_path = None
mn_path = None


def service_discovery_completed():
    global found_dis
    global found_mn
    global dis_path
    global mn_path
    global bus
    if found_dis and found_mn:
        print("Required service and characteristic found - device is OK")
        print("Device Information service path: ",dis_path)
        print("Model Number String characteristic path: ",mn_path)
    else:
        print("Required service and characteristic were not found - device is NOK")
        print("Device Information service found: ",str(found_dis))
        print("Device Name characteristic found: ",str(found_mn))
        bus.remove_signal_receiver(interfaces_added_sig_rcvd,"InterfacesAdded")
        bus.remove_signal_receiver(properties_changed,"PropertiesChanged")
        mainloop.quit()

def interfaces_added_sig_rcvd(path, interfaces):
    global found_dis
    global found_mn
    global dis_path
    global mn_path
    print('received signal')
    if bluetooth_constants.GATT_SERVICE_INTERFACE in interfaces:
        properties = interfaces[bluetooth_constants.GATT_SERVICE_INTERFACE]
        print("----------------------------------------------------------")
        print(f'service path: {path}')
        if 'UUID' in properties:
            uuid = properties['UUID']
            if uuid == bluetooth_constants.GATT:
                found_dis = True
                dis_path = path
            print("service UUID: ", bluetooth_utils.dbus_to_python(uuid))
            print("service name: ", bluetooth_utils.get_name_from_uuid(uuid))
        return

    if bluetooth_constants.GATT_CHARACTERISTIC_INTERFACE in interfaces:
        properties = interfaces[bluetooth_constants.GATT_CHARACTERISTIC_INTERFACE]
        print(f'characteristic path: {path}')
        if 'UUID' in properties:
            uuid = properties['UUID']
            if uuid == bluetooth_constants.SVC_CH:
                found_mn = True
                mn_path = path
            print(" CHR UUID: ", bluetooth_utils.dbus_to_python(uuid))
            print(" CHR name: ", bluetooth_utils.get_name_from_uuid(uuid))
            flags = ""
            for flag in properties['Flags']:
                flags = flags + flag + ","
            print(" CHR flags : ", flags)
        return


def properties_changed(interface, changed, invalidated, path):
    global device_path
    if path != device_path:
        return

    if 'ServicesResolved' in changed:
        sr = bluetooth_utils.dbus_to_python(changed['ServicesResolved'])
        print("ServicesResolved : ", sr)
        if sr == True:
            service_discovery_completed()





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
        bus.add_signal_receiver(properties_changed, dbus_interface = bluetooth_constants.DBUS_PROPERTIES, signal_name = "PropertiesChanged",
                path_keyword = "path")
        mainloop = GLib.MainLoop()
        mainloop.run()


print('----exit---')

