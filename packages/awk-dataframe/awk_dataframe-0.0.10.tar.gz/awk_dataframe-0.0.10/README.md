# awk_dataframe

This library is intended to use for fast and low RAM memory consumption of very large .csv files. It works by accumulating a sequence of awk commands that will be executed through pipes in bash when the actual values of the dataframe are to be consumed.

## First things first

This is an wrapper around AWK for its use as a dataframe implementation, therefore, it won't work unless you are using a Linux distribution that can run BASH and AWK. It could work on a macOS but I haven't tested it. I am personally running Ubuntu 22.04.

It will also not work if your regional settings use the comma as the decimal separator. One way to change this is to set the regional settings to the UK as follows:

```
sudo update-locale LC_NUMERIC="en_GB.UTF-8"
```

and then logout of your system.

## Disk usage

Not only this library runs directly from the hard drive trying to avoid RAM limitations which will degrade your hard drive.
It also stores temporary files into the ```~/.tmp``` folder. Altough they should be deleted automatically, please check from time to time, since there might be some bug that leaves files behind. Also, although it will be automatically created, make sure that it already exists in your disk, in order to avoid failures at creation time due to permissions.

Most commands do not take time, but be advised that ```print(df)```, ```df.head()```, ```df.values()```, ```df.to_pandas()```, ```df.to_npd()``` and ```df.to_csv(path)``` will run the full set of commands and might take time, avoid using them as much as possible. The best implementation would be to generate all conditions for subsetting and then either going to a pandas/numpy_dataframe object if you want to further manipulate in RAM or using ```df.to_csv(path)``` to save the results to the hard drive.

Using ```df.to_csv(path)``` consolidates the set of commands to run and deletes them, starting anew (but with the same data) and therefore runs faster. Consider using that function to create intermediate points in your calculation.

## Authors and acknowledgment
Implemented by Carlos Molinero.

## License
MIT license.


## Project status
Currently this is an early implementation, meaning that it is in a very unstable state, and the syntax might change and bugs may arise. I do not recommend installing it, I am publishing it for my personal use.
