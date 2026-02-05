class NavigationChatbot:
    MENU = {
        "1": "Campaign Help: To create a campaign, go to Messaging > Campaigns.",
        "2": "Credit & Billing: Check your balance in the Wallet section.",
        "3": "Device Issues: Ensure your phone is connected to the internet and QR is scanned.",
        "4": "API Help: Documentation is available at /docs.",
        "5": "Talk to Support: Open a ticket in the Support section."
    }

    @staticmethod
    def get_response(input_text: str):
        input_text = input_text.strip()
        if input_text in NavigationChatbot.MENU:
            return NavigationChatbot.MENU[input_text]
        
        return (
            "Welcome to WhatsApp SaaS Support Bot!\n"
            "Please choose an option:\n"
            "1️⃣ Campaign Help\n"
            "2️⃣ Credit & Billing\n"
            "3️⃣ Device Issues\n"
            "4️⃣ API Help\n"
            "5️⃣ Talk to Support"
        )
