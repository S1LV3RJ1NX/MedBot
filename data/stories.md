## Story simple 
* greet
  - utter_greet
* affirm
  - medicine_form
  - form{"name" : "medicine_form"}
  - form{"name" : null}
* goodbye
  - utter_bye 

## Story simple 2
* request_medicine_reminder
  - medicine_form
  - form{"name": "medicine_form"}
  - form{"name" : null}

## Story simple 3
* request_medicine_reminder{"medicine_name":"clipa"}
  - medicine_form
  - form{"name": "medicine_form"}
  - form{"name" : null}

## Story simple 4
* request_medicine_reminder{"time":"2020-07-19T17:00:00.000+00:00","medicine_name":"clipa"}
  - medicine_form
  - form{"name": "medicine_form"}
  - form{"name" : null}

## Story affirm
* affirm
  - medicine_form
  - form{"name" : "medicine_form"}
  - form{"name" : null}
* goodbye
  - utter_bye

## chitchat
* request_medicine_reminder
    - medicine_form
    - form{"name": "medicine_form"}
* chitchat
    - utter_chitchat
    - medicine_form
    - form{"name": null}

## chitchat 2
* request_medicine_reminder
    - medicine_form
    - form{"name": "medicine_form"}
* stop
    - utter_ask_continue
* deny
    - action_deactivate_form
    - form{"name": null}

## chitchat 3
* request_medicine_reminder
    - medicine_form
    - form{"name": "medicine_form"}
* stop
    - utter_ask_continue
* affirm
    - medicine_form
    - form{"name": null}

## Story react_reminder
* EXTERNAL_reminder
  - action_react_to_reminder

## Story cancel_reminder
* cancel_reminder
  - action_cancel_reminder

## Story deny
* deny
  - utter_bye





