//sailbotsketch
//Created by David Lee on Dec 13, 2012

//based on
//UBCsailBot2012_2_14_5
//Ver. 2.14.5
//Last update by John K. June 9, 2012

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
#include <PIDv1.h>  
#include <avr/pgmspace.h>


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
int appWind2SecAvg = 0; 
int appWind6SecAvg = 0;

float sog2SecAvg = 0.0;


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
  
  //**TODO update this so that it reads from the new encoder
  windEncoder = &encoder_driver;
  windEncoder->init();

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
         pi_sail();
 
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
    static boolean appWind6secArrayFilled = false;
    static boolean appWind2secArrayFilled = false;    
    static int appWindArray6sec[120]; 
    static int appWindArray2sec[40]; 
    static int i6 = 0,i2 = 0;
    static long appWind2SecTotal = 0;
    static long appWind6SecTotal = 0;


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

    
}


void averageSOG() {

    static boolean sog2secArrayFilled = false;  
    static int sogArray2sec[40]; 
    static int i2 = 0;
    static long sog2SecTotal = 0;

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

void pi_sail() {
  
  
//**TODO**
  

}



//***********************************************************************************************************************************

 void read_data_fromGUI () {
 
 //**TODO**
 //change this to read from Pi
 //  #define INLENGTH 250
//  
//   
//   char inString[INLENGTH + 1] ;
//   int inCount; 
//   
// 
//   
//   inCount = 0;
// 
//   while(Serial3.available() > 0)  {                                                 
//     inString[inCount++] = Serial3.read();                                           
//     delay(2);   // Changed from 1 May 17, 2012 by JK.
//     
//   }
// 
//   inString[inCount] = '\0';      
//     
//    if(inCount > 0)  
//     {
//      // inCount = 0; 
//       data_received = true;
//       challenge.parse_challenge_data(inString+1,inCount-1);  
//       
//       
//       Serial3.println(inString);                                                    
//     }
 } 

//***********************************************************************************************************************************
void setPIDforChallenge() {
  
  rudder.SetMode(AUTOMATIC);
  
  //**TODO** test these constants
  int  rudderLimit=20;
  double kp = 1.2;
  double ki = 0.05;
  double kd = 0;
  double pidInterval = 200;
  
  rudder.SetOutputLimits(-rudderLimit,rudderLimit);
  rudder.SetTunings(kp, ki, kd);                     //set PID Constants    
  rudder.SetSampleTime(pidInterval);   
  
}

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
  
  //**TODO find out what leewayCor does
  //  preTackRudderAngle = challenge.leewayCor;   
  
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
    //**TODO find out what leewayCor does
   // baseRudderTime = challenge.leewayMax*100;
   // preTackRudderAngle = challenge.leewayCor;   

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
