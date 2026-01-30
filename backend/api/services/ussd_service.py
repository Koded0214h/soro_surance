class USSDService:
    """Service for handling USSD requests"""
    
    def process_request(self, session_id, phone_number, service_code, text):
        """Process USSD request"""
        
        # Parse USSD text
        text_array = text.split('*')
        user_input = text_array[-1] if text_array else ''
        step = len(text_array)
        
        # Initialize session
        if step == 0 or user_input == '':
            return self._show_welcome_menu()
        
        # Process based on step
        if step == 1:
            return self._process_main_menu(user_input, phone_number)
        elif step == 2:
            return self._process_insurance_menu(user_input, phone_number)
        elif step == 3:
            return self._process_claim_menu(user_input, phone_number, text_array)
        elif step == 4:
            return self._process_payment_menu(user_input, phone_number, text_array)
        else:
            return self._show_error_menu()
    
    def _show_welcome_menu(self):
        """Show welcome menu"""
        response = "CON Welcome to Sorosurance\n"
        response += "1. Buy Insurance\n"
        response += "2. File Claim\n"
        response += "3. Check Policy\n"
        response += "4. Make Payment\n"
        response += "5. Speak to Agent\n"
        return response
    
    def _process_main_menu(self, user_input, phone_number):
        """Process main menu selection"""
        if user_input == '1':
            return self._show_insurance_types()
        elif user_input == '2':
            return self._initiate_voice_claim(phone_number)
        elif user_input == '3':
            return self._check_policy_status(phone_number)
        elif user_input == '4':
            return self._show_payment_options()
        elif user_input == '5':
            return self._connect_to_agent(phone_number)
        else:
            return self._show_error_menu()
    
    def _show_insurance_types(self):
        """Show insurance types"""
        response = "CON Select Insurance Type:\n"
        response += "1. Motor Insurance\n"
        response += "2. Health Insurance\n"
        response += "3. Property Insurance\n"
        response += "4. Go Back\n"
        return response
    
    def _initiate_voice_claim(self, phone_number):
        """Initiate voice claim via USSD"""
        # This would trigger a voice call back
        response = "END Your claim request has been received.\n"
        response += "You will receive a voice call shortly to record your claim details.\n"
        response += "Thank you for using Sorosurance."
        return response
    
    def _check_policy_status(self, phone_number):
        """Check policy status"""
        # In production, query database for user's policies
        response = "CON Enter your Policy Number:\n"
        return response
    
    def _show_payment_options(self):
        """Show payment options"""
        response = "CON Select Payment Type:\n"
        response += "1. Pay Premium\n"
        response += "2. Pay Claim Deductible\n"
        response += "3. Go Back\n"
        return response
    
    def _connect_to_agent(self, phone_number):
        """Connect to human agent"""
        response = "END You will receive a call from our agent within 5 minutes.\n"
        response += "Thank you for choosing Sorosurance."
        return response
    
    def _show_error_menu(self):
        """Show error menu"""
        response = "END Invalid selection. Please try again.\n"
        response += "Dial *384*7676# to restart."
        return response