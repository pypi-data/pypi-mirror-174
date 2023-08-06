import sys
from listen.main import main

try:
    main()
except KeyboardInterrupt:
    sys.exit(1)