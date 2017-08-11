#!/usr/bin/env python

'''
urgslam.py : BreezySLAM Python with Hokuyo URG04LX Lidar
                 
Copyright (C) 2015 Simon D. Levy

This code is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as 
published by the Free Software Foundation, either version 3 of the 
License, or (at your option) any later version.

This code is distributed in the hope that it will be useful,     
but WITHOUT ANY WARRANTY without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU Lesser General Public License 
along with this code.  If not, see <http://www.gnu.org/licenses/>.
'''

MAP_SIZE_PIXELS         = 700
MAP_SIZE_METERS         = 3
LIDAR_DEVICE            = '/dev/ttyACM2'
mapa			= '/mapa1'
from breezyslam.algorithms import RMHC_SLAM
from breezyslam.components import URG04LX as LaserModel

from breezylidar import URG04LX as Lidar

from pltslamshow import SlamShow

from pgm_utils import pgm_save

if __name__ == '__main__':
    import sys

    #print sys.argv[1:][0]
    #+sys.argv[1:][0]
    # Connect to Lidar unit
    lidar = Lidar(LIDAR_DEVICE)

    # Create an RMHC SLAM object with a laser model and optional robot model
    slam = RMHC_SLAM(LaserModel(), MAP_SIZE_PIXELS, MAP_SIZE_METERS)

    # Set up a SLAM display
    display = SlamShow(MAP_SIZE_PIXELS, MAP_SIZE_METERS*1000/MAP_SIZE_PIXELS, 'SLAM')

    # Initialize empty map
    mapbytes = bytearray(MAP_SIZE_PIXELS * MAP_SIZE_PIXELS)

    while True:

        # Update SLAM with current Lidar scan
	scan=lidar.getScan()
        print scan
        slam.update(scan)
	
        # Get current robot position
        x, y, theta = slam.getpos()

        # Get current map bytes as grayscale
        slam.getmap(mapbytes)

        display.displayMap(mapbytes)

        display.setPose(x, y, theta)
	
	pgm_save('mapa',mapbytes,(MAP_SIZE_PIXELS,MAP_SIZE_PIXELS))
	
        # Exit on ESCape
        key = display.refresh()
        print key
        if not key:
            exit(0)
     
