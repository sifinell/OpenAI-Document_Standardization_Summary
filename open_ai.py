import openai
import tiktoken

# Get the API key and resource endpoint from environment variables
API_KEY = "your_api_key"
RESOURCE_ENDPOINT = "your_resource_endpoint"

# Set the API type and key in the openai library
openai.api_type = "azure"
openai.api_key = API_KEY
openai.api_base = RESOURCE_ENDPOINT
openai.api_version = "2023-07-01-preview"

MODEL = "gpt-4-32k"

def num_tokens_from_string(string: str, encoding_name: str) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    print("Input tokens: " + str(num_tokens))
    return num_tokens

def prompt_open_ai(text_input_long, section_paragraph):

    messages = []
    paragraphs = []

    # Setting system role
    messages.append({"role":"system","content":text_input_long})

    for title, content in section_paragraph.items():

        messages.append({"role": "user", "content": content})
        content_tokens = num_tokens_from_string(content, "cl100k_base")

        response = openai.ChatCompletion.create(
                    engine=MODEL,
                    messages=messages,
                    request_timeout=2000,
                    max_tokens=content_tokens+500,
                    temperature=0.8
                )
        
        chat_message = response['choices'][0]['message']['content']
        
        try:
            messages.append({"role": "assistant", "content": chat_message})
        except:
            messages.append({"role": "assistant", "content": "Error"})

        print(f"## {title}\n\n{chat_message}\n\n")
        paragraphs.append(f"## {title}\n\n{chat_message}\n\n")
        print("\n\n")

    return paragraphs

def prompt_open_ai_recap(text_input_long, content):

    messages = []

    # Setting system role
    messages.append({"role":"system","content":text_input_long})
    messages.append({"role": "user", "content": content})
    
    content_tokens = num_tokens_from_string(content, "cl100k_base")

    response = openai.ChatCompletion.create(
                engine=MODEL,
                messages=messages,
                request_timeout=2000,
                max_tokens=content_tokens+500,
                temperature=0.8
            )
        
    output = response['choices'][0]['message']['content']

    return output