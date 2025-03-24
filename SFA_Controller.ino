#include <SerialPort.h>

/* global variables*/

// normal mode variables
double output_frequency;
double output_amplitude;
double prev_output_frequency;
double prev_output_amplitude;
double input_phase;
double input_amplitude;
double setpoint_amplitude;
double exponential_term;
double linear_term;
double linear_term_amplitude;
int frequency_controller_flag;
int amplitude_controller_flag;

// shear mode variables
double output_frequency_shear;
double output_amplitude_shear;
double prev_output_frequency_shear;
double prev_output_amplitude_shear;
double input_phase_shear;
double input_amplitude_shear;
double setpoint_amplitude_shear;
double exponential_term_shear;
double linear_term_shear;
double linear_term_amplitude_shear;
int frequency_controller_flag_shear;
int amplitude_controller_flag_shear;

// general variables
int serial_bytes_inputBuffer;
String user_input;
String lock_in_responce;
String command;
long Stream_start;
int data_stream_flag;
double temp_counter;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(19200);  // The computer serial port
  Serial.setTimeout(50);
  Serial1.begin(9600); // lock-in amplifier 1 serial port (normal mode)
  Serial1.setTimeout(50);
  delay(50);
  Serial1.print("OUTX0\n");
  Serial1.print("LOCL1\n");
  Serial2.begin(9600); // lock-in amplifier 2 serial port (shear mode)
  Serial2.setTimeout(50);
  delay(50);
  Serial2.print("OUTX0\n");
  Serial2.print("LOCL1\n");

  output_frequency = 840;
  output_amplitude = 1.0;
  prev_output_frequency = 0;
  prev_output_amplitude = 0;
  input_phase = 0;
  input_amplitude = 0;
  serial_bytes_inputBuffer = 0;
  user_input = "";
  lock_in_responce = "";
  command = "";
  setpoint_amplitude = 1.0;
  frequency_controller_flag = 0;
  amplitude_controller_flag = 0;
  data_stream_flag = 0;
  exponential_term = 0.00003;
  linear_term = 0.001;
  linear_term_amplitude = 20;
  Stream_start = 0;
  output_frequency_shear = 375;
  output_amplitude_shear = 1.0;
  prev_output_frequency_shear = 0;
  prev_output_amplitude_shear = 0;
  input_phase_shear = 0;
  input_amplitude_shear = 0;
  setpoint_amplitude_shear = 100.0;
  exponential_term_shear = 0.00015;
  linear_term_shear = 0.003;
  linear_term_amplitude_shear = 0.2;
  frequency_controller_flag_shear = 0;
  amplitude_controller_flag_shear = 0;
  temp_counter = 0.0;
}

void loop() {
  // put your main code here, to run repeatedly:

  /* check user input*/
  serial_bytes_inputBuffer = Serial.available();
  user_input = "";
  while (serial_bytes_inputBuffer != 0) {
    user_input = Serial.readStringUntil(';');
    //Serial.print("user command: ");  // for debugging
    //Serial.println(user_input);


    if (user_input.compareTo("Help") == 0 || user_input.compareTo("help") == 0) { //-----------------------------------------Help command------------------------------------------------
      Serial.println("The available commands are:");
      Serial.println("Sf (x);   | This command sets the normal frequency to x (note that if the frequency controller is engaged this value will be overwritten)");
      Serial.println("sSf (x);  | This command sets the shear frequency to x (note that if the frequency controller is engaged this value will be overwritten)");
      Serial.println("Rf;       | This command returns the current normal frequency");
      Serial.println("sRf;      | This command returns the current shear frequency");
      Serial.println("Sa (x);   | This command sets the normal sine out amplitude to x (note that if the amplitude controller is engaged this value will be overwritten)");
      Serial.println("sSa (x);  | This command sets the shear sine out amplitude to x (note that if the amplitude controller is engaged this value will be overwritten)");
      Serial.println("Ra;       | This command returns the current normal sine out amplitude");
      Serial.println("sRa;      | This command returns the current shear sine out amplitude");
      Serial.println("Ssa (x);  | This command sets the amplitude setpoint for the normal amplitude controller to x");
      Serial.println("sSsa (x); | This command sets the amplitude setpoint for the shear amplitude controller to x");
      Serial.println("Rsa;      | This command returns the current normal amplitude setpoint for the amplitude controller");
      Serial.println("sRsa;     | This command returns the current shear amplitude setpoint for the amplitude controller");
      Serial.println("Ef (X);   | This command enables or disables the normal frequency controller (x = 1 enables the controller and x = 2 disables the controller)");
      Serial.println("sEf (X);  | This command enables or disables the shear frequency controller (x = 1 enables the controller and x = 2 disables the controller)");
      Serial.println("Ea (X);   | This command enables or disables the normal amplitude controller (x = 1 enables the controller and x = 2 disables the controller)");
      Serial.println("sEa (X);  | This command enables or disables the shear amplitude controller (x = 1 enables the controller and x = 2 disables the controller)");
      Serial.println("Ed (X);   | This command enables or disables the data stream (x = 1 enables the stream and x = 2 disables the stream)");
      Serial.println("SCe (X);  | This command sets the exponential term for the normal frequency controller");
      Serial.println("sSCe (X); | This command sets the exponential term for the shear frequency controller");
      Serial.println("SCl (X);  | This command sets the linear term for the normal frequency controller");
      Serial.println("sSCl (X); | This command sets the linear term for the shear frequency controller");
      Serial.println("SCp (X);  | This command sets both exponential and linear terms for the normal frequency controller (1 = open air, 2 = 20 cSt, 3 = 500 cSt, 4 = 10 000 cSt, 5 = 30 000 cSt)");
      Serial.println("sSCp (X); | This command sets both exponential and linear terms for the shear frequency controller (1 = open air, 2 = 20 cSt, 3 = 500 cSt, 4 = 10 000 cSt, 5 = 30 000 cSt)");
      Serial.println("SCAl (X); | This command sets the linear term for the normal amplitude controller");
      Serial.println("sSCAl (X);| This command sets the linear term for the shear amplitude controller");
      Serial.println("SCAp (X); | This command sets the linear term for the normal amplitude controller (preset 1 is most conservative and preset 5 is most agressive)");
      Serial.println("sSCAp (X);| This command sets the linear term for the shear amplitude controller (preset 1 is most conservative and preset 5 is most agressive)");
    }
    else if (user_input.substring(0, 2).compareTo("Sf") == 0) { //------------------------------------------------------------Sf command--------------------------------------------------
      if (user_input.length() > 3 && user_input.substring(3).toDouble() != 0.0) {
        output_frequency = user_input.substring(3).toDouble();
        //Serial.println(output_frequency);
      }
      else {
        Serial.println("x not recognised");
      }
    }
    else if (user_input.substring(0, 3).compareTo("sSf") == 0) { //------------------------------------------------------------sSf command--------------------------------------------------
      if (user_input.length() > 4 && user_input.substring(4).toDouble() != 0.0) {
        output_frequency_shear = user_input.substring(4).toDouble();
        //Serial.println(output_frequency);
      }
      else {
        Serial.println("x not recognised");
      }
    }
    else if (user_input.substring(0, 2).compareTo("Rf") == 0) { //------------------------------------------------------------Rf command--------------------------------------------------
      Serial.print("normal frequency = ");
      Serial.println(output_frequency,4);
    }
    else if (user_input.substring(0, 3).compareTo("sRf") == 0) { //------------------------------------------------------------sRf command--------------------------------------------------
      Serial.print("shear frequency = ");
      Serial.println(output_frequency_shear,4);
    }
    else if (user_input.substring(0, 2).compareTo("Sa") == 0) { //------------------------------------------------------------Sa command--------------------------------------------------
      if (user_input.length() > 3 && user_input.substring(3).toDouble() != 0.0) {
        output_amplitude = user_input.substring(3).toDouble();
        //Serial.println(output_amplitude);
      }
      else {
        Serial.println("x not recognised");
      }
    }
    else if (user_input.substring(0, 3).compareTo("sSa") == 0) { //------------------------------------------------------------sSa command--------------------------------------------------
      if (user_input.length() > 4 && user_input.substring(4).toDouble() != 0.0) {
        output_amplitude_shear = user_input.substring(4).toDouble();
        //Serial.println(output_amplitude);
      }
      else {
        Serial.println("x not recognised");
      }
    }
    else if (user_input.substring(0, 2).compareTo("Ra") == 0) { //------------------------------------------------------------Ra command--------------------------------------------------
      Serial.print("normal amplitude = ");
      Serial.println(output_amplitude,4);
    }
    else if (user_input.substring(0, 3).compareTo("sRa") == 0) { //------------------------------------------------------------sRa command--------------------------------------------------
      Serial.print("shear amplitude = ");
      Serial.println(output_amplitude_shear,4);
    }
    else if (user_input.substring(0, 3).compareTo("Ssa") == 0) { //------------------------------------------------------------Ssa command-------------------------------------------------
      if (user_input.length() > 4 && user_input.substring(4).toDouble() != 0.0) {
        setpoint_amplitude = user_input.substring(4).toDouble();
        //Serial.println(output_amplitude);
      }
      else {
        Serial.println("x not recognised");
      }
    }
    else if (user_input.substring(0, 4).compareTo("sSsa") == 0) { //------------------------------------------------------------sSsa command-------------------------------------------------
      if (user_input.length() > 5 && user_input.substring(5).toDouble() != 0.0) {
        setpoint_amplitude_shear = user_input.substring(5).toDouble();
        //Serial.println(output_amplitude);
      }
      else {
        Serial.println("x not recognised");
      }
    }
    else if (user_input.substring(0, 3).compareTo("Rsa") == 0) { //------------------------------------------------------------Rsa command-------------------------------------------------
      Serial.print("normal amplitude setpoint = ");
      Serial.println(setpoint_amplitude,4);
    }
    else if (user_input.substring(0, 4).compareTo("sRsa") == 0) { //------------------------------------------------------------sRsa command-------------------------------------------------
      Serial.print("shear amplitude setpoint = ");
      Serial.println(setpoint_amplitude_shear,4);
    }
    else if (user_input.substring(0, 2).compareTo("Ef") == 0) { //------------------------------------------------------------Ef command--------------------------------------------------
      if (user_input.length() > 3 && user_input.substring(3).toInt() != 0) {
        if(user_input.substring(3).toInt() == 1){
          //Serial.println("normal frequency controller enabled");
          frequency_controller_flag = 1;
          }
        else if(user_input.substring(3).toInt() == 2){
          //Serial.println("normal frequency controller disabled");
          frequency_controller_flag = 0;
          }
        else {
          Serial.println("x not recognised");
          }
      }
      else {
        Serial.println("x not recognised");
      }
    }
    else if (user_input.substring(0, 3).compareTo("sEf") == 0) { //------------------------------------------------------------sEf command--------------------------------------------------
      if (user_input.length() > 4 && user_input.substring(4).toInt() != 0) {
        if(user_input.substring(4).toInt() == 1){
          //Serial.println("shear frequency controller enabled");
          frequency_controller_flag_shear = 1;
          }
        else if(user_input.substring(4).toInt() == 2){
          //Serial.println("shear frequency controller disabled");
          frequency_controller_flag_shear = 0;
          }
        else {
          Serial.println("x not recognised");
          }
      }
      else {
        Serial.println("x not recognised");
      }
    }
    else if (user_input.substring(0, 2).compareTo("Ea") == 0) { //------------------------------------------------------------Ea command--------------------------------------------------
      if (user_input.length() > 3 && user_input.substring(3).toInt() != 0) {
        if(user_input.substring(3).toInt() == 1){
          //Serial.println("normal amplitude controller enabled");
          amplitude_controller_flag = 1;
          }
        else if(user_input.substring(3).toInt() == 2){
          //Serial.println("normal amplitude controller disabled");
          amplitude_controller_flag = 0;
          }
        else {
          Serial.println("x not recognised");
          }
      }
      else {
        Serial.println("x not recognised");
      }
    }
    else if (user_input.substring(0, 3).compareTo("sEa") == 0) { //------------------------------------------------------------sEa command--------------------------------------------------
      if (user_input.length() > 4 && user_input.substring(4).toInt() != 0) {
        if(user_input.substring(4).toInt() == 1){
          //Serial.println("shear amplitude controller enabled");
          amplitude_controller_flag_shear = 1;
          }
        else if(user_input.substring(4).toInt() == 2){
          //Serial.println("shear amplitude controller disabled");
          amplitude_controller_flag_shear = 0;
          }
        else {
          Serial.println("x not recognised");
          }
      }
      else {
        Serial.println("x not recognised");
      }
    }
    else if (user_input.substring(0, 2).compareTo("Ed") == 0) { //------------------------------------------------------------Ed command--------------------------------------------------
      if (user_input.length() > 3 && user_input.substring(3).toInt() != 0) {
        if(user_input.substring(3).toInt() == 1){
          //Serial.println("data stream enabled");
          data_stream_flag = 1;
          Stream_start = millis();
          }
        else if(user_input.substring(3).toInt() == 2){
          //Serial.println("data stream disabled");
          data_stream_flag = 0;
          //Serial.print(millis()- Stream_start);
          //Serial.print("\nt");
          }
        else {
          Serial.println("x not recognised");
          }
      }
      else {
        Serial.println("x not recognised");
      }
    }
    else if (user_input.substring(0, 3).compareTo("SCe") == 0) { //------------------------------------------------------------SCe command--------------------------------------------------
      if (user_input.length() > 4 ) {
        exponential_term = user_input.substring(4).toDouble();
        //Serial.println("normal frequency controller exponential term updated");
      }
      else {
        Serial.println("x not recognised");
      }
    }
    else if (user_input.substring(0, 4).compareTo("sSCe") == 0) { //------------------------------------------------------------sSCe command--------------------------------------------------
      if (user_input.length() > 5 ) {
        exponential_term_shear = user_input.substring(5).toDouble();
        //Serial.println("shear frequency controller exponential term updated");
      }
      else {
        Serial.println("x not recognised");
      }
    }
    else if (user_input.substring(0, 3).compareTo("SCl") == 0) { //------------------------------------------------------------SCl command--------------------------------------------------
      if (user_input.length() > 4) {
        linear_term = user_input.substring(4).toDouble();
        //Serial.println("normal frequency controller linear term updated");
      }
      else {
        Serial.println("x not recognised");
      }
    }
    else if (user_input.substring(0, 4).compareTo("sSCl") == 0) { //------------------------------------------------------------sSCl command--------------------------------------------------
      if (user_input.length() > 5) {
        linear_term_shear = user_input.substring(5).toDouble();
        //Serial.println("shear frequency controller linear term updated");
      }
      else {
        Serial.println("x not recognised");
      }
    }
    else if (user_input.substring(0, 3).compareTo("SCp") == 0) { //------------------------------------------------------------SCp command--------------------------------------------------
      if (user_input.length() > 4 && user_input.substring(4).toInt() != 0) {
        if(user_input.substring(4).toInt() == 1){
          Serial.println("open air preset used");
          exponential_term = 0.000005;
          linear_term = 0.0002;
          }
        else if(user_input.substring(4).toInt() == 2){
          Serial.println("20 cSt preset used");
          exponential_term = 0.000006;
          linear_term = 0.0002;
          }
        else if(user_input.substring(4).toInt() == 3){
          Serial.println("500 cSt preset used");
          exponential_term = 0.000006;
          linear_term = 0.0002;
          } 
        else if(user_input.substring(4).toInt() == 4){
          Serial.println("10 000 cSt preset used");
          exponential_term = 0.000007;
          linear_term = 0.0009;
          }  
        else if(user_input.substring(4).toInt() == 5){
          Serial.println("30 000 cSt preset used");
          exponential_term = 0.00002;
          linear_term = 0.002;
          }
        else {
          Serial.println("x not recognised");
          }
      }
      else {
        Serial.println("x not recognised");
      }
    }
    else if (user_input.substring(0, 4).compareTo("sSCp") == 0) { //------------------------------------------------------------sSCp command--------------------------------------------------
      if (user_input.length() > 5 && user_input.substring(5).toInt() != 0) {
        if(user_input.substring(5).toInt() == 1){
          Serial.println("open air preset used");
          exponential_term_shear = 0.000005;
          linear_term_shear = 0.0002;
          }
        else if(user_input.substring(5).toInt() == 2){
          Serial.println("20 cSt preset used");
          exponential_term_shear = 0.000006;
          linear_term_shear = 0.0002;
          }
        else if(user_input.substring(5).toInt() == 3){
          Serial.println("500 cSt preset used");
          exponential_term_shear = 0.000006;
          linear_term_shear = 0.0002;
          } 
        else if(user_input.substring(5).toInt() == 4){
          Serial.println("10 000 cSt preset used");
          exponential_term_shear = 0.000007;
          linear_term_shear = 0.0009;
          }  
        else if(user_input.substring(5).toInt() == 5){
          Serial.println("30 000 cSt preset used");
          exponential_term_shear = 0.00002;
          linear_term_shear = 0.002;
          }
        else {
          Serial.println("x not recognised");
          }
      }
      else {
        Serial.println("x not recognised");
      }
    }
    
    else if (user_input.substring(0, 4).compareTo("SCAl") == 0) { //------------------------------------------------------------SCAl command--------------------------------------------------
      if (user_input.length() > 5) {
        linear_term_amplitude = user_input.substring(5).toDouble();
        //Serial.println("normal amplitude controller linear term updated");
      }
      else {
        Serial.println("x not recognised");
      }
    }
    else if (user_input.substring(0, 5).compareTo("sSCAl") == 0) { //------------------------------------------------------------sSCAl command--------------------------------------------------
      if (user_input.length() > 6) {
        linear_term_amplitude_shear = user_input.substring(6).toDouble();
        //Serial.println("shear amplitude controller linear term updated");
      }
      else {
        Serial.println("x not recognised");
      }
    }
    else if (user_input.substring(0, 4).compareTo("SCAp") == 0) { //------------------------------------------------------------SCAp command--------------------------------------------------
      if (user_input.length() > 5 && user_input.substring(5).toInt() != 0) {
        if(user_input.substring(5).toInt() == 1){
          Serial.println("preset 1 used");
          linear_term_amplitude = 50;
          }
        else if(user_input.substring(5).toInt() == 2){
          Serial.println("preset 2 used");
          linear_term_amplitude = 100;
          }
        else if(user_input.substring(5).toInt() == 3){
          Serial.println("preset 3 used");
          linear_term_amplitude = 200;
          } 
        else if(user_input.substring(5).toInt() == 4){
          Serial.println("preset 4 used");
          linear_term_amplitude = 500;
          }  
        else if(user_input.substring(5).toInt() == 5){
          Serial.println("preset 5 used");
          linear_term_amplitude = 1000;
          }
        else {
          Serial.println("x not recognised");
          }
      }
      else {
        Serial.println("x not recognised");
      }
    }
    else if (user_input.substring(0, 5).compareTo("sSCAp") == 0) { //------------------------------------------------------------sSCAp command--------------------------------------------------
      if (user_input.length() > 6 && user_input.substring(6).toInt() != 0) {
        if(user_input.substring(6).toInt() == 1){
          Serial.println("preset 1 used");
          linear_term_amplitude_shear = 50;
          }
        else if(user_input.substring(6).toInt() == 2){
          Serial.println("preset 2 used");
          linear_term_amplitude_shear = 100;
          }
        else if(user_input.substring(6).toInt() == 3){
          Serial.println("preset 3 used");
          linear_term_amplitude_shear = 200;
          } 
        else if(user_input.substring(6).toInt() == 4){
          Serial.println("preset 4 used");
          linear_term_amplitude_shear = 500;
          }  
        else if(user_input.substring(6).toInt() == 5){
          Serial.println("preset 5 used");
          linear_term_amplitude_shear = 1000;
          }
        else {
          Serial.println("x not recognised");
          }
      }
      else {
        Serial.println("x not recognised");
      }
    }
    
    else { //-----------------------------------------------------------------------------------------------------------------Command not recognised--------------------------------------
      Serial.println("Command not recognised");
    }

    serial_bytes_inputBuffer = Serial.available();
  } // end of while loop


  /*request update from lock-in */
  // update input_frequency/amplitude normal mode
  
  Serial1.print("outp ? 3\n");
  //Serial1.print("*IDN?\n");
  delay(1);
  if(Serial1.available() != 0){
    lock_in_responce = Serial1.readStringUntil('\r');
    if(lock_in_responce.toDouble() != 0.0){
      input_amplitude = lock_in_responce.toDouble();
      //printDouble_S0(input_amplitude,1000000);
    } 
    else{
      input_amplitude = lock_in_responce.toDouble();
      //Serial.println("Failed to get amplitude from lock-in");
      } 
    }
    
  Serial1.print("outp ? 4\n");
  delay(1);
  if(Serial1.available() != 0.0){
    lock_in_responce = Serial1.readStringUntil('\r');
    if(lock_in_responce.toDouble() != 0.0){
      input_phase = lock_in_responce.toDouble();
      //Serial.print("p");
      //printDouble_S0(input_phase,1000000);
    } 
    else{
      input_phase = lock_in_responce.toDouble();
      //Serial.print("p");
      //printDouble_S0(input_phase,1000000);
      //Serial.println("Failed to get phase from lock-in");
      } 
    } 

// update input_frequency/amplitude shear mode
  
  Serial2.print("outp ? 3\n");
  //Serial1.print("*IDN?\n");
  delay(1);
  if(Serial2.available() != 0){
    lock_in_responce = Serial2.readStringUntil('\r');
    if(lock_in_responce.toDouble() != 0.0){
      input_amplitude_shear = lock_in_responce.toDouble();
      //printDouble_S0(input_amplitude,1000000);
    } 
    else{
      input_amplitude_shear = lock_in_responce.toDouble();
      //Serial.println("Failed to get amplitude from lock-in");
      } 
    }
    
  Serial2.print("outp ? 4\n");
  delay(1);
  if(Serial2.available() != 0.0){
    lock_in_responce = Serial2.readStringUntil('\r');
    if(lock_in_responce.toDouble() != 0.0){
      input_phase_shear = lock_in_responce.toDouble();
      //Serial.print("p");
      //printDouble_S0(input_phase,1000000);
    } 
    else{
      input_phase_shear = lock_in_responce.toDouble();
      //Serial.print("p");
      //printDouble_S0(input_phase,1000000);
      //Serial.println("Failed to get phase from lock-in");
      } 
    } 
  /* run frequency and or amplitude controller based on the control variables/flags*/
  // if normal frequency controller flag = 1 run frequency controller. else dont run.
  if(frequency_controller_flag == 1){
    double correction = 0.0;
    if(input_phase >= 0.0){
      correction = (((input_phase*input_phase) * exponential_term)+ input_phase*linear_term);
      if(correction > 0.5){
       correction = 0.5;
      }
    }
    else{
      correction = (((input_phase*input_phase) * -exponential_term)+ input_phase*linear_term);
      if(correction < -0.5){
       correction = -0.5;
      }
      }
    //Serial.print("c");
    //printDouble_S0(correction,1000000);
    output_frequency = output_frequency + correction;  
  }
  // if normal amplitude controller flag = 1 run amplitude controller. else dont run.
  if(amplitude_controller_flag == 1){
    double setpoint_voltage = (19.7392088022 * pow(output_frequency,2) * setpoint_amplitude/1000000000) / 9.80665;
    setpoint_voltage = setpoint_voltage/4.545454545454546;
    setpoint_voltage = setpoint_voltage/2.83286119;
    double error = setpoint_voltage - input_amplitude;
    output_amplitude = output_amplitude + linear_term_amplitude * error;
    //printDouble_S0(output_amplitude,1000000);
    
    }

  // if shear frequency controller flag = 1 run frequency controller. else dont run.
  if(frequency_controller_flag_shear == 1){
    double correction = 0.0;
    if(input_phase_shear >= 0.0){
      correction = (((input_phase_shear*input_phase_shear) * exponential_term_shear)+ input_phase_shear*linear_term_shear);
      if(correction > 0.5){
       correction = 0.5;
      }
    }
    else{
      correction = (((input_phase_shear*input_phase_shear) * -exponential_term_shear)+ input_phase_shear*linear_term_shear);
      if(correction < -0.5){
       correction = -0.5;
      }
      }
    //Serial.print("c");
    //printDouble_S0(correction,1000000);
    output_frequency_shear = output_frequency_shear + correction;  
  }
  // if shear amplitude controller flag = 1 run amplitude controller. else dont run.
  if(amplitude_controller_flag_shear == 1){
    double setpoint_voltage_shear = (19.7392088022 * pow(output_frequency_shear,2) * setpoint_amplitude_shear/1000000000) / 9.80665;
    setpoint_voltage_shear = setpoint_voltage_shear/4.545454545454546;
    setpoint_voltage_shear = setpoint_voltage_shear/2.83286119;
    double error = setpoint_voltage_shear - input_amplitude_shear;
    output_amplitude_shear = output_amplitude_shear + linear_term_amplitude_shear * error;
    //printDouble_S0(output_amplitude,1000000);
    
    }

  if(data_stream_flag == 1){
    
    printDouble_S0(output_frequency,100000);
    Serial.print(',');
    printDouble_S0(output_amplitude,100000);
    Serial.print(',');
    printDouble_S0(input_phase,100000);
    Serial.print(',');
    printDouble_S0(input_amplitude,100000000);
    Serial.print(',');
    printDouble_S0(output_frequency_shear,100000);
    Serial.print(',');
    printDouble_S0(output_amplitude_shear,100000);
    Serial.print(',');
    printDouble_S0(input_phase_shear,100000);
    Serial.print(',');
    printDouble_S0(input_amplitude_shear,100000000);
    
    /*printDouble_S0(temp_counter,100000);
    Serial.print(',');
    printDouble_S0(temp_counter+1,100000000);
    Serial.print(',');
    printDouble_S0(temp_counter+2,100000);
    Serial.print(',');
    printDouble_S0(temp_counter+3,100000);
    Serial.print(',');
    printDouble_S0(temp_counter+4,100000);
    Serial.print(',');
    printDouble_S0(temp_counter+5,100000000);
    Serial.print(',');
    printDouble_S0(temp_counter+6,100000);
    Serial.print(',');
    printDouble_S0(temp_counter+7,100000);*/
    Serial.print("\nt");
    
    }

  /* Update the frequency and amplitude by sending a message to the DDS and amplifier*/
  // if normal frequency or amplitude did not change then don't send a message.
  if(abs(prev_output_frequency - output_frequency) > 0.0001){
    String command = "FREQ ";
    //Serial.print("Debug: ");
    //Serial.print(command);
    Serial1.print(command);
    printDouble_S1(output_frequency,10000);
    //Serial.print("f");
    //printDouble_S0(output_frequency,10000);
    prev_output_frequency = output_frequency;
    
    }
  if(abs(prev_output_amplitude - output_amplitude) > 0.0001){
    if(output_amplitude > 5.0){
      output_amplitude = 5.0;
      }
    if(output_amplitude < 0.004){
      output_amplitude = 0.004;
      }
    String command = "SLVL ";
    //Serial.print("Debug: ");
    //Serial.print(command);
    Serial1.print(command);
    printDouble_S1(output_amplitude,1000000);
    prev_output_amplitude = output_amplitude;
    
    }
  // if shear frequency or amplitude did not change then don't send a message.
  if(abs(prev_output_frequency_shear - output_frequency_shear) > 0.0001){
    String command = "FREQ ";
    //Serial.print("Debug: ");
    //Serial.print(command);
    Serial2.print(command);
    printDouble_S2(output_frequency_shear,10000);
    //Serial.print("f");
    //printDouble_S0(output_frequency,10000);
    prev_output_frequency_shear = output_frequency_shear;
    
    }
  if(abs(prev_output_amplitude_shear - output_amplitude_shear) > 0.0001){
    if(output_amplitude_shear > 5.0){
      output_amplitude_shear = 5.0;
      }
    if(output_amplitude_shear < 0.004){
      output_amplitude_shear = 0.004;
      }
    String command = "SLVL ";
    //Serial.print("Debug: ");
    //Serial.print(command);
    Serial2.print(command);
    printDouble_S2(output_amplitude_shear,1000000);
    prev_output_amplitude_shear = output_amplitude_shear;
    
    }
    delay(95);
  
}

void printDouble_S0( double val, unsigned int precision){
// prints val with number of decimal places determine by precision
// NOTE: precision is 1 followed by the number of zeros for the desired number of decimial places
// example: printDouble( 3.1415, 100); // prints 3.14 (two decimal places)

    Serial.print (int(val));  //prints the int part
    Serial.print("."); // print the decimal point
    unsigned int frac;
    if(val >= 0)
      frac = (val - int(val)) * precision;
    else
       frac = (int(val)- val ) * precision;
    int frac1 = frac;
    while( frac1 /= 10 )
        precision /= 10;
    precision /= 10;
    while(  precision /= 10)
        Serial.print("0");

    Serial.print(frac,DEC) ;
}

void printDouble_S1( double val, unsigned int precision){
// prints val with number of decimal places determine by precision
// NOTE: precision is 1 followed by the number of zeros for the desired number of decimial places
// example: printDouble( 3.1415, 100); // prints 3.14 (two decimal places)

    Serial1.print (int(val));  //prints the int part
    Serial1.print("."); // print the decimal point
    unsigned int frac;
    if(val >= 0)
      frac = (val - int(val)) * precision;
    else
       frac = (int(val)- val ) * precision;
    int frac1 = frac;
    while( frac1 /= 10 )
        precision /= 10;
    precision /= 10;
    while(  precision /= 10)
        Serial1.print("0");

    Serial1.println(frac,DEC) ;
}

void printDouble_S2( double val, unsigned int precision){
// prints val with number of decimal places determine by precision
// NOTE: precision is 1 followed by the number of zeros for the desired number of decimial places
// example: printDouble( 3.1415, 100); // prints 3.14 (two decimal places)

    Serial2.print (int(val));  //prints the int part
    Serial2.print("."); // print the decimal point
    unsigned int frac;
    if(val >= 0)
      frac = (val - int(val)) * precision;
    else
       frac = (int(val)- val ) * precision;
    int frac1 = frac;
    while( frac1 /= 10 )
        precision /= 10;
    precision /= 10;
    while(  precision /= 10)
        Serial2.print("0");

    Serial2.println(frac,DEC) ;
}
