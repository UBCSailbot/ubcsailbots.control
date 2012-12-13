


//UBCsailBot2012_2_14_5

//Ver. 2.14.5
//Last update by John K. June 9, 2012
//changed LD Tack test to include apparent wind <= 35
//added no tack until 5sec. elapsed
//added leeway and sheet adjust on slow and fast station keeping exit
//added restricted rudder for leeward mark roundings when beat to start line
//added weather dependent (time vary) LD Tack
//added PID clamping for first 5 sec. on test routine - will add to other challenges 
//removed PID Clamping
//Changed the radius for LD race

#include <FastSerial.h>
#include <AP_Math.h>
#include <AP_Common.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <APM_RC.h>
#include <Wire.h>
#include <math.h>
#include <AP_GPS.h>         // ArduPilot GPS libray
#include <ChallengeClass.h>
#include <PIDv1.h>  
#include <avr/pgmspace.h>

#define PIx 3.141592653589793
#define RADIUS 63718
#define ToDeg(x) (x*57.29577951308233)
#define ToRadians(x) (x*0.017453292519943)
#define LonX(x) (x*0.007303173)
#define LatY(x) (x*0.011131885)
#define MeterToLonX(x) (x*136.926785111074)
#define MeterToLatY(x) (x*89.83220455161008)

#define rudder_output 0
#define sheet_output 1
#define RC_sail 1200
#define Read_GUI_Data_Challenge_Finished 1200

#define UPWIND_APPRENT_LIMIT_WEATHER_0  30                                                         // weather code 0 settings - upwind apprent limit

#define UPWIND_APPRENT_LIMIT_WEATHER_1  30                                                         // weather code 1 settings - upwind apprent limit 

#define UPWIND_APPRENT_LIMIT_WEATHER_2  30                                                         // weather code 2 settings - upwind apprent limit 

#define UPWIND_APPRENT_LIMIT_WEATHER_3  35                                                         // weather code 3 settings - upwind apprent limit



double rudder_centre = 1519;
double rudder_increment = 8.97;
double sheet_end = 1932;
double sheet_increment = 9.53736;
         
int y = 1500;


enum course_descp {
  B,CCR,CR,R,BR,BBR,DR,J};    //used to read sheet_setting[course_descp][weather]

enum tack_type {
  reach,beat,bear_off,gybe};  //used to read tack_rudder_angles[tack_type][weather] 
  
enum sailByCourse {  
  compassMethod,
  cogMethod,
  apprentWindMethod  
};  
 
int tack_rudder_angles[4][4] = {
  { 80,80,80,80}
  ,{80,80,80,90}
  ,{70,70,80,90}
  ,{80,70,80,90}
};


/*
int sheet_setting[8][4] = {
   {85,95,95,90}
  ,{85,95,95,90}
  ,{75,80,80,65}
  ,{60,60,60,50}
  ,{40,40,40,35}
  ,{25,25,25,25}
  ,{15,5,5,15}
  ,{35,20,20,35}
}; 
*/

int sheet_setting[8][4] = {
   {95,100,100,100}
  ,{90,86,86,86}
  ,{78,73,73,73}
  ,{57,54,54,54}
  ,{40,38,38,38}
  ,{29,29,29,29}
  ,{25,18,18,18}
  ,{35,20,20,35}
}; 

int  SR[4] = {15,2,2,2};
                
int weather = 0; 
boolean starboard;

double Setpoint,Input,Output; //PID variables 
PID rudder(&Input,&Output,&Setpoint,1,0.05,0.25,DIRECT);//used to Initialize PID
double course;
double current_heading;
int COG;
int intSOG;
double SOG;

int apprentWind = 0;
//int appWind1SecAvg = 0;
int appWind2SecAvg = 0; 
int appWind6SecAvg = 0;
//int appWind30SecAvg = 0;

//int heading30SecAvg = 0;
//int heading15SecAvg = 0;
//int heading2SecAvg = 0;

//int sog30SecAvg = 0;
//float sog15SecAvg = 0.0;
float sog2SecAvg = 0.0;

//static int apprentSheetSettings[181];  
//static int sogArray[4][181];  

prog_int16_t PROGMEM sogArray[181][4]   = 
{{ 119,131,175,183},
{ 119,131,175,183},
{ 119,131,175,183},
{ 119,131,175,183},
{ 119,131,175,183},
{ 119,131,175,183},
{ 119,131,175,183},
{ 119,131,175,183},
{ 119,131,175,183},
{ 119,131,175,183},
{ 119,131,175,183},
{ 119,131,175,183},
{ 119,131,175,183},
{ 119,131,175,183},
{ 119,131,175,183},
{ 119,131,175,183},
{ 119,131,175,183},
{ 119,131,175,183},
{ 119,131,175,183},
{ 119,131,175,183},
{ 119,131,175,183},
{ 119,131,175,183},
{ 119,131,175,183},
{ 119,131,175,183},
{ 119,131,175,183},
{ 119,131,175,183},
{ 119,131,175,183},
{ 123,131,175,183},
{ 128,131,175,183},
{ 129,132,176,183},
{ 131,134,177,183},
{ 133,136,179,183},
{ 134,138,180,183},
{ 136,139,181,183},
{ 138,141,183,184},
{ 138,143,184,186},
{ 139,145,186,188},
{ 140,146,187,189},
{ 141,147,189,191},
{ 142,149,191,193},
{ 143,150,193,195},
{ 144,151,195,197},
{ 145,153,197,199},
{ 146,154,199,201},
{ 147,156,201,204},
{ 147,156,202,206},
{ 147,157,203,208},
{ 148,158,205,211},
{ 148,159,206,212},
{ 149,159,207,213},
{ 149,160,209,215},
{ 149,161,210,216},
{ 150,162,212,218},
{ 150,163,213,219},
{ 151,163,214,221},
{ 151,164,216,222},
{ 151,165,217,223},
{ 151,166,219,225},
{ 151,167,218,226},
{ 151,167,218,228},
{ 151,168,218,229},
{ 151,169,218,231},
{ 151,169,218,231},
{ 151,170,218,231},
{ 151,171,217,231},
{ 151,171,217,231},
{ 151,172,217,231},
{ 151,173,217,231},
{ 152,173,217,232},
{ 150,174,217,232},
{ 149,175,217,232},
{ 148,175,216,232},
{ 147,175,216,232},
{ 146,175,216,232},
{ 145,175,216,233},
{ 144,175,215,233},
{ 143,176,215,233},
{ 142,176,215,233},
{ 141,176,215,234},
{ 140,176,215,234},
{ 139,176,214,234},
{ 138,176,214,234},
{ 137,177,214,235},
{ 136,177,214,235},
{ 136,177,213,235},
{ 135,177,213,235},
{ 134,177,213,236},
{ 133,177,213,236},
{ 132,178,213,236},
{ 132,176,212,236},
{ 131,175,212,237},
{ 130,174,211,237},
{ 129,173,211,237},
{ 128,172,211,238},
{ 128,171,210,238},
{ 127,170,210,238},
{ 126,169,210,239},
{ 125,168,210,239},
{ 124,167,210,240},
{ 124,166,211,240},
{ 123,165,211,240},
{ 122,164,212,241},
{ 122,163,212,241},
{ 121,162,213,242},
{ 120,162,213,243},
{ 120,161,213,244},
{ 119,160,214,246},
{ 118,159,214,247},
{ 118,158,215,248},
{ 117,157,215,250},
{ 116,156,216,251},
{ 116,155,216,253},
{ 115,155,217,254},
{ 115,154,215,255},
{ 114,153,214,257},
{ 113,152,213,258},
{ 113,151,212,259},
{ 112,150,211,261},
{ 111,149,209,262},
{ 111,148,208,264},
{ 110,147,207,263},
{ 109,146,206,262},
{ 109,145,205,262},
{ 108,144,204,261},
{ 108,143,202,260},
{ 106,142,201,260},
{ 104,141,200,259},
{ 103,140,199,258},
{ 103,139,198,258},
{ 103,138,196,257},
{ 103,137,195,257},
{ 103,136,194,256},
{ 103,135,193,255},
{ 103,134,192,255},
{ 103,134,191,254},
{ 103,133,190,253},
{ 103,132,189,253},
{ 103,131,189,252},
{ 103,130,188,252},
{ 103,129,187,251},
{ 103,128,187,250},
{ 103,127,186,250},
{ 103,127,185,249},
{ 103,127,185,248},
{ 103,127,184,248},
{ 103,127,184,247},
{ 103,127,183,247},
{ 103,127,182,246},
{ 103,127,182,245},
{ 103,127,181,245},
{ 103,127,180,244},
{ 103,127,180,243},
{ 103,127,179,243},
{ 103,127,179,242},
{ 103,127,178,242},
{ 103,127,177,241},
{ 103,127,177,240},
{ 103,127,176,240},
{ 103,127,175,239},
{ 103,127,175,238},
{ 103,127,174,238},
{ 103,127,174,237},
{ 103,127,173,237},
{ 103,127,172,236},
{ 103,127,172,235},
{ 103,127,171,235},
{ 103,127,170,234},
{ 103,127,170,233},
{ 103,127,169,233},
{ 103,127,169,232},
{ 103,127,169,232},
{ 103,127,169,232},
{ 103,127,169,232},
{ 103,127,169,232},
{ 103,127,169,232},
{ 103,127,169,232},
{ 103,127,169,232},
{ 103,127,169,232},
{ 103,127,169,232},
{ 103,127,169,232},
{ 103,127,169,232}};


prog_int16_t PROGMEM apprentSheetSettings[181][4] =

{{ 95,100,100,100},
{ 95,100,100,100},
{ 95,100,100,100},
{ 95,100,100,100},
{ 95,100,100,100},
{ 95,100,100,100},
{ 95,100,100,100},
{ 95,100,100,100},
{ 95,100,100,100},
{ 95,100,100,100},
{ 95,100,100,100},
{ 95,100,100,100},
{ 95,100,100,100},
{ 95,100,100,100},
{ 95,100,100,100},
{ 95,100,100,100},
{ 95,100,100,100},
{ 95,100,100,100},
{ 95,100,100,100},
{ 95,100,100,100},
{ 95,100,100,100},
{ 95,100,100,100},
{ 95,100,100,100},
{ 95,100,100,100},
{ 95,100,100,100},
{ 95,100,100,100},
{ 95,100,100,100},
{ 95,100,100,100},
{ 95,100,100,100},
{ 95,100,100,100},
{ 95,100,100,100},
{ 95,99,99,99},
{ 95,98,98,98},
{ 95,97,97,97},
{ 95,96,96,96},
{ 95,95,95,95},
{ 95,94,94,94},
{ 95,93,93,93},
{ 95,92,92,92},
{ 95,91,91,91},
{ 95,90,90,90},
{ 95,89,89,89},
{ 95,88,88,88},
{ 95,87,86,86},
{ 94,86,86,86},
{ 94,84,84,84},
{ 94,82,82,82},
{ 93,80,80,80},
{ 93,78,78,78},
{ 93,76,76,76},
{ 92,74,74,74},
{ 92,73,73,73},
{ 91,72,72,72},
{ 91,71,71,71},
{ 91,70,70,70},
{ 90,69,69,69},
{ 90,67,67,67},
{ 89,66,66,66},
{ 89,65,65,65},
{ 88,64,64,64},
{ 87,62,62,62},
{ 86,61,61,61},
{ 86,60,60,60},
{ 85,59,59,59},
{ 85,58,58,58},
{ 84,57,57,57},
{ 84,56,56,56},
{ 83,55,55,55},
{ 82,54,54,54},
{ 81,53,53,53},
{ 80,51,55,58},
{ 79,50,54,57},
{ 78,48,53,56},
{ 77,47,53,55},
{ 75,45,52,55},
{ 74,44,52,54},
{ 72,42,51,53},
{ 71,41,51,53},
{ 69,39,50,52},
{ 68,38,50,52},
{ 66,37,49,51},
{ 65,36,48,51},
{ 64,35,35,35},
{ 62,35,35,35},
{ 61,34,34,34},
{ 59,34,34,34},
{ 58,34,34,34},
{ 58,33,33,33},
{ 57,33,33,33},
{ 56,33,33,33},
{ 55,32,32,32},
{ 55,32,32,32},
{ 54,32,32,32},
{ 54,31,31,31},
{ 53,31,31,31},
{ 52,30,30,30},
{ 52,30,30,30},
{ 51,30,30,30},
{ 50,30,30,30},
{ 50,30,30,30},
{ 49,30,30,30},
{ 48,30,30,30},
{ 48,30,30,30},
{ 47,30,30,30},
{ 47,30,30,30},
{ 46,30,30,30},
{ 46,29,29,29},
{ 45,29,29,29},
{ 45,29,29,29},
{ 44,29,29,29},
{ 43,29,29,29},
{ 42,29,29,29},
{ 41,29,29,29},
{ 40,29,29,29},
{ 39,29,29,29},
{ 38,29,29,29},
{ 37,29,29,29},
{ 36,29,29,29},
{ 35,28,28,28},
{ 35,28,28,28},
{ 34,28,28,28},
{ 34,28,28,28},
{ 34,28,28,28},
{ 33,28,28,28},
{ 33,28,28,28},
{ 33,28,28,28},
{ 32,28,28,28},
{ 32,28,28,28},
{ 32,28,28,28},
{ 31,27,27,27},
{ 31,25,25,25},
{ 31,24,24,24},
{ 30,23,23,23},
{ 30,21,21,21},
{ 30,20,20,20},
{ 30,18,18,18},
{ 30,18,18,18},
{ 30,18,18,18},
{ 30,18,18,18},
{ 30,18,18,18},
{ 29,18,18,18},
{ 29,18,18,18},
{ 29,18,18,18},
{ 29,17,17,17},
{ 29,17,17,17},
{ 28,17,17,17},
{ 28,17,17,17},
{ 28,17,17,17},
{ 28,17,17,17},
{ 28,16,16,16},
{ 27,16,16,16},
{ 26,16,16,16},
{ 25,16,16,16},
{ 24,16,16,16},
{ 23,16,16,16},
{ 22,15,15,15},
{ 21,15,15,15},
{ 20,15,15,15},
{ 19,15,15,15},
{ 18,15,15,15},
{ 17,14,14,14},
{ 16,14,14,14},
{ 15,14,14,14},
{ 14,14,14,14},
{ 13,14,14,14},
{ 13,13,13,13},
{ 13,13,13,13},
{ 13,13,13,13},
{ 13,13,13,13},
{ 13,13,13,13},
{ 13,13,13,13},
{ 13,13,13,13},
{ 13,13,13,13},
{ 13,13,13,13},
{ 13,13,13,13},
{ 13,13,13,13},
{ 13,13,13,13},
{ 13,13,13,13},
{ 13,13,13,13},
{ 13,13,13,13},
{ 13,13,13,13}};


/*
{{ 95,100,100,100},
{ 95,100,100,100},
{ 95,100,100,100},
{ 95,100,100,100},
{ 95,100,100,100},
{ 95,100,100,100},
{ 95,100,100,100},
{ 95,100,100,100},
{ 95,100,100,100},
{ 95,100,100,100},
{ 95,100,100,100},
{ 95,100,100,100},
{ 95,100,100,100},
{ 95,100,100,100},
{ 95,100,100,100},
{ 95,100,100,100},
{ 95,100,100,100},
{ 95,100,100,100},
{ 95,100,100,100},
{ 95,100,100,100},
{ 95,100,100,100},
{ 95,100,100,100},
{ 95,100,100,100},
{ 95,100,100,100},
{ 95,100,100,100},
{ 95,100,100,100},
{ 95,100,100,100},
{ 95,100,100,100},
{ 95,100,100,100},
{ 95,100,100,100},
{ 95,99,99,99},
{ 95,98,98,98},
{ 95,97,97,97},
{ 95,96,96,96},
{ 95,95,95,95},
{ 95,94,94,94},
{ 95,93,93,93},
{ 95,92,92,92},
{ 95,91,91,91},
{ 95,90,90,90},
{ 95,89,89,89},
{ 95,88,88,88},
{ 95,87,86,86},
{ 94,86,86,86},
{ 94,84,84,84},
{ 94,82,82,82},
{ 93,80,80,80},
{ 93,78,78,78},
{ 93,76,76,76},
{ 92,74,74,74},
{ 92,73,73,73},
{ 91,72,72,72},
{ 91,71,71,71},
{ 91,70,70,70},
{ 90,69,69,69},
{ 90,67,67,67},
{ 89,66,66,66},
{ 89,65,65,65},
{ 88,64,64,64},
{ 87,62,62,62},
{ 86,61,61,61},
{ 86,60,60,66},
{ 85,59,59,59},
{ 84,57,57,57},
{ 84,56,56,56},
{ 83,55,55,55},
{ 82,54,54,54},
{ 81,53,53,53},
{ 80,51,55,58},
{ 79,50,54,57},
{ 78,48,53,56},
{ 77,47,53,55},
{ 75,45,52,55},
{ 74,44,52,54},
{ 72,42,51,53},
{ 71,41,51,53},
{ 69,39,50,52},
{ 68,38,50,52},
{ 66,37,49,51},
{ 65,36,48,51},
{ 64,35,35,35},
{ 62,35,35,35},
{ 61,34,34,34},
{ 59,34,34,34},
{ 58,33,33,33},
{ 57,33,33,33},
{ 56,33,33,33},
{ 56,32,32,32},
{ 55,32,32,32},
{ 54,32,32,32},
{ 54,31,31,31},
{ 53,31,31,31},
{ 52,30,30,30},
{ 52,30,30,30},
{ 51,30,30,30},
{ 50,30,30,30},
{ 50,30,30,30},
{ 49,32,32,40},
{ 48,30,30,30},
{ 48,30,30,30},
{ 47,30,30,30},
{ 47,30,30,30},
{ 46,30,30,30},
{ 46,29,29,29},
{ 45,29,29,29},
{ 45,29,29,29},
{ 44,29,29,29},
{ 43,29,29,29},
{ 42,29,29,29},
{ 41,29,29,29},
{ 40,29,29,29},
{ 39,29,29,29},
{ 38,29,29,29},
{ 37,29,29,29},
{ 36,29,29,29},
{ 35,28,28,28},
{ 35,28,28,28},
{ 34,28,28,28},
{ 34,28,28,28},
{ 34,28,28,28},
{ 33,28,28,28},
{ 33,28,28,28},
{ 33,28,28,28},
{ 32,28,28,28},
{ 32,28,28,28},
{ 32,28,28,28},
{ 31,27,27,27},
{ 31,25,25,25},
{ 31,24,24,24},
{ 30,23,23,23},
{ 30,21,21,21},
{ 30,20,20,20},
{ 30,18,18,18},
{ 30,18,18,18},
{ 30,18,18,18},
{ 30,18,18,18},
{ 30,18,18,18},
{ 29,18,18,18},
{ 29,18,18,18},
{ 29,18,18,18},
{ 29,17,17,17},
{ 29,17,17,17},
{ 28,17,17,17},
{ 28,17,17,17},
{ 28,17,17,17},
{ 28,17,17,17},
{ 28,16,16,16},
{ 27,16,16,16},
{ 26,16,16,16},
{ 25,16,16,16},
{ 24,16,16,16},
{ 23,16,16,16},
{ 22,15,15,15},
{ 21,15,15,15},
{ 20,15,15,15},
{ 19,15,15,15},
{ 18,15,15,15},
{ 17,14,14,14},
{ 16,14,14,14},
{ 15,14,14,14},
{ 14,13,13,13},
{ 13,13,13,13},
{ 13,13,13,13},
{ 13,13,13,13},
{ 13,13,13,13},
{ 13,13,13,13},
{ 13,13,13,13},
{ 13,13,13,13},
{ 13,13,13,13},
{ 13,13,13,13},
{ 13,13,13,13},
{ 13,13,13,13},
{ 13,13,13,13},
{ 13,13,13,13},
{ 13,13,13,13},
{ 13,13,13,13},
{ 13,13,13,13},
{ 13,13,13,13},
{ 13,13,13,13},
{ 13,13,13,13},
{ 13,13,13,13}};

*/
int numberSatelites;

//long gps_timer = 0;
//long radio_timer = 0;
long update_timer = 0;
long windTimer = 0;
long gpsTimer = 0;

struct Waypoint{
  long latitude;
  long longitude;
};

Waypoint *current_position = new Waypoint;


int radio_in[8];      // current values from the transmitter - microseconds
int radio_out[2];     // Output......0(rudder)  1(sheet winch)
int  pilot_switch = 1200;  
int  data_input_switch = 1200;


FastSerialPort0(Serial);    // FTDI/console
FastSerialPort1(Serial1);   // GPS port (except for GPS_PROTOCOL_IMU)
FastSerialPort2(Serial2);   // Aprrent Wind read from 2nd processor
FastSerialPort3(Serial3);   // xBee communication between boat and laptop

boolean data_received = false;
boolean sailingChallenge = false;
//int inCount = 0;

GPS         *g_gps;
HEMISPHERE_GPS_NMEA     g_gps_driver(&Serial1);

Encoder          *windEncoder;
EncoderRead      encoder_driver(&Serial2);

//Reader          *readData;
//DataRead      data_driver(&Serial3);

Challenge challenge;        // Used to hold Challenge data sent from GUI






//***********************************************************************************************************************************

void setup()
{

  delay(500);          //Wait at least 500 milli-seconds for device initialization
  Wire.begin();        // join i2c bus (address optional for master)
  
  Serial.begin(57600, 128, 128);  
  Serial1.begin(57600, 128, 128); 
  Serial2.begin(9600,128,128);
  Serial3.begin(57600, 256, 128);

  
  g_gps = &g_gps_driver;
  g_gps->init(); 
  
  windEncoder = &encoder_driver;
  windEncoder->init();
  
  //readData = &data_driver;
 // readData->init();  
  			// GPS Initialization
  APM_RC.Init();                        // Radio Initialization
  pilot_switch = 968;
  
}

//***********************************************************************************************************************************

void loop()
{
  
 
    read_radio();
     
 
    if(pilot_switch < RC_sail || data_input_switch < Read_GUI_Data_Challenge_Finished )      // This needs more testing
      rc_sail(); 
    else
      if(data_received)
         challenge_sail();
 

  
}

//***********************************************************************************************************************************

void read_radio(void)
{
 
    
           
        for (int y = 0; y < 4; y++)  
            radio_in[y] = APM_RC.InputCh(y);
               
        
        data_input_switch = radio_in[2];
        pilot_switch = radio_in[3]; 

}

//***********************************************************************************************************************************

void update_GPS(void)
{
    
    g_gps->update();
    current_position -> latitude = g_gps->latitude;
    current_position -> longitude = g_gps->longitude;  
    COG = ((double)(g_gps -> ground_course ))/100;
    intSOG = (int)g_gps->ground_speed;
    SOG = ((double)intSOG)/100;     
    current_heading = ((double)(g_gps -> true_heading))/100; 
    numberSatelites = g_gps -> hemisphereSatelites;  
 
}

//***********************************************************************************************************************************
void update_ApprentWind(void)  {
  
  windEncoder->update();
  apprentWind = windEncoder->apprentWind;
  averageApprentWind();
  
}



void averageApprentWind() {
  
 
    
//    static boolean appWind30secArrayFilled = false;
    static boolean appWind6secArrayFilled = false;
    static boolean appWind2secArrayFilled = false;    
//    static boolean appWind1secArrayFilled = false;    

    
//    static int appWindArray30sec[600]; 
    static int appWindArray6sec[120]; 
    static int appWindArray2sec[40]; 
//    static int appWindArray1sec[20]; 
    
//    static int i30 = 0,i6 = 0,i2 = 0,i1 = 0;
    static int i6 = 0,i2 = 0;
   
//    static long appWind1SecTotal = 0;
    static long appWind2SecTotal = 0;
    static long appWind6SecTotal = 0;
//    static long appWind30SecTotal = 0;

/*    
    if (i30 < 600 && !appWind30secArrayFilled) {
        
        appWind30SecTotal += apprentWind;        
        appWindArray30sec[i30] = apprentWind; 
        i30++;        
        appWind30SecAvg = int(appWind30SecTotal/i30);   
        
    } else {
        
        if (i30 == 600) 
            i30 = 0;
        
        appWind30SecTotal -= appWindArray30sec[i30]; 
        appWind30SecTotal += apprentWind;        
        appWindArray30sec[i30] = apprentWind;   
        appWind30SecAvg = int(appWind30SecTotal/600);  
        appWind30secArrayFilled = true;
        i30++;
        
    }
*/    
    if (i6 < 120 && !appWind6secArrayFilled) {
        
        appWind6SecTotal += apprentWind;        
        appWindArray6sec[i6] = apprentWind; 
        i6++;        
        appWind6SecAvg = (int)(appWind6SecTotal/i6);   
        if(appWind6SecAvg > 180)
           appWind6SecAvg = 180; 
        if(appWind6SecAvg < -179)
           appWind6SecAvg = -179;         
        
    } else {
        
          
        if (i6 == 120) 
            i6 = 0;
        
        appWind6SecTotal -= appWindArray6sec[i6]; 
        appWind6SecTotal += apprentWind;        
        appWindArray6sec[i6] = apprentWind;   
        appWind6SecAvg = (int)(appWind6SecTotal/120);
        if(appWind6SecAvg > 180)
           appWind6SecAvg = 180; 
        if(appWind6SecAvg < -179)
           appWind6SecAvg = -179;         
        appWind6secArrayFilled = true;
        i6++;
        
    }

    if (i2 < 40 && !appWind2secArrayFilled) {
        
        appWind2SecTotal += apprentWind;        
        appWindArray2sec[i2] = apprentWind;  
        i2++;        
        appWind2SecAvg = (int)(appWind2SecTotal/i2); 
        if(appWind2SecAvg > 180)
           appWind2SecAvg = 180; 
        if(appWind2SecAvg < -179)
           appWind2SecAvg = -179;    
        
    } else {
        
        if (i2 == 40) 
            i2 = 0;        
        
        appWind2SecTotal -= appWindArray2sec[i2]; 
        appWind2SecTotal += apprentWind;        
        appWindArray2sec[i2] = apprentWind;   
        appWind2SecAvg = (int)(appWind2SecTotal/40);
        if(appWind2SecAvg > 180)
           appWind2SecAvg = 180; 
        if(appWind2SecAvg < -179)
           appWind2SecAvg = -179;          
        appWind2secArrayFilled = true;
        i2++;
        
    }
/*    
    if (i1 < 20 && !appWind1secArrayFilled) {
        
        appWind1SecTotal += apprentWind;        
        appWindArray1sec[i1] = apprentWind;
        i1++;        
        appWind1SecAvg = int(appWind1SecTotal/i1);   
        
    } else {
        
        if (i1 == 20) 
            i1 = 0;
        
        appWind1SecTotal -= appWindArray1sec[i1]; 
        appWind1SecTotal += apprentWind;        
        appWindArray1sec[i1] = apprentWind;   
        appWind1SecAvg = int(appWind1SecTotal/20);  
        appWind1secArrayFilled = true;
        i1++;
        
    }
*/    
    
}

//***********************************************************************************************************************************


void averageHeading() {
  
/* 
    
    static boolean heading30secArrayFilled = false;
    static boolean heading15secArrayFilled = false;
    static boolean heading2secArrayFilled = false;  


    
    static int headingArray30sec[600]; 
    static int headingArray15sec[300]; 
    static int headingArray2sec[40]; 

    
    static int i30 = 0,i15 = 0,i2 = 0;
    
    static long heading30SecTotal = 0;
    static long heading15SecTotal = 0;
    static long heading2SecTotal = 0;
    
    if (i30 < 600 && !heading30secArrayFilled) {
        
        heading30SecTotal += current_heading;        
        headingArray30sec[i30] = current_heading; 
        i30++;        
        heading30SecAvg = int(heading30SecTotal/i30);   
        
    } else {
        
        if (i30 == 600) 
            i30 = 0;
        
        heading30SecTotal -= headingArray30sec[i30]; 
        heading30SecTotal += current_heading;        
        headingArray30sec[i30] = current_heading;   
        heading30SecAvg = int(heading30SecTotal/600);  
        heading30secArrayFilled = true;
        i30++;
        
    }
    
    if (i15 < 300 && !heading15secArrayFilled) {
        
        heading15SecTotal += current_heading;        
        headingArray15sec[i15] = current_heading; 
        i15++;        
        heading15SecAvg = int(heading15SecTotal/i15);   
        
    } else {
        
        if (i15 == 300) 
            i15 = 0;
        
        heading15SecTotal -= headingArray15sec[i15]; 
        heading15SecTotal += current_heading;        
        headingArray15sec[i15] = current_heading;   
        heading15SecAvg = int(heading15SecTotal/300);  
        heading15secArrayFilled = true;
        i15++;
        
    }

    if (i2 < 40 && !heading2secArrayFilled) {
        
        heading2SecTotal += current_heading;        
        headingArray15sec[i2] = current_heading; 
        i2++;        
        heading2SecAvg = int(heading2SecTotal/i2);   
        
    } else {
        
        if (i2 == 40) 
            i2 = 0;
        
        heading2SecTotal -= headingArray15sec[i2]; 
        heading2SecTotal += current_heading;        
        headingArray2sec[i2] = current_heading;   
        heading2SecAvg = int(heading2SecTotal/40);  
        heading2secArrayFilled = true;
        i2++;
        
    }
  */  
}

//***********************************************************************************************************************************


void averageSOG() {
  

    
 //   static boolean sog30secArrayFilled = false;
 //   static boolean sog15secArrayFilled = false;
    static boolean sog2secArrayFilled = false;  


    
//    static int sogArray30sec[600]; 
//    static int sogArray15sec[300]; 
    static int sogArray2sec[40]; 

    
//    static int i30 = 0,i15 = 0,i2 = 0;
//    static int i15 = 0,i2 = 0;
        static int i2 = 0;
    
//    static long sog30SecTotal = 0;
//    static long sog15SecTotal = 0;
    static long sog2SecTotal = 0;
/*    
    if (i30 < 600 && !sog30secArrayFilled) {
        
        sog30SecTotal += SOG;        
        sogArray30sec[i30] = SOG; 
        i30++;        
        sog30SecAvg = int(sog30SecTotal/i30);   
        
    } else {
        
        if (i30 == 600) 
            i30 = 0;
        
        sog30SecTotal -= sogArray30sec[i30]; 
        sog30SecTotal += SOG;        
        sogArray30sec[i30] = SOG;   
        sog30SecAvg = int(sog30SecTotal/600);  
        sog30secArrayFilled = true;
        i30++;
        
    }
 

    if (i15 < 300 && !sog15secArrayFilled) {
        
        sog15SecTotal += intSOG;        
        sogArray15sec[i15] = intSOG; 
        i15++;        
        sog15SecAvg = ((float)sog15SecTotal)/(i15*100);   
        
    } else {
        
        if (i15 == 300) 
            i15 = 0;
        
        sog15SecTotal -= sogArray15sec[i15]; 
        sog15SecTotal += intSOG;        
        sogArray15sec[i15] = intSOG;   
        sog15SecAvg = ((float)sog15SecTotal)/(300*100);  
        sog15secArrayFilled = true;
        i15++;
        
    }
*/
    if (i2 < 40 && !sog2secArrayFilled) {
        
        sog2SecTotal += intSOG;        
        sogArray2sec[i2] = intSOG; 
        i2++;        
        sog2SecAvg = ((float)sog2SecTotal)/(i2*100);   
        
    } else {
        
        if (i2 == 40) 
            i2 = 0;
        
        sog2SecTotal -= sogArray2sec[i2]; 
        sog2SecTotal += intSOG;        
        sogArray2sec[i2] = intSOG;   
        sog2SecAvg = (float)(sog2SecTotal)/(40*100);  
        sog2secArrayFilled = true;
        i2++;
        
    }
    
}


//***********************************************************************************************************************************

int updateWindDirection() {
  
  int newWindDirection = 0;
 
 return newWindDirection;
  
}

//***********************************************************************************************************************************
void emergencySail() {
  while(pilot_switch < RC_sail) {
   
         read_radio();   
         APM_RC.OutputCh(rudder_output, radio_in[rudder_output]);           
         APM_RC.OutputCh(sheet_output, radio_in[sheet_output]);   
  
   
  } 
  
}



//***********************************************************************************************************************************

void rc_sail() {
  
   char guiDataRC[200]; 
   char cogStr[10];
   char current_headingStr[10];
   char sogStr[10];
   char calcSOGStr[10];
  

   int tableSheetPerecnt;
   int calcSheetPerc;
   int upWindTargetApprentWind;
   int newWeather;   
   int memory;
   
   float rcSheetPercent;  
   int altRcPercent;   
   
   float calcSOG;
   weather = 0;
   
   upWindTargetApprentWind = UPWIND_APPRENT_LIMIT_WEATHER_0;
     
   while(pilot_switch < RC_sail || data_input_switch < Read_GUI_Data_Challenge_Finished) {
                   
         read_radio();   
         APM_RC.OutputCh(rudder_output, radio_in[rudder_output]);           
         APM_RC.OutputCh(sheet_output, radio_in[sheet_output]);   
         
         
         rcSheetPercent = (sheet_end - radio_in[sheet_output])/sheet_increment;
         
         altRcPercent = pow(rcSheetPercent,0.625) * 5.62 ;
         
         newWeather = resetWeather(); 
       
         if(newWeather != weather) {            // test to see if average SOG and avg. aprrent is still in range if not change weather code
       
         weather = newWeather;
         
         switch (weather) {                                                                    // if weather not in range reset targets 
      
            case 0:upWindTargetApprentWind = UPWIND_APPRENT_LIMIT_WEATHER_0;
                  
            break;
            case 1:upWindTargetApprentWind = UPWIND_APPRENT_LIMIT_WEATHER_1;
                   
            break;
            case 2:upWindTargetApprentWind = UPWIND_APPRENT_LIMIT_WEATHER_2;
            
            break;        
            case 3:upWindTargetApprentWind = UPWIND_APPRENT_LIMIT_WEATHER_3;
                      
            break;      
      
            }         
                   
         }  
           // weather = 0; 
            update_GPS();
            update_ApprentWind();           
            averageSOG();
                
         if(millis() - update_timer >= 50) {
        
            update_timer = millis();
         
            if(data_input_switch > Read_GUI_Data_Challenge_Finished && sailingChallenge == false)                     
               read_data_fromGUI();              
         
            if(apprentWind > 0)
              upWindTargetApprentWind = abs(upWindTargetApprentWind);
            else
              upWindTargetApprentWind = -1*abs(upWindTargetApprentWind);
            
           calcSheetPerc = pgm_read_word_near( & apprentSheetSettings[abs(appWind2SecAvg)][weather] ); //pgm_read_word_near(charSet + k)
           calcSOG = ((double)(pgm_read_word_near( & sogArray[abs(appWind2SecAvg)][weather])))/100;
                        
           dtostrf(COG, 7, 0,cogStr );     
           dtostrf(current_heading, 7, 1,current_headingStr );  
           dtostrf(sog2SecAvg, 7, 2,sogStr );  
           dtostrf(calcSOG, 7, 2,calcSOGStr);             
          
           memory = freeRam ();
            
           sprintf(guiDataRC,"$A%11ld %11ld %8s %8s %8d %8d %8d %9s %7s %8d %9d %11d %9d %8d %8d %8d",current_position -> longitude,
                             current_position -> latitude,cogStr,current_headingStr,apprentWind,appWind2SecAvg,
                             appWind6SecAvg,sogStr,calcSOGStr,altRcPercent,calcSheetPerc,
                             upWindTargetApprentWind,weather,g_gps -> hemisphereSatelites,g_gps->hdop,memory);  
                                                                                                                                                                                                                                                                                                    
           if(!data_received)                  
                Serial3.println(guiDataRC);    
                Serial.println(guiDataRC);                          
        
      }                                                            
     
   }

}

//***********************************************************************************************************************************



void test_sail() {
  
   char guiDataRC[220]; 
   char steerMethodStr[10];
   char OutputStr[20];
   char PTermStr[20];
   char ITermStr[20];
   char DTermStr[20];
  
   int calcSheetPerc;
   int target;
   int compassTarget;
   int delta;
   int error;
   int memory;
   int steerMethod;
   int currentValue;
   
   long tackTimer;
   long compassTimer;
//   long clampPIDTimer;
   
   boolean doSomeTacks;
   boolean useCompass7SecAfterTack;
//   boolean pidStartTimerExpired = false;
   
   sailingChallenge = true;   
   setPIDforChallenge();  
   
   target = challenge.testTarget;
     
   
   if(challenge.heading3)
      doSomeTacks = true;
   else
      doSomeTacks = false;  
      
   if(challenge.heading4)   
      useCompass7SecAfterTack = true;
   else   
      useCompass7SecAfterTack = false;
   
   
   weather = challenge.weather;
   
   course = target;
   
   steerMethod = challenge.testMethod;
   
   switch(steerMethod) {
      
       case compassMethod:strcpy(steerMethodStr,"Compass");
            break;
       case cogMethod:strcpy(steerMethodStr,"COG");
            break;
       case apprentWindMethod:strcpy(steerMethodStr,"Apparent");
            break;  
   }    
    
    
   tackTimer = millis();
//   clampPIDTimer = millis();
//   rudder.SetOutputLimits(-5,5);
   
   
   while(data_input_switch > Read_GUI_Data_Challenge_Finished) {
                   
        read_radio();   
        if(pilot_switch < RC_sail)                                                                     // if pilot switch moved to RC go to RC 
          emergencySail();
          
        update_GPS();
        update_ApprentWind();   
/*
        if(!pidStartTimerExpired  && (millis() - clampPIDTimer >= 5000)) {
         
           rudder.SetOutputLimits(-challenge.rudderLimit,challenge.rudderLimit);
           pidStartTimerExpired = true;
          
        }
 */               
        if(millis() - update_timer >= 50) {
        
           update_timer = millis();         
         
           error = Setpoint - Input;
           
           switch(steerMethod) {
      
               case compassMethod:currentValue = (int)current_heading;
                    break;
               case cogMethod:currentValue = (int)COG;
                    break;
               case apprentWindMethod:currentValue = appWind6SecAvg;                     
                    break;  
           }               
            
           calcSheetPerc = pgm_read_word_near( & apprentSheetSettings[abs(appWind2SecAvg)][weather] ); 
            
           if( steerMethod == apprentWindMethod && abs(target) <= 40) {
           
              calcSheetPerc = 100;
              
              if(doSomeTacks) {
                 if(millis() - tackTimer >= 20000) {
                
                    tackTimer = millis();
                    compassTarget = current_heading;
                    if(target < 0) {
                      
                       compassTarget = compass_calculation(compassTarget - 100);
                       starboard = false;
                       
                    } else {  
                      
                       compassTarget = compass_calculation(compassTarget + 100);
                       starboard = true;  
                    }
                                           
                    longDistanceRaceTack();
                    if(starboard)
                       starboard = false;
                    else
                       starboard = true;   
                    if(useCompass7SecAfterTack) {
                       compassTimer = millis();
                       course = compassTarget;   
                       while(millis() - compassTimer <= 6000)
                          steer(compassMethod);
                       
                    }
                    
                    target = -1*target;
                    course = target;             
                  }
              }
           } 
           
           
               
           
           adjust_sheets(calcSheetPerc);      
           steer(steerMethod);                 
  
           dtostrf(Output, 8, 2, OutputStr);
           dtostrf(rudder.PTerm, 10, 2,PTermStr );
           dtostrf(rudder.ITerm, 8, 2,ITermStr );     
           dtostrf(rudder.DTerm, 8, 2,DTermStr );                  
          
           memory = freeRam ();
            
           sprintf(guiDataRC,"$G%9s %11d %11d %12d %10d %10d %9d %11s %9d %11s %11s %11s %8d %11d",
               steerMethodStr,(int)current_heading,target,currentValue,error,appWind2SecAvg,appWind6SecAvg,OutputStr,error,PTermStr,ITermStr,DTermStr,apprentWind,memory);  
                                                                                                                                                                                                                                                                                                    
                           
           Serial3.println(guiDataRC);
        
      }                                                            
     
   }
   
   data_received = false;
   sailingChallenge = false;   
  

}




//***********************************************************************************************************************************

void challenge_sail() {
  
  
  switch(challenge.task) {
    
    case 0:navigationChallenge();
    break;
    
    case 1:stationKeepingChallenge();
    break;
    
    case 2:longDistanceRaceChallenge();
    break;
    
    case 3:test_sail();
    break;    
  }
  

}



//***********************************************************************************************************************************

 void read_data_fromGUI () {

 #define INLENGTH 250
 
  
  char inString[INLENGTH + 1] ;
  int inCount; 
  

  
  inCount = 0;

  while(Serial3.available() > 0)  {                                                 
    inString[inCount++] = Serial3.read();                                           
    delay(2);   // Changed from 1 May 17, 2012 by JK.
    
  }

  inString[inCount] = '\0';      
    
   if(inCount > 0)  
    {
     // inCount = 0; 
      data_received = true;
      challenge.parse_challenge_data(inString+1,inCount-1);  
      
      
      Serial3.println(inString);                                                    
 
           
/*    
   char pStr[10]; 
   char iStr[10];
   char dStr[10];
   
   dtostrf(challenge.kp, 6, 4, pStr);   
   dtostrf(challenge.ki, 6, 4, iStr);    
   dtostrf(challenge.kd, 6, 4, dStr);    

   char head1Str[10]; 
   char head2Str[10];
   char head3Str[10];
   
   int i;
   
   dtostrf(challenge.heading1, 6, 1, head1Str);   
   dtostrf(challenge.heading2, 6, 1, head2Str);    
   dtostrf(challenge.heading3, 6, 1, head3Str);    
   
   
   Serial.print("Challenge = ");
   Serial.println(challenge.task);  
   Serial.print("Weather = ");
   Serial.println(challenge.weather);    
    
   Serial.print("P = ");
   Serial.println(pStr);    
   Serial.print("I = ");
   Serial.println(iStr);     
   Serial.print("D = ");
   Serial.println(dStr);    
   
   Serial.print("PID Interval = ");
   Serial.println(challenge.pidInterval);  
   Serial.print("Test target = ");
   Serial.println(challenge.testTarget);   
   Serial.print("Test Steering Method = ");
   Serial.println(challenge.testMethod);  
   Serial.print("Rudder Limit = ");
   Serial.println(challenge.rudderLimit);   
   Serial.print("Leeway Correction = ");
   Serial.println(challenge.leewayCor);  

   Serial.print("Leeway Max = ");
   Serial.println(challenge.leewayMax); 

   Serial.print("Heading 1 = ");
   Serial.println(head1Str);    
   Serial.print("Heading 2 = ");
   Serial.println(head2Str);     
   Serial.print("Heading 3 = ");
   Serial.println(head3Str); 

   switch(challenge.task) {
     
    case 0:for(i = 0 ; i < 2; i++) {
             Serial.print(challenge.wpts[i].longitude); 
             Serial.print("    ");
             Serial.println(challenge.wpts[i].latitude);
    }
    break;
     
    case 1:for(i = 0 ; i < 4; i++) {
             Serial.print(challenge.wpts[i].longitude); 
             Serial.print("    ");
             Serial.println(challenge.wpts[i].latitude);
    }
    break;     

    case 2:for(i = 0 ; i < 7; i++) {
             Serial.print(challenge.wpts[i].longitude); 
             Serial.print("    ");
             Serial.println(challenge.wpts[i].latitude);
    }
    break;     
     
   }
*/
    }




 // readData->update();
  //Serial3.println(readData -> data);
 } 

//***********************************************************************************************************************************
void setPIDforChallenge() {
  
  rudder.SetMode(AUTOMATIC);
  rudder.SetOutputLimits(-challenge.rudderLimit,challenge.rudderLimit);
  rudder.SetTunings(challenge.kp, challenge.ki, challenge.kd);                     //set PID Constants    
  rudder.SetSampleTime(challenge.pidInterval);   
  
}



//***********************************************************************************************************************************

void navigationChallenge() {
  
    char data[150];
    char courseStr[8];
    char headingStr[8];
    char headingDiffStr[8];
    char bearingStr[8];
    char bearingTargetStr[8];
    char bearingDiffStr[8];
    char distMnStr[12];
    char distFStr[12];
    char tackStr[3];
  
     Waypoint F;
     Waypoint Mn;      
     Waypoint P;
 

    
     Mn.longitude = challenge.wpts[0].longitude;
     Mn.latitude = challenge.wpts[0].latitude;
     F.longitude = challenge.wpts[1].longitude;
     F.latitude = challenge.wpts[1].latitude;   
    
     
   //  double windDirection = challenge.wind_direction;
     double bearing,headingDiff,target,bearingDiff,dstMn,dstF;
     
     int leg = 1;
     int steerMethod; 
     
     double courseLeg1and3, courseLeg2,  courseLeg4, courseLeg5;
     double avgCOG = 0.0;
     double totalCOG = 0.0;
     long count = 0;  
     long leg5Timer = 0;
      
     double bearingFtoMn = Bearing_to_wpts(F.longitude,F.latitude, Mn.longitude,Mn.latitude); 
     double bearingMntoF = Bearing_to_wpts(Mn.longitude,Mn.latitude,F.longitude,F.latitude);
     
     sailingChallenge = true;   
     setPIDforChallenge();  
     
     calcWpt(bearingFtoMn,15.0,&Mn,&P);
     
     weather = challenge.weather;
     
     steerMethod = challenge.testMethod;
     
     if(steerMethod == 2)
        steerMethod = 0;
     
     courseLeg1and3 = challenge.heading1;
     courseLeg2 = challenge.heading2; 
     courseLeg4 = challenge.heading3;     
     
     if(challenge.rounding == 0) {
       
       starboard = false;
       courseLeg5 = compass_calculation(bearingMntoF + 10.0);   

     } else {
               starboard = true; 
               courseLeg5 = compass_calculation(bearingMntoF - 10.0);         
     }  
          
     update_GPS(); 
          
     while(data_input_switch > Read_GUI_Data_Challenge_Finished) {
      
       read_radio();
       if(pilot_switch < RC_sail)
         emergencySail();         


       if(starboard) 
         tackStr[0]= 'S'; 
       else
         tackStr[0] = 'P';  
        
       tackStr[1] = '\0';   
         
       update_GPS();
                    
       if(starboard) {
           switch(leg) {
       
              case 1: //courseLeg1and3 -= (apprentWind - 25.0); 
                      //courseLeg2 += (apprentWind - 25.0);
                      course = courseLeg1and3;
                      target = courseLeg2 - 15.0;
                      
                      bearing = Bearing_to_wpts(current_position -> longitude,current_position -> latitude,Mn.longitude,Mn.latitude);
                      headingDiff = calculate_bearing_delta(course, current_heading); 
                      
                      if(calculate_bearing_delta(bearing,target) >= 0 || 
                            Dist_to_wpts(current_position -> longitude,current_position -> latitude,F.longitude,F.latitude) >= 30.0) {      //change to 30.0                 
                        navigation_tack();
                        leg++;  
                        
                      } else {
                             
                        adjust_sheets(sheet_setting[B][weather]);
                        steer(compassMethod);
                      
                      }
                        
                    
              break;
  
              case 2: //courseLeg1and3 -= (apprentWind - 25.0);
                      //courseLeg2 += (apprentWind - 25.0);
                      course = courseLeg2;
                      target = courseLeg1and3;
                      
                      bearing = Bearing_to_wpts(current_position -> longitude,current_position -> latitude,P.longitude,P.latitude);
                      headingDiff = calculate_bearing_delta(course, current_heading); 
                      
                      if(calculate_bearing_delta(bearing,target) >= 0) {                       
                        navigation_tack();
                        leg++;  
                        
                      } else {
                        
                        adjust_sheets(sheet_setting[B][weather]);
                        steer(compassMethod);
                      
                      }
              break;  
  
              case 3: course = courseLeg1and3; 
                      target = compass_calculation(courseLeg2 + 180.0);
                      
                      bearing = Bearing_to_wpts(current_position -> longitude,current_position -> latitude,Mn.longitude,Mn.latitude);
                      headingDiff = calculate_bearing_delta(course, current_heading); 
                      
                      if (calculate_bearing_delta(bearing,target) <= 0) {                       
                        navigation_bearaway_gybe(800);
                        leg++;                       
                      } else {
                        
                        adjust_sheets(sheet_setting[B][weather]);
                        steer(compassMethod);
                      
                      }
              break;
              
              case 4: course = courseLeg4;  
                      target = courseLeg5;
                      
                      bearing = Bearing_to_wpts(current_position -> longitude,current_position -> latitude,F.longitude,F.latitude);
                      headingDiff = calculate_bearing_delta(course, current_heading); 
              
                      if( calculate_bearing_delta(bearing,target) <= 0) {                       
                        navigation_bearaway_gybe(1500);
                        leg++;     
                        leg5Timer = millis();                  
                      } else {
                        
                        adjust_sheets(sheet_setting[R][weather]);
                        steer(compassMethod);
                      
                      }  
              break;
              
              case 5: course = Bearing_to_wpts(current_position -> longitude,current_position -> latitude,F.longitude,F.latitude);
                      target = 0.0;
                      bearing = 0.0;
                      headingDiff = calculate_bearing_delta(course, current_heading); 
                      adjust_sheets(sheet_setting[BBR][weather]);
                      steer(steerMethod);
                      
                      
                       /*
                        if (Dist_to_wpts(current_position -> longitude,current_position -> latitude,F.longitude,F.latitude) > 30.0) {
                
                          course = Bearing_to_wpts(current_position -> longitude,current_position -> latitude,F.longitude,F.latitude);
                          target = 0.0;
                          bearing = 0.0;
                          headingDiff = calculate_bearing_delta(course, current_heading);                                         
                          adjust_sheets(sheet_setting[BBR][weather]);
                          
                          if(millis() - leg5Timer <= 10000) {
                          steer(compassMethod);  
                          } else {
                             steer(cogMethod); 
                          }  
                          
                      } else if (Dist_to_wpts(current_position -> longitude,current_position -> latitude,F.longitude,F.latitude) <= 30.0 &&                                          
                          Dist_to_wpts(current_position -> longitude,current_position -> latitude,F.longitude,F.latitude) >= 0.0)  {                       
                          count++;
                          totalCOG += COG;
                          
                          course = Bearing_to_wpts(current_position -> longitude,current_position -> latitude,F.longitude,F.latitude); 
                          target = 0.0;
                          bearing = 0.0;
                          headingDiff = calculate_bearing_delta(course, current_heading); 
                          
                          
                          adjust_sheets(sheet_setting[BBR][weather]);
                          steer(cogMethod);                                        
                      } else {
                        
                         if(!(int)avgCOG && count > 0)
                             avgCOG = totalCOG/count;                           
                          course = avgCOG; 
                          target = 0.0;
                          bearing = 0.0;
                          headingDiff = calculate_bearing_delta(course, COG); 
                          
                          
                          adjust_sheets(sheet_setting[BBR][weather]);
                          steer(cogMethod);                                      
                      }  
              */                      
              break;                      
                               
           }
 
           
     } else {
           switch(leg) {
       
        
              case 1: //courseLeg1and3 += (apprentWind - 25.0); 
                      //courseLeg2 -= (apprentWind - 25.0);
                      course = courseLeg1and3;                     
                      target = courseLeg2 + 15.0;
                      
                      bearing = Bearing_to_wpts(current_position -> longitude,current_position -> latitude,Mn.longitude,Mn.latitude);
                      headingDiff = calculate_bearing_delta(course, current_heading);   
                      
                      if(calculate_bearing_delta(bearing,target) <= 0 || 
                                       Dist_to_wpts(current_position -> longitude,current_position -> latitude,F.longitude,F.latitude) >= 30.0) {                       
                        navigation_tack();
                        leg++;                       
                      } else {
                        
                        adjust_sheets(sheet_setting[B][weather]);
                        steer(compassMethod);   
                      
                      }
                                         
              break;
  
              case 2: //courseLeg1and3 += (apprentWind - 25.0);
                      //courseLeg2 -= (apprentWind - 25.0);
                      course = courseLeg2;
                      target = courseLeg1and3;
                      
                      bearing = Bearing_to_wpts(current_position -> longitude,current_position -> latitude,P.longitude,P.latitude);
                      headingDiff = calculate_bearing_delta(course, current_heading); 
                      
                      if(calculate_bearing_delta(bearing,target) <= 0) {                       
                        navigation_tack();
                        leg++;                       
                      } else {
                        
                        adjust_sheets(sheet_setting[B][weather]);
                        steer(compassMethod);
                      
                      }
              break;  
  
              case 3: course = courseLeg1and3;  
                      target = compass_calculation(courseLeg2 + 180.0);
                      
                      bearing = Bearing_to_wpts(current_position -> longitude,current_position -> latitude,Mn.longitude,Mn.latitude);
                      headingDiff = calculate_bearing_delta(course, current_heading); 
 
                      if (calculate_bearing_delta(bearing,target) >= 0) {                       
                        navigation_bearaway_gybe(800);
                        leg++;  
                        
                      } else {
                        
                        adjust_sheets(sheet_setting[B][weather]);
                        steer(compassMethod);
                      
                      }
              break;
              
              case 4: course = courseLeg4; 
                      target = courseLeg5;
                      
                      bearing = Bearing_to_wpts(current_position -> longitude,current_position -> latitude,F.longitude,F.latitude);
                      headingDiff = calculate_bearing_delta(course, current_heading); 
 
                      if( calculate_bearing_delta(bearing,target) >= 0) {                       
                        navigation_bearaway_gybe(1500);
                        leg5Timer = millis();
                        leg++; 
                        
                      } else {
                        
                        adjust_sheets(sheet_setting[R][weather]);
                        steer(compassMethod);
                      
                      } 
              break; 
              
              case 5: course = Bearing_to_wpts(current_position -> longitude,current_position -> latitude,F.longitude,F.latitude);
                      target = 0.0;
                      bearing = 0.0;
                      headingDiff = calculate_bearing_delta(course, current_heading);
                      adjust_sheets(sheet_setting[BBR][weather]);
                      steer(steerMethod);
                      
                      
                     /*
                     if (Dist_to_wpts(current_position -> longitude,current_position -> latitude,F.longitude,F.latitude) > 30.0) {
                                          
                          course = Bearing_to_wpts(current_position -> longitude,current_position -> latitude,F.longitude,F.latitude);
                          target = 0.0;
                          bearing = 0.0;
                          headingDiff = calculate_bearing_delta(course, current_heading);                           
                                                                           
                          adjust_sheets(sheet_setting[BBR][weather]);
                          
                           if(millis() - leg5Timer <= 10000) {                            
                             steer(compassMethod);                             
                           } else {                            
                             steer(cogMethod); 
                          }                           
                                                       
                          
                      } else if (Dist_to_wpts(current_position -> longitude,current_position -> latitude,F.longitude,F.latitude) <= 30.0 &&                                          
                          Dist_to_wpts(current_position -> longitude,current_position -> latitude,F.longitude,F.latitude) >= 0.0)  {                       
                          count++;
                          totalCOG += COG;
                             
                          
                          course = Bearing_to_wpts(current_position -> longitude,current_position -> latitude,F.longitude,F.latitude); 
                          target = 0.0;
                          bearing = 0.0;
                          headingDiff = calculate_bearing_delta(course, current_heading); 
                                                       
                          adjust_sheets(sheet_setting[BBR][weather]);
                          steer(cogMethod);  
                          
                      } else {
                        
                          if(!(int)avgCOG && count > 0)
                             avgCOG = totalCOG/count; 
                          course = avgCOG; 
                          target = 0.0;
                          bearing = 0.0;
                          headingDiff = calculate_bearing_delta(course, COG); 
                                                    
                          
                          adjust_sheets(sheet_setting[BBR][weather]);
                          steer(cogMethod);                                      
                      }
              */                                         
              break;            
           }          
       
     }
     
     bearingDiff = calculate_bearing_delta(bearing, target);
     dstF = Dist_to_wpts(current_position -> longitude,current_position -> latitude,F.longitude,F.latitude);
     dstMn = Dist_to_wpts(current_position -> longitude,current_position -> latitude,Mn.longitude,Mn.latitude);  
 
       
     dtostrf(course, 6, 1, courseStr); 
     dtostrf(current_heading, 6, 1, headingStr);
     dtostrf(headingDiff, 6, 1, headingDiffStr);
     dtostrf(target, 6, 1, bearingTargetStr);
     dtostrf(bearing, 6, 1, bearingStr);           
     dtostrf(bearingDiff, 6, 1, bearingDiffStr);
     dtostrf(dstF, 8, 1, distFStr);           
     dtostrf(dstMn, 8, 1, distMnStr);  

     sprintf(data,"$B%7s %10s %9s %11s %12s %9s %11s %11s %9d %6s %7d",
        courseStr,headingStr,headingDiffStr,bearingTargetStr,bearingStr,bearingDiffStr,distFStr,distMnStr,apprentWind,tackStr,leg);             
     
     if(millis() - update_timer >= 50) {
   
          update_timer = millis();
          Serial3.println(data);                                     
          update_ApprentWind();
     }     

   }
   

   data_received = false;
   sailingChallenge = false;   

}

//***********************************************************************************************************************************

// ***** Course Sailed = Height in Box Method ***********

void stationKeepingChallenge() {                        //*WptU
 
     #define FULL_TIME  300                             //100M
     #define TIME_TO_GYBE 4 
     
     Waypoint P1;                        //P1 *           *P1S1               *S1
     Waypoint S1;      
     Waypoint P2;
     Waypoint S2;
     Waypoint P1S1;                     //P1P2*           *m                  *S1S2                100M                        *wptMs
     Waypoint P2S2;      
     Waypoint P1P2;
     Waypoint S1S2;
//     Waypoint m;                        //P2             *P2S2                *S2     
     Waypoint wptMs;
     Waypoint wptU;

     
     double bearingP1S1, distP1S1;
     double bearingP2S2, distP2S2;
     double bearingP2P1, distP2P1;
     double bearingS2S1, distS2S1;
     double bearingP2S2P1S1;
     double bearingP1P2S1S2;  
     double distP1P2S1S2;     
     double U,P,S,M,N,tackDistance,heightDistance;                                                                             
     double calcSOG;
     double course_by_leg[2];
     double avgSog = 0.75;
     double fastSog = 1.0;
     double portBeatHeading;
     double starboardBeatHeading;
     double sheetAdjustFactor;
     
     int current_leg = 1;
     int error;
     int sheet_percent;
     int starboardDistanceOut;
     int portDistanceOut;
     int totalDistanceOut;
     int calcSheetPerc;
     int sheetAdjust = 0;
     int baseSheetAdjustment;
     int incrementalSheetAdjustment;
     int sailTime;
     int L;
//     int leeway_correction;
     int leeway_max = 30;
     int leeway_min = -10;
     
     long station_keeping_time;     
     long start_time;
     long timeRemaining;
                                                                                      
     char data[150];
     char leg_str[10];     
     char courseStr[12];
     char sogStr[10];
     char headingStr[12];                 
     char errorStr[12];
     char tackDistanceStr[12];
     char heightDistanceStr[12];
     
     boolean timeToSailOut = false;

     sailingChallenge = true;   
     setPIDforChallenge();  

 //    leeway_max = challenge.leewayMax;
//     leeway_correction = challenge.leewayCor;   
     
     starboardBeatHeading = challenge.heading1;
     portBeatHeading = challenge.heading2; 
     
     weather = challenge.weather; 
     
     P1.longitude = challenge.wpts[0].longitude;
     P1.latitude = challenge.wpts[0].latitude;
     S1.longitude = challenge.wpts[1].longitude;
     S1.latitude = challenge.wpts[1].latitude;   
     P2.longitude = challenge.wpts[2].longitude;
     P2.latitude = challenge.wpts[2].latitude;
     S2.longitude = challenge.wpts[3].longitude;
     S2.latitude = challenge.wpts[3].latitude;        
          
     bearingP1S1 = Bearing_to_wpts(P1.longitude, P1.latitude, S1.longitude, S1.latitude);
     distP1S1 = Dist_to_wpts(P1.longitude, P1.latitude, S1.longitude, S1.latitude);
     calcWpt(bearingP1S1,0.5*distP1S1,&P1,&P1S1);

     
     bearingP2S2 = Bearing_to_wpts(P2.longitude, P2.latitude, S2.longitude, S2.latitude);
     distP2S2 = Dist_to_wpts(P2.longitude, P2.latitude, S2.longitude, S2.latitude);
     calcWpt(bearingP2S2,0.5*distP2S2,&P2,&P2S2);   

   
     bearingP2S2P1S1 = Bearing_to_wpts(P2S2.longitude, P2S2.latitude, P1S1.longitude, P1S1.latitude);
     calcWpt(bearingP2S2P1S1,100.0,&P1S1,&wptU);

     bearingP2P1 = Bearing_to_wpts(P2.longitude, P2.latitude, P1.longitude, P1.latitude);
     distP2P1 = Dist_to_wpts(P2.longitude, P2.latitude, P1.longitude, P1.latitude);
     calcWpt(bearingP2P1,0.5*distP2P1,&P2,&P1P2);   

     bearingS2S1 = Bearing_to_wpts(S2.longitude, S2.latitude, S1.longitude, S1.latitude);
     distS2S1 = Dist_to_wpts(S2.longitude, S2.latitude, S1.longitude, S1.latitude);
     calcWpt(bearingS2S1,0.5*distS2S1,&S2,&S1S2);  
 

     bearingP1P2S1S2 = Bearing_to_wpts(P1P2.longitude, P1P2.latitude, S1S2.longitude, S1S2.latitude);
     calcWpt(bearingP1P2S1S2,100.0,&S1S2,&wptMs);
 
 
     distP1P2S1S2 = Dist_to_wpts(P1P2.longitude, P1P2.latitude, S1S2.longitude, S1S2.latitude);
//     calcWpt(bearingP1P2S1S2,0.5*distP1P2S1S2,&P1P2,&m); 

     U = Dist_to_wpts(P2S2.longitude, P2S2.latitude, wptU.longitude, wptU.latitude);               // changed U to measure to bottom of box ***************************************************************
     P = Dist_to_wpts(P1P2.longitude, P1P2.latitude, wptMs.longitude, wptMs.latitude);
     S = Dist_to_wpts(S1S2.longitude, S1S2.latitude, wptMs.longitude, wptMs.latitude);
         
     course_by_leg[0] = compass_calculation(0.5*(compass_calculation(portBeatHeading - starboardBeatHeading)) + starboardBeatHeading - 90.0);       
     course_by_leg[1] = compass_calculation(course_by_leg[0] + 180.0);   
     
      fastSog = challenge.heading3;
     
      avgSog = (0.60)*fastSog + (0.40)*challenge.heading4;
     
     
     start_time = millis();
                                                                                                                                     
     while (data_input_switch > Read_GUI_Data_Challenge_Finished  ) {
         
          station_keeping_time =  (millis() - start_time)/1000; 
          timeRemaining =  FULL_TIME - station_keeping_time;        
          read_radio();
          if(pilot_switch < RC_sail)
             emergencySail();
           
          update_GPS();
          update_ApprentWind();
           
          M =  Dist_to_wpts(current_position -> longitude,
                    current_position -> latitude,wptMs.longitude,wptMs.latitude);                                            // Distance from current position to wptM 
                   
          N =   Dist_to_wpts(current_position -> longitude,
                    current_position -> latitude,wptU.longitude,wptU.latitude);                                              // Distance from current position to wptU  
          
           

          
          heightDistance = U - N;

          starboardDistanceOut = P - M;    
          portDistanceOut = M - S;
         
          L = -10 + (int)(1.6*(35.0 - (double)heightDistance));
          
          if(L < -10)
             L = -10;
             
          if(L > 30)
             L = 30;   
          
          sheetAdjustFactor =  (30.0 - (double)heightDistance) * 6.6666 ;  
          
          if(sheetAdjustFactor < 0)
             sheetAdjustFactor = 0;
             
          if(sheetAdjustFactor > 100)
             sheetAdjustFactor = 100;             
          
          sheet_percent = (int)(sheetAdjustFactor/100 * (double)pgm_read_word_near( & apprentSheetSettings[abs(appWind2SecAvg)][weather]));  
          
          if (current_leg % 2 == 0) {                                                                                        
          
             starboard = false;
             tackDistance = M - (S + 15);                                                                                    // distance to next tack - to starboard  
             totalDistanceOut = M - S;
             strcpy(leg_str,"P");
             
             if (sheet_percent < 0) 
                 sheet_percent = 0;
             if (sheet_percent > 100) 
                 sheet_percent = 100;
                
             course = compass_calculation(course_by_leg[1] - L ); 
             
             if (M <= S + 15) {                                                                                                // reached 15m to starboard edge of box
                  station_keeping_gybe("regular port");                                                                                    
                  starboard = true;            
                  current_leg++;             
            
             }          
 
          }
          else
          {
              starboard = true;
              tackDistance = (P - 15) - M;
              totalDistanceOut = P - M;
              strcpy(leg_str,"S");
             
              if (sheet_percent < 0) 
                  sheet_percent = 100;              
              if (sheet_percent > 100) 
                  sheet_percent = 100;
                  
              course = compass_calculation(course_by_leg[0] + L );
              
              if (M >= P - 15) {                                                                                                      
                 station_keeping_gybe("regular starboard");                                                                                        
                 starboard = false;            
                 current_leg++;                   
              }           
                           
          }
          
        update_ApprentWind(); 
                
        if(starboard) {
          
            if(starboardDistanceOut/avgSog - timeRemaining >= 2) {
              
               timeToSailOut = true;
              
            } else 
               
              if ((portDistanceOut/avgSog + TIME_TO_GYBE) - timeRemaining >= 2) {
              
                   timeToSailOut = true;
                   station_keeping_gybe("exit port");
                   starboard = false;
              }
                           
        } else {
          
             if(portDistanceOut/avgSog - timeRemaining >= 2) {
              
                timeToSailOut = true;
              
            } else 
               
              if ((starboardDistanceOut/avgSog + TIME_TO_GYBE) - timeRemaining >= 2) {
              
                   timeToSailOut = true;
                   station_keeping_gybe("exit starboard");
                   starboard = true;
            }
                        
        }
        
       
        
        if(timeToSailOut) {                                                         //*** Start Exit Routine 
        
            while (data_input_switch > Read_GUI_Data_Challenge_Finished ) {
             
                 read_radio();
                 if(pilot_switch < RC_sail)
                      emergencySail(); 
                           
                  update_ApprentWind();
                  update_GPS();
                  
                  M =  Dist_to_wpts(current_position -> longitude,                                                           // distance from current position to wptMs 
                                        current_position -> latitude,wptMs.longitude,wptMs.latitude);
                                        
                  N =   Dist_to_wpts(current_position -> longitude,
                                        current_position -> latitude,wptU.longitude,wptU.latitude);                          // Distance from current position to wptU  
                                                  
                  heightDistance = U - N; 
                  
                  L = -10 + (int)(1.6*(35.0 - (double)heightDistance));
          
                  if(L < -10)
                     L = -10;
             
                  if(L > 30)
                     L = 30; 
                     
                  sheetAdjustFactor =  (30.0 - (double)heightDistance) * 1.6666 ;  
          
                  if(sheetAdjustFactor < 0)
                     sheetAdjustFactor = 0;
             
                  if(sheetAdjustFactor > 25)
                     sheetAdjustFactor = 25;                      
                  
                  station_keeping_time =  (millis() - start_time)/1000;
                  timeRemaining =  FULL_TIME - station_keeping_time;
                  
                  if(starboard) {
                    
                      
                      totalDistanceOut  = P - M;
                      
                  } else {
                  
                      
                      totalDistanceOut  = M - S;
                  }
                  
                  if( totalDistanceOut/fastSog - timeRemaining >= 2) {                                                                   // if leave now at max speed exit box at 302 sec.               
                                       
                          sheet_percent = pgm_read_word_near( & apprentSheetSettings[abs(appWind2SecAvg)][weather] );
                          
                          if(starboard) {
                            
                              course = compass_calculation(course_by_leg[0] + L);
                              totalDistanceOut  = P - M;
                              strcpy(leg_str,"S-Fast"); 
                               
                          }                    
                          else {
                                  
                              course = compass_calculation(course_by_leg[1] - L);                     
                              totalDistanceOut  = M - S;
                              strcpy(leg_str,"P-Fast");
                                                                                 
                          }  
                                         
                      adjust_sheets(sheet_percent);                                                                                  
                      steer(compassMethod);   
 
                   } else {
                                                       
                      if(starboard) {
                        
                              course = compass_calculation(course_by_leg[0] + L);
                              totalDistanceOut  = P - M;
                              strcpy(leg_str,"S-Slow"); 
                              
                      }                    
                      else {
                        
                              course = compass_calculation(course_by_leg[0] - L); 
                              totalDistanceOut  = M - S;
                              strcpy(leg_str,"P-Slow");                                       
                      }                  
   
                    sheet_percent = (int)(sheetAdjustFactor/100 * (double)pgm_read_word_near( & apprentSheetSettings[abs(appWind2SecAvg)][weather]));                         
                    adjust_sheets(sheet_percent);                                                                                  
                    steer(compassMethod); 
                 }           
                                  
                  if(SOG > 0.13)
                     sailTime = totalDistanceOut/SOG;
                   else
                     sailTime = 300;  
 
                   error = calculate_bearing_delta(course,current_heading);   
   
                   dtostrf(course, 6, 1, courseStr); 
                   dtostrf(current_heading, 7, 1, headingStr);
                   dtostrf(error, 8, 1, errorStr);                        
                   dtostrf(SOG, 7, 2,sogStr );
                    
                   sprintf(data,"$E%7s %9s %10s %9s %8d %10d %10d %12d %10s %10d %11d",leg_str,courseStr,headingStr,errorStr,
                                     (int)totalDistanceOut,(int)timeRemaining,(int)sailTime,(int)(sailTime - timeRemaining),sogStr,sheet_percent,appWind6SecAvg);      
                      
                      if(millis() - update_timer >= 50) {
   
                         update_timer = millis();
                         Serial3.println(data);                
                           
                  }              
            }
          
        } 
                
        adjust_sheets(sheet_percent);
        steer(compassMethod);
   
        error = calculate_bearing_delta(course,current_heading);      
        dtostrf(course, 6, 1, courseStr); 
        dtostrf(current_heading, 7, 1, headingStr);
        dtostrf(error, 8, 1, errorStr);  
        dtostrf(tackDistance, 8, 1, tackDistanceStr);
        dtostrf(heightDistance, 8, 1, heightDistanceStr);         
  
        sprintf(data,"$C%6s %9s %8s %9d %7ld %11s %11s %10d %9d %8s",courseStr,headingStr,
                  errorStr,apprentWind,timeRemaining,tackDistanceStr,heightDistanceStr,L,sheet_percent,leg_str); 
                
                  
       if(millis() - update_timer >= 50) {
   
           update_timer = millis();
           Serial3.println(data);
           update_ApprentWind();
       }     
            
    }

     data_received = false; 
     sailingChallenge = false; 
   
}

//***********************************************************************************************************************************

void longDistanceRaceChallenge() {

  
    char data[170];                                                                                   // used to hold data to send to GUI  
    char cogStr[6];                                                                                  // used to convert COG float
    char current_headingStr[6];                                                                      // used to convert bearing float
    char bearingStr[6];
    char bearingDeltaStr[6];
    char sogStr[6];
    char polarSogStr[6];   
    char vmgStr[6];  
    char steerMethodStr[10];
    char nextMarkStr[9];
    char distToMarkStr[8];     
    char distNorthBoundaryStr[8];
    char distSouthBoundaryStr[8];  
    
    Waypoint westMark;                                                                                 // westerly mark    
    Waypoint startMark;                                                                                // centre of startline
    Waypoint eastMark;                                                                                 // easterly mark
    Waypoint westMarkNorth;                                                                            // used to limit south boundary for start mark to west mark
    Waypoint westMarkSouth;                                                                            // used to limit north boundary for start mark to west mark
    Waypoint eastMarkNorth;                                                                            // used to limit south boundary for start mark to east mark
    Waypoint eastMarkSouth;                                                                            // used to limit north boundary for start mark to east mark
    Waypoint northWest;                                                                                // used for rounding west mark - north side of west mark 
    Waypoint southWest;                                                                                // used for rounding west mark - south side of west mark                     
    Waypoint southEast;                                                                                // used for rounding west mark - south side of east mark
    Waypoint northEast;                                                                                // used for rounding west mark - north side of east mark
    Waypoint nextMark; 
                                                                                                        // time at start of long distance race
    long inIornsTimer;
    long inIornsRoutine;
    long sailingAwayFromBoundaryTimer;
    long okToTackTimer;
    long restrictRudderTimer;
    
    int nextMarkNumber = 1;                                                                            //  start mark is 0 to start sequence next mark is 1 (west or east)                                                                     
    int steerMethod;                                                                                   // compass or aprrentWind or COG 
    int helm;                                                                                          // used only if boat is goint too slow ( < 0.6 M/sec.)    
    int upWindTargetApprentWind;                                                                       // target apprent while beating                                                                             // down wind tack (gybe) angle
    int newWeather;
    int targetApprentWind;
    int actualAprrentDelta;
    int calcSheetPerc;
    int apprentDelta;   
    int tackBearing; 
    int sheetSetting;
    int markRadius;
    int memory;

    double bearingToNextMark;                                                                          // bearing from boat to next mark
    double bearingDelta;                                                                               // diffrence between current boat heading and called for heading
    double distanceToMark;                                                                             // distance from boat to mark
    double directBearingWest;                                                                          // bearing from start mark to west mark
    double directBearingEast;                                                                          // bearing from start mark to east mark
    double northBoundaryDist;                                                                          // distance to north boundary
    double southBoundaryDist;                                                                          // distance to south boundary
    double VMC;                                                                                        // velocity made good  
    
    boolean beatCourse;                                                                                // need to beat to get to next mark
    boolean directCourse;                                                                              // SOG high enough to sail directly to next mark
    boolean beyondBoundary;                                                                            // has the sailbot reached the north or south boundary?
    boolean beatRequired;                                                                              // a beat is required to reach next mark
    boolean sailingAwayFromBoundary = false;
    boolean okToTack = true;
    boolean restrictRudder = false;
    
    sailingChallenge = true;                                                                           // sailbot is sailing on a challenge
    setPIDforChallenge();                                                                              // set the PID variables sent by GUI
    weather = challenge.weather;                                                                       // weather code 0 (3knots) 1 (5knots) 2(9knots) 3(14knots)
    
    startMark.longitude = challenge.wpts[0].longitude;                                                 // centre start line longitude
    startMark.latitude = challenge.wpts[0].latitude;                                                   // centre start line latitude
    westMark.longitude = challenge.wpts[1].longitude;                                                  // west mark longitude
    westMark.latitude = challenge.wpts[1].latitude;                                                    // west mark line latitude   
    eastMark.longitude = challenge.wpts[2].longitude;                                                  // east mark line longitude
    eastMark.latitude = challenge.wpts[2].latitude;                                                    // east mark line latitude     

    southWest.longitude = challenge.wpts[3].longitude;                                                 // southwest mark longitude - used to limit boat on north side of course from start to west mark
    southWest.latitude = challenge.wpts[3].latitude;                                                   // southwest mark latitude - used to limit boat on north side of course from start to west mark
    northWest.longitude = challenge.wpts[4].longitude;                                                 // northhwest mark longitude - used to limit boat on south side of course from start to west mark
    northWest.latitude = challenge.wpts[4].latitude;                                                   // northwest mark latitude - used to limit boat on south side of course from start to west mark   
    southEast.longitude = challenge.wpts[5].longitude;                                                 // southeastt mark longitude - used to limit boat on north side of course from start to east mark
    southEast.latitude = challenge.wpts[5].latitude;                                                   // southeast mark latitude - used to limit boat on north side of course from start to east mark      
    northEast.longitude = challenge.wpts[6].longitude;                                                 // northeast mark longitude - used to limit boat on south side of course from start to east mark
    northEast.latitude = challenge.wpts[6].latitude;                                                   // northeast mark latitude - used to limit boat on south side of course from start to east mark   
    
    directBearingWest = Bearing_to_wpts(startMark.longitude,startMark.latitude,westMark.longitude,westMark.latitude ); //bearing from start mark to west mark   
    directBearingEast = Bearing_to_wpts(startMark.longitude,startMark.latitude,eastMark.longitude,eastMark.latitude ); //bearing from start mark to east mark 
    
    calcWpt(compass_calculation(directBearingWest + 45.0),10.0,&westMark,&westMarkNorth);              // used to round west mark - first mark rounded if going west
    calcWpt(compass_calculation(directBearingWest - 65.0),16.0,&westMark,&westMarkSouth);              // used to round west mark - second mark rounded if going west 
    calcWpt(compass_calculation(directBearingEast - 65.0),16.0,&eastMark,&eastMarkNorth);              // used to round east mark - first mark rounded if going east 
    calcWpt(compass_calculation(directBearingEast + 45.0),10.0,&eastMark,&eastMarkSouth);              // used to round east mark - second mark rounded if going east 
                                  
    update_ApprentWind();                                                                              // read apprent wind from encoder also calculate 1,2,6 and 30 sec. apprent wind averages
    update_GPS();                                                                                      // read GPS data
    averageSOG();                                                                                      // use average SOG for iniorns routine
    
    switch (weather) {                                                                                 // set targets based on weather code
      
      case 0:upWindTargetApprentWind = UPWIND_APPRENT_LIMIT_WEATHER_0;                                 // 30 (-30 port)
 
      break;
      case 1:upWindTargetApprentWind = UPWIND_APPRENT_LIMIT_WEATHER_1;                                 // 30 (-30 port)
 
      break;
      case 2:upWindTargetApprentWind = UPWIND_APPRENT_LIMIT_WEATHER_2;                                 // 30 (-30 port)
 
      break;        
      case 3:upWindTargetApprentWind = UPWIND_APPRENT_LIMIT_WEATHER_3;                                 // 35 (-35 port)
      
      break;      
      
    }
        
                                                                                  
    strcpy(nextMarkStr,"WestN-1");                                                                    // set mark 1 description
    nextMark = westMarkNorth;                                                                         // set mark 1 waypoint
    markRadius = 6.0;
       
    inIornsRoutine = millis();                                                                        // start timer to test to see if boat in iorns - test once every 3 min.
    sailingAwayFromBoundaryTimer = millis();                                                          // set sailing away from boundary timer to system clock 
    
      
    while (data_input_switch > Read_GUI_Data_Challenge_Finished  ) {                                  // start of loop to sail to each of 13 marks 
    
      
       read_radio();                                                                                  // read radio to allow RC sail if needed
       if(pilot_switch < RC_sail)                                                                     // if pilot switch moved to RC go to RC 
          emergencySail(); 
      
       update_ApprentWind();                                                                          // update apparent wind
       update_GPS();                                                                                  // update GPS
       averageSOG();                                                                                  // update SOG calculation 
     
       if(sailingAwayFromBoundary) {                                                                  // if tacked (or gybed) away from boundary don't tack (or gybe) for at laest 30 sec
          
          if(millis() - sailingAwayFromBoundaryTimer >= 60000)                                        // test to see if 60 sec. has elapsed
             sailingAwayFromBoundary = false;                                                         // if 30 sec. has passed re-set sailing away from boundary test to false 
         
       } 
       
       if(!okToTack) {
         
          if(millis() - okToTackTimer >= 5000)                                        
             okToTack = true;          
                
       }
       
       if(restrictRudder) {
         
          if(millis() - restrictRudderTimer >= 5000) {                                       
             restrictRudder = false;          
             rudder.SetOutputLimits(-challenge.rudderLimit,challenge.rudderLimit);                
          }      
       }       
       
       
  /*     
       if (sog2SecAvg < 0.6 && (millis() - inIornsRoutine) > 180000 ) {                               // use average SOG for 2 sec.  if SOG < 0.6 m/sec. and not tested for last 3min.   **** INIORNS ROUTINE BEGIN
                
         inIornsRoutine = millis();                                                                   // reset inIornsRoutine to system clock
         
         adjust_sheets(75);                                                                           // adjust sheets to 75
         
         if(appWind2SecAvg >= 0) {                                                                    // if starboard set course (apprentWind) to 50 and helm to 45
           
             course = 50.0;
             helm = 45;
             
         } else {                                                                                     // if port set course (apprentWind) to -50 and helm to -45
           
             course = -50.0;
             helm = -45;
         }  
   
         while(millis() - inIornsTimer > 15000 && sog2SecAvg < 1.0) {                                 // for 15 sec. and SOG < 1.0 steer to apprent wind of 50 (-50 port)
         
             update_ApprentWind();
             update_GPS();
             averageSOG();
             steerMethod = apprentWindMethod;  
             steer(steerMethod);         
         }
         
         inIornsTimer = millis();                                                                    // set inIornsTimer to system clock .... reset it
       
         if(SOG < 1.0) {
           
             while(millis() - inIornsTimer > 15000 && sog2SecAvg < 1.0) {                            // for 15 sec. and SOG < 1.0 steer to helm of 45 (-45 port)
       
                 update_GPS();
                 averageSOG();               
                 APM_RC.OutputCh(rudder_output, helm*rudder_increment + rudder_centre);
                 
             }          
          }
          
          update_ApprentWind();                                                                      // update all data
          update_GPS();
          averageSOG();           
       }                                                                                             // **** INIORNS ROUTINE END
     */ 
       
       
       newWeather = resetWeather();                                                                 // test what weather is based on polars
       
       if(newWeather != weather) {                                                                  // test to see if average SOG given avg. aprrent is still in range if not change weather code
       
        weather = newWeather;
         
        switch (weather) {                                                                          // if weather not in range reset targets 
      
            case 0:upWindTargetApprentWind = UPWIND_APPRENT_LIMIT_WEATHER_0;

            break;
            case 1:upWindTargetApprentWind = UPWIND_APPRENT_LIMIT_WEATHER_1;

            break;
            case 2:upWindTargetApprentWind = UPWIND_APPRENT_LIMIT_WEATHER_2;

            break;        
            case 3:upWindTargetApprentWind = UPWIND_APPRENT_LIMIT_WEATHER_3;
    
            break;      
      
            }         
          
         }  
         
         
       bearingToNextMark = Bearing_to_wpts(current_position -> longitude,current_position -> latitude, 
                           nextMark.longitude,nextMark.latitude );                                       // bearing from boat to next mark
                           
       bearingDelta = calculate_bearing_delta(bearingToNextMark,current_heading);                        //  difference between bearing to next mark and current course 
                                                                                                         //  if positive clockwise if negative counter clockwise
       distanceToMark = Dist_to_wpts(current_position -> longitude,current_position -> latitude,         //  distance from boat to next mark
                                     nextMark.longitude,
                                     nextMark.latitude );
        
      VMC = cos(ToRadians((abs(bearingDelta)))) * SOG;                                                   // calculate velocity made good to mark 
      
                                                                                                          // calculate distance to boundaries based on next mark
      switch(nextMarkNumber) {                                                                      
               case 1:
               case 2: 
               case 3:          
               case 7:
               case 8:
               case 9: northBoundaryDist = 860.0 -  Dist_to_wpts(current_position -> longitude,current_position -> latitude, 
                                                    southWest.longitude,southWest.latitude);
                       southBoundaryDist = 2870.0 - Dist_to_wpts(current_position -> longitude,current_position -> latitude,
                                                    northWest.longitude,northWest.latitude); 
                                                    
                       if ( northBoundaryDist <= 0 || southBoundaryDist <= 0)                              // test if sailed too far north or south
               
                            beyondBoundary = true;
                       else               
                            beyondBoundary = false;
              break;
               case 4:                                                                                
               case 5:           
               case 6:
               case 10:
               case 11:               
               case 12: northBoundaryDist = 1500.0 - Dist_to_wpts(current_position -> longitude,current_position -> latitude,
                                                     southEast.longitude,southEast.latitude);
                        southBoundaryDist = 2530.0 - Dist_to_wpts(current_position -> longitude,current_position -> latitude,
                                                     northEast.longitude,northEast.latitude);                            
               
                       if ( northBoundaryDist <= 0 || southBoundaryDist <= 0)                              // test if sailed too far north or south                       
                          
                            beyondBoundary = true;
                       else               
                            beyondBoundary = false;
             break;                            
       }
   
          
      //beyondBoundary = false;                                                                        // ****************** Testing Only ******************************
               
       if(appWind2SecAvg >= 0)  {                                                                       // use  2 sec. apprent wind angle to determine tack .... positive starboard **** STARBOARD BEGIN **** APPRENT WIND BEGIN
         
           starboard = true;
           upWindTargetApprentWind = abs(upWindTargetApprentWind);                                      // set upWind target for starboard tack 
       
            apprentDelta = appWind2SecAvg - upWindTargetApprentWind;                                    // apprentDelta is room to sail to weather before reaching beat heading
         
           if(bearingDelta > 0 ) {                                                                      // if (bearingToMark - current_heading) > 0 need to sail in clockwise direction
                   
             if(bearingDelta > apprentDelta)                                                            // if angle between heading and mark > room to weather need to sail beat
                beatRequired = true;
             else   
                beatRequired = false;
                      
           } else {                                                                                     // if (bearingToMark - current_heading) < 0 need to sail in counter clockwise direction
                          
              if(appWind2SecAvg < upWindTargetApprentWind) {                                            // if heading too high - need to bear off
              
                  if(bearingDelta > apprentDelta)                                                       // for example bearingDelta = -5 and apprentDelta = -10 need to bear off to beat
                     beatRequired = true;                                                                
                  else  
                     beatRequired = false;                                                              // for example bearingDelta = -5 and apprentDelta = -2  don't need to beat can bear off to fetch 
              } else
            
                  beatRequired = false;                                                                 // for example bearingDelta = -5 and apprentDelta = +1  don't need beat can bear off to fetch                                                             
            
           }                                                    
                
       } else {                                                                                        // **** STARBOARD END  **** PORT BEGIN
         
         starboard = false;                                                           
         upWindTargetApprentWind = -1*abs(upWindTargetApprentWind);                                    // set upWind target for port tack 

          apprentDelta = appWind2SecAvg - upWindTargetApprentWind;                                     // apprentDelta is room to sail to weather before reaching beat heading
          
         if(bearingDelta < 0 ) {                                                                       // if (bearingToMark - current_heading) < 0 need to sail in clockwise direction
          
           if(bearingDelta < apprentDelta)                                                             // if angle between heading and mark > room to weather need to sail beat
              beatRequired = true;
           else
              beatRequired = false;   
                
         } else {                                                                                      // if (bearingToMark - current_heading) < 0 need to sail in counter clockwise direction
                  
            if(appWind2SecAvg > upWindTargetApprentWind) {
              
                if(bearingDelta < apprentDelta)
                   beatRequired = true;
                else  
                   beatRequired = false;
            } else
            
                beatRequired = false;                                           
            
         }
         
       }                                                                                            // **** TEST for BEAT REQUIRED END                                                                                                                                                                                    
     
       if (beatRequired) {                                                                          // need to beat to next mark  **** BEAT REQUIRED BEGIN
       
           if (distanceToMark <= 20.0) {
             
               if(starboard)
                  tackBearing = 45;
               else
                  tackBearing = 90;   
             
           } else {
             
              tackBearing = 75;
             
           }
                          
           if (( okToTack  && ((abs(bearingDelta) > tackBearing) && (abs(appWind2SecAvg) <= 35))) || (beyondBoundary && !sailingAwayFromBoundary)) {    // need to tack because either reached sub layline and apparent <= 35  or a boundary
           
               if(beyondBoundary  && !sailingAwayFromBoundary) {
                 
                  sailingAwayFromBoundaryTimer = millis();
                  sailingAwayFromBoundary = true;
                 
               }
               

                 
               longDistanceRaceTack();
               okToTack = false;
               okToTackTimer = millis();
                          
               if(!starboard) {                                                              // set port settings - tacking from starboard to port **** TACK BEGIN  
                  
                    starboard = true;
                    upWindTargetApprentWind = abs(upWindTargetApprentWind);
                     
               } else {                                                                               // set starboard settings - tacking from port to starboard 
                   
                    starboard = false;
                    upWindTargetApprentWind = -1*abs(upWindTargetApprentWind);
           
               }
                            
           }                                                                                          // **** BEAT END
            
           beatCourse = true;                                                                         // set beat to true
           directCourse = false;
           course = upWindTargetApprentWind;                                                                     
           steerMethod = apprentWindMethod;                     

       } else {                                                                                          // beat required  **** TACK END
                                                                                                    
        beatCourse = false;                                                                              // if beat or gybe not required sail directly to mark 
        directCourse = true;   
        course = bearingToNextMark;                                                                      // course is bearing to next mark
        steerMethod = compassMethod;                                                                     // steer method is compass 
        
       }
                                  
      
      if( beatCourse) {
        
        if(restrictRudder) {
          
           rudder.SetOutputLimits(-5,5);
           
        }
        
        sheetSetting = 100;        
      } 
      else
         sheetSetting = pgm_read_word_near( & apprentSheetSettings[abs(appWind2SecAvg)][weather]);       // pgm_read_word_near( & apprentSheetSettings[abs(appWind2SecAvg)][weather] )
       
      adjust_sheets(sheetSetting); 
      steer(steerMethod);  
            
      switch(steerMethod) {
      
            case compassMethod:strcpy(steerMethodStr,"Compass");
            break;
            case cogMethod:strcpy(steerMethodStr,"COG");
            break;
            case apprentWindMethod:strcpy(steerMethodStr,"Apparent");
            break;  
       }    
     
       if(beatCourse) {
          
           targetApprentWind = upWindTargetApprentWind;
           actualAprrentDelta = appWind2SecAvg - targetApprentWind ;         
        }
  
        if(directCourse) {
          
          targetApprentWind = 0;
          actualAprrentDelta = 0;
        } 
    
        dtostrf(COG, 5, 0, cogStr); 
        dtostrf(current_heading, 5, 0, current_headingStr);   
        dtostrf(bearingToNextMark, 5, 0, bearingStr);  
        dtostrf(bearingDelta, 5, 0, bearingDeltaStr); 
        dtostrf(SOG, 5, 2, sogStr);  
        dtostrf(((float)(pgm_read_word_near( & sogArray[abs(appWind2SecAvg)][weather])))/100, 5, 2, polarSogStr);       
        dtostrf(VMC, 5, 2, vmgStr);  
        
        dtostrf(distanceToMark, 6, 0, distToMarkStr);   
        dtostrf(northBoundaryDist, 6, 0, distNorthBoundaryStr);   
        dtostrf(southBoundaryDist, 6, 0, distSouthBoundaryStr);  
                
        //calcSheetPerc = pgm_read_word_near( & apprentSheetSettings[abs(appWind2SecAvg)][weather] );
        memory = freeRam (); 
       
        sprintf(data,"$F%7s %7s %8s %7s %7d %7d %7d %7d %7s %7s %7s %11s %5d %9s %9s %9s %9s %8d",cogStr,current_headingStr,
                      bearingStr,bearingDeltaStr,appWind2SecAvg,targetApprentWind,actualAprrentDelta,
                      sheetSetting,sogStr,polarSogStr,vmgStr,                  
                      steerMethodStr,weather,nextMarkStr,distToMarkStr,distNorthBoundaryStr,distSouthBoundaryStr,memory);                              
   
      if(millis() - update_timer >= 50) {
      
        update_timer = millis();
        Serial3.println(data);
                         
    }     
      
    if (distanceToMark <= markRadius)   {                                                            // if within 6m or 8m of mark sail to next mark - set mark description and next mark waypoint
       if(nextMarkNumber < 13)                                                                       // if not finished increment next mark number
           nextMarkNumber++;  
                                                                                                     
       switch(nextMarkNumber) {                                                                      
               case 1:strcpy(nextMarkStr,"WestN-1");                                                
                      nextMark = westMarkNorth;
                      markRadius = 6.0;                      
               break;
               case 2:strcpy(nextMarkStr,"WestS-1");
                      nextMark = westMarkSouth; 
                      markRadius = 8.0;
               break;
               case 3:strcpy(nextMarkStr,"Start-1"); 
                      nextMark = startMark;
                      restrictRudder = true;  
                      restrictRudderTimer  = millis();                  
                      markRadius = 6.0;                      
               break;        
               case 4:strcpy(nextMarkStr,"EastS-1");
                      nextMark = eastMarkSouth;   
                      markRadius = 6.0;                      
               break;
               case 5:strcpy(nextMarkStr,"EastN-1");
                      nextMark = eastMarkNorth;                   
                      markRadius = 8.0;                      
               break;
               case 6:strcpy(nextMarkStr,"Start-2");
                      nextMark = startMark;  
                      restrictRudder = true; 
                      restrictRudderTimer  = millis();                        
                      markRadius = 6.0;                      
               break;
               case 7:strcpy(nextMarkStr,"WestN-2"); 
                      nextMark = westMarkNorth;  
                      markRadius = 6.0;                      
               break;               
               case 8:strcpy(nextMarkStr,"WestS-2"); 
                      nextMark = westMarkSouth ;                      
                      markRadius = 8.0;                      
               break;          
               case 9:strcpy(nextMarkStr,"Start-3");
                      nextMark = startMark;   
                      restrictRudder = true;  
                       restrictRudderTimer  = millis();                       
                      markRadius = 6.0;                      
               break;
               case 10:strcpy(nextMarkStr,"EastS-2");
                      nextMark = eastMarkSouth;  
                      markRadius = 6.0;                      
               break;
               case 11:strcpy(nextMarkStr,"EastN-2"); 
                      nextMark = eastMarkNorth;  
                      markRadius = 8.0;                      
               break;             
               case 12:strcpy(nextMarkStr,"Finish"); 
                      nextMark = startMark;  
                      restrictRudder = true;  
                      restrictRudderTimer  = millis();                       
                      markRadius = 6.0;                      
               break; 
               case 13:strcpy(nextMarkStr,"Done"); 
                      nextMark = westMarkNorth;
                      markRadius = 6.0;                      
               break;                            
            }
                            
       }   

   }                                                                                                // END of LD RACE LOOP -  data switch is now data_input_switch < Read_GUI_Data_Challenge_Finished  
   
   data_received = false; 
   sailingChallenge = false;                                                                        // challenge complete
 
}

//***********************************************************************************************************************************

void longDistanceRaceTack() {
  
  int H = ((double)tack_rudder_angles[reach][weather]/100)*45;
  long tackTimer,startTimer;
  
  boolean prevTackStarbard;
  boolean tackFailed = false;
 // boolean useActualApparent = false;
  
  int baseRudderTime;
  int preTackRudderAngle;
  int newTarget;
  
  Serial3.println("$FTack ");
  
//  baseRudderTime = challenge.leewayMax*100;
  preTackRudderAngle = challenge.leewayCor;   
  
  switch(weather) {
   
    case 0: baseRudderTime = 1500;
            break;
   
    case 1: baseRudderTime = 1300;
            break;
            
    case 2: baseRudderTime = 1200;
            break;
   
    case 3: baseRudderTime = 1100;
            break;             
  } 
  
  /*
  if(challenge.heading1 == 1)
     useActualApparent = true;
  */   

  if (!starboard) H = -H;
   
  if (starboard) { 
    
     newTarget = -30;
     prevTackStarbard = true;
     preTackRudderAngle =  -preTackRudderAngle;    
     
  } else {
  
     newTarget = 30;
     prevTackStarbard = false;
     
  }
    
 
  adjust_sheets(95);
  APM_RC.OutputCh(rudder_output,((preTackRudderAngle*rudder_increment) + rudder_centre));    
  tackTimer = 0;
  startTimer = millis();
  while(tackTimer < 2000){
    
    tackTimer = millis() - startTimer;
    read_radio();
    if(pilot_switch < RC_sail) {
        emergencySail();
        break;
    }
  }
  
  startTimer = millis();
  tackTimer = 0;  
  APM_RC.OutputCh(rudder_output,((0.5*H*rudder_increment) + rudder_centre));  
  while(tackTimer < baseRudderTime){
    
    tackTimer = millis() - startTimer;
    read_radio();
    if(pilot_switch < RC_sail) {
        emergencySail();
        break;
    }
  }  

  startTimer = millis();  
  tackTimer = 0; 
  APM_RC.OutputCh(rudder_output, ((1.2*H*rudder_increment) + rudder_centre));  
  while(tackTimer < baseRudderTime*2){
        
    tackTimer = millis() - startTimer;
    read_radio();
    if(pilot_switch < RC_sail) {
        emergencySail();
        break;
    }
  }      
 
  adjust_sheets(sheet_setting[CCR][weather]);
  tackTimer = 0;
  startTimer = millis();
  while(tackTimer < baseRudderTime){
    
    tackTimer = millis() - startTimer;
    read_radio();
    if(pilot_switch < RC_sail) {
        emergencySail();
        break;
    }
  }    
  /*
  update_ApprentWind();
  
  if(appWind2SecAvg >= 0) {
    
    if(prevTackStarbard == true) 
       tackFailed = true;
    
  } else {
    
    if(prevTackStarbard == false) 
       tackFailed = true;    
    
  }
  
  if(tackFailed) {
  
     Serial3.println("$FGybe ");
     longDistanceRaceGybe();
     
  }   
 */    
 
 
 int apparentCount = 0;
 int apparentTotal = 0;
 long apparentTimer = millis();
  
 while(apparentCount < 10) {
   
   if(millis() - apparentTimer >= 50) {
     
      update_ApprentWind(); 
      apparentTotal += apprentWind;
      apparentCount++;
      apparentTimer = millis();
   }
   
 }
 
 apprentWind = apparentTotal/10;

/*
 if(!useActualApparent)   
    apprentWind = newTarget; 
*/

 for(int i  = 0; i < 120 ; i++)                           
      averageApprentWind();


}
  


//***********************************************************************************************************************************
int freeRam () {
  extern int __heap_start, *__brkval; 
  int v; 
  return (int) &v - (__brkval == 0 ? (int) &__heap_start : (int) __brkval); 
}


//***********************************************************************************************************************************

void longDistanceRaceGybe() {

  
  int H = ((double)tack_rudder_angles[bear_off][weather]/100)*45;
  long tackTimer,startTimer;

  if (starboard) H = -H;
       
    adjust_sheets(sheet_setting[BBR][weather]);
    Output = H;
    APM_RC.OutputCh(rudder_output, H*rudder_increment + rudder_centre); 
    tackTimer = 0;
    startTimer = millis();
    while(tackTimer < 4000){
    
    tackTimer = millis() - startTimer;
    read_radio();
    if(pilot_switch < RC_sail) {
        emergencySail();
        break;
    }
  }    
}
  
  

//***********************************************************************************************************************************

void navigation_tack() {
  
  int H = ((double)tack_rudder_angles[reach][weather]/100)*45;
  long tackTimer,startTimer;
  
  
  int baseRudderTime;
  int preTackRudderAngle;
  
  baseRudderTime = challenge.leewayMax*100;
  preTackRudderAngle = challenge.leewayCor;   

  if (!starboard) H = -H;
   
  if (starboard) {
    
     preTackRudderAngle =  -preTackRudderAngle;    
     
  }
 
  adjust_sheets(95);
  APM_RC.OutputCh(rudder_output,((preTackRudderAngle*rudder_increment) + rudder_centre));      
  tackTimer = 0;
  startTimer = millis();
  while(tackTimer < 2000){
    
    tackTimer = millis() - startTimer;
    read_radio();
    if(pilot_switch < RC_sail) {
        emergencySail();
        break;
    }
  }
   
  if (starboard)
    starboard = false;
  else
    starboard = true;    
  
  startTimer = millis();
  tackTimer = 0;  
  APM_RC.OutputCh(rudder_output,((0.5*H*rudder_increment) + rudder_centre));   
  while(tackTimer < baseRudderTime){
    
    tackTimer = millis() - startTimer;
    read_radio();
    if(pilot_switch < RC_sail) {
        emergencySail();
        break;
    }
  }  

  startTimer = millis();  
  tackTimer = 0; 
  APM_RC.OutputCh(rudder_output, ((1.2*H*rudder_increment) + rudder_centre));  
  while(tackTimer < baseRudderTime*2){
        
    tackTimer = millis() - startTimer;
    read_radio();
    if(pilot_switch < RC_sail) {
        emergencySail();
        break;
    }
  }      
 
  adjust_sheets(sheet_setting[CCR][weather]);
  tackTimer = 0;
  startTimer = millis();
  while(tackTimer < baseRudderTime){
    
    tackTimer = millis() - startTimer;
    read_radio();
    if(pilot_switch < RC_sail) {
        emergencySail();
        break;
    }
  }    


}
    
/*  

void navigation_tack() {


  int H = ((double)tack_rudder_angles[reach][weather]/100)*45;
  long tackTimer,startTimer;

  if (!starboard) H = -H;
   
  if (starboard) 
     course  = compass_calculation(course - 5);
  else
     course  = compass_calculation(course + 5);  

  Serial3.println("$B***** Navigation Tack *****");
    
 
  adjust_sheets(sheet_setting[B][weather]);
  tackTimer = 0;
  startTimer = millis();
  while(tackTimer < 4000){
    
    steer(compassMethod);
    tackTimer = millis() - startTimer;
    read_radio();
    if(pilot_switch < RC_sail) {
        emergencySail();
        break;
    }
  }
  

    

  startTimer = millis();
  tackTimer = 0;  
  APM_RC.OutputCh(rudder_output, 0.5*H*rudder_increment + rudder_centre);  
  while(tackTimer < 1000){
    
    tackTimer = millis() - startTimer;
    read_radio();
    if(pilot_switch < RC_sail) {
        emergencySail();
        break;
    }
  }  

  startTimer = millis();
  tackTimer = 0; 
  APM_RC.OutputCh(rudder_output, H*rudder_increment + rudder_centre);  
  while(tackTimer < 1000){
    
    tackTimer = millis() - startTimer;
    read_radio();
    if(pilot_switch < RC_sail) {
        emergencySail();
        break;
    }
  }    
  
  startTimer = millis();  
  tackTimer = 0; 
  APM_RC.OutputCh(rudder_output, 1.2*H*rudder_increment + rudder_centre);  
  while(tackTimer < 1000){
    
    tackTimer = millis() - startTimer;
    read_radio();
    if(pilot_switch < RC_sail) {
        emergencySail();
        break;
    }
  }      
  
  adjust_sheets(sheet_setting[R][weather]);
  tackTimer = 0;
  startTimer = millis();
  while(tackTimer < 1500){
    
    tackTimer = millis() - startTimer;
    read_radio();
    if(pilot_switch < RC_sail) {
        emergencySail();
        break;
    }
  }    



}

*/

//***********************************************************************************************************************************

void navigation_bearaway_gybe(int timeInGybe) {

  
  int H = ((double)tack_rudder_angles[bear_off][weather]/100)*45;
  long gybeTimer,startTimer;

  if (starboard) H = -H;

   
    Serial3.println("$B***** Navigation bearaway / gybe *****");
  
       
    adjust_sheets(sheet_setting[BBR][weather]);
    //Output = H;
    APM_RC.OutputCh(rudder_output, H*rudder_increment + rudder_centre); 
    gybeTimer = 0;
    startTimer = millis();
    while(gybeTimer < timeInGybe){
          
      gybeTimer = millis() - startTimer;
      read_radio();
      if(pilot_switch < RC_sail) {
         emergencySail();
         break;
      }
  }    
    

}

//***********************************************************************************************************************************


void station_keeping_gybe(String message) {

  
  int H = 85;
  long gybeTimer,startTimer;

  if (starboard) H = -H;

   Serial3.println("$C"+message);
   
  
       
    adjust_sheets(25);
    //Output = H;
    APM_RC.OutputCh(rudder_output, H*rudder_increment + rudder_centre); 
    gybeTimer = 0;
    startTimer = millis();
    while(gybeTimer < 4000){
    
      gybeTimer = millis() - startTimer;
      read_radio();
      if(pilot_switch < RC_sail) {
          emergencySail();
          break;
    }
  }    
    

}

//***********************************************************************************************************************************
/*
void station_keeping_tack() {

  int H = ((double)tack_rudder_angles[beat][weather]/100)*45;
  long tackTimer,startTimer;
  
  if (!starboard) H = -H;
  
     
  Serial3.println("$C***** Station Keeping Tack *****");
 
  
  adjust_sheets(sheet_setting[CR][weather]);
  steer(compassMethod);
  tackTimer = 0;
  startTimer = millis();
  while(tackTimer < 2000){
    
    tackTimer = millis() - startTimer;
    read_radio();
    if(pilot_switch < RC_sail) {
        emergencySail();
        break;
    }
  }
  
  adjust_sheets(sheet_setting[B][weather]);
  APM_RC.OutputCh(rudder_output, H*rudder_increment + rudder_centre); 

  
  tackTimer = 0;
  startTimer = millis();   
  while(tackTimer < 3000){
    
    tackTimer = millis() - startTimer;
    read_radio();
    if(pilot_switch < RC_sail) {
        emergencySail();
        break;
    }
  }  
   
  adjust_sheets(sheet_setting[R][weather]);
  tackTimer = 0;
  startTimer = millis();
  while(tackTimer < y){
    
    tackTimer = millis() - startTimer;
    read_radio();
    if(pilot_switch < RC_sail) {
        emergencySail();
        break;
    }
  }                                

}
*/
//***********************************************************************************************************************************

int resetWeather() {
  

  int newWeather = 0;
  float level1;
  float level2;  
  float level3;  
  
  
  
  level1 = ((((float)pgm_read_word_near( &sogArray[abs(appWind2SecAvg)][0]))/100 + ((float)pgm_read_word_near( &sogArray[abs(appWind2SecAvg)][1]))/100))/2;  
  level2 = ((((float)pgm_read_word_near( &sogArray[abs(appWind2SecAvg)][1]))/100 + ((float)pgm_read_word_near( &sogArray[abs(appWind2SecAvg)][2]))/100))/2; //1 2
  level3 = ((((float)pgm_read_word_near( &sogArray[abs(appWind2SecAvg)][2]))/100 + ((float)pgm_read_word_near( &sogArray[abs(appWind2SecAvg)][3]))/100))/2; //2 3  
  
  if(sog2SecAvg <= level1) {
    
     newWeather = 0; 
    
  }
 
  if(sog2SecAvg > level1 && sog2SecAvg <= level2) {
    
     newWeather = 1;
    
  }
  
  if(sog2SecAvg > level2 && sog2SecAvg <= level3) {
    
     newWeather = 2;    
    
  }

  if(sog2SecAvg > level3)  {
    
     newWeather = 3;    
    
  }
  
 return newWeather; 
}  

//***********************************************************************************************************************************
/*
void fillSogArray() {
    
    
    int j;
    int i,k;
    int range;
    float increment;
    
    int  sogByWeatherByApprent[4][2][10]
                 = {{{26,28,34,44,54,68,75,94,122,128},{119,128,138,147,151,153,152,138,117,115}},
                    {{27,33,40,52,64,80,89,108,131,150},{131,145,157,167,175,181,183,173,153,148}},
                    {{28,36,44,57,70,88,97,112,134,170},{161,170,178,190,204,216,228,241,217,197}},
                    {{34,40,48,63,75,93,102,116,136,170},{168,177,187,201,218,240,263,294,286,270}}};
    
    for (int weatherCode = 0; weatherCode < 4; weatherCode++) {
        j = 0;
        while (j <= sogByWeatherByApprent[weatherCode][0][0]) 
            sogArray[weatherCode][j++] = sogByWeatherByApprent[weatherCode][1][0];
            for (i = 0; i < 9; i++) {
                range = sogByWeatherByApprent[weatherCode][0][i+1] 
                                - sogByWeatherByApprent[weatherCode][0][i];
                increment = (sogByWeatherByApprent[weatherCode][1][i+1]
                                - sogByWeatherByApprent[weatherCode][1][i])/(float)range;  
                for (k = 0; k < range - 1 ; k++) {
                    sogArray[weatherCode][j++]
                       = (int)((float)sogByWeatherByApprent[weatherCode][1][i] + increment*(k+1) );
                }
                sogArray[weatherCode][j++] = sogByWeatherByApprent[weatherCode][1][i+1];                
    
            }
            while (j < 181)
                sogArray[weatherCode][j++] = sogByWeatherByApprent[weatherCode][1][9];  
    }
    
}
*/
//***********************************************************************************************************************************
/*
void sheetPercentCalculation(int weather,int sheetPercentArray[]) {
    
    
    int j = 0;
    int i,k;
    int range;
    float increment;
    
    
    int  sheetPercentByWeatherByApprent[4][2][10]
                 = {{{26,28,34,44,54,68,75,94,122,128},{95,90,85,80,70,60,50,40,20,15}},
                    {{27,33,40,52,64,80,89,108,131,150},{100,95,92,80,70,60,50,40,20,15}},
                    {{28,36,44,57,70,88,97,112,134,170},{95,93,90,80,69,59,50,40,20,15}},
                    {{34,40,48,63,75,93,102,116,136,170},{90,88,85,78,65,56,48,38,20,15}}};
    
        while (j <= sheetPercentByWeatherByApprent[weather][0][0]) 
            sheetPercentArray[j++] = sheetPercentByWeatherByApprent[weather][1][0];
            for (i = 0; i < 9; i++) {
                range = sheetPercentByWeatherByApprent[weather][0][i+1] 
                                - sheetPercentByWeatherByApprent[weather][0][i];
                increment = (sheetPercentByWeatherByApprent[weather][1][i+1]
                                - sheetPercentByWeatherByApprent[weather][1][i])/(float)range;  
                for (k = 0; k < range - 1 ; k++) {
                    sheetPercentArray[j++]
                       = (int)((float)sheetPercentByWeatherByApprent[weather][1][i] + increment*(k+1) );
                }
                sheetPercentArray[j++] = sheetPercentByWeatherByApprent[weather][1][i+1];                
    
            }
            while (j < 181)
                sheetPercentArray[j++]= sheetPercentByWeatherByApprent[weather][1][9];      
    
}

*/
//***********************************************************************************************************************************

void adjust_sheets(int sheet_percent) {

       int altRcPercent;
       
       //altRcPercent = pow( sheet_percent,1.65) * 0.05 ;
       
       altRcPercent = pow( sheet_percent,1.74) * 0.033 ;
       
       APM_RC.OutputCh(sheet_output,sheet_end - altRcPercent*sheet_increment ); 
}

//***********************************************************************************************************************************

void steer(int  sailByCourse) {
  

    
  calculate_PID_input(sailByCourse);
  
  rudder.Compute();          //PID calculates rudder Output correction
 

  APM_RC.OutputCh(rudder_output, Output*rudder_increment + rudder_centre);
     

}


//***********************************************************************************************************************************

void calculate_PID_input(int sailByCourse) {
    

    int difference;
   
    Input = 0;
       
        
    switch(sailByCourse) {
   
    case compassMethod: difference = course - current_heading;
    break;
    
    case cogMethod: difference = course - COG;
    break;
 
    case apprentWindMethod: difference = appWind6SecAvg - course;
    break;      
      
  
    }    
    
  
    if (difference > 180 || difference < -180) {
        if (difference < 0) {
            difference += 360;
        }
        else {
               difference -= 360;
        }
        Setpoint = 0;
        Input -= difference;
            
        }
        else {
                Setpoint = 0;
                Input -= difference;        
        }
    

}


//***********************************************************************************************************************************

double compass_calculation(double compass_heading) {

  if (compass_heading >= 360.0) 
    return (compass_heading - 360.0);
  else
    if (compass_heading < 0.0) 
      return (360.0 + compass_heading);
    else
      return compass_heading;

}
//***********************************************************************************************************************************


double calculate_bearing_delta(double bearing1, double bearing2) {
    
    double difference;
    
    difference = bearing1 - bearing2;
    if (difference > 180.0 || difference < -180.0) {
        if (difference < 0) {
            difference += 360.0;
        }
        else {
            difference -= 360.0;
        }
    }        

    return difference;
}



//***********************************************************************************************************************************


double Bearing_to_wpts(long llon1,long llat1,long llon2,long llat2)

{
   
  double deltaX = llon1 - llon2 ;
  double deltaY = llat1 - llat2 ;

  double angle;
  double new_angle;   
    
  if(deltaX == 0) {
    
    if(deltaY == 0 )
      return 0.0;
    else
      if(deltaY > 0)
        return 180.0;
      else
        return 0.0;     
  
  }  
  
  if(deltaY == 0) {
    
    if(deltaX == 0)
      return 0.0;
    else  
      if(deltaX > 0)
        return 270.0;
      else
        return 90.0;  
    
    
  }
  
  angle = ToDeg((atan((LonX(deltaX)/(LatY(deltaY))))));

  if(angle < 0)
    angle += 90;  
  
  if(deltaX > 0) {
    
      if(deltaY > 0)
        return 180.0 + angle;
      else
        return 270.0 + angle;     
  
  }  else {
    
      if(deltaY > 0)
        return 90.0 + angle;
      else
        return 0.0 + angle;    
  }
  

}

//***********************************************************************************************************************************

double Dist_to_wpts(long llon1,long llat1,long llon2,long llat2)

{

  double deltaX = llon1 - llon2;
  double deltaY = llat1 - llat2;
  double distance_to_wpt;
  
  distance_to_wpt = sqrt(LonX(deltaX) * LonX(deltaX) + LatY(deltaY) * LatY(deltaY));
  
  return distance_to_wpt ;     
  
}

//***********************************************************************************************************************************


void calcWpt (double angle, double distVector, struct Waypoint *p, struct Waypoint *calcWpt ) {
  
   int sector = angle / 90;
   double radAngle;
 
  switch(sector) {
    
    case 0: radAngle = ToRadians(angle);
            calcWpt -> longitude = p -> longitude + (long)MeterToLonX(sin(radAngle) * (distVector));
            calcWpt -> latitude = p -> latitude + (long)MeterToLatY(cos(radAngle) * (distVector));    
            break;   

    case 1: radAngle = ToRadians((angle - 90.0));
            calcWpt -> longitude = p -> longitude + (long)MeterToLonX(cos(radAngle) * (distVector));
            calcWpt -> latitude = p -> latitude - (long)MeterToLatY(sin(radAngle) * (distVector));    
            break;   
    
    case 2: radAngle = ToRadians((angle - 180.0));
            calcWpt -> longitude = p -> longitude - (long)MeterToLonX(sin(radAngle) * (distVector));
            calcWpt -> latitude = p -> latitude - (long)MeterToLatY(cos(radAngle) * (distVector));    
            break;     

    case 3: radAngle = ToRadians((angle - 270.0));
            calcWpt -> longitude = p -> longitude - (long)MeterToLonX(cos(radAngle) * (distVector));
            calcWpt -> latitude = p -> latitude + (long)MeterToLatY(sin(radAngle) * (distVector));    
            break;
   
  }
}  

//***********************************************************************************************************************************
