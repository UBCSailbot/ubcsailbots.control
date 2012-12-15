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

FastSerialPort0(Serial);
FastSerialPort1(Serial1);   // GPS port (except for GPS_PROTOCOL_IMU)
FastSerialPort3(Serial3);   // xBee communication between boat and laptop

boolean data_received = false;
boolean sailingChallenge = false;
//int inCount = 0;

GPS         *g_gps;
HEMISPHERE_GPS_NMEA     g_gps_driver(&Serial1);
unsigned short MA3_pin=63;//**TODO this needs to be verified!

//***********************************************************************************************************************************

void setup()
{

  delay(500);          //Wait at least 500 milli-seconds for device initialization
  Wire.begin();        // join i2c bus (address optional for master)
  
  pinMode(MA3_pin, OUTPUT);
  digitalWrite(MA3_pin, HIGH);

  Serial.begin(57600, 128, 128); 
  Serial1.begin(57600, 128, 128); 
  Serial3.begin(57600, 256, 128);
  
  g_gps = &g_gps_driver;
  g_gps->init(); 

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

  apprentWind = readEncoder();
  averageApprentWind();
  
}

//from http://rpg.dosmage.net/project/sailboat/_m_a3_8pde_source.html
int readEncoder(){
  int  MA3_OFFSET=0;//this is the absolute offset
   int MA3_reading = analogRead(MA3_pin);
   int MA3_heading = add_headings( map(MA3_reading, 0, 1007, 0, 359), - MA3_OFFSET );
   return MA3_heading;
}

 int add_headings(int heading_a, int heading_b)
{
   return (heading_a + heading_b + 360) % 360; //this could be a problem since we have typically done things in +/- 180
}

void averageApprentWind() {
  //**TODO
  //complete a new averaging algorithm
  
  
  
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

  

   int tableSheetPerecnt;
   int calcSheetPerc;
   
   float rcSheetPercent;  
   int altRcPercent;   
     
   while(pilot_switch < RC_sail || data_input_switch < Read_GUI_Data_Challenge_Finished) {
                   
         read_radio();   
         APM_RC.OutputCh(rudder_output, radio_in[rudder_output]);           
         APM_RC.OutputCh(sheet_output, radio_in[sheet_output]);   
         read_data_fromPi();                 
         
         rcSheetPercent = (sheet_end - radio_in[sheet_output])/sheet_increment;
         
         altRcPercent = pow(rcSheetPercent,0.625) * 5.62 ;
         
            update_GPS();
            update_ApprentWind();           
                
         if(millis() - update_timer >= 50) {
        
            update_timer = millis();   
                        
           dtostrf(COG, 7, 0,cogStr );     
           dtostrf(current_heading, 7, 1,current_headingStr );  
            
           sprintf(guiDataRC,"$A%11ld %11ld %8s %8s %8d %8d %8d %8d %8d %8d ",current_position -> longitude,
                             current_position -> latitude,cogStr,current_headingStr,apprentWind,appWind2SecAvg,
                             appWind6SecAvg,altRcPercent,g_gps -> hemisphereSatelites,g_gps->hdop);  
                                                                                                                                                                                                                                                                                                    
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

 void read_data_fromPi () {

    #define INLENGTH 250
   char inString[INLENGTH + 1] ;
   int inCount; 

   inCount = 0;
 
   while(Serial.available() > 0)  {                                                 
     inString[inCount++] = Serial.read();                                           
     delay(2);   // Changed from 1 May 17, 2012 by JK.
     
   }
 
   inString[inCount] = '\0';      
     
    if(inCount > 0)  
     {
      int sheet_percentage=atoi(inString);
      Serial.println(sheet_percentage);
      adjust_sheets(sheet_percentage);
      //**TODO this won't work because it is called inside RC_sail so RC overrids
      }


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
