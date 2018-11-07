/*
 * AfstandSensor Project.c
 *
 * Created: 5-11-2018 
 * Author : Alfred
 */ 

/* 
 * HC-SR04
 * trigger to sensor : uno 0 (PD0) output
 * echo from sensor  : uno 3 (PD3 = INT1) input
 * 
 * DIO : uno 8  (PB0) data
 * CLK : uno 9  (PB1) clock
 * STB : uno 10 (PB2) strobe
 *
 */

#include <avr/io.h>
#include <avr/interrupt.h>
#define F_CPU 16E6
#include <util/delay.h>
#include "distance.h"
#include <NewPing.h>

volatile uint16_t gv_counter; // 16 bit counter value
volatile uint8_t gv_echo; // a flag

//********** start display ***********

void reset_display()
{
    // clear memory - all 16 addresses
    sendCommand(0x40); // set auto increment mode
    write(strobe, LOW);
    shiftOut(0xc0);   // set starting address to 0
    for(uint8_t i = 0; i < 16; i++)
    {
        shiftOut(0x00);
    }
    write(strobe, HIGH);
    sendCommand(0x89);  // activate and set brightness to medium
}

void show_distance(uint16_t cm)
{
                        /*0*/ /*1*/ /*2*/ /*3*/ /*4*/ /*5*/ /*6*/ /*7*/ /*8*/ /*9*/
    uint8_t digits[] = {0x3f, 0x06, 0x5b, 0x4f, 0x66, 0x6d, 0x7d, 0x07, 0x7f, 0x6f};
    uint8_t ar[8] = {0};
    uint8_t digit = 0, i = 0;
    uint8_t temp, nrs, spaces;
    
    // cm=1234 -> ar[0..7] = {4,3,2,1,0,0,0,0}
    while (cm > 0 && i < 8) {
        digit = cm % 10;
        ar[i] = digit;
        cm = cm / 10;
        i++;
    }

    nrs = i;      // 4 digits
    spaces = 8-i; // 4 leading spaces  
    
    // invert array -> ar[0..7] = {0,0,0,0,1,2,3,4}
    uint8_t n = 7;
    for (i=0; i<4; i++) {
        temp = ar[i];
        ar[i] = ar[n];
        ar[n] = temp;
        n--;
    }
    
    write(strobe, LOW);
    shiftOut(0xc0); // set starting address = 0
    // leading spaces
    for (i=0; i<8; i++) {
        if (i < spaces) {
            shiftOut(0x00);
        } else {
            shiftOut(digits[ar[i]]);
        }           
        shiftOut(0x00); // the dot
    }
    
    write(strobe, HIGH);
}

void sendCommand(uint8_t value)
{
    write(strobe, LOW);
    shiftOut(value);
    write(strobe, HIGH);
}

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
    return 0;		//sensor sends echo lo->hi trigger EXT INT
					//senosr sends echo hi->lo trigger EXT INT
}

void init_timer(void)
// prescaling : max time = 2^16/16E6 = 4.1 ms, 4.1 >> 2.3, so no prescaling required
// normal mode, no prescale, stop timer
{
    TCCR1A = 0;
    TCCR1B = 0;
}

void init_ext_int(void)
{
    // any change triggers ext interrupt 1
    EICRA = (1 << ISC10);
    EIMSK = (1 << INT1);
}


uint16_t calc_cm(uint16_t counter)
{
    return 0;		//stop counting & get timer value
}

int main(void)
{
    int trigPin = 11;    // Trigger
    int echoPin = 12;    // Echo
    long duration, cm, inches;
    
    void setup() {
	    //Serial Port begin
	    Serial.begin (9600);
	    //Define inputs and outputs
	    pinMode(trigPin, OUTPUT);
	    pinMode(echoPin, INPUT);
    }
    
    void loop() {
	    // The sensor is triggered by a HIGH pulse of 10 or more microseconds.
	    // Give a short LOW pulse beforehand to ensure a clean HIGH pulse:
	    digitalWrite(trigPin, LOW);
	    delayMicroseconds(5);
	    digitalWrite(trigPin, HIGH);
	    delayMicroseconds(10);
	    digitalWrite(trigPin, LOW);
	    
	    // Read the signal from the sensor: a HIGH pulse whose
	    // duration is the time (in microseconds) from the sending
	    // of the ping to the reception of its echo off of an object.
	    pinMode(echoPin, INPUT);
	    duration = pulseIn(echoPin, HIGH);
	    
	    // Convert the time into a distance
	    cm = (duration/2) / 29.1;     // Divide by 29.1 or multiply by 0.0343
	    inches = (duration/2) / 74;   // Divide by 74 or multiply by 0.0135
	    
	    Serial.print(inches);
	    Serial.print("in, ");
	    Serial.print(cm);
	    Serial.print("cm");
	    Serial.println();
	    
	    delay(200);
    }		//Send trigger pulse to sensor
					//delay = 20ms
					//Bereken en toon de afstand
}

ISR (INT1_vect)
{
	set 
    return 0;      //set timer value = 0 & start counting 
	              //get timer value (hier de ADC valuables invullen)
}