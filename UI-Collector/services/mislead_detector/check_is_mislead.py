import requests

def check_is_mislead_text(text: str) -> bool:
    """
    Check if the input text is misleading text
    :param text: The input text to be checked
    :return: True if the text is misleading, False otherwise
    """
    api_url = 'http://172.16.108.178:5193/check_misleading'  # Replace with the actual URL where the API is hosted
    data = {'text': text}
    response = requests.post(api_url, json=data)

    if response.status_code == 200:
        result = response.json()
        return result['is_misleading']
    else:
        print("Failed to call the API:", response.status_code, response.text)
        return False  # Return False if there was an error calling the API