

#ifndef readdata_h
#define readdata_h

#include <inttypes.h>
#include <Stream.h>


class ReadData
{
public:

	void			update(void);
 
	virtual void	init(void) = 0;

	char	data[250];			



protected:
	Stream	*_port;			


	Encoder(Stream *s) : _port(s) {};


	virtual bool	read(void) = 0;
    
 

private:


	
};

#endif
