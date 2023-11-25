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
                "text": "This is the first interesting part of the video",
                "duration": 20.00
            },
            {
                "start_time": 60.00,
                "end_time": 90.00,
                "text": "This is the second interesting part of the video",
                "duration": 30.00
            },
            {
                "start_time": 120.00,
                "end_time": 150.00,
                "text": "This is the third interesting part of the video",
                "duration": 30.00
            }
        ]
    '''

    def interesting_parts(self, transcript):
        prompt = f"I am going to pass you the transcript of a video, identify {self.amount_of_interesting_parts} interesting parts of the video. Make sure they are around 30 seconds in duration, and provide the accurate timestamps being passed. Follow this format: {self.formatted_example}. Return in JSON format."
        messages = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": transcript}
        ]
        print(self.model)

        return self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.1,
            response_format={"type": "json_object"}
        ).choices[0].message.content


