# libemail

## Installation

1. Install the app
    
    ```
    pip install libemail
    ```

2. Add `libemail` to `INSTALLED_APPS` in `settings.py` file

## Usage:

1. Build the template context

    ```
    from libemail.generic import Email, EmailContext


    email_context = EmailContext(
        title="A simple title",
        subtitle="A descriptive subtitle",
        body="A long enough body, very detailed",
        preview="Preview text that will be displayed on the list view of the mail client",
        branding="A link to a image, white or transparent background",
    )
    ```

2. Initialize an email object

    ```
    email = Email(subject="A very serious subject", context=email_context, to="some@email.com")
    ```

3. Send it!

    ```
    email.send()
    ```

