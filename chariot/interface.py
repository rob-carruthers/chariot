"""Main interface classes for chariot"""

from .input import NaturalLanguageJourneyRequestTRF
from .journey import JourneyRequest

class ChariotJourneyPipeline:
    """
    Main interface for accessing language processing and journey requests from TFL
    """
    def __init__(self):
        # Holding nlp object in memory to reduce reloading time
        self.nlp = NaturalLanguageJourneyRequestTRF()

    def request_from_natural_language(self, natural_input):
        """
        Request a journey via TFL from a natural language input
        """

        journey_request_params = self.nlp.process_input(natural_input)
        journey_from = journey_request_params.get("from", None)
        journey_to = journey_request_params.get("to", None)

        if journey_from and journey_to:
            journey_request = JourneyRequest()
            journey = journey_request.get_best_journey(journey_from, journey_to)
            return journey

        # Return None if no valid from or to points
        return None
