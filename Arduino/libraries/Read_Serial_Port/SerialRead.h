

#ifndef SerialRead_h
#define SerialRead_h

#include "WProgram.h"

#include <inttypes.h>
#include <Stream.h>

class SerialRead
{
public:


    

//	void	init(void) = 0;
	
        
	char dataRead[512];

	SerialRead(Stream *s) : _port(s) {};
	int readPort(void);
	
protected:
	Stream	*_port;	
	




    

	long	_swapl(const void *bytes);

	int	_swapi(const void *bytes);



};

inline long
SerialRead::_swapl(const void *bytes)
{
	const uint8_t	*b = (const uint8_t *)bytes;
	union {
		long	v;
		uint8_t b[4];
	} u;

	u.b[0] = b[3];
	u.b[1] = b[2];
	u.b[2] = b[1];
	u.b[3] = b[0];

	return(u.v);
}

inline int16_t
SerialRead::_swapi(const void *bytes)
{
	const uint8_t	*b = (const uint8_t *)bytes;
	union {
		int16_t	v;
		uint8_t b[2];
	} u;

	u.b[0] = b[1];
	u.b[1] = b[0];

	return(u.v);
}

#endif
