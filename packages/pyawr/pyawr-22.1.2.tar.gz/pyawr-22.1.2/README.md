## pyawr: Module for interfacing Python with the AWR Design Environment 

AWR Design Enviroment Python interface module that supports code-completion using external IDEs. 

# Installation
    pip install pyawr

# Upgrade

    pip install --upgrade pyawr

# Requirements
* Python >= 3.9
* pywin32 >= 220

# Usage

    import pyawr.mwoffice as mwoffice
	awrde = mwo.CMWOffice()
	
# History

# 22.1.2
* AWRDE 22.1.2
* Changed the version name to follow Cadence naming conventions

# 16.1.0
* AWRDE 16.01 release

# 16.0.2
* Added version and CLSID options when calling CMWOffice()

# 16.0.1
* Resolved variable names with double underscores