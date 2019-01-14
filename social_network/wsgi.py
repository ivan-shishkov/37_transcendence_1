import os

from configurations.wsgi import get_wsgi_application
import dotenv

dotenv.read_dotenv(
    os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'),
)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'social_network.settings')

application = get_wsgi_application()
