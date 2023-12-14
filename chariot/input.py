"""Classes for processing natural language requests"""

import spacy

class NaturalLanguageJourneyRequestTRF:
    """
    Process a natural language request using the SpaCy core transformer model
    """
    def __init__(self):
        self.nlp = spacy.load('en_core_web_trf')

    def process_input(self, natural_input):
        """
        Pass a single natural language input through SpaCy.

        Do not process if the request is ambiguous (eg. "Get me
        from London Bridge from Blackfriars to Highgate")
        """
        doc = self.nlp(natural_input)

        journey_request = {
            "from": None,
            "to": None,
        }

        for chunk in doc.noun_chunks:
            # If entities have been detected, assign them to from | to | via
            if chunk.ents:
                head = chunk.root.head.text.lower()
                if head in ["from", "to", "via"]:
                    # If >1 from | to | via entity, halt
                    if journey_request.get(head, None):
                        return f"Ambiguous input - multiple '{head}' points"

                    journey_request[head] = chunk.text.strip()

        return journey_request
