// -*- tab-width: 4; Mode: C++; c-basic-offset: 4; indent-tabs-mode: t -*-
#ifndef EncoderRead_h
#define EncoderRead_h

#include <Encoder.h>
#include <stdio.h>
#include <stdlib.h>


#define ENCODER_BUFFERSIZE 10 





class EncoderRead : public Encoder
{
  public:
    // Methods
	EncoderRead(Stream *s);
	virtual void init();
	virtual bool read();
 

  private:
 
	char buffer[ENCODER_BUFFERSIZE];
	int bufferidx;

	bool parse_apptWind(void);


};

#endif
