/*
	AP_RcChannel.cpp - Radio library for Arduino
	Code by Jason Short, James Goppert. DIYDrones.com
	
	This library is free software; you can redistribute it and / or
		modify it under the terms of the GNU Lesser General Public
		License as published by the Free Software Foundation; either
		version 2.1 of the License, or (at your option) any later version.

*/

#include <math.h>
#include <avr/eeprom.h>
#include "AP_RcChannel.h"
#include <AP_Common.h>

AP_RcChannel::AP_RcChannel(AP_Var::Key key, const prog_char_t * name, APM_RC_Class & rc, const uint8_t & ch,
			const float & scale, const float & center, 
			const uint16_t & pwmMin, 
			const uint16_t & pwmNeutral, const uint16_t & pwmMax,
			const uint16_t & pwmDeadZone,
			const bool & filter, const bool & reverse) :
		AP_Var_group(key,name),
		_rc(rc),
		ch(this,0,ch,PSTR("CH")),
		scale(this,1,scale,PSTR("SCALE")),
		center(this,2,center,PSTR("CENTER")),
		pwmMin(this,3,pwmMin,PSTR("PMIN")),
		pwmMax(this,4,pwmMax,PSTR("PMAX")),
		pwmNeutral(this,5,pwmNeutral,PSTR("PNTRL")),
		pwmDeadZone(this,6,pwmDeadZone,PSTR("PDEAD")),
		filter(this,7,filter,PSTR("FLTR")),
		reverse(this,8,reverse,PSTR("REV")),
		_pwm(0)
	{
		setNormalized(0.0);
	}


uint16_t AP_RcChannel::readRadio() {
	return _rc.InputCh(ch);
}

void
AP_RcChannel::setPwm(uint16_t pwm)
{
	//Serial.printf("pwm in setPwm: %d\n", pwm);
	//Serial.printf("reverse: %s\n", (reverse)?"true":"false");
	
	// apply reverse
	if(reverse) pwm = int16_t(pwmNeutral-pwm) + pwmNeutral;

	//Serial.printf("pwm after reverse: %d\n", pwm);

	// apply filter
	if(filter){
		if(_pwm == 0)
			_pwm = pwm;
		else
			_pwm = ((pwm + _pwm) >> 1);		// Small filtering
	}else{
		_pwm = pwm;
	}

	//Serial.printf("pwm after filter: %d\n", _pwm);

	// apply deadzone
	_pwm = (abs(_pwm - pwmNeutral) < pwmDeadZone) ? uint16_t(pwmNeutral) : _pwm;

	//Serial.printf("pwm after deadzone: %d\n", _pwm);
	_rc.OutputCh(ch,_pwm);
}

void
AP_RcChannel::setPosition(float position)
{
	if (position > scale) position = scale;
	else if (position < -scale) position = -scale;
	setPwm(_positionToPwm(position));
}

void
AP_RcChannel::setNormalized(float normPosition)
{
	setPosition(normPosition*scale);
}

void
AP_RcChannel::mixRadio(uint16_t infStart)
{
	uint16_t pwmRadio = _rc.InputCh(ch);
	float inf = abs( int16_t(pwmRadio - pwmNeutral) );
	inf = min(inf, infStart);
	inf = ((infStart - inf) /infStart);
	setPwm(_pwm*inf + pwmRadio); 
}

uint16_t
AP_RcChannel::_positionToPwm(const float & position)
{
	uint16_t pwm;
	//Serial.printf("position: %f\n", position);
	float p = position - center;	
	if(p < 0)
		pwm = p * int16_t(pwmNeutral - pwmMin) / 
			scale + pwmNeutral;
	else
		pwm = p * int16_t(pwmMax - pwmNeutral) / 
			scale + pwmNeutral;
	constrain(pwm,uint16_t(pwmMin),uint16_t(pwmMax));
	return pwm;
}

float
AP_RcChannel::_pwmToPosition(const uint16_t & pwm)
{
	float position;
	if(pwm < pwmNeutral)
		position = scale * int16_t(pwm - pwmNeutral)/ 
			int16_t(pwmNeutral - pwmMin) + center;
	else
		position = scale * int16_t(pwm - pwmNeutral)/ 
			int16_t(pwmMax - pwmNeutral) + center;
	constrain(position,center-scale,center+scale);
	return position;
}

// ------------------------------------------
