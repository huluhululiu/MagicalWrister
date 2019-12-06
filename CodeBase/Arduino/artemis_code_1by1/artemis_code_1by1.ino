
#define RFIX 22000
#define VDD 3.3
#define SAMPLES 50
#define NUMSENSOR 8
#define SAMPLE_DELAY 100 //ms
#define WINDOW_SIZE 10 //size of sliding window for sliding average
struct sensor{
  int pin;
  double sum;
  double reading [SAMPLES];
};

int sensorPtr;
sensor sensorArray [NUMSENSOR];
int samplePtr;
double window [NUMSENSOR][WINDOW_SIZE];
boolean flip = false;
void setup() {
  analogReadResolution(14);
  pinMode(8, INPUT);
  Serial.begin(115200);
  uint8_t analog_pins[] = {A0,A1,A2,A3,A5,A14,A15,A16};
  for (sensorPtr=0; sensorPtr<NUMSENSOR; sensorPtr++){
    sensor sTemp = {analog_pins[sensorPtr], 0, * new double [SAMPLES]};
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
      reading = analogRead(sensorArray[j].pin);
      sensorArray[j].sum = reading + sensorArray[j].sum;
    }
  }
     for (int i = 0; i < NUMSENSOR; i++){
        if(digitalRead(8) == flip){
          Serial.print(sensorArray[i].sum / SAMPLES);
          Serial.print(",");
        }
        sensorArray[i].sum = 0;
     }
     if(digitalRead(8) == flip){
        Serial.println("");
        flip = !flip;
     }
  delay(SAMPLE_DELAY);
}
