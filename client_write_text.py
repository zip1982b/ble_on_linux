#!/usr/bin/python3
import bluetooth_constants
import bluetooth_utils
import dbus
import sys
import time
import dbus.mainloop.glib
from gi.repository import GLib

sys.path.insert(0, '.')

mainloop = None
bus = None
device_interface = None
device_path = None
found_led_service = False
found_led_characteristic = False
led_service_path = None
led_characteristic_path = None
text = None


def write_text(text):
    global led_characteristic_path
    char_proxy = bus.get_object(bluetooth_constants.BLUEZ_SERVICE_NAME, led_characteristic_path)
    char_interface = dbus.Interface(char_proxy, bluetooth_constants.GATT_CHARACTERISTIC_INTERFACE)
    try:
        ascii = bluetooth_utils.text_to_ascii_array(text)
        value = char_interface.WriteValue(ascii, {})
    except Exception as e:
        print("Failed to write to LED Text")
        print(e.get_dbus_name())
        print(e.get_dbus_message())
        return bluetooth_constants.RESULT_EXCEPTION
    else:
        print("LED TExt written OK")
        return bluetooth_constants.RESULT_OK




def service_discovery_completed():
    global found_led_service
    global found_led_characteristic
    global led_service_path
    global led_characteristic_path
    global bus
    global text

    if found_led_service and found_led_characteristic:
        print("Required service and characteristic found - device is OK")
        print("led service path: ",led_service_path)
        print("led characteristic path: ",led_characteristic_path)
        write_text(text)
    else:
        print("Required service and characteristic were not found - device is NOK")
        print("led service found: ",str(found_led_service))
        print("led text characteristic found: ",str(found_led_characteristic))
        bus.remove_signal_receiver(interfaces_added_sig_rcvd,"InterfacesAdded")
        bus.remove_signal_receiver(properties_changed,"PropertiesChanged")
        mainloop.quit()

def interfaces_added_sig_rcvd(path, interfaces):
    global found_led_service
    global found_led_characteristic
    global led_service_path
    global led_characteristic_path
    if bluetooth_constants.GATT_SERVICE_INTERFACE in interfaces:
        properties = interfaces[bluetooth_constants.GATT_SERVICE_INTERFACE]
        print("----------------------------------------------------------")
        print(f'service path: {path}')
        if 'UUID' in properties:
            uuid = properties['UUID']
            if uuid == bluetooth_constants.LED_SVC_UUID:
                found_led_service = True
                led_service_path = path
            print("service UUID: ", bluetooth_utils.dbus_to_python(uuid))
            print("service name: ", bluetooth_utils.get_name_from_uuid(uuid))
        return

    if bluetooth_constants.GATT_CHARACTERISTIC_INTERFACE in interfaces:
        properties = interfaces[bluetooth_constants.GATT_CHARACTERISTIC_INTERFACE]
        print(f'characteristic path: {path}')
        if 'UUID' in properties:
            uuid = properties['UUID']
            if uuid == bluetooth_constants.LED_TEXT_CHR_UUID:
                found_led_characteristic = True
                led_characteristic_path = path
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

if(len(sys.argv) != 3):
    print("usage: ./client_write_text.py [bdaddr] [text]")
    sys.exit(1)

dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

bdaddr = sys.argv[1]
text = sys.argv[2]
bus = dbus.SystemBus()
adapter_path = bluetooth_constants.BLUEZ_NAMESPACE + bluetooth_constants.ADAPTER_NAME
device_path = bluetooth_utils.device_address_to_path(bdaddr, adapter_path)
device_proxy = bus.get_object(bluetooth_constants.BLUEZ_SERVICE_NAME, device_path)

iface_prop = dbus.Interface(device_proxy, bluetooth_constants.DBUS_PROPERTIES) #интерфейс чтобы посмотреть свойства
con = iface_prop.Get(bluetooth_constants.DEVICE_INTERFACE, 'Connected') #для Connected()

device_interface = dbus.Interface(device_proxy, bluetooth_constants.DEVICE_INTERFACE)#интерфейс для конкретного устройства

if con:
    print('device is already connected')
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

