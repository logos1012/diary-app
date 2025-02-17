from app import create_app, db
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = create_app()

def init_db():
    with app.app_context():
        try:
            db.create_all()
            logger.info("Database tables created successfully")
        except Exception as e:
            logger.error(f"Error creating database tables: {str(e)}")

if __name__ == '__main__':
    logger.info("Initializing application...")
    init_db()
    try:
        # 파일 핸들러 추가
        file_handler = logging.FileHandler('app.log')
        file_handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        app.logger.addHandler(file_handler)
        
        app.run(host='0.0.0.0', port=5001, debug=True)
    except Exception as e:
        logger.error(f"Application failed to start: {str(e)}") 