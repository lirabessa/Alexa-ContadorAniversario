import ask_sdk_core.utils as ask_utils
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_model import Response
from datetime import datetime

# Definição dos handlers de intenções

class LaunchRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        speak_output = "Bem-vinde! Quando é o seu aniversário?"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

class GetBirthdayIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("GetBirthdayIntent")(handler_input)

    def handle(self, handler_input):
        slots = handler_input.request_envelope.request.intent.slots
        birthday_date = slots["BirthdayDate"].value

        if not birthday_date:
            speak_output = "Desculpe, não entendi a data do seu aniversário. Por favor, diga novamente."
        else:
            try:
                today = datetime.now()
                birthday = datetime.strptime(birthday_date, "%Y-%m-%d")
                days_until_birthday = (birthday - today).days

                if days_until_birthday == 0:
                    speak_output = "Feliz aniversário!"
                elif days_until_birthday < 0:
                    speak_output = "Seu aniversário já passou."
                else:
                    speak_output = f"Faltam {days_until_birthday} dias para o seu aniversário."
            except ValueError:
                speak_output = "Desculpe, parece que a data do seu aniversário está em um formato incorreto. Por favor, diga novamente."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

class HelpIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        speak_output = "Você pode me dizer a data do seu aniversário. Por exemplo, 'Meu aniversário é em 12 de setembro'."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

class CancelAndStopIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return (
            ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input)
            or ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input)
        )

    def handle(self, handler_input):
        speak_output = "Até a próxima! Tenha um ótimo dia!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .set_should_end_session(True)
                .response
        )

class SessionEndedRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        return handler_input.response_builder.response

# Configuração do Skill Builder e adição de handlers

from ask_sdk_core.skill_builder import SkillBuilder

sb = SkillBuilder()

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(GetBirthdayIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelAndStopIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())

# Função Lambda

def lambda_handler(event, context):
    return sb.lambda_handler()(event, context)