## Story simple 
* greet
  - utter_greet
* affirm
  - utter_ask_medicine_name
* medicine_name
  - utter_ask_medicine_time
* medicine_time
  - action_set_reminder
* goodbye
  - utter_bye 

## Story affirm
* affirm
  - utter_ask_medicine_name
* medicine_name
  - utter_ask_medicine_time
* medicine_time
  - action_set_reminder
* goodbye
  - utter_bye

## Story affirm 2
* medicine_time
  - utter_ask_medicine_name
* medicine_name
  - action_set_reminder

## Story affirm 3
* medicine_name
  - utter_ask_medicine_time
* medicine_time
  - action_set_reminder

## Story react_reminder
* EXTERNAL_reminder
  - action_react_to_reminder

## Story cancel_reminder
* cancel_reminder
  - action_cancel_reminder

## Story deny
* deny
  - utter_bye


