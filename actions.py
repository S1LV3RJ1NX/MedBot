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

def get_medicine_and_time(tracker):
	"""This function gets the medicine and tracker name for corresponding reminder
	It extracts it from the latest event"""

	# print(tracker.events[-1])
	last_event = tracker.events[-1]
	medicine = last_event['parse_data']['entities'][0]['value']
	time = last_event['parse_data']['entities'][1]['value']
	interval = last_event['parse_data']['entities'][2]['value']
	return medicine,time,interval


class MedicineForm(FormAction):
	""" This class gets the required form entries and sets the reminder"""
	def name(self) -> Text:
		return "medicine_form"

	@staticmethod
	def required_slots(tracker: Tracker) -> List[Text]:
		"""A list of required slots the form has to fill"""
		return ["medicine_name", "time", "interval"]

	def slot_mappings(self):
		return  {
			"medicine_name": [
				self.from_entity(entity="medicine_name", intent=["tell_medicine_name","request_medicine_reminder"]),
				self.from_entity(entity="medicine_name",not_intent=["greet","goodbye","chitchat","affirm","deny","stop"])
				# self.from_text(not_intent=["greet","goodbye","chitchat","affirm","deny","stop"]),
			],
			"time" : [
				self.from_entity(entity="time", intent=["tell_medicine_time","request_medicine_reminder"])
			],
			"interval" : [
				self.from_entity(entity="duration", intent=["tell_interval", "request_medicine_reminder"])
			]
		}
			
	def validate_interval(
		self,
		value: Text,
		dispatcher: CollectingDispatcher,
		tracker: Tracker,
		domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

		seconds = None
		enitites_from_sentence = tracker.latest_message['entities']
		for entities in enitites_from_sentence:
			if entities['entity'] == 'duration':
				seconds = entities['additional_info']['normalized']['value']
		return {"interval":seconds}

	def validate_medicine_name(
		self,
		value: Text,
		dispatcher: CollectingDispatcher,
		tracker: Tracker,
		domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

		value = value.strip()
		# print("value: ",value)
		if value == None or value == '':
			# dispatcher.utter_message(template='utter_wrong_medicine')
			return {"medicine_name":None}
		else:
			return {"medicine_name":value}

	async def submit(
		self, 
		dispatcher: CollectingDispatcher,
		tracker: Tracker,
		domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
		# try:
			# get medicine, reminder time and interval from corresponding slots
			medicine = tracker.get_slot("medicine_name")
			full_time = tracker.get_slot("time")[:19]
			interval = tracker.get_slot("interval")

			resp = "Medbot will remind you daily for your medicine!!"
			
			# strip the time in required format
			date_time = datetime.datetime.strptime(full_time,"%Y-%m-%dT%H:%M:%S")

			print(medicine,full_time,interval)

			# Schedule the reminder
			reminder = ReminderScheduled(
				"EXTERNAL_reminder",
				trigger_date_time=date_time,
				entities = {"medicine":medicine,"time":date_time,"interval":interval},
				kill_on_user_message=False,
			)
			dispatcher.utter_message(text=resp)
			return [reminder, AllSlotsReset()]
		# except:
		# 	dispatcher.utter_message(text="Some error unable to set reminder..")

		# 	return []

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
		medicine,d_time,interval = get_medicine_and_time(tracker)
		# print(medicine, d_time)
		resp = "Hii it's your time to take medicine: "+str(medicine)
		# print(resp)
		dispatcher.utter_message(text=resp)


		new_time = datetime.datetime.utcfromtimestamp(d_time) + datetime.timedelta(seconds=interval)
		
		reminder = ReminderScheduled(
				"EXTERNAL_reminder",
				trigger_date_time=new_time,
				entities = {"medicine":medicine,"time":new_time,"interval":interval},
				kill_on_user_message=False,
			)
		
		return [reminder, AllSlotsReset()]

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


