/*
 * GccApplication5.c
 *
 * Created: 7-11-2018 12:13:24
 * Author : veste
 */ 


#include <avr/io.h>
#include <util/delay.h>





float duration, distance;

void setup()
{
	DDRD = 0xFF;//output
	DDRB = 0x00;//input
	
}

void readdistance(){
	
		int timer = 0;
	
		PIND = 0x00;
		_delay_ms(2);
		PIND = 0xFF;
		_delay_ms(10);
		PIND = 0x00;
		
		
		while((PIND & PINB) != PINB){
			timer = 0;
		}
		
		while((PIND & PINB) == PINB){
			timer ++;
		}
		
		
		distance = timer / 180;
		
		return distance;
}


int main(void)
{
	readdistance();
}

