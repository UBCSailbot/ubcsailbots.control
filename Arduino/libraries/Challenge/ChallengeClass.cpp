//
//  ChallengeClass.cpp
//  challenge
//
//  Created by John Kine on 11-12-20.
//  Copyright (c) 2011 None. All rights reserved.
//

#include "WProgram.h"

#include <stdlib.h>
#include <string.h>
#include "ChallengeClass.h"



void Challenge::parse_challenge_data(char *s, int s_len) {

    strcpy(data,s);
    data_len = s_len;
	
    char * parseptr;
    
    if (data[0] == 64 && data[data_len - 1] == 35) { 
        validData = true;
        
    } else {
        
        validData = false;
    }

    
    parseptr = strchr(data, '@')+1;        
    task = atoi(parseptr);
    
    switch (task) {
        case 0:
            number_wpts = 2;
            break;
        case 1:
            number_wpts = 4;
            break;   
        case 2:
            number_wpts = 7;
            break;             
        default:
            break;
    }
    
    parseptr = strchr(parseptr, ',') + 1;
    
    weather = atoi(parseptr);
    
    parseptr = strchr(parseptr, ',') + 1;
    
    rounding = atoi(parseptr);    
        
    parseptr = strchr(parseptr, ',') + 1;
    
    kp = atof(parseptr);        

    parseptr = strchr(parseptr, ',') + 1;
    
    ki = atof(parseptr);        

    parseptr = strchr(parseptr, ',') + 1;
    
    kd = atof(parseptr);   
    
    parseptr = strchr(parseptr, ',') + 1;    

    pidInterval = atoi(parseptr);  
	
    parseptr = strchr(parseptr, ',') + 1;    
	
    testTarget = atoi(parseptr);  
	
    parseptr = strchr(parseptr, ',') + 1;    
	
    testMethod = atoi(parseptr);  
	
    parseptr = strchr(parseptr, ',') + 1;

    rudderLimit = atoi(parseptr);    
    
    parseptr = strchr(parseptr, ',') + 1;
    
    leewayCor = atoi(parseptr);    
    
    parseptr = strchr(parseptr, ',') + 1;

    leewayMax = atoi(parseptr);    
    
    parseptr = strchr(parseptr, ',') + 1;
        
    heading1 = atof(parseptr);    
	
    parseptr = strchr(parseptr, ',') + 1;
	
    heading2 = atof(parseptr);    
    
    parseptr = strchr(parseptr, ',') + 1;
	
    heading3 = atof(parseptr); 
	
	
	for (int i = 0; i < number_wpts; i++) {
        
        parseptr = strchr(parseptr, ',') + 1;
        
        wpts[i].longitude = atol(parseptr);
        
        parseptr = strchr(parseptr, ',') + 1;
        
        wpts[i].latitude = atol(parseptr);
        
    }    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
};