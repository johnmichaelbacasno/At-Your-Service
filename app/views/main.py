from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from datetime import datetime

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
