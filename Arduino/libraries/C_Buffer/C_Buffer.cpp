#include "C_Buffer.h"

C_Buffer{
	unsigned int length =129;
	unsigned int readInd = 0;
	unsigned int writeInd = 0;
	unsigned int nBytes = 0;
	unsigned char array[129];
}

int C_Buffer::get_length()
{
	return length;
	
}

int C_Buffer::get_nBytes()
{
	return nBytes;
	
}

unsigned char C_Buffer::read()
{
	unsigned char readByte;
	if (nBytes <=0)
		readByte = 13;
	else {
		readByte = array[readInd];
		readInd = (readInd + 1) % length;
		if (readInd <= writeInd){
			nBytes = writeInd - readInd;
		}
		else {
			nBytes = writeInd + length - readInd;
		}
	}
	return readByte;
	
}

int C_Buffer::write(unsigned char w)
{
	int overFlowFlag;
	if (nBytes >= 50)
		overFlowFlag = 1;
	else {
		array[writeInd] = w;
		writeInd = (writeInd + 1) % length;
		if (readInd <= writeInd){
			nBytes = writeInd - readInd;
		}
		else {
			nBytes = writeInd + length - readInd;
		}
		overFlowFlag = 0;
	}
	return overFlowFlag;
}
	