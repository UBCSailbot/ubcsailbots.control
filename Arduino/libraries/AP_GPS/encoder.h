

#ifndef encoder_h
#define encoder_h

#include <inttypes.h>
#include <Stream.h>


class Encoder
{
public:

	void			update(void);
 
	virtual void	init(void) = 0;

	int	apprentWind;			



protected:
	Stream	*_port;			


	Encoder(Stream *s) : _port(s) {};


	virtual bool	read(void) = 0;
    
 

private:


	
};

#endif
