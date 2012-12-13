// -*- tab-width: 4; Mode: C++; c-basic-offset: 4; indent-tabs-mode: t -*-
#ifndef DataRead_h
#define DataRead_h

#include <Reader.h>
#include <stdio.h>
#include <stdlib.h>


#define DATA_BUFFERSIZE 250 





class DataRead : public Reader
{
  public:
    // Methods
	DataRead(Stream *s);
	virtual void init();
	virtual bool read();
 

  private:
 
	char buffer[DATA_BUFFERSIZE];
	int bufferidx;

	bool parse_data(void);


};

#endif
