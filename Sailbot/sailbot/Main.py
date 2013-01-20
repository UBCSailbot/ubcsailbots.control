'''
Created on Jan 19, 2013

@author: joshandrews
'''
import sys

def main(argv=None):
    if argv is None:
        argv = sys.argv
    
    challenge = argv[1]
    if (challenge == "long_distance"):
        challenge.longdistance.run()
    if (challenge == "navigation"):
        challenge.navigation.run()
    if (challenge == "station_keeping"):
        challenge.stationkeeping.run()
    
    
    
if __name__ == '__main__':
    sys.exit(main())
