#ifndef C_Buffer_h
#define C_Buffer_h


class C_Buffer
{
  public:

	C_Buffer::C_Buffer();
	int get_length();
	int get_nBytes();
	unsigned char read();
	int write(unsigned char w);
	


  private:
	unsigned int length;
	unsigned int readInd;
	unsigned int writeInd;
	unsigned int nBytes;
	unsigned char array;
};

#endif

