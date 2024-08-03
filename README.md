chat with llms
Running the API:

Linux

    API:
        export FLASK_APP=chatbot
        export FLASK_ENV=development
        flask init-db
        (optional: flask fill-db)
        flask run

Windows

    API:
        set FLASK_APP=chatbot
        set FLASK_ENV=development
        flask init-db
        (optional: flask fill-db)
        flask run
