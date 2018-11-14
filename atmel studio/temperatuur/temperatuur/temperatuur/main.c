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
#include "distance.h"

uint8_t analog;
volatile uint16_t gv_counter = 0; // 16 bit counter value
volatile uint8_t gv_echo = 0; // a flag

double temp;
double voltage;
double tempC;

void init_ports(void)
{
	DDRB |=  0xFF;
	DDRD &=~ (1 << PIND3);
	DDRD |= (1 << PIND2);
	DDRC = 0x00;

}

void init_timer(void)
// prescaling : max time = 2^16/16E6 = 4.1 ms, 4.1 >> 2.3, so no prescaling required
// normal mode, no prescale, stop timer
{
	TCCR1A = 0;
	TCCR1B = 0;
	TIMSK1 |= _BV(TOIE1);
}

void start_timer(void)
{
	TCNT1 = 0;
	gv_counter = 0;
	TCCR1B |= _BV(CS10);
}

void init_ext_int(void)
{
	// any change triggers ext interrupt 1
	EICRA = (1 << ISC10);
	EIMSK = (1 << INT1);
}

void send_trigger(void)
{
	_delay_ms(50);		//Restart HC-SR04
	PORTD &=~ (1 << PIND2);
	_delay_us(1);
	PORTD |= (1 << PIND2); //Send 10us second pulse
	_delay_us(10);
	PORTD &=~ (1 << PIND2);
}


uint16_t calc_cm(uint16_t counter)
{
	uint16_t result = (counter * 65536 + TCNT1) / (58 * 16);
	return result;
}
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

uint8_t readlight()
{
	uint8_t value;
	value = PINC;
	return value;
}

ISR (INT1_vect)
{
	gv_echo = (~gv_echo) & 1;
	if (gv_echo){
		start_timer();
		} else {
		init_timer();
		
	}
}

ISR (TIMER1_OVF_vect)
{
	gv_counter++;
}
int main(void)
{
    uart_init();
	init_adc();
	init_ports();
	init_ext_int();
	init_timer();
	sei();
    while (1) 
    {
		send_trigger();
		_delay_ms(300);
		uint16_t distance = calc_cm(gv_counter);
		analog = get_adc_value();
		voltage = analog * 0.004882814 * 5000;
		tempC = (voltage - 500) * 0.1;
		transmit(tempC);
		_delay_ms(10);
		transmit(distance);
    }
}

