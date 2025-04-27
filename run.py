#!/usr/bin/env python3
"""
Inventory Management System Launcher
This script provides a simple way to launch either the CLI or web interface.
"""

import os
import sys
import argparse
import subprocess
import webbrowser
from time import sleep

def get_data_dir():
    """Get the data directory path"""
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')

def ensure_data_dir():
    """Ensure the data directory exists"""
    data_dir = get_data_dir()
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    return data_dir

def run_cli(args=None):
    """Run the CLI with optional arguments"""
    cmd = [sys.executable, 'main.py']
    if args:
        cmd.extend(args)
    subprocess.run(cmd)

def run_web(host='127.0.0.1', port=5000, open_browser=True):
    """Run the web interface"""
    # Start the Flask web server
    print(f"Starting Inventory Management System web server on http://{host}:{port}")
    print("Press Ctrl+C to stop the server")
    
    # Open browser after a short delay
    if open_browser:
        def open_web_browser():
            sleep(1)  # Give the server a moment to start
            url = f"http://{host}:{port}"
            print(f"Opening {url} in web browser...")
            webbrowser.open(url)
        
        import threading
        threading.Thread(target=open_web_browser).start()
    
    # Import and run the Flask app
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'web')))
    from web.app import app
    app.run(host=host, port=port)

def main():
    """Main entry point for the launcher"""
    parser = argparse.ArgumentParser(description='Inventory Management System Launcher')
    
    # Create subparsers for different interfaces
    subparsers = parser.add_subparsers(dest='interface', help='Interface to launch')
    
    # CLI interface
    cli_parser = subparsers.add_parser('cli', help='Launch the command-line interface')
    cli_parser.add_argument('args', nargs='*', help='Arguments to pass to the CLI')
    
    # Web interface
    web_parser = subparsers.add_parser('web', help='Launch the web interface')
    web_parser.add_argument('--host', default='127.0.0.1', help='Host to run the web server on')
    web_parser.add_argument('--port', type=int, default=5000, help='Port to run the web server on')
    web_parser.add_argument('--no-browser', action='store_true', help='Don\'t open the browser automatically')
    
    args = parser.parse_args()
    
    # Ensure data directory exists
    ensure_data_dir()
    
    # Launch the selected interface
    if args.interface == 'cli':
        run_cli(args.args)
    elif args.interface == 'web':
        run_web(args.host, args.port, not args.no_browser)
    else:
        # If no interface specified, show menu
        print("==== Inventory Management System ====")
        print("1) Launch Web Interface")
        print("2) Launch Command Line Interface")
        print("0) Exit")
        
        choice = input("Enter your choice (0-2): ")
        
        if choice == '1':
            run_web()
        elif choice == '2':
            run_cli()
        else:
            print("Exiting.")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting Inventory Management System.")
        sys.exit(0) 