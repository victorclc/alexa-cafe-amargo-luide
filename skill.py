from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model import Response
from ask_sdk_model.ui import SimpleCard
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from cafes import cafes
import random

CARD_TITLE = "Café amargo"


def get_random_cafe():
    return random.choice(cafes)


class LaunchRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech_text = get_random_cafe()

        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard(CARD_TITLE, speech_text)).set_should_end_session(
            True)
        return handler_input.response_builder.response


class GetNewCafeIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("GetNewCafe")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech_text = get_random_cafe()

        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard(CARD_TITLE, speech_text)).set_should_end_session(
            True)
        return handler_input.response_builder.response


class HelpIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech_text = 'Voce pode me pedir um café amargo.'

        handler_input.response_builder.speak(speech_text).ask(speech_text).set_card(
            SimpleCard(CARD_TITLE, speech_text))
        return handler_input.response_builder.response


class CancelAndStopIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.CancelIntent")(handler_input) or is_intent_name("AMAZON.StopIntent")(
            handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech_text = "Nunca é tarde para desistir no meio do caminho. Até a próxima!"

        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Café amargo", speech_text)).set_should_end_session(True)
        return handler_input.response_builder.response


class SessionEndedRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        # any cleanup logic goes here

        return handler_input.response_builder.response


class AllExceptionHandler(AbstractExceptionHandler):

    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        # Log the exception in CloudWatch Logs
        print(exception)

        speech = "Fala direito, não entendi."
        handler_input.response_builder.speak(speech).ask(speech)
        return handler_input.response_builder.response


sb = SkillBuilder()

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(GetNewCafeIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelAndStopIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())

sb.add_exception_handler(AllExceptionHandler())

handler = sb.lambda_handler()
