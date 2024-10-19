from rdmanager import admin,db
from rdmanager.models import User,UserLogins,Customer,Terminal
from flask import abort
from flask_login import current_user
from flask_admin.contrib.sqla import ModelView
from flask_admin.menu import MenuLink

class ProtectedModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated
    
    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return abort(404)
    
class ProtectedMenuLink(MenuLink):
    def is_accessible(self):
        return current_user.is_authenticated
    
    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return abort(404)

class UserView(ProtectedModelView):
    can_delete = False
    column_labels = {"user.id":"ID",
                     "user.name":"Name",
                     "user.lastname":"Last Name",
                     "user.email":"E-Mail",
                     "user.password":"Password Hash"}


class UserLoginView(ProtectedModelView):
    can_delete = False
    column_labels = {"user_logins.id":"ID",
                     "user_logins.user_id":"User",
                     "user_logins.login_date":"Login Date",
                     "user_logins.login_ip":"IP"} 

class CustomerView(ProtectedModelView):
    form_columns = ['name','email','phone','address','number','complement',
                    'city','state','postal_code','date_created','terminals']
    column_labels = {"cliente.id":"ID",
                     "cliente.name":"Name",
                     "cliente.email":"E-Mail",
                     "cliente.phone":"Phone",
                     "cliente.address":"Address",
                     "cliente.number":"Number",
                     "cliente.complement":"Complement",
                     "cliente.city":"City",
                     "cliente.state":"State",
                     "cliente.postal_code":"Postal Code",
                     "cliente.date_created":"Date created"} 

class TerminalView(ProtectedModelView):
    form_columns = ['customer_id','description','rustdesk_id', 'rustdesk_password']
    column_list = ['id','customer_id','description','rustdesk_id','rustdesk_password']
    column_labels = {"terminal.id":"ID",
                     "terminal.customer_id":"Customer",
                     "terminal.description":"Description",
                     "terminal.rustdesk_id":"RustDesk ID",
                     "terminal.rustdesk_Password":"RustDesk Password",
                     "terminal.date_created":"Date Created"}

def register_modelviews():
    admin.add_view(UserView(User,db.session, category='Users'))
    admin.add_view(UserLoginView(UserLogins,db.session, category='Users'))
    admin.add_view(CustomerView(Customer,db.session, category='Customers'))
    admin.add_view(TerminalView(Terminal,db.session, category='Customers'))