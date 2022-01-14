from flask import Blueprint, render_template

miscellaneous = Blueprint('miscellaneous', __name__)

@miscellaneous.route('/client')
def landing_page_client():
    return render_template('client/landing_page.html')

@miscellaneous.route('/service-provider')
def landing_page_service_provider():
    return render_template('service_provider/landing_page.html')

@miscellaneous.route('/privacy-policy')
def privacy_policy():
    return render_template('privacy_policy.html')

@miscellaneous.route('/terms-and-conditions')
def terms_and_conditions():
    return render_template('terms_and_conditions.html')