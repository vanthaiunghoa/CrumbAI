import itertools
import json
from openai import OpenAI

class gpt:
    """
    Class to handle GPT model operations for video transcript analysis.
    It initializes with API key and model configuration and provides functionality to identify interesting parts of a video.
    """

    def __init__(self, key, model="gpt-3.5-turbo", needed_interesting_parts=3):
        """
        Initializes the gpt class with API key, model type, and the number of interesting parts needed.
        """
        self.key = key
        self.model = model
        self.amount_of_interesting_parts = needed_interesting_parts
        self.client = OpenAI(api_key=self.key)
        # Example formatted JSON structure for AI predictions
        self.formatted_example = '''
        [
            {
                "start_time": 10.00,
                "end_time": 60.00,
                "description": "This is the first interesting part of the video",
                "summary": "short summary with context to the clip e.g Joe Rogan Talking about the importance of mental health in the workplace. Leads to unexpected argument with guest.",
                "duration": 50.00
            },
            {
                "start_time": 70.00,
                "end_time": 130.00,
                "description": "This is the second interesting part of the video",
                "summary": "short summary with context to the clip e.g Joe Rogan Talking about the importance of mental health in the workplace. Leads to unexpected argument with guest.",
                "duration": 60.00
            },
            {
                "start_time": 150.00,
                "end_time": 190.00,
                "description": "This is the third interesting part of the video",
                "summary": "short summary with context to the clip e.g Joe Rogan Talking about the importance of mental health in the workplace. Leads to unexpected argument with guest.",
                "duration": 40.00
            }
        ]
        '''

    def interesting_parts(self, transcript):
        """
        Analyzes a video transcript and identifies potentially viral segments based on the model's predictions.
        Handles token limit errors by splitting the transcript and processing in parts.
        """
        try:
            prompt = f"Given the following video transcript, analyse each part for potential virality and identify {self.amount_of_interesting_parts} most viral segments from the transcript. Each segment should have nothing less than 50 seconds in duration and more than 20 seconds, for a clip contains an interesting conversation, you can ignore the duration requirement if it goes beyond it. Do not cut the conversation off and let it finish before cutting it out. The provided transcript is as follows: {transcript}. Based on your analysis, return a JSON document containing the timestamps (start and end), the description of the viral part, the summary with context to the situation this should be said in a manner suitable for a tiktok description, and its duration. The JSON document should follow this format: {self.formatted_example}. Please replace the placeholder values with the actual results from your analysis, and name the key of the JSON 'segments'."
            system = f"You are a Viral Segment Identifier, an AI system that analyses a video's transcript and predict which segments might go viral on social media platforms. You use factors such as emotional impact, humor, unexpected content, and relevance to current trends to make your predictions. You return a structured JSON document detailing the start and end times, the description, and the duration of the potential viral segments. Evaluate the text chunks on their clarity, relevance, and ability to stand alone as engaging content without needing external context"

            messages = [
                {"role": "system", "content": system},
                {"role": "user", "content": prompt}
            ]

            # Generate predictions using the OpenAI API
            return self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                response_format={"type": "json_object"}
            ).choices[0].message.content

        except Exception as e:
            if 'This model\'s maximum context length is 16385 tokens. However, your messages resulted' in str(e):
                split_transcript_1, split_transcript_2 = self.split_sequence(transcript)
                first_half = json.loads(self.interesting_parts(split_transcript_1))
                second_half = json.loads(self.interesting_parts(split_transcript_2))
                merged_result = {
                    "segments": first_half["segments"] + second_half["segments"]
                }

                return json.dumps(merged_result)
            else:
                print('Error analysing transcript.')
                print(e)
                return None

    def merge_two_dicts(self, processed_part_1, processed_part_2):
        """
        Helper function to merge the results from two processed parts of a transcript.
        """
        processed_part_1 = processed_part_1["segments"]
        processed_part_2 = processed_part_2["segments"]
        return {"segments": processed_part_1 + processed_part_2}

    def split_sequence(self, sequence):
        """
        Splits a sequence into two halves, attempting to divide it evenly.
        Used to manage large inputs that exceed the token limit of the model.
        """
        n = len(sequence) // 2
        i = iter(sequence)

        first_half = list(itertools.islice(i, n))
        second_half = list(i)

        return first_half, second_half
