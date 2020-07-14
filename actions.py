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
from rasa_sdk.events import SlotSet, ReminderScheduled
from datetime import datetime

# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

class ActionSetReminder(Action):

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

	async def run(self, dispatcher: CollectingDispatcher,
			tracker: Tracker,
			domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
		# try:	
			medicine = tracker.get_slot("medicine_name")
			full_time = tracker.get_slot("time")[:23]
			print(full_time)
			time = full_time[11:19].split(":")
			hour,minute = time[0],time[1]
			resp = "Your reminder for medicine "+str(medicine)+" is set for "+str(hour)+" hr and "+str(minute)+" min daily."
			print(resp)
			dispatcher.utter_message(text=resp)
			date = datetime.strptime(full_time,"%Y-%m-%dT%H:%M:%S.%f")
			print("Time is: ",date)
			reminder = ReminderScheduled(
				"EXTERNAL_reminder",
				trigger_date_time=date,
				name="my_reminder",
				kill_on_user_message=False,
			)
			return [reminder]
		# except:
		# 	print("Some error unable to set reminder..")

		# 	return []

class ActionReactToReminder(Action):
	"""Reminds the user to call someone."""

	def name(self) -> Text:
		return "action_react_to_reminder"

	async def run(
		self,
		dispatcher: CollectingDispatcher,
		tracker: Tracker,
		domain: Dict[Text, Any],
	) -> List[Dict[Text, Any]]:

		medicine = tracker.get_slot("medicine_name")
		time = tracker.get_slot("time")[11:19].split(":")
		hr,minute = time[0],time[1]
		resp = "Hii it's your time to take medicine: "+str(medicine)+" on "+str(hr)+" hr "+str(minute)+" min"
		print(resp)
		dispatcher.utter_message(text=resp)
		return []

