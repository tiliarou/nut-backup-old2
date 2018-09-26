Homebrew network title installer, and title key dumper.

If the app hangs when you launch it, it means you didnt edit the junk info out of locations.conf and its hung up waiting for timeout.

![alt text](https://raw.githubusercontent.com/blawar/nut/master/dz/ss.jpg)

# Supported Protocols #
### FTP ###
Regular FTP, not FTPS, not SFTP, normal plain jane FTP.

### HTTP ###
Http requires directory listing / browsing be enabled!

# Installation

 - Create the directory /switch/dz/ on your switch's SD card.
 
 - Copy dz.nro to /switch/dz/dz.nro .
 
 - Obtain or generate a keys.txt file and place it in /switch/dz/keys.txt .  keys.txt is a text file containing various switch encryption keys.  If you plan to generate it yourself, you can find instructions here:  https://gbatemp.net/threads/how-to-get-switch-keys-for-hactool-xci-decrypting.506978/
 
 - Copy locations.conf to /switch/dz/locations.conf .  You should edit this file, it is only an example, and points to the various local and network locations hosting your switch content.

# Disclaimer

Use at your own risk, and always have a NAND backup.'

# Dumping Title Keys

Title keys are saved to sdmc:/switch/dz/titlekeys.txt when dumped.

# Backing up title keys

You can place a single http url into /switch/dz/titlekeys.url.txt , to automatically submit your keys to that url to back them up.

# Credits

Tinfoil source code was reverse-engineered with plenty of help from Adubbz answering questions:
https://github.com/Adubbz/Tinfoil

HACTOOL source code was reverse-engineered, with small bits of code lifted here and there:
https://github.com/SciresM/hactool

Random JSON parser:
https://github.com/nlohmann/json
