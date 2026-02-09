# Secure Authentication System (Python and SQLite)

## Security Analysis

I conducted a full CIA Triad analysis (Confidentiality, Integrity, Availability) to assess the system's security,
identify trade-offs, and evaluate real-world risks.

CIA Triad Analysis:
docs/CIA_Triad_Analysis_of_a_Secure_Authentication_System.pdf

Additional documentation:
  -System design & Secure Coding Write-up:
    docs/Secure_Authentication_System_Writeup.pdf

## What the program does

This project's purpose is to demonstrate secure coding principles in practice via a locally hosted SQLite database.
The program gives users the ability to create, delete and view any information that they have entered into the
database after authentication with a username and password system. This was developed as a project to learn
more about cyber security principles and apply my current knowledge in a practical environment similar to
real-world systems, allowing me to explore common security practices such as password hashing and encryption

Sensitive user data is encrypted before being written into the database, and all user passwords are hashed
with a per-user salt before being written to the database, ensuring plaintext is never used for any sensitive
data. Parameterised queries are always used during database interactions to protect from SQL injection risks.
The system will also log any attempt to log into an account, enforcing temporary lockouts if the user has too
many failed login attempts, protecting from brute-force attacks.

This project is not intended to store real-world sensitive data, but to demonstrate an understanding of common
threats in authentication systems and how to prevent them. It is intentionally a local, non-networked application,
as it has a focus is on secure programming principles.


## Core features

- User account creation ensuring unique usernames to be used as identifiers
- Secure user authentication system using usernames and passwords
- Account lockouts after repeated failed login attempts
- Users can create user-specific data after successful account authentication
- Users can view data which only belongs to them
- Users can delete data which belongs to them
- Sensitive data is securely stored within a SQLite database
- All data is locally stored with no web or network dependencies
- A command-line interface is used for all user interactions


## File structure

- main.py
Used as the starting point for the program and controls overall program flow and user interactions.

- auth.py
Manages authentication-related logic, such as encryption of sensitive user data and password handling.

- databaseHandler.py
Contains all interactions with the SQLite database, including retrieving user information and storing login attempts.


## Security design decisions

- Password Hashing
Passwords are never stored in plaintext. As an alternative, passwords are hashed before storage
to reduce the impact of data compromise.

- Salting
Before password hashing, a unique salt is generated and combined with the password. This guarantees that
identical passwords do not produce identical hashes and helps prevent precomputed attacks.

- Encryption
Sensitive user data is encrypted before being written to the database. This is done to minimize
data exposure in the event of unauthorised database access.

- SQL Injection Prevention
Parameterised queries are used for all SQL statements, ensuring user inputs are treated exclusively as data.
This prevents attackers from altering SQL logic when being prompted to enter data.

- Attack Surface Reduction
The program is intentionally designed to focus on secure coding principles via a local non-networked system
which minimizes exposure.

- Login Attempt Logging / Lockouts
All attempts at authentication are logged and after repeated failures, temporary lockouts are enforced.
This is done to reduce the impact of brute-force attacks whilst retaining usability.

- Timing-Based Attack Prevention
Care is taken during authentication, ensuring that timing differences during credential comparison does not
leak information. This greatly reduces the risk of timing-based attacks.


## Database design

This program uses a locally stored SQLite database to store encrypted user data, authentication data and login attempts.
Data is separated across tables to allow for easier management, reduce exposure and create clear ownership relations.

- auth 
Used to store account credentials and identifiers. All usernames are forced to be unique along with each user being
assigned a unique "user_id" primary key. The user credentials are stored as a per-user salt and hashed password which are
stored as BLOBs.

- data
Stores user-specific data listed as "notes". Each entry has a primary key called "data_id" and a foreign key used to link it
to the user called "user_id". The "user_id" foreign key is most notably used during note deletion, making sure that the note
belongs to the user before deletion. All notes are considered sensitive data, therefore they are encrypted before being
stored and are stored as BLOBs.

- attempts 
Stores all attempts at authentication, which is used for lockout logic, audit and monitoring. It includes information such as
the username of the attempted login, the timestamp of the attempted login and the reason why the login failed.


## Limitations

- Local only system
The application does not include any network or web-based functionality as it was only designed with a locally hosted database.
Because of this, network-level features such as geolocation which could have been used when logging authentication attempts
or IP-based lockouts are not implemented.

- Username based Lockouts
Because of a lack of network source to use as a base to lock someone out from, usernames have been used as an alternative. In a web-based
or a networked system, this would be susceptible to denial-of-service attacks. However, due to the local scope of this project this is considered 
acceptable.

- Single-factor authentication
The only authentication that this system relies on is username and password authentication. Two-factor authentication was out of scope for
this implementation.

- Simplified encryption key handling
Due to the local nature of this project, all encryption keys are stored in the same directory as the code and database, and managed by the
application. Secure storage solutions for the key such as vault services are not implemented due to the scope of the project.

- Command-line Interface
The application uses a CLI rather than a GUI, reducing attack surface but also removing features like user interface design.

This allows the focus to remain on secure coding principles instead of intuitive user interface design.



