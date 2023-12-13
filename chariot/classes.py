"""Classes for chariot, including requests from the TFL API and NLP"""
import requests

from .params import APP_KEY, PREFERRED_MODES, TFL_BASE_URL, TIMEOUT

class Journey:
    """
    Class for holding a planned journey.
    """
    def __init__(self, legs):
        self.duration = 0
        self.legs = legs
        self.departure_stop = legs[0]['departure_station']
        self.arrival_stop = legs[-1]['arrival_station']

        for leg in legs:
            self.duration += leg.get('duration', 0)
            self.duration += leg.get('interchange_duration', 0)

    def __str__(self):
        return f"<Journey from '{self.departure_stop}' to '{self.arrival_stop}'>"

    def __repr__(self):
        return f"<Journey('{self.departure_stop}' to '{self.arrival_stop}')>"

class JourneyRequest:
    """
    Class for handling requests from the TFL API and handling ambiguous input.
    """
    app_key = APP_KEY
    endpoint = "Journey/JourneyResults/"
    base_url = TFL_BASE_URL
    preferred_modes = PREFERRED_MODES

    def request_tfl_journey(self, journey_from, journey_to):
        """
        Request a journey from TFL between two points.

        Returns a JSON response, containing:
            - A Disambiguation for both from and to points
            - A Disambiguation for one of these points and a known stop
            - Two known stops
        """
        params = {
            "app_key": self.app_key
            }

        response = requests.get(self.base_url +
                                self.endpoint +
                                journey_from +
                                "/to/" +
                                journey_to,
                                params=params,
                                timeout=TIMEOUT).json()

        return response

    def return_top_matching_stops_from_disambiguation(self, response, from_or_to):
        """
        Process a LocationDisambiguation using only the preferred modes of transport.

        Return the top matching stops.
        """
        stops_with_allowed_modes = {}
        try:
            for option in response[from_or_to + 'LocationDisambiguation']['disambiguationOptions']:
                common_name = option['place'].get('commonName', None)
                naptan_id = option['place'].get('naptanId', None)
                modes = option['place'].get('modes', None)
                match_quality = option.get('matchQuality', None)
                if modes:
                    for preferred_mode in self.preferred_modes:
                        if preferred_mode in modes:
                            stops_with_allowed_modes[naptan_id] = {'naptan_id': naptan_id,
                                                                   'common_name': common_name,
                                                                   'match_quality': match_quality}
            top_matches = sorted(stops_with_allowed_modes.items(),
                                 key=lambda stop: stop[1]['match_quality'],
                                 reverse=True)
            return top_matches

        except KeyError as e:
            raise KeyError("No LocationDisambiguation found") from e

    def get_stop_names(self, response):
        """
        Parse a TFL response and invoke return_top_matching_stops_from_disambiguation
        where necessary.

        Else, return the stop name as is.
        """

        # If a Disambiguation list is found, process it
        if response.get('fromLocationDisambiguation', None).get('matchStatus', None) == 'list':
            from_stop = self.return_top_matching_stops_from_disambiguation(response, "from")
        # If not, return the stop name as is
        else:
            from_stop = response['journeyVector']['from']

        if response.get('toLocationDisambiguation', None).get('matchStatus', None) == 'list':
            to_stop = self.return_top_matching_stops_from_disambiguation(response, "to")
        else:
            to_stop = response['journeyVector']['to']

        return {"from": from_stop, "to": to_stop}

    def extract_legs(self, journey):
        """
        Extract the legs from a TFL journey request, with stops and metadata
        """
        legs = []
        for leg in journey['legs']:
            legs.append({
                'summary': leg['instruction']['summary'],
                'duration': int(leg['duration']),
                'departure_station': leg['departurePoint']['commonName'],
                'arrival_station': leg['arrivalPoint']['commonName'],
                'interchange_duration': int(leg.get('interChangeDuration', 0))
            })
        return legs

    def get_best_journey(self, journey_from, journey_to):
        """
        Get the best journey from a set of (possibly ambiguous) from and to points.
        """
        disambiguation = self.request_tfl_journey(journey_from, journey_to)

        stop_names = self.get_stop_names(disambiguation)

        # Get the most likely stop names, if a disambiguation was performed and a list was returned
        if stop_names['from']:
            stop_from = stop_names['from'] \
                if isinstance(stop_names['from'], str) \
                else stop_names['from'][0][0]
        else:
            raise KeyError("No 'from' stops found matching input criteria.")

        if stop_names['to']:
            stop_to = stop_names['to'] \
                if isinstance(stop_names['to'], str) \
                else stop_names['to'][0][0]
        else:
            raise KeyError("No 'to' stops found matching input criteria.")

        # Get a new journey with the disambiguated stop names
        # Extract only the best journey
        journey = self.request_tfl_journey(stop_from, stop_to)['journeys'][0]
        legs = self.extract_legs(journey)

        return Journey(legs)
