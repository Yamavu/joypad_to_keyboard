
Python script to capture controller input and send keystrokes

gui programs like [Antimicro](https://github.com/AntiMicroX/antimicrox/) or [Input Remapper](https://github.com/sezanzeb/input-remapper) didn't work out for me

single dependancy: [python-evdev](https://github.com/gvalkov/python-evdev)

## Permissions
the tools above want superuser rights just to access uinput

### add user to uinput user group
```
sudo groupadd uinput
sudo usermod -a -G uinput $USER
sudo udevadm control --reload-rules
echo "SUBSYSTEM==\"misc\", KERNEL==\"uinput\", GROUP=\"uinput\", MODE=\"0660\"" | sudo tee /etc/udev/rules.d/99-uinput.rules
echo uinput | sudo tee /etc/modules-load.d/uinput.conf
```

### /etc/udev/rules.d/99-uinput.rules
```
KERNEL=="uinput", GROUP:="input", MODE:="0660"
```

