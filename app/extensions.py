from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_talisman import Talisman

# We initialize our factories here to make use of the 'init_app' function.
cors = CORS()
limiter = Limiter(key_func=get_remote_address, default_limits=["250 per hour"])
talisman = Talisman()
