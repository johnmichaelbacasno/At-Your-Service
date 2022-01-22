CREATE DATABASE `AYS`;

USE `AYS`;

CREATE TABLE `User`
(
    `user_id` VARCHAR(100) NOT NULL,
    `user_password` VARCHAR(100) NOT NULL,
    `user_account_type` VARCHAR(2) NOT NULL, -- "C", "SP"
    
    `user_rating` FLOAT(3, 2) NOT NULL,
    `user_level` INT NOT NULL,
    `user_is_trusted` BOOLEAN NOT NULL,

    `user_first_name` VARCHAR(255) NULL,
    `user_middle_name` VARCHAR(255) NULL,
    `user_last_name` VARCHAR(255) NULL,
    `user_address_zip_code` VARCHAR(10) NULL,
    `user_address_street` VARCHAR(255) NULL,
    `user_address_barangay` VARCHAR(255) NULL,
    `user_address_city` VARCHAR(100) NULL,
    `user_address_province` VARCHAR(100) NULL,
    `user_address_country` VARCHAR(100) NULL,
    `user_profile_description` TEXT NULL,
    `user_profile_picture` VARCHAR(255) NULL,
    `user_sex` CHAR(1) NULL, -- "M", "F"
    `user_education` VARCHAR(255) NULL,
    `user_birthdate` DATE NULL,

    `user_email_address` VARCHAR(100) NULL,
    `user_phone_number` VARCHAR(15) NULL,

    PRIMARY KEY (`user_id`)
);

CREATE TABLE `ServiceCategory`
(
    `service_category_id` INT NOT NULL AUTO_INCREMENT,
    `service_category_name` VARCHAR(100) NOT NULL,

    PRIMARY KEY (`service_category_id`)
);

CREATE TABLE `ServiceType`
(
    `service_type_id` INT NOT NULL AUTO_INCREMENT,
    `service_type_name` VARCHAR(100) NOT NULL,
    `service_category` INT NOT NULL,

    PRIMARY KEY (`service_type_id`),
    FOREIGN KEY (`service_category`) REFERENCES `ServiceCategory` (`service_category_id`)
);

CREATE TABLE `ServicePost`
(
    `service_post_id` INT NOT NULL AUTO_INCREMENT,
    `service_post_title` VARCHAR(100) NOT NULL,
    `service_post_description` TEXT NOT NULL,
    `service_post_user` VARCHAR(100) NOT NULL,
    `service_post_date_posted` DATE NOT NULL,
    `service_post_schedule` DATE NOT NULL,
    `service_post_location` VARCHAR(100) NOT NULL,
    `service_post_service_type` INT NOT NULL,
    `service_post_amount` FLOAT(20, 2) NOT NULL,

    PRIMARY KEY (`service_post_id`),
    FOREIGN KEY (`service_post_user`) REFERENCES `User` (`user_id`),
    FOREIGN KEY (`service_post_service_type`) REFERENCES `ServiceType` (`service_type_id`)
);

CREATE TABLE `RequestPost`
(
    `request_post_id` INT NOT NULL AUTO_INCREMENT,
    `request_post_status` VARCHAR(10) NOT NULL, -- "Open", "Closed"
    `request_post_title` VARCHAR(100) NOT NULL,
    `request_post_description` TEXT NOT NULL,
    `request_post_user` VARCHAR(100) NOT NULL,
    `request_post_date_posted` DATE NOT NULL,
    `request_post_schedule` DATE NOT NULL,
    `request_post_location` VARCHAR(100) NOT NULL,
    `request_post_service_type` INT NOT NULL,
    `request_post_amount` FLOAT(20, 2) NOT NULL,
    
    PRIMARY KEY (`request_post_id`),
    FOREIGN KEY (`request_post_user`) REFERENCES `User` (`user_id`),
    FOREIGN KEY (`request_post_service_type`) REFERENCES `ServiceType` (`service_type_id`)
);

CREATE TABLE `ServiceBook`
(
    `service_book_id` INT NOT NULL AUTO_INCREMENT,
    `service_book_status` VARCHAR(10) NOT NULL, -- "Pending", "Ongoing", "Cancelled", "Completed"
    `service_book_service_post` INT NULL,
    `service_book_client` VARCHAR(100) NOT NULL,
    `service_book_service_provider` VARCHAR(100) NOT NULL,
    `service_book_client_notes` TEXT NULL,
    `service_book_provider_notes` TEXT NULL,
    `service_book_start_date` DATE NULL,
    `service_book_end_date` DATE NULL,
    `service_book_payment_method` VARCHAR(10) NULL, -- "", "On Cash", "GCash", "Bank"
    
    PRIMARY KEY (`service_book_id`),
    FOREIGN KEY (`service_book_client`) REFERENCES `User` (`user_id`),
    FOREIGN KEY (`service_book_service_provider`) REFERENCES `User` (`user_id`)
);

CREATE TABLE `Job`
(
    `job_id` INT NOT NULL AUTO_INCREMENT,

    `job_application_applicant_first_name` VARCHAR(255) NOT NULL,
    `job_application_applicant_middle_name` VARCHAR(255) NOT NULL,
    `job_application_applicant_last_name` VARCHAR(255) NOT NULL,
    `job_application_applicant_email_address` VARCHAR(255) NOT NULL,
    `job_application_applicant_contact_number` VARCHAR(255) NOT NULL,
    `job_application_applicant_current_address` VARCHAR(255) NOT NULL,
    `job_application_applicant_resume` BLOB NULL,
    `job_application_applicant_cover_letter` BLOB NULL,
    `job_application_applicant_education` VARCHAR(15) NOT NULL,
    `job_application_applicant_years_experience` FLOAT(20, 2) NOT NULL,

    `job_status` VARCHAR(10) NOT NULL, -- "Declined", "Pending", "Active", "Completed"
    `job_request_post` INT NOT NULL,
    `job_client` VARCHAR(100) NOT NULL,
    `job_service_provider` VARCHAR(100) NOT NULL,
    `job_client_notes` TEXT NULL,
    `job_service_provider_notes` TEXT NULL,
    `job_start_date` DATE NULL,
    `job_end_date` DATE NULL,

    PRIMARY KEY (`job_id`),
    FOREIGN KEY (`job_request_post`) REFERENCES `RequestPost` (`request_post_id`),
    FOREIGN KEY (`job_client`) REFERENCES `User` (`user_id`),
    FOREIGN KEY (`job_service_provider`) REFERENCES `User` (`user_id`)
);