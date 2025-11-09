from job_portal import create_app

# Create and run the application
app = create_app()

if __name__ == '__main__':
    # Setting debug=True automatically reloads the app upon changes
    # and provides error messages in the browser.
    app.run(debug=True)