from config.settings import create_app
from flask_login import LoginManager
from model.Models import Users
from config.settings import db
app = create_app()
app.config['SQLALCHEMY_POOL_RECYCLE'] = 280
app.app_context().push()
login_manager = LoginManager()
login_manager.login_view = 'index.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(id):
    try:
        return Users.query.get(int(id))
    except:
        db.session.rollback()
        raise
    finally:
        db.session.close()
if __name__ == "__main__":
    app.run(host=app.config['HOST'],port=app.config['PORT'], debug=app.config['DEBUG'])
