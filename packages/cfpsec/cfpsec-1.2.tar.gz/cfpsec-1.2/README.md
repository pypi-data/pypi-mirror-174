# cfpsec

CFPsec is program to list Call For Papers or upcoming Hacking/Security Conferences based on cfptime.org website.

Copyright (C)  2022 Alexandre Borges <alexandreborges at blackstormsecurity dot com>

      This program is free software: you can redistribute it and/or modify
      it under the terms of the GNU General Public License as published by
      the Free Software Foundation, either version 3 of the License, or
      (at your option) any later version.

      This program is distributed in the hope that it will be useful,
      but WITHOUT ANY WARRANTY; without even the implied warranty of
      MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
      GNU General Public License for more details.

      See GNU Public License on <http://www.gnu.org/licenses/>.
      
 # Current Version: 1.2
 
 CFPsec has been tested on Ubuntu and Windows 11. Likely, it also works on other 
 operating systems. Before using CFPsec, execute:

        $ Install Python 3.9 or newer.
        $ pip install cfpsec
 
 # USAGE

To use the CFPsec, execute the command as shown below:

      # cfpsec.py -c 1 
      # cfpsec.py -u 1 

      usage: usage: python cfpsec.py -c <0|1> -u <0|1> -w <0|1>
      
      Optional arguments:
      
      -h, --help            show this help message and exit
      -c CFP, --cfp CFP     List Call For Papers of Hacking/Securiy Conferences.
      -u UPCOMING, --upcoming UPCOMING List all upcoming Hacking/Security Conferences.
      -w WIN, --win WIN     Set to 1 whether you are running it on Windows 10 or older.
 
 # HISTORY

Version 1.2:

      This version:
      
            * Small fixes have been introduced. 
            * Small structure change. 

Version 1.0.2:

      This version:
      
            * Introduces a small fix. 

Version 1.0.1:

      This version:
      
            * Introduces the possibility to install the cfpsec by using the Python pip module: pip install cfpsec. 

Version 1.0:

      This version:
      
            * Includes the -c option to list Call for Papers of Hacking/Security Conferences. 
            * Includes the -u option to list upcoming Hacking/Security Conferences.
