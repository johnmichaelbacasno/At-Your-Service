import pymysql

from extensions import db

def user_id_exists(user_id):
    conn = db.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT * FROM `User` where `user_id`=%s", (user_id,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return bool(user)

def user_is_client(user_id):
    conn = db.connect()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT `user_account_type` FROM `User`
        WHERE user_id = %s
        """,
        (user_id,))
    account_type = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return account_type == 'C'

def user_is_service_provider(user_id):
    conn = db.connect()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT `user_account_type` FROM `User`
        WHERE user_id = %s
        """,
        (user_id,))
    account_type = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return account_type == 'SP'

def get_user_password(user_id):
    conn = db.connect()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT `user_password` FROM `User`
        WHERE user_id = %s
        """,
        (user_id,))
    password = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return password

def all_clients():
    conn = db.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("""
        SELECT * FROM `User` WHERE `user_account_type` = 'C'
        """)
    all_clients = cursor.fetchall()
    cursor.close()
    conn.close()
    return all_clients

def all_service_providers():
    conn = db.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("""
        SELECT * FROM `User` WHERE `user_account_type` = 'SP'
        """)
    all_service_providers = cursor.fetchall()
    cursor.close()
    conn.close()
    return all_service_providers

def all_service_categories():
    conn = db.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("""
        SELECT * FROM `ServiceCategory`
        """)
    all_service_categories = cursor.fetchall()
    cursor.close()
    conn.close()
    return all_service_categories

def all_service_posts():
    conn = db.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("""
        SELECT ServicePost.service_post_id,
               ServicePost.service_post_title,
               ServicePost.service_post_description,
               User.user_id AS service_post_user_id,
               User.user_first_name AS service_post_user_first_name,
               User.user_middle_name AS service_post_user_middle_name,
               User.user_last_name AS service_post_user_last_name,
               User.user_rating AS service_post_user_rating,
               User.user_level as service_post_user_level,
               User.user_is_trusted AS service_post_user_is_trusted,
               ServicePost.service_post_date_posted,
               ServicePost.service_post_schedule,
               ServicePost.service_post_location,
               ServicePost.service_post_service_type AS service_post_service_type_id,
               ServiceType.service_type_name AS service_post_service_type_name,
               ServiceCategory.service_category_id AS service_post_service_category_id,
               ServiceCategory.service_category_name AS service_post_service_category_name,
               ServicePost.service_post_amount
        FROM `ServicePost`
        JOIN `User` ON ServicePost.service_post_user = User.user_id
        JOIN `ServiceType` ON ServicePost.service_post_service_type = ServiceType.service_type_id
        JOIN `ServiceCategory` ON ServiceType.service_category = ServiceCategory.service_category_id
        """)
    all_service_posts = cursor.fetchall()
    cursor.close()
    conn.close()
    return all_service_posts

def featured_clients():
    conn = db.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("""
        SELECT * FROM `User` WHERE `user_account_type` = 'C'
        ORDER BY user_rating DESC
        LIMIT 6
        """)
    featured_clients = cursor.fetchall()
    cursor.close()
    conn.close()
    return featured_clients

def featured_service_providers():
    conn = db.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("""
        SELECT * FROM `User` WHERE `user_account_type` = 'SP'
        ORDER BY user_rating DESC
        LIMIT 6
        """)
    featured_providers = cursor.fetchall()
    cursor.close()
    conn.close()
    return featured_providers

def featured_service_categories():
    conn = db.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("""
        SELECT * FROM `ServiceCategory`
        LIMIT 6
        """)
    featured_service_categories = cursor.fetchall()
    cursor.close()
    conn.close()
    return featured_service_categories

def featured_service_posts():
    conn = db.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("""
        SELECT ServicePost.service_post_id,
               ServicePost.service_post_title,
               ServicePost.service_post_description,
               User.user_id AS service_post_user_id,
               User.user_first_name AS service_post_user_first_name,
               User.user_middle_name AS service_post_user_middle_name,
               User.user_last_name AS service_post_user_last_name,
               User.user_rating AS service_post_user_rating,
               User.user_level as service_post_user_level,
               User.user_is_trusted AS service_post_user_is_trusted,
               ServicePost.service_post_date_posted,
               ServicePost.service_post_schedule,
               ServicePost.service_post_location,
               ServicePost.service_post_service_type AS service_post_service_type_id,
               ServiceType.service_type_name AS service_post_service_type_name,
               ServiceCategory.service_category_id AS service_post_service_category_id,
               ServiceCategory.service_category_name AS service_post_service_category_name,
               ServicePost.service_post_amount
        FROM `ServicePost`
        JOIN `User` ON ServicePost.service_post_user = User.user_id
        JOIN `ServiceType` ON ServicePost.service_post_service_type = ServiceType.service_type_id
        JOIN `ServiceCategory` ON ServiceType.service_category = ServiceCategory.service_category_id
        ORDER BY service_post_user_rating DESC
        LIMIT 3;
        """)
    featured_service_posts = cursor.fetchall()
    cursor.close()
    conn.close()
    return featured_service_posts

def get_user_info(user):
    conn = db.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT * FROM `User` where `user_id`=%s", (user,))
    user_info = cursor.fetchone()
    cursor.close()
    conn.close()
    return user_info

def all_user_request_post(user_id):
    conn = db.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("""
        SELECT RequestPost.request_post_id,
               RequestPost.request_post_title,
               RequestPost.request_post_description,
               User.user_id AS request_post_user_id,
               User.user_first_name AS request_post_user_first_name,
               User.user_middle_name AS request_post_user_middle_name,
               User.user_last_name AS request_post_user_last_name,
               User.user_rating AS request_post_user_rating,
               User.user_level as request_post_user_level,
               User.user_is_trusted AS request_post_user_is_trusted,
               RequestPost.request_post_date_posted,
               RequestPost.request_post_schedule,
               RequestPost.request_post_location,
               RequestPost.request_post_service_type AS request_post_service_type_id,
               ServiceType.service_type_name AS request_post_service_type_name,
               ServiceCategory.service_category_id AS request_post_service_category_id,
               ServiceCategory.service_category_name AS request_post_service_category_name,
               RequestPost.request_post_amount
        FROM `RequestPost`
        JOIN `User` ON RequestPost.request_post_user = User.user_id
        JOIN `ServiceType` ON RequestPost.request_post_service_type = ServiceType.service_type_id
        JOIN `ServiceCategory` ON ServiceType.service_category = ServiceCategory.service_category_id

        WHERE User.user_id = %s
        """, (user_id), )
    all_request_posts = cursor.fetchall()
    cursor.close()
    conn.close()
    return all_request_posts

def all_service_types():
    conn = db.connect()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT `service_type_id`, `service_type_name` FROM `ServiceType`
        """)
    all_service_types = cursor.fetchall()
    cursor.close()
    conn.close()
    return all_service_types

def all_user_service_post(user_id):
    conn = db.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("""
        SELECT ServicePost.service_post_id,
               ServicePost.service_post_title,
               ServicePost.service_post_description,
               User.user_id AS service_post_user_id,
               User.user_first_name AS service_post_user_first_name,
               User.user_middle_name AS service_post_user_middle_name,
               User.user_last_name AS service_post_user_last_name,
               User.user_rating AS service_post_user_rating,
               User.user_level as service_post_user_level,
               User.user_is_trusted AS service_post_user_is_trusted,
               ServicePost.service_post_date_posted,
               ServicePost.service_post_schedule,
               ServicePost.service_post_location,
               ServicePost.service_post_service_type AS service_post_service_type_id,
               ServiceType.service_type_name AS service_post_service_type_name,
               ServiceCategory.service_category_id AS service_post_service_category_id,
               ServiceCategory.service_category_name AS service_post_service_category_name,
               ServicePost.service_post_amount
        FROM `ServicePost`
        JOIN `User` ON ServicePost.service_post_user = User.user_id
        JOIN `ServiceType` ON ServicePost.service_post_service_type = ServiceType.service_type_id
        JOIN `ServiceCategory` ON ServiceType.service_category = ServiceCategory.service_category_id

        WHERE User.user_id = %s
        """, (user_id), )
    all_service_posts = cursor.fetchall()
    cursor.close()
    conn.close()
    return all_service_posts

def all_service_posts():
    conn = db.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("""
        SELECT ServicePost.service_post_id,
               ServicePost.service_post_title,
               ServicePost.service_post_description,
               User.user_id AS service_post_user_id,
               User.user_first_name AS service_post_user_first_name,
               User.user_middle_name AS service_post_user_middle_name,
               User.user_last_name AS service_post_user_last_name,
               User.user_rating AS service_post_user_rating,
               User.user_level as service_post_user_level,
               User.user_is_trusted AS service_post_user_is_trusted,
               ServicePost.service_post_date_posted,
               ServicePost.service_post_schedule,
               ServicePost.service_post_location,
               ServicePost.service_post_service_type AS service_post_service_type_id,
               ServiceType.service_type_name AS service_post_service_type_name,
               ServiceCategory.service_category_id AS service_post_service_category_id,
               ServiceCategory.service_category_name AS service_post_service_category_name,
               ServicePost.service_post_amount
        FROM `ServicePost`
        JOIN `User` ON ServicePost.service_post_user = User.user_id
        JOIN `ServiceType` ON ServicePost.service_post_service_type = ServiceType.service_type_id
        JOIN `ServiceCategory` ON ServiceType.service_category = ServiceCategory.service_category_id
        """)
    all_service_posts = cursor.fetchall()
    cursor.close()
    conn.close()
    return all_service_posts

def all_request_posts():
    conn = db.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("""
        SELECT RequestPost.request_post_id,
               RequestPost.request_post_title,
               RequestPost.request_post_description,
               User.user_id AS request_post_user_id,
               User.user_first_name AS request_post_user_first_name,
               User.user_middle_name AS request_post_user_middle_name,
               User.user_last_name AS request_post_user_last_name,
               User.user_rating AS request_post_user_rating,
               User.user_level as request_post_user_level,
               User.user_is_trusted AS request_post_user_is_trusted,
               User.user_address_city AS service_post_user_address_city,
               User.user_address_country AS service_post_user_address_country,
               User.user_profile_description AS service_post_user_profile_description,
               RequestPost.request_post_date_posted,
               RequestPost.request_post_schedule,
               RequestPost.request_post_location,
               RequestPost.request_post_service_type AS request_post_service_type_id,
               ServiceType.service_type_name AS request_post_service_type_name,
               ServiceCategory.service_category_id AS request_post_service_category_id,
               ServiceCategory.service_category_name AS request_post_service_category_name,
               RequestPost.request_post_amount
        FROM `RequestPost`
        JOIN `User` ON RequestPost.request_post_user = User.user_id
        JOIN `ServiceType` ON RequestPost.request_post_service_type = ServiceType.service_type_id
        JOIN `ServiceCategory` ON ServiceType.service_category = ServiceCategory.service_category_id
        """)
    all_request_posts = cursor.fetchall()
    cursor.close()
    conn.close()
    return all_request_posts

def get_service_post_info(service_post_id):
    conn = db.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("""
        SELECT ServicePost.service_post_id,
               ServicePost.service_post_title,
               ServicePost.service_post_description,
               User.user_id AS service_post_user_id,
               User.user_first_name AS service_post_user_first_name,
               User.user_middle_name AS service_post_user_middle_name,
               User.user_last_name AS service_post_user_last_name,
               User.user_rating AS service_post_user_rating,
               User.user_level as service_post_user_level,
               User.user_is_trusted AS service_post_user_is_trusted,
               User.user_address_city AS service_post_user_address_city,
               User.user_address_country AS service_post_user_address_country,
               User.user_profile_description AS service_post_user_profile_description,
               ServicePost.service_post_date_posted,
               ServicePost.service_post_schedule,
               ServicePost.service_post_location,
               ServicePost.service_post_service_type AS service_post_service_type_id,
               ServiceType.service_type_name AS service_post_service_type_name,
               ServiceCategory.service_category_id AS service_post_service_category_id,
               ServiceCategory.service_category_name AS service_post_service_category_name,
               ServicePost.service_post_amount
        FROM `ServicePost`
        JOIN `User` ON ServicePost.service_post_user = User.user_id
        JOIN `ServiceType` ON ServicePost.service_post_service_type = ServiceType.service_type_id
        JOIN `ServiceCategory` ON ServiceType.service_category = ServiceCategory.service_category_id

        WHERE ServicePost.service_post_id = %s
        """, (service_post_id), )
    service_post_info = cursor.fetchone()
    cursor.close()
    conn.close()
    return service_post_info

def get_request_post_info(request_post_id):
    conn = db.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("""
        SELECT RequestPost.request_post_id,
               RequestPost.request_post_title,
               RequestPost.request_post_description,
               User.user_id AS request_post_user_id,
               User.user_first_name AS request_post_user_first_name,
               User.user_middle_name AS request_post_user_middle_name,
               User.user_last_name AS request_post_user_last_name,
               User.user_rating AS request_post_user_rating,
               User.user_level as request_post_user_level,
               User.user_is_trusted AS request_post_user_is_trusted,
               RequestPost.request_post_date_posted,
               RequestPost.request_post_schedule,
               RequestPost.request_post_location,
               RequestPost.request_post_service_type AS request_post_service_type_id,
               ServiceType.service_type_name AS request_post_service_type_name,
               ServiceCategory.service_category_id AS request_post_service_category_id,
               ServiceCategory.service_category_name AS request_post_service_category_name,
               RequestPost.request_post_amount
        FROM `RequestPost`
        JOIN `User` ON RequestPost.request_post_user = User.user_id
        JOIN `ServiceType` ON RequestPost.request_post_service_type = ServiceType.service_type_id
        JOIN `ServiceCategory` ON ServiceType.service_category = ServiceCategory.service_category_id
        
        WHERE RequestPost.request_post_id = %s
        """, (request_post_id), )
    request_post_info = cursor.fetchone()
    cursor.close()
    conn.close()
    return request_post_info