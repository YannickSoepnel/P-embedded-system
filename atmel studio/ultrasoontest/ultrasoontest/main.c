/* 
 * HC-SR04
 * trigger to sensor : uno 0 (PD0) output
 * echo from sensor  : uno 3 (PD3 = INT1) input
 * 
 */

#include <avr/io.h>
#include <avr/interrupt.h>
#define F_CPU 16E6
#include <stdlib.h>
#include <avr/sfr_defs.h>
#include <util/delay.h>
#include "distance.h"

volatile uint16_t gv_counter = 0; // 16 bit counter value
volatile uint8_t gv_echo = 0; // a flag
#define UBBRVAL 51

// write value to pin
void write(uint8_t pin, uint8_t val)
{
    if (val == LOW) {
        PORTB &= ~(_BV(pin)); // clear bit
    } else {
        PORTB |= _BV(pin); // set bit
    }
}

// shift out value to data
void shiftOut (uint8_t val)
{
    uint8_t i;
    for (i = 0; i < 8; i++)  {
        write(clock, LOW);   // bit valid on rising edge
        write(data, val & 1 ? HIGH : LOW); // lsb first
        val = val >> 1;
        write(clock, HIGH);
    }
}

//********** end display ***********

void init_ports(void)
{
	DDRB |=  0xFF;
	DDRD &=~ (1 << PIND3);
	DDRD |= (1 << PIND2);
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

void transmit(uint8_t data)
{
	// wait for an empty transmit buffer
	// UDRE is set when the transmit buffer is empty
	loop_until_bit_is_set(UCSR0A, UDRE0);
	// send the data
	UDR0 = data;
}


int main(void)
{
	init_ext_int();
	init_timer();
	init_ports();
	uart_init();
	sei();
	
	while(1){
		send_trigger();
		_delay_ms(50);
		uint16_t distance = calc_cm(gv_counter);
		transmit(distance);		
		
	}
    return 0;
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