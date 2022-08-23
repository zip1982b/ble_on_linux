dbus.Dictionary(
        {   dbus.String('Address'): dbus.String('60:1C:F5:04:60:FE', variant_level=1),
            dbus.String('AddressType'): dbus.String('random', variant_level=1),
            dbus.String('Alias'): dbus.String('60-1C-F5-04-60-FE', variant_level=1),
            dbus.String('Paired'): dbus.Boolean(False, variant_level=1),
            dbus.String('Trusted'): dbus.Boolean(False, variant_level=1),
            dbus.String('Blocked'): dbus.Boolean(False, variant_level=1),
            dbus.String('LegacyPairing'): dbus.Boolean(False, variant_level=1),
            dbus.String('Connected'): dbus.Boolean(False, variant_level=1),
            dbus.String('UUIDs'): dbus.Array([], signature=dbus.Signature('s'), variant_level=1),
            dbus.String('Adapter'): dbus.ObjectPath('/org/bluez/hci0', variant_level=1),
            dbus.String('ServicesResolved'): dbus.Boolean(False, variant_level=1)
        },
        signature=dbus.Signature('sv'))

received signal
path = /org/bluez/hci0/dev_6D_9E_14_7C_30_26/service0001 #путь к объекту (правое окно в d-feet)
interfaces = dbus.Dictionary(
{
dbus.String('org.freedesktop.DBus.Introspectable'): dbus.Dictionary({}, signature=dbus.Signature('sv')),
dbus.String('org.bluez.GattService1'): 
                    dbus.Dictionary(
                        {dbus.String('UUID'): dbus.String('00001801-0000-1000-8000-00805f9b34fb', variant_level=1),
                         dbus.String('Device'): dbus.ObjectPath('/org/bluez/hci0/dev_6D_9E_14_7C_30_26', variant_level=1),
                         dbus.String('Primary'): dbus.Boolean(True, variant_level=1),
                         dbus.String('Includes'): dbus.Array([], signature=dbus.Signature('o'), variant_level=1)
                        }, signature=dbus.Signature('sv')
                        ),

dbus.String('org.freedesktop.DBus.Properties'): dbus.Dictionary({}, signature=dbus.Signature('sv'))
}, signature=dbus.Signature('sa{sv}')
)
end

interfaces = {'org.freedesktop.DBus.Introspectable': {},
        'org.bluez.GattService1': {'UUID': '00001801-0000-1000-8000-00805f9b34fb', 'Device': '/org/bluez/hci0/dev_6D_9E_14_7C_30_26', 'Primary': True, 'Includes': []}
        'org.freedesktop.DBus.Properties': {}
        }

received signal
path = /org/bluez/hci0/dev_6D_9E_14_7C_30_26/service0001/char0002
interfaces = dbus.Dictionary(
        {dbus.String('org.freedesktop.DBus.Introspectable'): dbus.Dictionary({}, signature=dbus.Signature('sv')),
        dbus.String('org.bluez.GattCharacteristic1'): 
            dbus.Dictionary(
                {dbus.String('UUID'): dbus.String('00002a05-0000-1000-8000-00805f9b34fb', variant_level=1), 
                dbus.String('Service'): dbus.ObjectPath('/org/bluez/hci0/dev_6D_9E_14_7C_30_26/service0001', variant_level=1),
                dbus.String('Value'): dbus.Array([], signature=dbus.Signature('y'), variant_level=1), 
                dbus.String('Notifying'): dbus.Boolean(False, variant_level=1),
                dbus.String('Flags'): dbus.Array([dbus.String('indicate')], signature=dbus.Signature('s'), variant_level=1)
                }, signature=dbus.Signature('sv')), 
        dbus.String('org.freedesktop.DBus.Properties'): dbus.Dictionary({}, signature=dbus.Signature('sv'))
        }, signature=dbus.Signature('sa{sv}')
        )
end


