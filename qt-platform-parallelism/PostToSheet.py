from requests import post

DEPLOYED_SHEET_URL = "https://script.google.com/macros/s/AKfycbwcem4Ihq-y3vkVZcbr7d9SAHY2lYP519-2VOddnl1f6PilMSekuXqvHu8o-i41LPEF/exec"

def post_to_google_sheets(json_data: dict) -> bool:
    '''
    Post data to Google Sheets

    Args:
        json_data (dict): Data to post

    eturns:
        bool: True if successful, False otherwise
    '''
    response = post(DEPLOYED_SHEET_URL, json=json_data)

    return response.status_code == 200