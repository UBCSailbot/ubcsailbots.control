//
//  ChallengeClass.h
//  challenge
//
//  Created by John Kine on 11-12-20.
//  Copyright (c) 2011 None. All rights reserved.
//

#ifndef challenge_ChallengeClass_h
#define challenge_ChallengeClass_h

#include "WProgram.h"

class Challenge {
    
public:
    
    void parse_challenge_data(char *s, int s_len);

    
    struct wpt {
        
        long longitude;
        long latitude;
    };
 

    
    char data[256];
    int data_len;
    bool validData;
    int task;
    int weather;
    int rounding;
    float heading1;
    float heading2;
    float heading3;
    float kp;
    float ki;
    float kd;
    int pidInterval;
	int testTarget;
	int testMethod;
    int rudderLimit;
    int leewayCor;
    int leewayMax;
    wpt wpts[8];
    int number_wpts;
    
};

#endif
