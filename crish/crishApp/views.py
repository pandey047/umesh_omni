from . models import DatabaseConnection,DataModel,DataSource,Explorer
from . serializers import DatabaseConnectionSerializer,DataModelSerializer,DataSourceSerializer, ExplorerSerializer, SendPasswordResetEmailSeializer, UserPasswordResetSerializer
import json
from rest_framework.views import APIView
import mysql.connector
from rest_framework import viewsets,status
from rest_framework.response import Response
from crishApp.renderers import UserRenderer
from rest_framework.authentication import SessionAuthentication,BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from pprint import pprint
from jinja2 import Template, Environment, FileSystemLoader
# from rest_framework.parsers import MultiPartParser, FormParser,FileUploadParser
# import pandas as pd

# Create your views here.

#Database Connections Views
class DatabaseConnectionViewSet(viewsets.ModelViewSet):
    queryset=DatabaseConnection.objects.all()
    serializer_class=DatabaseConnectionSerializer
    # parser_classes = (FormParser, MultiPartParser)
    # parser_classes = (FileUploadParser,)# set parsers if not set in settings. Edited
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
   
    def list(self,request):
        db_connection=DatabaseConnection.objects.filter(creationUser=request.user)
        serializer=DatabaseConnectionSerializer(db_connection,many=True)
        
        return Response(serializer.data)
 
    def create(self, request):
        serializer=DatabaseConnectionSerializer(data=request.data) 
        try:
            qs=DatabaseConnection.objects.get(name=request.data['name'],creationUser=request.user) 
        except DatabaseConnection.DoesNotExist:
            qs=None
        # print(qs)
        # print(request.data)
        if serializer.is_valid():
            if qs is None:
                f=serializer.save()
                f.creationUser=request.user 
                f.save()
                return Response(serializer.data,status=status.HTTP_201_CREATED)
            elif qs is not None:
                context={"Error":"Database Connection name already exists, please try with different Database connection name!! "}
                return Response(data=context)
                
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self, request,pk):
        try:
            db_connection=DatabaseConnection.objects.get(pk=pk)
            with open(f'{db_connection.parameter}') as j:
                    data = json.load(j)
        except:
            db_connection=None
        if db_connection is None:
            return Response("Data does not exist in DB")
        # elif db_connection.parameter =="":
        #     return Response("Please Upload Json Configuration File!")
        else:
            try:     
                print(data)
                
                db = mysql.connector.connect(host=data['host'], 
                        user=data['username'],database=data['database'],password=data['password'],port=data['port'])
                db=str(db)
                print(db)
                
                if 'MySQLConnection object at' in db:
                    con_obj=''
                    con_obj= con_obj+"Connection is successful!"  
                    serializer=DatabaseConnectionSerializer(db_connection)
                    print(con_obj,"63")
                    context={"DB Details":serializer.data,"Configuration Details":data,"status":con_obj}   
                    #return Response(data=context) 
                #else:
                    #db=None

            except :
                con_obj=''
                con_obj= con_obj+"Connection is not successful! Check your credentials !!"
                serializer=DatabaseConnectionSerializer(db_connection)
                print(con_obj,"66")
                context={"DB Details":serializer.data,"Configuration Details":data,"status":con_obj}
            return Response(data=context)

        
    def update(self,request,pk):
        db_connection=DatabaseConnection.objects.get(pk=pk)
        serializer=DatabaseConnectionSerializer(db_connection,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def partial_update(self,request,pk):
        db_connection=DatabaseConnection.objects.get(pk=pk)
        serializer=DatabaseConnectionSerializer(db_connection,data=request.data)
        if serializer.is_valid():
            serializer.save()
            d1={'data':serializer.data,'response':'Object has been updated succesfully!'}
            return Response(d1)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
    def destroy(self,request,pk):
        db_connection=DatabaseConnection.objects.get(pk=pk)
        # serializer=DatabaseConnectionSerializer(db_connection)
        db_connection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)      
    
     
        

#Data Models Views
class DataModelViewSet(viewsets.ModelViewSet):
    queryset = DataModel.objects.all()
    serializer_class = DataModelSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    
    def list(self, request):
        dataModel=DataModel.objects.filter(creationUser=request.user)
        serializer=DataModelSerializer(dataModel,many=True)
        return Response(serializer.data)  
    
    def create(self,request):
        serializer=DataModelSerializer(data=request.data)
        try:
            qs=DataModel.objects.get(name=request.data['name'],creationUser=request.user)
        except DataModel.DoesNotExist:
            qs=None
        if serializer.is_valid():
            if qs is None:
                f=serializer.save()
                f.creationUser=request.user
                f.save()
                return Response(serializer.data,status=status.HTTP_201_CREATED)
            elif qs is not None:
                context={"Error":"Data Model name already exists, please try with different Data Model name!! "}
                return Response(data=context)
                          
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    
    def retrieve(self,request,pk):
        try:
            dataModel=DataModel.objects.get(pk=pk)
        except DataModel.DoesNotExist:
            dataModel=None
        if dataModel:
            serializer=DataModelSerializer(dataModel)
            with open(f'{dataModel.parameter}') as j:
                data=json.load(j)
                # print('data',data)
            try:
                database_obj=DatabaseConnection.objects.get(name=data['database_connection'])
                with open(f'{database_obj.parameter}') as k:
                    data2=json.load(k)
                    # print('data2',data2)
            except DatabaseConnection.DoesNotExist:
                    database_obj=None
                    context={"Error":"Databaseconnection name in file does not exist!"}
                    return Response(data=context)
                
            try:
                db = mysql.connector.connect(host=data2['host'], 
                        user=data2['username'],database=data['schema_name'],password=data2['password'],port=data2['port'])
                print(db)
                tab=data['table_name']
                print(tab)
                cursor=db.cursor()
                # q=f"SELECT * FROM {tab}"
                cursor.execute("SELECT * FROM {}".format(tab))
                result=cursor.fetchall()
                # print(result)
                # return Response(sql.data)
                db=str(db)
                if 'MySQLConnection object at' in db:
                        con_obj=''
                        con_obj= con_obj+"Connection is successful!" 
                        context={"Data Model Details":serializer.data,"Database Result":result,"Connection Status":con_obj,"Configuration Details":data}
                        return Response(data=context)
            except :
                    return Response("Connection is not successful! Check your credentials!!")
        else:
            return Response("Model Object does not exist!") 
    
    def update(self,request,pk):
        dataModel=DataModel.objects.get(pk=pk)
        serializer=DataModelSerializer(dataModel,data=request.data)
        if serializer.is_valid():
            serializer.save()
            d1={'data':serializer.data,'response':'Object has been updated succesfully!'}
            return Response(d1)
        
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
    def destroy(self,request,pk):
        dataModel=DataModel.objects.get(pk=pk)
        # serializer=DataModelSerializer(dataModel)
        dataModel.delete()
        return Response("Object has been deleted successfully!") 

# Data Source Views
class DataSourceViewSet(viewsets.ModelViewSet):
    queryset=DataSource.objects.all()
    serializer_class=DataSourceSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self,request):
        data_source=DataSource.objects.filter(creationUser=request.user)
        serializer=DataSourceSerializer(data_source,many=True)
        return Response(serializer.data)
    '''
    DatabaseConnection.objects.create(name='',host='',port='',username='',password='')
    '''
    
    def create(self,request):
        serializer=DataSourceSerializer(data=request.data)
        try:
            qs=DataSource.objects.get(name=request.data['name'],creationUser=request.user)
        except DataSource.DoesNotExist:
            qs=None
        if serializer.is_valid():
            if qs is None:
                f=serializer.save()
                f.creationUser=request.user
                f.save()
                return Response(serializer.data,status=status.HTTP_201_CREATED)
            elif qs is not None:
                context={"Error":"Data Source name already exists, please try with different Data Source name!! "}
                return Response(data=context)
                
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self,request,pk):
        try:
            data_source=DataSource.objects.get(pk=pk)
            serializer=DataSourceSerializer(data_source)
    
            if data_source.parameter:
                with open(f'{data_source.parameter}') as k:
                    json_data=json.load(k)
                    print("jsondata",json_data)
                try:    
                    dataModel=DataModel.objects.get(name=json_data["data_model"])
                    with open(f'{dataModel.parameter}') as l:
                        json_data2=json.load(l)
                        # print(json_data2['database_connection'])
                      
                    database_obj=DatabaseConnection.objects.get(name=json_data2['database_connection'])
                    with open(f'{database_obj.parameter}') as m:
                        data2=json.load(m)
                        # print('data2',data2)
                    
                    try:
                        db = mysql.connector.connect(host=data2['host'], 
                                user=data2['username'],database=json_data['schema_name'],password=data2['password'],port=data2['port'])
                        # print("db",db)
                        cursor=db.cursor()
                        sql_file_str = json_data['data_source_type'] + '.sql'
                        print(sql_file_str,type(sql_file_str))
                        # D:/Umesh Pandey/Tasks/Clients/Christopher Funaki/Crish_Drf/crish/sql_templates/
                        # /home/ubuntu/omni_analytics/crish/sql_templates
                        # template_file = open(r'D:/Umesh Pandey/Tasks/Clients/Christopher Funaki/Crish_Drf/crish/sql_templates' + '/' + sql_file_str, "r").read()
                        with open(f"D:/Umesh Pandey/Tasks/Clients/Christopher Funaki/Crish_Drf/crish/sql_templates/{sql_file_str}") as p:
                            template_file=p.read()
                            # print("new temp",template_file)    

                        t = Template(template_file)

                        sql = t.render(
                            data_model = json_data2,
                            data_source = json_data
                        )

                        print("sqldata",sql)
                        # print("cursor",cursor)
                        cursor.execute(sql)
                        # result=cursor.fetchall()
                        # cursor.execute(f'SELECT * FROM {tab}')
                        # result2=cursor.fetchall()
                        # print("238",result2)
                        db=str(db)
                        if 'MySQLConnection object at' in db:
                                    con_obj=''
                                    con_obj= con_obj+"Connection is successful!" 
                                    serializer=DataSourceSerializer(data_source)
                                    context={"Data Source Details":serializer.data,
                                             "Database Result":["Table created successfully"],
                                             "Connection Status":con_obj,"Configuration Details":json_data}
                                    return Response(data=context)
                    except:
                        context={"Data Source Details":serializer.data,
                                 "Status":"Connection is not successfully! Check your credentials!!",
                                 "Configuration Details":json_data}
                        return Response(data=context)    
                except DataModel.DoesNotExist:
                    dataModel=None
                    context={"Error":"Data model name in file does not exist!"}
                    return Response(data=context)
                    
            tab=json_data["table_name"]
            
        except DataSource.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
    def update(self, request,pk):
        data_source=DataSource.objects.get(pk=pk)
        serializer=DataSourceSerializer(data_source,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self,request,pk):
        data_source=DataSource.objects.get(pk=pk)
        # serializer=DataModelSerializer(dataModel)
        data_source.delete()
        return Response("Object has been deleted successfully!")
       
# Explorer View
class ExplorerViewSet(viewsets.ModelViewSet):
    queryset=Explorer.objects.all()
    serializer_class=ExplorerSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
''' 
    def list(self,request):
        explorer=Explorer.objects.filter(creationUser=request.user,many=True)
        serializer=ExplorerSerializer(explorer)
        return Response(serializer.data)
        
    def create(self,request):
        serializer=ExplorerSerializer(data=request.data)
        try:
            qs=Explorer.objects.get(request.data['name'],creationUser=request.user)
        except Explorer.DoesNotExist:
            qs=None
        if serializer.is_valid():
            if qs is None:
                f=serializer.save()
                f.creationUser=request.user
                f.save()
                return Response(serializer.data,status=status.HTTP_201_CREATED)
            elif qs is not None:
                context={"Error":"Explorer name already exist, please try with differnt name !!"}
                return Response(data=context)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self, request, pk):
        try:
            explorer=Explorer.objects.get(pk=pk)
        except Explorer.DoesNotExist:
            explorer=None
        if explorer:
            serializer=ExplorerSerializer(explorer)
            with open(f'{explorer.parameter}') as j:
                json_data=json.load(j)
                print(json_data)
            try:
                data_source=DataSource.objects.get(name=json_data['data_source'])
                
            except DataSource.DoesNotExist:
                data_source=None
                
'''            
            
            
            
            
            
            
                
from django.contrib.auth.models import User
from .serializers import UserSerializer,UserLoginSerialzer
from django.contrib.auth import authenticate,login
from rest_framework.authtoken.models import Token

class Users(viewsets.ModelViewSet):
    queryset=User.objects.all()
    serializer_class=UserSerializer
    def create(self,request):
        serializer=UserSerializer(data=request.data)
        if serializer.is_valid():
            passwd=serializer.validated_data['password']
            # print(passwd)
            user=serializer.save()
            user.set_password(passwd)
            user.is_staff=True 
            user.save()
            token=Token.objects.get(user=user)
            json = serializer.data
            json['token'] = token.key 
            return Response(json, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class LoginView(APIView):
    def post(self,request,*args,**kwargs): 
        serializer=UserLoginSerialzer(data=request.data)
        # print(request.data)
        username=request.data['username']
        password=request.data['password']
        # print(username,password)
        user_auth=authenticate(username=username,password=password)
        
        # print(user_auth,type(user_auth))
        # print(user_auth.email)
        if user_auth:
            email=user_auth.email
            id=user_auth.id
            token=Token.objects.get(user=user_auth)
            token=token.key
            context={'Status':"User logged in successfully !","id":id,"username":username,"email":email,"token":token}
            return Response(data=context) 
              
        else:
            return Response("User or Password does not match !")
        
class SendPasswordResetEmailView(APIView):
#   renderer_classes = [UserRenderer]
  def post(self, request, format=None):
    serializer = SendPasswordResetEmailSeializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    return Response({'msg':'Password Reset link send. Please check your Email'}, status=status.HTTP_200_OK)
        
class UserPasswordResetView(APIView):
#   renderer_classes = [UserRenderer]
  def post(self, request, uid, token, format=None):
    serializer = UserPasswordResetSerializer(data=request.data, context={'uid':uid, 'token':token})
    serializer.is_valid(raise_exception=True)
    return Response({'msg':'Password Reset Successfully'}, status=status.HTTP_200_OK)
        

        
        
        
    
        
        
        
        



































'''
from .models import DatabaseConnection
from rest_framework.response import Response
from . serializers import DatabaseConnectionSerializer
from rest_framework.decorators import api_view
from rest_framework import status

@api_view(['GET','POST'])
def databaseConnection_list(request):
    if request.method=='GET':
        databaseConnection=DatabaseConnection.objects.all()
        serializer=DatabaseConnectionSerializer(databaseConnection,many=True)
        return Response(serializer.data)
    
    elif request.method=='POST':
        serializer=DatabaseConnectionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET','PUT','DELETE']) 
def databaseConnection_detail(request,pk):
    try:
        databaseConnection=DatabaseConnection.objects.get(pk=pk)
    except DatabaseConnection.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method=='GET':
        serializer=DatabaseConnectionSerializer(databaseConnection)
        return Response(serializer.data)
    
    elif request.method=='PUT':
        serializer=DatabaseConnectionSerializer(databaseConnection,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method=='DELETE':
        serializer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
'''  


