#!/usr/bin/env python3
"""
BedsideBot Startup Script
Ensures consistent behavior between localhost and deployment
"""

import os
import sys
from app import app

if __name__ == "__main__":
    # Set environment for consistent behavior
    port = int(os.environ.get('PORT', 8080))
    debug_mode = os.environ.get('FLASK_ENV') == 'development'
    
    print(f"[INFO] Starting BedsideBot...")
    print(f"[INFO] Port: {port}")
    print(f"[INFO] Debug: {debug_mode}")
    print(f"[INFO] Database: {app.config['SQLALCHEMY_DATABASE_URI']}")
    print(f"[INFO] Access URL: http://localhost:{port}")
    
    try:
        app.run(
            debug=debug_mode,
            host='0.0.0.0',
            port=port,
            use_reloader=False  # Prevent double startup in debug mode
        )
    except KeyboardInterrupt:
        print("\n[INFO] BedsideBot stopped by user")
    except Exception as e:
        print(f"[ERROR] Failed to start: {e}")
        sys.exit(1)