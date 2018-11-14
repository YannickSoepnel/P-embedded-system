#include <avr/io.h>
#include <stdlib.h>
#include <avr/sfr_defs.h>
#define F_CPU 16E6
#include <util/delay.h>
// output on USB = PD1 = board pin 1
// datasheet p.190; F_OSC = 16 MHz & baud rate = 19.200
#define UBBRVAL 51
uint8_t counter = 0;
uint8_t ultrasoonData = 0;
uint8_t light = 0;
uint8_t temperature = 0;
uint8_t temp;


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
uint8_t receive()
{  
	loop_until_bit_is_set(UCSR0A, RXC0);  
	return UDR0;   // return the data 
}
	
void insertOutput(int count)
{
	ultrasoonData = count;
	light = count + 1;
	temperature = count + 2;	
}

void led(uint8_t onoff){
    int a;
	int b;
	onoff;
    
    while(onoff == 0x0e){
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
	transmit(temp);
	led(temp);
}

void sending()
{
	counter = counter + 1;
	int thisisavalue = counter;
	insertOutput(thisisavalue);
	transmit(ultrasoonData);
	transmit(light);
	transmit(temperature);
}
 
int main(void)
{
	uart_init();
	DDRB = 0xff;
	_delay_ms(1000);
	int onoff;
	while (1) {
		
		if(UDR0 != 0x00){
			recieving();
		}
		UDR0 = 0x00;
		sending();
	}
	return 0;
}
