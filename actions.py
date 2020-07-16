# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
#
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction
from rasa_sdk.events import SlotSet, ReminderScheduled, AllSlotsReset, ReminderCancelled
import datetime
# from dateutil import parser


def get_medicine_and_time(tracker):
	"""This function gets the medicine and tracker name for corresponding reminder
	It extracts it from the latest event"""

	# print(tracker.events[-1])
	last_event = tracker.events[-1]
	medicine = last_event['parse_data']['entities'][0]['value']
	time = last_event['parse_data']['entities'][1]['value']
	return medicine,time


class ActionSetReminder(Action):
	""" This class sets the reminder"""
	def name(self) -> Text:
		return "action_set_reminder"

	@staticmethod
	def required_slots(tracker: Tracker) -> List[Text]:
		"""A list of required slots the form has to fill"""
		return ["medicine_name", "time"]

	def slot_mappings(self):
		return {
			"medicine_name": [
				self.from_entity(intent="medicine_name"),
			],
			"time" : [
				self.from_entity(intent="time"),
			]
		}

	async def run(
		self, 
		dispatcher: CollectingDispatcher,
		tracker: Tracker,
		domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
		try:
			# get medicine and tracker name from corresponding slots
			medicine = tracker.get_slot("medicine_name")
			full_time = tracker.get_slot("time")[:19]
			# print(full_time, type(full_time))
			resp = "Medbot will remind you daily for your medicine!!"
			# print(resp)
			dispatcher.utter_message(text=resp)

			# strip the time in required format
			date_time = datetime.datetime.strptime(full_time,"%Y-%m-%dT%H:%M:%S")

			# print("Time is: ",date_time)
			# date_time = datetime.datetime.now() + datetime.timedelta(seconds=18)
			
			# Schedule the reminder
			reminder = ReminderScheduled(
				"EXTERNAL_reminder",
				trigger_date_time=date_time,
				entities = {"medicine":medicine,"time":date_time},
				kill_on_user_message=False,
			)
			return [reminder]
		except:
			dispatcher.utter_message(text="Some error unable to set reminder..")

			return []

class ActionReactToReminder(Action):
	"""Reminds the user to take the medicine."""

	def name(self) -> Text:
		return "action_react_to_reminder"

	async def run(
		self,
		dispatcher: CollectingDispatcher,
		tracker: Tracker,
		domain: Dict[Text, Any],
	) -> List[Dict[Text, Any]]:

		# get medicine and requied time
		medicine,d_time = get_medicine_and_time(tracker)
		# print(medicine, d_time)
		resp = "Hii it's your time to take medicine: "+str(medicine)
		# print(resp)
		dispatcher.utter_message(text=resp)

		# for easy check right now timing set to 43 seconds.
		new_time = datetime.datetime.utcfromtimestamp(d_time) + datetime.timedelta(seconds=43)
		reminder = ReminderScheduled(
				"EXTERNAL_reminder",
				trigger_date_time=new_time,
				entities = {"medicine":medicine,"time":new_time},
				kill_on_user_message=False,
			)
		
		return [reminder]

class ForgetReminders(Action):
    """Cancels all reminders."""

    def name(self) -> Text:
        return "action_cancel_reminder"

    async def run(
        self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(f"Okay, all your reminders are cancelled !!")

        # Cancel all reminders
        return [ReminderCancelled(), AllSlotsReset()]


