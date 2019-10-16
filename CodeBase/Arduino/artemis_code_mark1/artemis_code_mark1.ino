
#define RFIX 22000
#define VDD 3.3
#define SAMPLES 100
#define NUMSENSOR 8
#define SAMPLE_DELAY 10 //ms

struct sensor{
  int pin;
  double reading [SAMPLES];
};

int sensorPtr;
sensor sensorArray [NUMSENSOR];
int samplePtr;


void setup() {
  analogReadResolution(14);
  Serial.begin(115200);
  uint8_t analog_pins[] = {A0,A1,A2,A3,A5,A14,A15,A16};
  for (sensorPtr=0; sensorPtr<NUMSENSOR; sensorPtr++){
    sensor sTemp = {analog_pins[sensorPtr], * new double [SAMPLES]};
    sensorArray[sensorPtr] = sTemp;
  }
  sensorPtr = 0;
  samplePtr = 0;
  

}

void loop() {
  double sVolt;
  double reading;
  for (int i=0; i<SAMPLES; i++){
    for(int j=0; j<NUMSENSOR; j++){
      sVolt = VDD * (analogRead(sensorArray[j].pin)/16384.0);
      reading = ((VDD-sVolt)*RFIX)/(sVolt);
      sensorArray[j].reading[i] = reading;
      
      Serial.print(reading);
      Serial.print(',');
    }
    //Serial.print(';');
    Serial.print('\n');
    delay(SAMPLE_DELAY);
  }
  delay(SAMPLE_DELAY);
  
}
