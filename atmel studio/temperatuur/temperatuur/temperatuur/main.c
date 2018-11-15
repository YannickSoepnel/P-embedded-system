/*
 * lichtintensiteisensor.c
 *
 * Created: 7-11-2018 10:15:43
 * Author : jarco
 */ 

#include <avr/io.h>
#include <avr/interrupt.h>
#define F_CPU 16E6
#include <stdlib.h>
#include <avr/sfr_defs.h>
#include <util/delay.h>
#define UBBRVAL 51


uint8_t analog;

float temp;
float voltage;
float tempC;

void uart_init()
{
	// set the baud rate
	UBRR0H = 0;
	UBRR0L = UBBRVAL;     	// disable U2X mode
	UCSR0A = 0;		        // enable transmitter
	UCSR0B = _BV(TXEN0); 	// enable receiver
	UCSR0B = _BV(TXEN0) | _BV(RXEN0);
	// set frame format : asynchronous, 8 data bits, 1 stop bit, no parity
	UCSR0C = _BV(UCSZ01) | _BV(UCSZ00);
}

void init_adc()
{
	// ref=Vcc, left adjust the result (8 bit resolution),
	// select channel 0 (PC0 = input)
	ADMUX = (1<<REFS0)|(1<<ADLAR);
	// enable the ADC & prescale = 128
	ADCSRA = (1<<ADEN)|(1<<ADPS2)|(1<<ADPS1)|(1<<ADPS0);
}
uint8_t get_adc_value()
{
	ADCSRA |= (1<<ADSC); // start conversion
	loop_until_bit_is_clear(ADCSRA, ADSC);
	return ADCH; // 8-bit resolution, left adjusted
}

void transmit(uint8_t data)
{
	// wait for an empty transmit buffer
	// UDRE is set when the transmit buffer is empty
	loop_until_bit_is_set(UCSR0A, UDRE0);
	// send the data
	UDR0 = data;
}

uint8_t receive()
{
	loop_until_bit_is_set(UCSR0A, RXC0);
	return UDR0;   // return the data
}

void led(uint8_t onoff){

	
	if(onoff == 0x0e){
		PORTB = 0x02;
		_delay_ms(500);
		PORTB = 0x00;
		_delay_ms(500);
	}

	if(onoff == 0xff){                   //rode led gaat aan (hij is ingerold dus)
		PORTB = 0x01;
	}
	else if(onoff == 0x0f){               //Groene led gaat aan (hij is uitgerold dus)
		PORTB = 0x04;
	}
}

void recieving()
{
	temp = receive();
	led(temp);
}

int main(void)
{
    uart_init();
	init_adc();
	DDRB = 0xff;
    while (1) 
    {
		_delay_ms(500);
		analog = get_adc_value();
		voltage = analog * 0.004882814;
		tempC = (voltage - 0.5) * 100.0;
		tempC = tempC * 10;
		int sendtemp = tempC;
		transmit(0xff);
		transmit(sendtemp);
		if(UDR0 != 0x00){
			recieving();
		}
		
    }
}

