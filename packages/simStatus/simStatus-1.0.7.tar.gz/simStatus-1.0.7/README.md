# SimStatus
A simple interface to get updates from simulation programs.
## Installation
using pip:
```
pip install simStatus
```
## Usage
Import it and create your simStatus record:
```
import simStatus
simstatus = simStatus.simStatus('simulation title',qrcode = True, link = True)
```
it will generate a qrCode and link, which can be used to get updates from your simulation program.

In your code, at any time, you can send a new update.
Example:
```
simstatus.sendStatus(progress=50,status='run 4 of 8')
```
Note 1: it is recommended to keep the reported progress between 0 and 100 (%).
Note 2: you can leave `status` blank.
