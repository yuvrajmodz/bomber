from flask import Flask, request, jsonify
from playwright.sync_api import sync_playwright
import os

app = Flask(__name__)

# Function to automate the SMS bomber process using Playwright
def automate_sms_bomber(target_number):
    try:
        with sync_playwright() as p:
            # Launch browser
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            # Navigate to the SMS bomber page
            page.goto("https://mytoolstown.com/smsbomber/#bestsmsbomber")

            # Fill in the mobile number field
            page.fill('input[id="mobno"]', target_number)

            # Fill in the number of SMS (e.g., 100)
            page.fill('input[id="count"]', '100')

            # Click the START button to initiate the SMS bombing
            page.click('button[id="startsms"]')

            # Wait for the button text to change from "START" to "Sending..."
            # We're waiting for the inner text of the button to change
            page.wait_for_selector('span#submitBtnText', state="attached")

            # Retrieve the changed button text
            button_text = page.text_content('span#submitBtnText')

            # Check if the button text has changed to "Sending..."
            if button_text == "Sending...":
                button_status = "Button text changed to 'Sending...'"
            else:
                button_status = f"Button text is still '{button_text}'"

            # Optionally, you can stay on the page without closing the browser
            # browser.close() is not called to keep the page open

            # Return success message along with button status
            return {"status": "success", "message": "SMS bombing initiated successfully", "button_status": button_status}

    except Exception as e:
        return {"status": "error", "message": str(e)}

# Flask route to handle the API request
@app.route('/smsbomber', methods=['GET'])
def smsbomber():
    target = request.args.get('target')

    # Validate the input (must be a 10-digit number)
    if target and len(target) == 10 and target.isdigit():
        result = automate_sms_bomber(target)
        return jsonify(result)
    else:
        return jsonify({"status": "error", "message": "Invalid target number. Please provide a valid 10-digit number."})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5026))
    app.run(host='0.0.0.0', port=port, debug=True)