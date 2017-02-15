# Statement for disabling the development environment
DEBUG = True

# Use a secure, unique and absolutely secret key for
# signing the data
CSRF_SECRET_KEY = 'mysecretkey-otherside!!!'

# Secret key for signing cookies
SECRET_KEY = 'mysecretkey-otherside!!!'

# Statement for disabling the testing environment
TESTING = False

# Application threads. A common general assumption is
# using 2 per available processor cores - use one
# to handle incoming requests and the other to perform
# background operations
THREADS_PER_PAGE = 2

# Enable protection against *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED = True