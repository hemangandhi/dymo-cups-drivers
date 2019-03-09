sudo cupsd

#sudo lpadmin -p labels -E -v usb://DYMO/LabelWriter%20450%20Turbo? -P ppd/lw450t.ppd
sudo lpadmin -p labels -E -v usb://DYMO/LabelWriter%20450%20Turbo?serial=07071200292292 -P ppd/lw450t.ppd
sudo cupsenable labels
sudo cupsaccept labels
