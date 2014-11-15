#include <Servo.h> 

/*
  TODO:
  - verify stays closed with new method when turn servos off
    might have to leave on...
*/

// bitmasks:      CCCRRR
//                321321
#define R1_press B000001
#define R2_press B000010
#define R3_press B000100
#define C1_press B001000
#define C2_press B010000
#define C3_press B100000
////////////////////////
#define B1_press B001001
#define B2_press B010001
#define B3_press B100001
#define B4_press B001010
#define B5_press B010010
#define B6_press B100010

// debounce threshold
#define DBNC_THRESH 25

// define pin-button mapping
const int R1 = A0;
const int R2 = A1;
const int R3 = A2;
const int C1 = A3;
const int C2 = A4;
const int C3 = A5;     

// track keypad state for debouncing
byte dbnc_state = 0; // 'official' debounced state
byte prev_state = 0; // last observed state
// keep track of how long state has been steady
long bounce_time = 0;
// track previously-pressed button
int button = 0;
int prev_button = 0;

// servo stuff
const int num_servos = 6;
Servo servos[num_servos];
const int servo_pins[] = {6, 10, 11, 3, 9, 5}; // ordered!
// initial and 'blocking' positions for servos
//const int rest_pos[] = {180, 120, 120, 180, 130, 120};
//const int goal_pos[] = {0, 70, 80, 120, 80, 70};
// was 700,2400
const int rest_pos[] = {2400, 2400, 2400, 2400, 2400, 2400};
const int goal_pos[] = {700,  700,  700,  700,  700, 700};
// array of previously sent servo positions to avoid repeatedly sending
// data. Not sure this is necessary.
int prev_sent[] = {699,699,699,699,699,699};
// default time for servo to be active
const long dwell_time = 1000; // consider making this an array
// timers for figuring out how long to hold servos active
long timers[]   = {0, 0, 0, 0, 0, 0};
// time to let servo move before detaching
const long travel_time = 1000; // consider making this an array
// array for tracking when servos can be detached
long detach_after[] = {0, 0, 0, 0, 0, 0};
// 6:  90  130
// 10: 70  120
// 11: 80  120
// 3:  120 180
// 9:  80  130
// 5:  70  120



void setup() {
  Serial.begin(9600);
  // initialize the switch pins as inputs
  pinMode(R1, INPUT); 
  pinMode(R2, INPUT);  
  pinMode(R3, INPUT);  
  pinMode(C1, INPUT);  
  pinMode(C2, INPUT);  
  pinMode(C3, INPUT);

  // init servos
  for (int i = 0; i < num_servos; i++) {
    servos[i].attach(servo_pins[i]);
    servos[i].writeMicroseconds(rest_pos[i]);
    detach_after[i] = millis() + travel_time*3;
  }
}

void loop(){
  // update state
  debounce_presses(get_presses());
  button = get_button(dbnc_state);
  if (button != prev_button) {
    Serial.println(button);
    if (button != 0) add_time(button-1);
  }
  actuate_servos();
  prev_button = button;
  
  delay(30);
}

byte get_presses() {
  // get current state of buttons
  // format: C3C2C1R3R2R1 i.e. 100001 if R1 and C3 are pressed
  return (!digitalRead(R1) * R1_press) |
    (!digitalRead(R2) * R2_press) |
    (!digitalRead(R3) * R3_press) |
    (!digitalRead(C1) * C1_press) |
    (!digitalRead(C2) * C2_press) |
    (!digitalRead(C3) * C3_press);
}

byte debounce_presses(byte read_state) {
  // given current presses, updates debounced button state
  // state change - reset timer
  if (read_state != prev_state) {
    prev_state = read_state;
    bounce_time = millis();
  }

  // state stable - update dbnc_state
  if (millis() - bounce_time > DBNC_THRESH) {
    dbnc_state = read_state;
  }    
}

int get_button(byte debounced_state) {
  // given a debounced state byte, return number of button (1-6)
  // format: B6B5B4B3B2B1
  // could do multi-buttons, but not sure how to deal with ghosting.
  if (debounced_state == B1_press) return 1;
  if (debounced_state == B2_press) return 2;
  if (debounced_state == B3_press) return 3;
  if (debounced_state == B4_press) return 4; 
  if (debounced_state == B5_press) return 5; 
  if (debounced_state == B6_press) return 6;
  return 0;
}

void add_time(int servo) {
  // add time to specified servo
  if (timers[servo] < millis())
    // servo resting - need to reset time
    timers[servo] = millis();
  timers[servo] += dwell_time;
}

void actuate_servos() {
  // go through list of servos, actuating as necessary
  int pos;
  for (int servo = 0; servo < num_servos; servo++) {
    // find target position
    if (millis() > timers[servo]) {
      pos = rest_pos[servo];
    } else {
      pos = goal_pos[servo];
    }
    // see if we should detach
    if (millis() < detach_after[servo]) {
      servos[servo].attach(servo_pins[servo]);
    } else {
      servos[servo].detach(); 
    }
    // write position to servo if new
    //if (pos != prev_sent[servo]) {
    if (pos != prev_sent[servo]) {
      if (servos[servo].attached()) {
        servos[servo].writeMicroseconds(pos);
        prev_sent[servo] = pos;
      }
      // figure out new time to detach 
      detach_after[servo] = millis() + travel_time;
    }
  }
}
