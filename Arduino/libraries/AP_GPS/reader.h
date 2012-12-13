

#ifndef reader_h
#define reader_h

#include <inttypes.h>
#include <Stream.h>


class Reader
{
public:

	void			update(void);
 
	virtual void	init(void) = 0;

	char data[250];			



protected:
	Stream	*_port;			


	Reader(Stream *s) : _port(s) {};


	virtual bool	read(void) = 0;
    
 

private:


	
};

#endif
