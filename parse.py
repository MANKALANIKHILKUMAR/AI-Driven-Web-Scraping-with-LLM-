from openai import OpenAI
import os

# Load OpenAI API key from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

def parse_with_openai(dom_chunks, parse_description):
    try:
        parsed_results = []
        for chunk in dom_chunks:
            # Create a prompt for OpenAI
            prompt = (
                f"Extract specific information from the following text content: {chunk}. "
                f"Follow these instructions carefully:\n\n"
                f"1. Extract only the information that matches this description: {parse_description}.\n"
                f"2. Do not include any additional text, comments, or explanations.\n"
                f"3. If no information matches, return an empty string ('')."
            )

            # Call OpenAI API
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt},
                ],
                max_tokens=500,
            )

            # Append the parsed result
            parsed_results.append(response.choices[0].message.content.strip())
        return parsed_results
    except Exception as e:
        print(f"Error during parsing: {e}")
        raise








