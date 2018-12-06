from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()
class unix_requst_data(Base):
    __tablename__ = 'Access_Requests'
    request_id = Column(Integer, primary_key=True ,autoincrement=True)
    requested_for_id = Column(String(50))
    requested_for_email_id = Column(String(50))
    manager_id = Column(String(50))
    manager_email_id = Column(String(25))
    user_having_access_to_unix_server = Column(String(3))
    server_names = Column(String(200))
    need_to_switch_to_application_user = Column(String(3))
    application_user_name = Column(String(100))
    reason = Column(String(500))
    contact_no = Column(String(12))
    need_to_any_specific_group = Column(String(3))
    specific_group = Column(String(100))
    status  = Column(String(25))
    datetime = Column (DateTime, default=datetime.datetime.now())




engine = create_engine(r'sqlite:///E:\Unix_Access_Request\unix_request.db' )
Base.metadata.create_all(engine)