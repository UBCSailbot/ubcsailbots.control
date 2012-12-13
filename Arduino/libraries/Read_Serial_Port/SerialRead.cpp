
#include "SerialRead.h"
	


int  SerialRead::readPort(void)
{
	char c;
	int numc;
	int i;
	bool parsed = false;
    

    
 	numc = _port->available();
	
	               
	dataRead[0] = '\0';               
    
	if (numc > 0){
		for (i = 0; i < numc; i++){
			c = _port->read();
            
            if (i < 512) {              
                dataRead[i] = c;        
            }

		}
		dataRead[numc] = '\0';	
    }
	
	return numc;
}
