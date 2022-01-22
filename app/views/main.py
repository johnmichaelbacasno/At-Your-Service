from distutils.command import upload
from flask import Blueprint, render_template, redirect, request_finished, url_for, flash, request, session, current_app, send_file
from graphviz import render
from werkzeug.utils import secure_filename
from datetime import datetime
import os

from extensions import db

from .. forms import *
from .. manage import *

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('landing_page.html', requests=all_request_posts(), services=all_service_posts())

@main.route('/sign-in', methods=["POST", "GET"])
def sign_in():
    form = SignInForm()
    user = session.get('user_id')

    if user is not None:
        return redirect('/dashboard')
    if form.validate_on_submit():
        session['user_id'] = form.user_id.data
        return redirect('/dashboard')
    return render_template('sign_in.html', form=form)

@main.route('/sign-out')
def sign_out():
    session["user_id"] = None
    return redirect('/')

@main.route('/account-type-selection')   
def account_type_selection():
    user = session.get('user_id')

    if user is not None:
        return redirect('/dashboard')
    else:
        return render_template('account_type_selection.html')

@main.route('/client/create-account', methods=["POST", "GET"])
def client_create_account():
    user = session.get('user_id')

    if user is not None:
        return redirect('/dashboard')
    else:
        form = SignUpForm(data={"user_account_type":"C"})
        if form.validate_on_submit():
            query = """
                INSERT INTO `User`(`user_id`, `user_password`, `user_account_type`, `user_rating`, `user_level`, `user_is_trusted`)
                VALUES(%s, %s, %s, 0, 1, false)
                """
            data = (
                form.user_id.data,
                form.user_password.data,
                form.user_account_type.data
                )
            session['user_id'] = form.user_id.data     

            conn = db.connect()
            cursor = conn.cursor()
            cursor.execute(query, data)
            cursor.close()
            conn.commit()
            conn.close()
            return redirect('/client/fill-up')
        else:
            return render_template('client/create_account.html', form=form)

@main.route('/service-provider/create-account', methods=["POST", "GET"])
def service_provider_create_account():
    user = session.get('user_id')

    if user is not None:
        return redirect('/dashboard')
    else:
        form = SignUpForm(data={"user_account_type":"SP"})
        if form.validate_on_submit():
            query = """
                INSERT INTO `User`(`user_id`, `user_password`, `user_account_type`, `user_rating`, `user_level`, `user_is_trusted`)
                VALUES(%s, %s, %s, 0, 1, false)
                """
            data = (
                form.user_id.data,
                form.user_password.data,
                form.user_account_type.data
                )
            session['user_id'] = form.user_id.data          

            conn = db.connect()
            cursor = conn.cursor()
            cursor.execute(query, data)
            cursor.close()
            conn.commit()
            conn.close()
            return redirect('/service-provider/fill-up')
        else:
            return render_template('service_provider/create_account.html', form=form)

@main.route('/client/fill-up', methods=["POST", "GET"])
def client_fill_up():
    user = session.get('user_id')

    if user is None:
        return redirect('/sign-in')
    else:
        form = ClientFillUpForm()
        if form.validate_on_submit():
            query = """
                UPDATE `User` 
                SET `user_first_name` = %s,
                    `user_middle_name` = %s,
                    `user_last_name` = %s,
                    `user_birthdate` = %s,
                    `user_sex` = %s,
                    `user_phone_number` = %s,
                    `user_address_country` = %s,
                    `user_address_province` = %s,
                    `user_address_city` = %s,
                    `user_address_barangay` = %s,
                    `user_address_street` = %s,
                    `user_address_zip_code` = %s,
                    `user_education` = %s
                WHERE `user_id` = %s
                """
            data = (                    
                    form.user_first_name.data,
                    form.user_middle_name.data,
                    form.user_last_name.data,
                    form.user_birthdate.data,
                    form.user_sex.data,
                    form.user_contact_number.data,
                    form.user_address_country.data,
                    form.user_address_province.data,
                    form.user_address_city.data,
                    form.user_address_barangay.data,
                    form.user_address_street.data,
                    form.user_zip_code.data,
                    form.user_education.data,
                    user,
                    )
            conn = db.connect()
            cursor = conn.cursor()
            cursor.execute(query, data)
            cursor.close()
            conn.commit()
            conn.close()
            return redirect('/dashboard')
        else:    
            return render_template('client/fill_up.html', form=form)

@main.route('/service-provider/fill-up', methods=["POST", "GET"])
def service_provider_fill_up():
    user = session.get('user_id')

    if user is None:
        return redirect('/sign-in')
    else:
        form = ServiceProviderFillUpForm()
        if form.validate_on_submit():
            query = """
                UPDATE `User` 
                SET `user_first_name` = %s,
                    `user_middle_name` = %s,
                    `user_last_name` = %s,
                    `user_birthdate` = %s,
                    `user_sex` = %s,
                    `user_phone_number` = %s,
                    `user_address_country` = %s,
                    `user_address_province` = %s,
                    `user_address_city` = %s,
                    `user_address_barangay` = %s,
                    `user_address_street` = %s,
                    `user_address_zip_code` = %s,
                    `user_education` = %s
                WHERE `user_id` = %s
                """
            data = (                    
                    form.user_first_name.data,
                    form.user_middle_name.data,
                    form.user_last_name.data,
                    form.user_birthdate.data,
                    form.user_sex.data,
                    form.user_contact_number.data,
                    form.user_address_country.data,
                    form.user_address_province.data,
                    form.user_address_city.data,
                    form.user_address_barangay.data,
                    form.user_address_street.data,
                    form.user_zip_code.data,
                    form.user_education.data,
                    user,
                    )
            conn = db.connect()
            cursor = conn.cursor()
            cursor.execute(query, data)
            cursor.close()
            conn.commit()
            conn.close()
            return redirect('/dashboard')
        else:    
            return render_template('service_provider/fill_up.html', form=form)

@main.route('/dashboard')
def dashboard():
    user = session.get('user_id')

    if user is None:
        return redirect('/sign-in')
    elif user_is_client(user):
        return render_template('client/dashboard.html')
    elif user_is_service_provider(user):
        return render_template('service_provider/dashboard.html')

@main.route('/explore-services')
def explore_services():
    user = session.get('user_id')

    if user is None:
        return redirect('/sign-in')
    elif user_is_client(user):
        return render_template(
            'client/explore_services.html',
            services=all_service_posts(),
            featured_service_categories=featured_service_categories(),
            featured_service_providers=featured_service_providers(),
            featured_service_posts=featured_service_posts()
        )
    elif user_is_service_provider(user):
         return render_template(
            'service_provider/explore_services.html',
            services=all_service_posts(),
            featured_service_categories=featured_service_categories(),
            featured_service_providers=featured_service_providers(),
            featured_service_posts=featured_service_posts()
         )

@main.route('/profile', methods=['GET'])
def profile():
    user = session.get('user_id')

    if user is None:
        return redirect('/sign-in')
    elif user_is_client(user):
        user_info = get_user_info(user)
        return render_template(
            'client/profile.html', user_info=user_info
        )
    elif user_is_service_provider(user):
        user_info = get_user_info(user)
        return render_template(
            'service_provider/profile.html', user_info=user_info
        )
 
@main.route('/edit-profile', methods=['GET', 'POST'])
def edit_profile():
    user = session.get('user_id')

    if user is None:
        return redirect('/sign-in')
    elif user_is_client(user):
        user_info = get_user_info(user)
        form = ClientEditForm(data=user_info)
        if form.validate_on_submit():
            query = """
                UPDATE `User` 
                SET `user_first_name` = %s,
                    `user_middle_name` = %s,
                    `user_last_name` = %s,
                    `user_birthdate` = %s,
                    `user_sex` = %s,
                    `user_phone_number` = %s,
                    `user_address_country` = %s,
                    `user_address_province` = %s,
                    `user_address_city` = %s,
                    `user_address_barangay` = %s,
                    `user_address_street` = %s,
                    `user_address_zip_code` = %s,
                    `user_education` = %s,
                    `user_profile_description` = %s
                WHERE `user_id` = %s
                """
            data = (                    
                    form.user_first_name.data,
                    form.user_middle_name.data,
                    form.user_last_name.data,
                    form.user_birthdate.data,
                    form.user_sex.data,
                    form.user_contact_number.data,
                    form.user_address_country.data,
                    form.user_address_province.data,
                    form.user_address_city.data,
                    form.user_address_barangay.data,
                    form.user_address_street.data,
                    form.user_zip_code.data,
                    form.user_education.data,
                    form.user_profile_description.data,
                    user,
                    )
            conn = db.connect()
            cursor = conn.cursor()
            cursor.execute(query, data)
            cursor.close()
            conn.commit()
            conn.close()
            return redirect('/profile')
        return render_template(
            'client/edit_profile.html', form=form
        )
    elif user_is_service_provider(user):
        user_info = get_user_info(user)
        form = ServiceProviderEditForm(data=user_info)
        if form.validate_on_submit():
            query = """
                UPDATE `User` 
                SET `user_first_name` = %s,
                    `user_middle_name` = %s,
                    `user_last_name` = %s,
                    `user_birthdate` = %s,
                    `user_sex` = %s,
                    `user_phone_number` = %s,
                    `user_address_country` = %s,
                    `user_address_province` = %s,
                    `user_address_city` = %s,
                    `user_address_barangay` = %s,
                    `user_address_street` = %s,
                    `user_address_zip_code` = %s,
                    `user_education` = %s,
                    `user_profile_description` = %s
                WHERE `user_id` = %s
                """
            data = (                    
                    form.user_first_name.data,
                    form.user_middle_name.data,
                    form.user_last_name.data,
                    form.user_birthdate.data,
                    form.user_sex.data,
                    form.user_contact_number.data,
                    form.user_address_country.data,
                    form.user_address_province.data,
                    form.user_address_city.data,
                    form.user_address_barangay.data,
                    form.user_address_street.data,
                    form.user_zip_code.data,
                    form.user_education.data,
                    form.user_profile_description.data,
                    user,
                    )
            conn = db.connect()
            cursor = conn.cursor()
            cursor.execute(query, data)
            cursor.close()
            conn.commit()
            conn.close()
            return redirect('/profile')
        else:
            return render_template(
                'service_provider/edit_profile.html', form=form
            )

@main.route('/users/<string:user_id>', methods=['GET'])
def user(user_id):
    user = user_id

    if user is None:
        return redirect('/sign-in')
    elif user_is_client(user):
        user_info = get_user_info(user)
        return render_template(
            'client/user.html', user_info=user_info
        )
    elif user_is_service_provider(user):
        user_info = get_user_info(user)
        return render_template(
            'service_provider/user.html', user_info=user_info
        )

@main.route('/my-requests', methods = ['POST', 'GET'])
def myrequests():
    user = session.get('user_id')

    if user is None:
        return redirect('/sign-in')
    elif user_is_client(user):
        form = RequestPostAddForm()
        form.request_post_service_type.choices += all_service_types()
        if form.validate_on_submit():
            query = """
                INSERT INTO `RequestPost` (`request_post_title`, `request_post_description`, `request_post_user`, `request_post_date_posted`, `request_post_schedule`, `request_post_location`, `request_post_service_type`, `request_post_amount`)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """
            data = (                    
                    form.request_post_title.data,
                    form.request_post_description.data,
                    user,
                    datetime.now().strftime('%Y-%m-%d'),
                    form.request_post_schedule.data,
                    form.request_post_location.data,
                    form.request_post_service_type.data,
                    form.request_post_amount.data,
                    )
            conn = db.connect()
            cursor = conn.cursor()
            cursor.execute(query, data)
            cursor.close()
            conn.commit()
            conn.close()
            flash('Request posted successfully!', 'success')
            return redirect('/my-requests')

        else:
            return render_template(
                'client/my_requests.html',
                requests = all_user_request_post(user),
                form = form
            )

    elif user_is_service_provider(user):
        form = RequestPostAddForm()
        form.request_post_service_type.choices += all_service_types()
        if form.validate_on_submit():
            query = """
                INSERT INTO `RequestPost` (`request_post_title`, `request_post_description`, `request_post_user`, `request_post_date_posted`, `request_post_schedule`, `request_post_location`, `request_post_service_type`, `request_post_amount`)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """
            data = (                    
                    form.request_post_title.data,
                    form.request_post_description.data,
                    user,
                    datetime.now().strftime('%Y-%m-%d'),
                    form.request_post_schedule.data,
                    form.request_post_location.data,
                    form.request_post_service_type.data,
                    form.request_post_amount.data,
                    )
            conn = db.connect()
            cursor = conn.cursor()
            cursor.execute(query, data)
            cursor.close()
            conn.commit()
            conn.close()
            flash('Request posted successfully!', 'success')
            return redirect('/my-requests')

        else:
            return render_template(
                'service_provider/my_requests.html',
                requests = all_user_request_post(user),
                form = form
            )

@main.route('/delete-request-post/<request_post_id>')
def delete_request_post(request_post_id):
    conn = db.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute('DELETE FROM `RequestPost` WHERE `request_post_id` = %s', (request_post_id))  
    conn.commit()
    cursor.close()
    conn.close()
    flash('Request post was removed successfully!', 'success')
    return redirect("/my-requests")

@main.route('/edit-request-post/<request_post_id>', methods=['POST', 'GET'])
def edit_request_post(request_post_id):
    user = session.get('user_id')

    conn = db.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute('SELECT * FROM `RequestPost` WHERE `request_post_id` = %s', (request_post_id))
    request_post_info = cursor.fetchone()
    cursor.close()
    conn.close()

    if user is None:
        return redirect('/sign-in')
    elif user_is_client(user):
        form = RequestPostEditForm(data=request_post_info)
        form.request_post_service_type.choices += all_service_types()
        if form.validate_on_submit():
            query = """
                UPDATE `RequestPost` 
                SET `request_post_title` = %s,
                    `request_post_description` = %s,
                    `request_post_schedule` = %s,
                    `request_post_location` = %s,
                    `request_post_service_type` = %s,
                    `request_post_amount` = %s
                WHERE `request_post_id` = %s
                """
            data = (                    
                    form.request_post_title.data,
                    form.request_post_description.data,
                    form.request_post_schedule.data,
                    form.request_post_location.data,
                    form.request_post_service_type.data,
                    form.request_post_amount.data,
                    request_post_info["request_post_id"]
                    )
            conn = db.connect()
            cursor = conn.cursor()
            cursor.execute(query, data)
            cursor.close()
            conn.commit()
            conn.close()
            flash('Request updated successfully!', 'success')
            return redirect('/my-requests')
        return render_template(
            'client/edit_request_post.html',
            form=form,
            request_post_id=request_post_info["request_post_id"]
        )
    elif user_is_service_provider(user):
        form = RequestPostEditForm(data=request_post_info)
        form.request_post_service_type.choices += all_service_types()
        if form.validate_on_submit():
            query = """
                UPDATE `RequestPost` 
                SET `request_post_title` = %s,
                    `request_post_description` = %s,
                    `request_post_schedule` = %s,
                    `request_post_location` = %s,
                    `request_post_service_type` = %s,
                    `request_post_amount` = %s
                WHERE `request_post_id` = %s
                """
            data = (                    
                    form.request_post_title.data,
                    form.request_post_description.data,
                    form.request_post_schedule.data,
                    form.request_post_location.data,
                    form.request_post_service_type.data,
                    form.request_post_amount.data,
                    request_post_info["request_post_id"]
                    )
            conn = db.connect()
            cursor = conn.cursor()
            cursor.execute(query, data)
            cursor.close()
            conn.commit()
            conn.close()
            flash('Request updated successfully!', 'success')
            return redirect('/my-requests')
        return render_template(
            'service_provider/edit_request_post.html',
            form=form,
            request_post_id=request_post_info["request_post_id"]
        )

@main.route('/my-services', methods = ['POST', 'GET'])
def myservices():
    user = session.get('user_id')

    if user is None:
        return redirect('/sign-in')
    elif user_is_client(user):
        return None
    elif user_is_service_provider(user):
        form = ServicePostAddForm()
        form.service_post_service_type.choices += all_service_types()
        if form.validate_on_submit():
            query = """
                INSERT INTO `ServicePost` (`service_post_title`, `service_post_description`, `service_post_user`, `service_post_date_posted`, `service_post_schedule`, `service_post_location`, `service_post_service_type`, `service_post_amount`)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """
            data = (                    
                    form.service_post_title.data,
                    form.service_post_description.data,
                    user,
                    datetime.now().strftime('%Y-%m-%d'),
                    form.service_post_schedule.data,
                    form.service_post_location.data,
                    form.service_post_service_type.data,
                    form.service_post_amount.data,
                    )
            conn = db.connect()
            cursor = conn.cursor()
            cursor.execute(query, data)
            cursor.close()
            conn.commit()
            conn.close()
            flash('Service posted successfully!', 'success')
            return redirect('/my-services')

        else:
            return render_template(
                'service_provider/my_services.html',
                services = all_user_service_post(user),
                form = form
            )

@main.route('/delete-service-post/<service_post_id>')
def delete_service_post(service_post_id):
    conn = db.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute('DELETE FROM `ServicePost` WHERE `service_post_id` = %s', (service_post_id))  
    conn.commit()
    cursor.close()
    conn.close()
    flash('Service post was removed successfully!', 'success')
    return redirect("/my-services")

@main.route('/edit-service-post/<service_post_id>', methods=['POST', 'GET'])
def edit_service_post(service_post_id):
    user = session.get('user_id')

    conn = db.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute('SELECT * FROM `ServicePost` WHERE `service_post_id` = %s', (service_post_id))
    service_post_info = cursor.fetchone()
    cursor.close()
    conn.close()

    if user is None:
        return redirect('/sign-in')
    elif user_is_client(user):
        return None
    elif user_is_service_provider(user):
        form = ServicePostEditForm(data=service_post_info)
        form.service_post_service_type.choices += all_service_types()
        if form.validate_on_submit():
            query = """
                UPDATE `ServicePost` 
                SET `service_post_title` = %s,
                    `service_post_description` = %s,
                    `service_post_schedule` = %s,
                    `service_post_location` = %s,
                    `service_post_service_type` = %s,
                    `service_post_amount` = %s
                WHERE `service_post_id` = %s
                """
            data = (                    
                    form.service_post_title.data,
                    form.service_post_description.data,
                    form.service_post_schedule.data,
                    form.service_post_location.data,
                    form.service_post_service_type.data,
                    form.service_post_amount.data,
                    service_post_info["service_post_id"]
                    )
            conn = db.connect()
            cursor = conn.cursor()
            cursor.execute(query, data)
            cursor.close()
            conn.commit()
            conn.close()
            flash('Service updated successfully!', 'success')
            return redirect('/my-services')
        return render_template(
            'service_provider/edit_service_post.html',
            form=form,
            service_post_id=service_post_info["service_post_id"]
        )

@main.route('/home-search-jobs')
def home_search_job():
    return render_template('home_search_jobs.html', requests=all_request_posts())

@main.route('/home-search-services')
def home_search_service():
    return render_template('home_search_services.html', services=all_service_posts())

@main.route('/service-post/<service_post_id>')
def service_post(service_post_id):
    user = session.get('user_id')

    if user is None:
        return redirect('/sign-in')
    elif user_is_client(user):
        service_post_info = get_service_post_info(service_post_id)
        return render_template('client/service_post.html', service_post_info=service_post_info)
    elif user_is_service_provider(user):
        service_post_info = get_service_post_info(service_post_id)
        return render_template('service_provider/service_post.html', service_post_info=service_post_info)

@main.route('/request-post/<request_post_id>')
def request_post(request_post_id):
    user = session.get('user_id')
    
    if user is None:
        return redirect('/sign-in')
    elif user_is_client(user):
        return redirect('/service-provider/create-account')
    elif user_is_service_provider(user):
        request_post_info = get_request_post_info(request_post_id)
        return render_template('service_provider/request_post.html', request_post_info=request_post_info)

@main.route('/apply/<request_post_id>', methods=['POST', 'GET'])
def apply(request_post_id):
    user = session.get('user_id')

    client = get_request_post_user(request_post_id)
    service_provider = user

    if user is None:
        return redirect('/sign-in')
    elif user_is_client(user):
        return redirect('/service-provider/create-account')
    elif user_is_service_provider(user):
        job = get_job_via_service_provider_and_request_post(service_provider, request_post_id)
        if job:
            return redirect(f"/application/{job['job_id']}")
        else:
            conn = db.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute("""
                SELECT `user_first_name` AS `applicant_first_name`,
                    `user_middle_name` AS `applicant_middle_name`,
                    `user_last_name` AS `applicant_last_name`,
                    `user_email_address` AS `applicant_email_address`,
                    `user_phone_number` AS `applicant_contact_number`,
                    `user_address_city` AS `applicant_current_address`,
                    `user_education` AS `applicant_education`
                FROM `User`
                WHERE `user_id` = %s
                """, (user,))
            applicant_info = cursor.fetchone()
            cursor.close()
            conn.close()

            form = ApplicationForm(data=applicant_info)
            
            if form.validate_on_submit():
                query = """
                    INSERT INTO `Job` (
                        `job_application_applicant_first_name`,
                        `job_application_applicant_middle_name`,
                        `job_application_applicant_last_name`,
                        `job_application_applicant_email_address`,
                        `job_application_applicant_contact_number`,
                        `job_application_applicant_current_address`,
                        `job_application_applicant_resume`,
                        `job_application_applicant_cover_letter`,
                        `job_application_applicant_education`,
                        `job_application_applicant_years_experience`,
                        `job_status`,
                        `job_request_post`,
                        `job_client`,
                        `job_service_provider`
                        )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """

                data = (                    
                        form.applicant_first_name.data,
                        form.applicant_middle_name.data,
                        form.applicant_last_name.data,
                        form.applicant_email_address.data,
                        form.applicant_contact_number.data,
                        form.applicant_current_address.data,
                        form.applicant_resume.data,
                        form.applicant_cover_letter.data,
                        form.applicant_education.data,
                        form.applicant_years_experience.data,
                        'Pending',
                        request_post_id,
                        client,
                        service_provider
                        )
                conn = db.connect()
                cursor = conn.cursor()
                cursor.execute(query, data)
                cursor.close()
                conn.commit()
                conn.close()

                resume = form.applicant_resume.data
                cover = form.applicant_cover_letter.data

                job_id = get_job_via_service_provider_and_request_post(service_provider, request_post_id)['job_id']

                if resume:
                    resume.save(os.path.join(current_app.config['UPLOAD_PATH'], 'applications', f"resume_{job_id}.pdf"))
                if cover:
                    cover.save(os.path.join(current_app.config['UPLOAD_PATH'], 'applications', f"cover_{job_id}.pdf"))
                
                flash('Application added!', 'success')
                return redirect('/my-status/applying')
            else:
                return render_template('service_provider/apply_job.html', form=form, request_post_id=request_post_id)

@main.route('/application/<job_id>')
def application(job_id):
    user = session.get('user_id')
    if user is None:
        return redirect('/sign-in')
    elif user_is_client(user):
        return redirect('/service-provider/create-account')
    elif user_is_service_provider(user):
        if user == get_job_client(job_id) or user == get_job_service_provider(job_id):
            return render_template('service_provider/application.html',
                                   job_info=get_job_info(job_id))
        else:
            return redirect("/not-available")

@main.route('/resume/<filename>')
def resume(filename):
    upload_path = current_app.config['UPLOAD_PATH']
    return send_file(f'{upload_path}\\applications\\{filename}', attachment_filename=filename)

@main.route('/cover_letter/<filename>')
def cover_letter(filename):
    upload_path = current_app.config['UPLOAD_PATH']
    return send_file(f'{upload_path}\\applications\\{filename}', attachment_filename=filename)

@main.route('/my-status')
@main.route('/my-status/hiring')
def my_status_hiring():
    user = session.get('user_id')
    if user is None:
        return redirect('/sign-in')
    elif user_is_client(user):
        return render_template('client/my_status_hiring.html',
                                pending_jobs=all_client_jobs(user, 'Pending'),
                                active_jobs=all_client_jobs(user, 'Active'),
                                completed_jobs=all_client_jobs(user, 'Completed'),
                                declined_jobs=all_client_jobs(user, 'Declined'))
    elif user_is_service_provider(user):
        return render_template('service_provider/my_status_hiring.html',
                                pending_jobs=all_client_jobs(user, 'Pending'),
                                active_jobs=all_client_jobs(user, 'Active'),
                                completed_jobs=all_client_jobs(user, 'Completed'),
                                declined_jobs=all_client_jobs(user, 'Declined'))

@main.route('/my-status/applying')
def my_status_applying():
    user = session.get('user_id')
    if user is None:
        return redirect('/sign-in')
    elif user_is_client(user):
        return redirect('/service-provider/create-account')
    elif user_is_service_provider(user):
        return render_template('service_provider/my_status_applying.html',
                                pending_jobs=all_service_provider_jobs(user, 'Pending'),
                                active_jobs=all_service_provider_jobs(user, 'Active'),
                                completed_jobs=all_service_provider_jobs(user, 'Completed'),
                                declined_jobs=all_service_provider_jobs(user, 'Declined'))

@main.route('/delete-job-application/<job_id>')
def delete_job_application(job_id):
    user = session.get('user_id')
    if user is None:
        return redirect('/sign-in')
    elif user_is_client(user):
        return redirect('/service-provider/create-account')
    elif user_is_service_provider(user):
        if user == get_job_service_provider(job_id):
            conn = db.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute('DELETE FROM `Job` WHERE `job_id` = %s', (job_id))  
            conn.commit()
            cursor.close()
            conn.close()
            flash('Your job application is cancelled!', 'success')
            return redirect("/my-status")
        else:
            return redirect("/not-available")

@main.route('/accept-job-application/<job_id>')
def accept_job_application(job_id):
    user = session.get('user_id')
    if user is None:
        return redirect('/sign-in')
    else:
        client = get_job_client(job_id)
        if user == client:
            conn = db.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute("UPDATE `Job` SET `job_status` = 'Active' WHERE `job_id` = %s", (job_id))
            conn.commit()
            cursor.close()
            conn.close()
            flash('The job application is accepted.', 'success')
            return redirect("/my-status/hiring")
        else:
            return redirect("/not-available")

@main.route('/decline-job-application/<job_id>')
def decline_job_application(job_id):
    user = session.get('user_id')
    if user is None:
        return redirect('/sign-in')
    else:
        client = get_job_client(job_id)
        if user == client:
            conn = db.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute("UPDATE `Job` SET `job_status` = 'Declined' WHERE `job_id` = %s", (job_id))
            conn.commit()
            cursor.close()
            conn.close()
            flash('The job application is declined.', 'success')
            return redirect("/my-status/hiring")
        else:
            return redirect("/not-available")

@main.route('/complete-job-application/<job_id>')
def complete_job_application(job_id):
    user = session.get('user_id')
    if user is None:
        return redirect('/sign-in')
    else:
        client = get_job_client(job_id)
        if user == client:
            conn = db.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute("UPDATE `Job` SET `job_status` = 'Completed' WHERE `job_id` = %s", (job_id))
            conn.commit()
            cursor.close()
            conn.close()
            flash('The job application is completed.', 'success')
            return redirect("/my-status/hiring")
        else:
            return redirect("/not-available")