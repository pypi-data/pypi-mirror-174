# awk_dataframe

## First things first

This is an wrapper around AWK for its use as a dataframe implementation, therefore, it won't work unless you are using a Linux distribution that can run BASH and AWK. It could work on a macOS but I haven't tested it. I am personally running Ubuntu 22.04.

It will also not work if your regional settings use the comma as the decimal separator. One way to change this is to set the regional settings to the UK as follows:

```Shell
sudo update-locale LC_NUMERIC="en_GB.UTF-8"
```

and then logout of your system.

## Authors and acknowledgment
Implemented by Carlos Molinero.

## License
MIT license.


## Project status
Currently this is an early implementation, meaning that it is in a very unstable state, and the syntax might change and bugs may arise. I do not recommend installing it, I am publishing it for my personal use.
