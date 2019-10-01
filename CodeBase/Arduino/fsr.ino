
int fsrPin = 0; // FSR is connected to analog 0
int LEDlow = 11;
int LEDmid = 12;
int LEDhigh = 10;// connect Red LED to pin 11 (PWM pin)
int fsrReading;   
int lowBri=0;
 int midBri=0;
 int highBri=0;
void setup(void) {
  Serial.begin(9600);   // We'll send debugging information via the Serial monitor
  pinMode(LEDlow, OUTPUT);
  pinMode(LEDmid, OUTPUT);
  pinMode(LEDhigh, OUTPUT);
}
 
void loop(void) {
  fsrReading = analogRead(fsrPin);  
  
   // the raw analog reading
   Serial.println("***",fsrReading);
  // We'll have a few threshholds, qualitatively determined
  if (fsrReading < 10) {
    lowBri=0;
    midBri=0;
    highBri=0;
    Serial.println(" - No pressure");
  } else if (fsrReading < 200) {
    lowBri=map(fsrReading,0,1023,0,255);
    midBri=0;
    highBri=0;
  } else if (fsrReading < 500) {
    lowBri=255;
    fsrReading=fsrReading-200;
    midBri=map(fsrReading,0,1023,0,255);
    highBri=0;
    Serial.println(" - Light squeeze");
  } else if (fsrReading < 800) {
    lowBri=255;
    midBri=255;
    fsrReading=fsrReading-500;
    highBri=map(fsrReading,0,1023,0,255);
    Serial.println(" - Medium squeeze");
  } else {
    lowBri=255;
    midBri=255;
    highBri=255;
    Serial.println(" - Big squeeze");
  }
  analogWrite(LEDlow,lowBri);
  analogWrite(LEDmid,midBri);
  analogWrite(LEDhigh,highBri);

} 
