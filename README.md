# These are useless on cupcake:

some command examples:

- print very long text on a tape:
lpr -o landscape -o PageSize=24_mm__1___Label__Auto_ test.txt

- set printing options specific to the LabelWriter driver
lpr -o PageSize=30252_Address -o PrintQuality=Graphics -o PrintDensity=Light test.txt

- set printing options specific to the LabelManager driver
lpr -o PageSize=Address_Label -o CutOptions=ChainMarks -o LabelAlignment=Right -o TapeColor=1

# What to do when you plug in the printer:
1) ./setup_printer.sh
2) ./qr_script.py <email=rnd@hackru.org> <name=Ms. Cupcake>

# How to change the labels:
1) Go to samples/test_labels.
2) Edit TestLabel.cpp
3) `make` (in the directory)
4) `./TestLabel <printer name> <email> <name> <opt = "">` where if the opt is passed,
   the printer is not run.
5) Open label.png if you did not run the printer.

# Gotchas:
1) Make sure that image paths are absolute in the python. Images are in `samples/test_label`
   as needed by the C++ executable.
2) CUPS 1.5 or later has deprecated the PPD API, so this driver currently does not work there.
   You have to install it from source.
3) You have to build automake-1.10 from source to build this.
