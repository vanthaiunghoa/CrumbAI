from openai import OpenAI


class gpt:

    def __init__(self, key, model="gpt-3.5-turbo", needed_interesting_parts=3):
        self.key = key
        self.model = model
        self.amount_of_interesting_parts = needed_interesting_parts
        self.client = OpenAI(api_key=self.key)
        self.formatted_example = '''
        [
            {
                "start_time": 10.00,
                "end_time": 30.00,
                "description": "This is the first interesting part of the video",
                "duration": 20.00
            },
            {
                "start_time": 60.00,
                "end_time": 90.00,
                "description": "This is the second interesting part of the video",
                "duration": 30.00
            },
            {
                "start_time": 120.00,
                "end_time": 150.00,
                "description": "This is the third interesting part of the video",
                "duration": 30.00
            }
        ]
    '''

    def interesting_parts(self, transcript):
        print('Analysing transcript...')
        prompt = f"Given the following video transcript, analyse each part for potential virality and identify {self.amount_of_interesting_parts} most viral segments from the transcript. Each segment should have nothing less than 50 seconds in duration. Do not cut the conversation off and let it finish before cutting it out. The provided transcript is as follows: {transcript}. Based on your analysis, return a JSON document containing the timestamps (start and end), the description of the viral part, and its duration. The JSON document should follow this format: {self.formatted_example}. Please replace the placeholder values with the actual results from your analysis, and name the key of the JSON 'segments'."
        system = f"You are a Viral Segment Identifier, an AI system that analyses a video's transcript and predict which segments might go viral on social media platforms. You use factors such as emotional impact, humor, unexpected content, and relevance to current trends to make your predictions. You return a structured JSON document detailing the start and end times, the description, and the duration of the potential viral segments."

        messages = [
            {"role": "system", "content": system},
            {"role": "user", "content": prompt}
        ]

        return self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            response_format={"type": "json_object"}
        ).choices[0].message.content


