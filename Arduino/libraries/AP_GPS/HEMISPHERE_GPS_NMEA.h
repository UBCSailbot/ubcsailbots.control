// -*- tab-width: 4; Mode: C++; c-basic-offset: 4; indent-tabs-mode: t -*-
#ifndef HEMISPHERE_GPS_NMEA_h
#define HEMISPHERE_GPS_NMEA_h

#include <GPS.h>

#define GPS_BUFFERSIZE 120 

//#define NMEA_OUTPUT_SENTENCES 	"$PMTK314,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0*28\r\n" //Set GPGGA and GPVTG
//#define NMEA_OUTPUT_GGA 		"$PSRF103,0,0,1,1*25\r\n"
//#define NMEA_OUTPUT_VTG		"$PSRF103,5,0,1,1*20\r\n"

#define HEMISPHERE_OUTPUT_GGA 		"$JASC,GPGGA,20\r\n"			// GPGGA at 20Hz
#define HEMISPHERE_OUTPUT_VTG		"$JASC,GPVTG,20\r\n"			// GPVTG at 20Hz
#define HEMISPHERE_OUTPUT_HDT 		"$JASC,GPHDT,20\r\n"			// GPHDT at 20Hz
#define HEMISPHERE_GP_HEADING		"$JATT,NMEAHE,0\r\n"			// Use GPHDT heading NOT HEHDT

#define HEMISPHERE_BAUD_RATE_A_4800     "$JBAUD,4800\r\n"			// Set Current port(A) to 4800 Baud
#define HEMISPHERE_BAUD_RATE_A_9600     "$JBAUD,9600\r\n"			// Set Current port(A) to 9600 Baud
#define HEMISPHERE_BAUD_RATE_A_19200    "$JBAUD,19200\r\n"			// Set Current port(A) to 19200 Baud
#define HEMISPHERE_BAUD_RATE_A_38400    "$JBAUD,38400\r\n"			// Set Current port(A) to 38400 Baud
#define HEMISPHERE_BAUD_RATE_A_57600    "$JBAUD,57600\r\n"			// Set Current port(A) to 57600 Baud
#define HEMISPHERE_BAUD_RATE_A_115200   "$JBAUD,115200\r\n"			// Set Current port(A) to 115200 Baud

#define HEMISPHERE_BAUD_RATE_C_4800     "$JBAUD,4800,OTHER\r\n"			// Set Current port(C) to 4800 Baud
#define HEMISPHERE_BAUD_RATE_C_9600     "$JBAUD,9600,OTHER\r\n"			// Set Current port(C) to 9600 Baud
#define HEMISPHERE_BAUD_RATE_C_19200    "$JBAUD,19200,OTHER\r\n"			// Set Current port(C) to 19200 Baud
#define HEMISPHERE_BAUD_RATE_C_38400    "$JBAUD,38400,OTHER\r\n"			// Set Current port(C) to 38400 Baud
#define HEMISPHERE_BAUD_RATE_C_57600    "$JBAUD,57600,OTHER\r\n"			// Set Current port(C) to 57600 Baud
#define HEMISPHERE_BAUD_RATE_C_115200   "$JBAUD,115200,OTHER\r\n"			// Set Current port(C) to 115200 Baud

#define HEMISPHERE_PORT_C_SERIAL        "$JRELAY,PORTC,$JSERIALMODE"	     // Set Port C to SERIAL

#define HEMISPHERE_PORT_A_DATA_OFF      "$JOFF\r\n"                        // Turn all messages to OFF
#define HEMISPHERE_SHOW                 "$JSHOW\r\n"                        // SHOW CURRENT CONFIGURATION

/*
#define NMEA_BAUD_RATE_4800    	"$PSRF100,1,4800,8,1,0*0E\r\n"
#define NMEA_BAUD_RATE_9600    	"$PSRF100,1,9600,8,1,0*0D\r\n"
#define NMEA_BAUD_RATE_38400    "$PSRF100,1,38400,8,1,0*3D\r\n"  
#define NMEA_BAUD_RATE_57600    "$PSRF100,1,57600,8,1,0*36\r\n"

#define NMEA_OUTPUT_1HZ		"$PMTK220,1000*1F\r\n"
#define NMEA_OUTPUT_2HZ		"$PMTK220,500*2B\r\n"
#define NMEA_OUTPUT_4HZ		"$PMTK220,250*29\r\n"
#define NMEA_OTUPUT_5HZ		"$PMTK220,200*2C\r\n"
#define NMEA_OUTPUT_10HZ	"$PMTK220,100*2F\r\n"

#define SBAS_ON			"$PMTK313,1*2E\r\n"
#define SBAS_OFF		"$PMTK313,0*2F\r\n"

#define WAAS_ON			"$PSRF151,1*3F\r\n"
#define WAAS_OFF		"$PSRF151,0*3E\r\n"

#define DGPS_OFF		"$PMTK301,0*2C\r\n"
#define DGPS_RTCM		"$PMTK301,1*2D\r\n"
#define DGPS_SBAS		"$PMTK301,2*2E\r\n"

#define DATUM_GOOGLE		"$PMTK330,0*2E\r\n"

*/ 



class HEMISPHERE_GPS_NMEA : public GPS
{
  public:
    // Methods
	HEMISPHERE_GPS_NMEA(Stream *s);
	virtual void init();
	virtual bool read();
   //virtual void showStatus();    //*************************** JK

	// Properties
	uint8_t quality;    // GPS Signal quality

  private:
    // Internal variables
    uint8_t GPS_checksum;
    uint8_t GPS_checksum_calc;
	char buffer[GPS_BUFFERSIZE];
	int bufferidx;

	bool parse_nmea_gps(void);
	uint8_t parseHex(char c);
	long parsedecimal(char *str,uint8_t num_car);
	long parsenumber(char *str,uint8_t numdec);

};

#endif
