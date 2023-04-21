# -*- coding: utf-8 -*-
import logging

from ask_sdk.standard import StandardSkillBuilder

import ask_sdk_core.utils as ask_utils

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model import Response
from ask_sdk_core import attributes_manager

from ask_sdk_core.utils import is_request_type, is_intent_name

import os
import openai
from datetime import date
from datetime import datetime
from datetime import timedelta
import time
import boto3
import json

session = boto3.session.Session()
secret = session.client(service_name = 'secretsmanager')
dynamo = boto3.resource('dynamodb')
secret_name = os.environ["SM_NAME"]
table_name = os.environ["DYNAMO_TABLE"]
response = secret.get_secret_value(SecretId = secret_name)

data = json.loads(response['SecretString'])
openai.api_key = data['chatgpt_token']

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

objectsToSearchTableName = "chatgpt"
todayDate = datetime.now().strftime("%Y-%m-%d %H:%M")

sb = StandardSkillBuilder(table_name = objectsToSearchTableName, auto_create_table = True)

class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):

        speak_output = "Bienvenido a la skill de Chat GPT, ahora puedes empezar a preguntar lo que desees, dime tu pregunta por favor?"
        
        attr = handler_input.attributes_manager.persistent_attributes
        print("Launch")
        print(attr)
        logger.info(attr)
        handler_input.attributes_manager.session_attributes = attr

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .set_should_end_session(False)
                .response
        )


class PreguntaIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("PreguntaIntent")(handler_input)

    def handle(self, handler_input):
        
        slots = handler_input.request_envelope.request.intent.slots
        logger.info(slots)
        print("question = " + str(slots["question"].slot_value.value))

        question = str(slots["question"].slot_value.value)
        #question = "Quién es Lionel Messi en 30 palabras"
        
        data = openai.Completion.create(
            model = "text-davinci-003",
            prompt = question,
            temperature = 0,
            max_tokens = 400,
            top_p = 1.0,
            frequency_penalty = 0.0,
            presence_penalty = 0.0
        )
        
        resp_chatgpt = str(data["choices"][0]["text"])
        print(resp_chatgpt)

        d = datetime.today() - timedelta(hours = 5, minutes = 0) #hora Lima
        date_reg = str(d.strftime("%Y-%m-%d %H:%M:%S"))  
        
        table_dynamo_execution = dynamo.Table(table_name)
        table_dynamo_execution.put_item(
          Item = {
              "id" : str(int(time.time())),
              "question" : question,
              "answer" : resp_chatgpt,
              "freg" : date_reg
              }
          )

        return (
            handler_input.response_builder
                .speak(resp_chatgpt + " ¿tienes otra pregunta para mí?")
                .ask("¿Tienes otra pregunta para mí?")
                .response
        )


class DespedidaIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("DespedidaIntent")(handler_input)

    def handle(self, handler_input):
        speak_output = "Soy Alexa y me agrada saber que me hayas integrado con la api de chat GPT, nos vemos pronto"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )

        
class HelloWorldIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("HelloWorldIntent")(handler_input)

    def handle(self, handler_input):
        speak_output = "Hello World probando!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )


class HelpIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        speak_output = "You can say hello to me! How can I help?"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class CancelOrStopIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        speak_output = "Goodbye!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )

class FallbackIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        logger.info("In FallbackIntentHandler")
        speech = "Hmm, I'm not sure. You can say Hello or Help. What would you like to do?"
        reprompt = "I didn't catch that. What can I help you with?"

        return handler_input.response_builder.speak(speech).ask(reprompt).response

class SessionEndedRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        return handler_input.response_builder.response


class IntentReflectorHandler(AbstractRequestHandler):
    """The intent reflector is used for interaction model testing and debugging.
    It will simply repeat the intent the user said. You can create custom handlers
    for your intents by defining them above, then also adding them to the request
    handler chain below.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        intent_name = ask_utils.get_intent_name(handler_input)
        speak_output = "You just triggered " + intent_name + "."

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Generic error handling to capture any syntax or routing errors. If you receive an error
    stating the request handler chain is not found, you have not implemented a handler for
    the intent being invoked or included it in the skill builder below.
    """
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)

        speak_output = "Sorry, I had trouble doing what you asked. Please try again."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(HelloWorldIntentHandler())
sb.add_request_handler(PreguntaIntentHandler())
sb.add_request_handler(DespedidaIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(IntentReflectorHandler()) # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers

sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()