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

uint8_t data;
uint8_t value;


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

void transmit(uint8_t data)
{
	// wait for an empty transmit buffer
	// UDRE is set when the transmit buffer is empty
	loop_until_bit_is_set(UCSR0A, UDRE0);
	// send the data
	UDR0 = data;
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


int main(void)
{
	DDRC = 0x00;
    uart_init();
	init_adc();
    while (1) 
    {
		_delay_ms(300);
		data = get_adc_value();
		transmit(data);
			
    }
}

