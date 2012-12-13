
#include "DataRead.h"
	
DataRead::DataRead(Stream *s) : Reader(s)
{
}

// Public Methods //////////////////////////////////////////////////////////////
void 
DataRead::init(void)
{
	
}

bool
DataRead::read(void)
{
	char c;
	int numc;
	int i;
	bool parsed = false;
    

    
 	numc = _port->available();

    
	if (numc > 0){
		
		for (i = 0; i < numc; i++){
			c = _port->read();
 
                                       
			if (c == '@'){											
				bufferidx = 0;
				buffer[bufferidx++] = c;
				continue;
				}
			if (c == '#'){										 
				
                
				buffer[bufferidx++] = c;
				buffer[bufferidx] = '\0';
				parsed = parse_data();
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
DataRead::parse_data(void)
{
	strcpy(data,buffer);
	return true;
}


