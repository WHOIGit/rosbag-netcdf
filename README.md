# Converting ROS bag data to NetCDF

## ROS bag reading workflow

Assuming you tag this image as `rosbag:latest`, here's how to run

```
docker run -v ${PWD}/data:/data -it --rm rosbag:latest bash
```

Inside the container, you can use the command `bag_csv` to extract information from a rosbag.

```
bag_csv -b /data/rosbags/phyto-arm_zeus_2023-02-09-19-11-39_0.bag -i /ctd -o ctd_data.csv
```

This will extract the `/ctd` topic to a csv file called `ctd_data.csv`

## NetCDF generation

* Reads two CSV files, one for `/ctd` and one for `/gps/fix`
* Subsets columns
* Interpolates the GPS data to the CTD timebase
* Writes NetCDF

