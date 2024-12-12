from invoice_ocr.app import app as application

if __name__ == "__main__":
    application.run(host=os.getenv('IP', '0.0.0.0'), 
            port=int(os.getenv('PORT', 444)))