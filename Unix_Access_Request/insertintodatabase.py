from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dbconnection import Base,unix_requst_data

def Insert_Into_Database (requested_for , requested_for_email_id,manager_id ,manager_email_id,user_having_access_to_unix_server,server_names,need_to_switch_to_application_user,application_user_name,reason,contact_no,need_to_any_specific_group,specific_group,status):
    engine = create_engine(r'sqlite:///E:\Unix_Access_Request\unix_request.db')
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    Session = DBSession()


    request = unix_requst_data()
    request.requested_for_id = requested_for
    request.requested_for_email_id = requested_for_email_id
    request.manager_id = manager_id
    request.manager_email_id = manager_email_id
    request.user_having_access_to_unix_server = user_having_access_to_unix_server
    request.server_names = server_names
    request.need_to_switch_to_application_user = need_to_switch_to_application_user
    request.application_user_name = application_user_name
    request.reason = reason
    request.contact_no = contact_no
    request.need_to_any_specific_group = need_to_any_specific_group
    request.specific_group = specific_group
    request.status = status
    Session.add(request)
    Session.commit()
    id = request.request_id
    Session.close()
    return id



def Get_Data_From_Database (request_id) :
    engine = create_engine(r'sqlite:///E:\Unix_Access_Request\unix_request.db')
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    Session = DBSession()

    session = DBSession()
    request_details = session.query(unix_requst_data).filter(unix_requst_data.request_id == request_id)
    for request  in request_details:
        temp = [request.requested_for_id ,request.manager_email_id ,request.server_names,request.need_to_switch_to_application_user,request.application_user_name,request.reason,request.need_to_any_specific_group,request.specific_group,request.status,request.manager_id,request.datetime,request.requested_for_email_id]
        session.close()
        return temp
#Get_Data_From_Database(9)


def Update_Status (request_id ,approvereject):
    engine = create_engine(r'sqlite:///E:\Unix_Access_Request\unix_request.db')
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    Session = DBSession()

    session = DBSession()
    request_details = session.query(unix_requst_data).filter(unix_requst_data.request_id == request_id)
    for request in request_details:
        print(request.request_id)
        request.status = 'Request ' + approvereject
    session.commit()
    session.close()



def Get_Request_For_Approval (user):
    engine = create_engine(r'sqlite:///E:\Unix_Access_Request\unix_request.db')
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    Session = DBSession()

    session = DBSession()
    requests = []
    request_details = session.query(unix_requst_data).filter(unix_requst_data.manager_id == user)
    for request in request_details:

        link = "http://10.102.112.150/request/id/"+str(request.request_id)
        status  = request.status
        if "sent" in status.lower() :
            status  = "Waiting For Your Approval"
        temp_dict  = {"request_id":request.request_id,"requested_for":request.requested_for_id,"server_list_final":request.server_names,"status":status,"link":link,"datetime":request.datetime.date()}
        requests.append(temp_dict)
    #print (requests)
    session.commit()
    session.close()
    return  requests


def My_Requests (user) :
    engine = create_engine(r'sqlite:///E:\Unix_Access_Request\unix_request.db')
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    Session = DBSession()

    session = DBSession()
    requests = []
    request_details = session.query(unix_requst_data).filter(unix_requst_data.requested_for_id == user)
    for request in request_details:

        link = "http://10.102.112.150/request/id/" + str(request.request_id)
        status = request.status
        if "sent" in status.lower():
            status = "Waiting For Approval"
        temp_dict = {"request_id": request.request_id, "requested_for": request.requested_for_id,
                     "server_list_final": request.server_names, "status": status, "link": link,
                     "datetime": request.datetime.date()}
        requests.append(temp_dict)
    # print (requests)
    session.commit()
    session.close()
    return requests

