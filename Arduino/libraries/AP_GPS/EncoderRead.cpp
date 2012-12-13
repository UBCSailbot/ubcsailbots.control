
#include "EncoderRead.h"
	



EncoderRead::EncoderRead(Stream *s) : Encoder(s)
{
}

// Public Methods //////////////////////////////////////////////////////////////
void 
EncoderRead::init(void)
{

	
}


 
 
bool
EncoderRead::read(void)
{
	char c;
	int numc;
	int i;
	bool parsed = false;
    

    
 	numc = _port->available();

    
	if (numc > 0){
		
		for (i = 0; i < numc; i++){
			c = _port->read();
 
                                       
			if (c == '*'){											
				bufferidx = 0;
				continue;
				}
			if (c == '#'){										 
				
                
				buffer[bufferidx] = '\0';
				parsed = parse_apptWind();
				bufferidx = 0;
				break;
				
				
			} else {
					
					buffer[bufferidx++] = c;
									 
				
			}
		}
	}
}

//****************************************************************
 
// Private Methods //////////////////////////////////////////////////////////////
bool
EncoderRead::parse_apptWind(void)
{
	apprentWind = atoi(buffer);
	return true;
}


