# add user to uinput user group
"""
sudo groupadd uinput
sudo usermod -a -G uinput $USER
sudo udevadm control --reload-rules
echo "SUBSYSTEM==\"misc\", KERNEL==\"uinput\", GROUP=\"uinput\", MODE=\"0660\"" | sudo tee /etc/udev/rules.d/99-uinput.rules
echo uinput | sudo tee /etc/modules-load.d/uinput.conf
"""

# /etc/udev/rules.d/99-uinput.rules
"""KERNEL=="uinput", GROUP:="input", MODE:="0660"
"""

