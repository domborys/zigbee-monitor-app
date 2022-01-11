Search.setIndex({docnames:["index","make_admin","modules","prepare","receiver","webserver"],envversion:{"sphinx.domains.c":2,"sphinx.domains.changeset":1,"sphinx.domains.citation":1,"sphinx.domains.cpp":4,"sphinx.domains.index":1,"sphinx.domains.javascript":2,"sphinx.domains.math":2,"sphinx.domains.python":3,"sphinx.domains.rst":2,"sphinx.domains.std":2,sphinx:56},filenames:["index.rst","make_admin.rst","modules.rst","prepare.rst","receiver.rst","webserver.rst"],objects:{"":[[1,0,0,"-","make_admin"],[3,0,0,"-","prepare"],[4,0,0,"-","receiver"],[5,0,0,"-","webserver"]],"receiver.example_client":[[4,1,1,"","execute_one_request"],[4,1,1,"","execute_parallel_requests"],[4,1,1,"","execute_sequential_requests"],[4,1,1,"","main"],[4,1,1,"","notifications_thread_func"],[4,1,1,"","prepare_parallel_requests"],[4,1,1,"","prepare_sequential_requests"]],"receiver.notify_server":[[4,2,1,"","SocketNotifyServer"]],"receiver.notify_server.SocketNotifyServer":[[4,3,1,"","address"],[4,3,1,"","notify_queue"],[4,3,1,"","port"],[4,4,1,"","run"]],"receiver.request_response_server":[[4,2,1,"","SocketRequestResponseServer"]],"receiver.request_response_server.SocketRequestResponseServer":[[4,3,1,"","address"],[4,3,1,"","command_queue"],[4,3,1,"","port"],[4,3,1,"","queue_timeout"],[4,4,1,"","run"]],"receiver.server_command":[[4,2,1,"","ServerCommand"]],"receiver.server_command.ServerCommand":[[4,3,1,"","description"],[4,3,1,"","response_queue"]],"receiver.socket_common":[[4,5,1,"","ConnectionBrokenError"],[4,1,1,"","recv_json"],[4,1,1,"","send_json"]],"receiver.xbee_console":[[4,2,1,"","ConsoleCommand"],[4,1,1,"","console_thread_func"],[4,1,1,"","data_received_callback"],[4,1,1,"","discover_network"],[4,1,1,"","execute_discover_command"],[4,1,1,"","execute_send_command"],[4,1,1,"","print_network"],[4,1,1,"","xbee_thread_func"],[4,1,1,"","xbee_thread_loop"]],"receiver.xbee_console.ConsoleCommand":[[4,4,1,"","get_arguments"],[4,4,1,"","get_name"],[4,4,1,"","parse_arguments"],[4,4,1,"","parse_command"]],"receiver.xbee_device_connection":[[4,2,1,"","XBeeDeviceConnection"]],"receiver.xbee_device_connection.XBeeDeviceConnection":[[4,3,1,"","command_queue"],[4,3,1,"","connection_startup_finished"],[4,3,1,"","connection_startup_successful"],[4,3,1,"","device"],[4,3,1,"","notify_queue"],[4,4,1,"","start"]],"receiver.xbee_device_server":[[4,1,1,"","main"]],"webserver.database":[[5,2,1,"","Base"],[5,6,1,"","SessionLocal"],[5,6,1,"","engine"]],"webserver.database.Base":[[5,3,1,"","metadata"],[5,3,1,"","registry"]],"webserver.dbmodels":[[5,2,1,"","Floor"],[5,2,1,"","Node"],[5,2,1,"","ReadingConfig"],[5,2,1,"","User"],[5,2,1,"","UserSession"]],"webserver.dbmodels.Floor":[[5,3,1,"","height"],[5,3,1,"","id"],[5,3,1,"","image"],[5,3,1,"","image_media_type"],[5,3,1,"","name"],[5,3,1,"","nodes"],[5,3,1,"","number"],[5,3,1,"","width"]],"webserver.dbmodels.Node":[[5,3,1,"","address64"],[5,3,1,"","floor"],[5,3,1,"","floor_id"],[5,3,1,"","id"],[5,3,1,"","name"],[5,3,1,"","reading_configs"],[5,3,1,"","x"],[5,3,1,"","y"]],"webserver.dbmodels.ReadingConfig":[[5,3,1,"","at_command"],[5,3,1,"","at_command_data"],[5,3,1,"","at_command_result_format"],[5,3,1,"","id"],[5,3,1,"","message_prefix"],[5,3,1,"","message_to_send"],[5,3,1,"","mode"],[5,3,1,"","name"],[5,3,1,"","node"],[5,3,1,"","node_id"],[5,3,1,"","refresh_period"]],"webserver.dbmodels.User":[[5,3,1,"","disabled"],[5,3,1,"","id"],[5,3,1,"","password_hash"],[5,3,1,"","role"],[5,3,1,"","sessions"],[5,3,1,"","username"]],"webserver.dbmodels.UserSession":[[5,3,1,"","id"],[5,3,1,"","session_id"],[5,3,1,"","time_last_activity"],[5,3,1,"","time_started"],[5,3,1,"","user"],[5,3,1,"","user_id"]],"webserver.dbsrv":[[5,1,1,"","authenticate_user"],[5,1,1,"","change_password"],[5,1,1,"","create_floor"],[5,1,1,"","create_user"],[5,1,1,"","delete_all_user_sessions"],[5,1,1,"","delete_expired_user_sessions"],[5,1,1,"","delete_floor"],[5,1,1,"","delete_user"],[5,1,1,"","end_all_user_sessions"],[5,1,1,"","end_user_session"],[5,1,1,"","get_all_floors"],[5,1,1,"","get_all_user_sessions"],[5,1,1,"","get_all_users"],[5,1,1,"","get_floor_by_id"],[5,1,1,"","get_session_and_refresh"],[5,1,1,"","get_session_by_session_id"],[5,1,1,"","get_user_by_id"],[5,1,1,"","get_user_by_username"],[5,1,1,"","modify_floor"],[5,1,1,"","modify_user"],[5,1,1,"","set_floor_image"],[5,1,1,"","start_user_session"]],"webserver.main":[[5,6,1,"","app"],[5,1,1,"","change_password"],[5,1,1,"","check_csrf_token"],[5,6,1,"","cookie_sid"],[5,1,1,"","create_floor"],[5,1,1,"","create_user"],[5,1,1,"","csrf_tokens_equal"],[5,1,1,"","delete_floor"],[5,1,1,"","delete_user"],[5,1,1,"","discover_network"],[5,1,1,"","execute_command"],[5,1,1,"","get_all_floors"],[5,1,1,"","get_current_active_user"],[5,1,1,"","get_current_session"],[5,1,1,"","get_current_session_ws"],[5,1,1,"","get_current_user"],[5,1,1,"","get_db"],[5,1,1,"","get_floor_by_id"],[5,1,1,"","get_floor_image_by_id"],[5,1,1,"","get_parameter"],[5,1,1,"","get_sessions"],[5,1,1,"","get_user_by_id"],[5,1,1,"","get_user_me"],[5,1,1,"","get_users"],[5,1,1,"","handle_xbee_error"],[5,1,1,"","is_valid_admin"],[5,1,1,"","is_valid_user"],[5,1,1,"","login"],[5,1,1,"","logout"],[5,1,1,"","logout_all"],[5,1,1,"","logout_all_users"],[5,1,1,"","message_websocket"],[5,1,1,"","modify_floor"],[5,1,1,"","modify_floor_image_by_id"],[5,1,1,"","modify_user"],[5,1,1,"","root"],[5,1,1,"","send_message"],[5,1,1,"","set_parameter"],[5,1,1,"","wait"]],"webserver.pwdcontext":[[5,6,1,"","pwd_context"]],"webserver.pydmodels":[[5,2,1,"","AtCommandBase"],[5,2,1,"","AtCommandGetExecute"],[5,2,1,"","AtCommandResult"],[5,2,1,"","AtCommandSet"],[5,2,1,"","AtCommandWithType"],[5,2,1,"","DeviceInDiscoveryResult"],[5,2,1,"","DiscoveryResult"],[5,2,1,"","Floor"],[5,2,1,"","FloorBase"],[5,2,1,"","FloorCreate"],[5,2,1,"","MessageToXBee"],[5,2,1,"","Node"],[5,2,1,"","NodeBase"],[5,2,1,"","NodeCreate"],[5,2,1,"","NodeInFloor"],[5,2,1,"","PasswordChange"],[5,2,1,"","ReadingConfigBase"],[5,2,1,"","ReadingConfigInNode"],[5,2,1,"","User"],[5,2,1,"","UserBase"],[5,2,1,"","UserCreate"],[5,2,1,"","UserModify"],[5,2,1,"","UserSession"],[5,2,1,"","XBeeMessageResult"],[5,2,1,"","XBeeWaiting"],[5,2,1,"","XBeeWaitingResult"]],"webserver.pydmodels.AtCommandBase":[[5,3,1,"","address64"],[5,3,1,"","apply_changes"],[5,3,1,"","at_command"]],"webserver.pydmodels.AtCommandGetExecute":[[5,3,1,"","value"]],"webserver.pydmodels.AtCommandResult":[[5,3,1,"","error"],[5,3,1,"","result"],[5,3,1,"","status"]],"webserver.pydmodels.AtCommandSet":[[5,3,1,"","value"]],"webserver.pydmodels.AtCommandWithType":[[5,3,1,"","command_type"],[5,3,1,"","value"]],"webserver.pydmodels.DeviceInDiscoveryResult":[[5,3,1,"","address16"],[5,3,1,"","address64"],[5,3,1,"","id"],[5,3,1,"","role"]],"webserver.pydmodels.DiscoveryResult":[[5,3,1,"","devices"]],"webserver.pydmodels.Floor":[[5,2,1,"","Config"],[5,3,1,"","id"]],"webserver.pydmodels.Floor.Config":[[5,3,1,"","orm_mode"]],"webserver.pydmodels.FloorBase":[[5,3,1,"","height"],[5,3,1,"","name"],[5,3,1,"","nodes"],[5,3,1,"","number"],[5,3,1,"","width"]],"webserver.pydmodels.FloorCreate":[[5,3,1,"","height"],[5,3,1,"","name"],[5,3,1,"","nodes"],[5,3,1,"","number"],[5,3,1,"","width"]],"webserver.pydmodels.MessageToXBee":[[5,3,1,"","address64"],[5,3,1,"","message"]],"webserver.pydmodels.Node":[[5,2,1,"","Config"],[5,3,1,"","floor_id"],[5,3,1,"","id"]],"webserver.pydmodels.Node.Config":[[5,3,1,"","orm_mode"]],"webserver.pydmodels.NodeBase":[[5,3,1,"","address64"],[5,3,1,"","name"],[5,3,1,"","reading_configs"],[5,3,1,"","x"],[5,3,1,"","y"]],"webserver.pydmodels.NodeCreate":[[5,3,1,"","floor_id"]],"webserver.pydmodels.NodeInFloor":[[5,2,1,"","Config"],[5,3,1,"","floor_id"],[5,3,1,"","id"]],"webserver.pydmodels.NodeInFloor.Config":[[5,3,1,"","orm_mode"]],"webserver.pydmodels.PasswordChange":[[5,3,1,"","new_password"],[5,3,1,"","old_password"]],"webserver.pydmodels.ReadingConfigBase":[[5,3,1,"","at_command"],[5,3,1,"","at_command_data"],[5,3,1,"","at_command_result_format"],[5,3,1,"","message_prefix"],[5,3,1,"","message_to_send"],[5,3,1,"","mode"],[5,3,1,"","name"],[5,3,1,"","refresh_period"]],"webserver.pydmodels.ReadingConfigInNode":[[5,2,1,"","Config"],[5,3,1,"","id"],[5,3,1,"","node_id"]],"webserver.pydmodels.ReadingConfigInNode.Config":[[5,3,1,"","orm_mode"]],"webserver.pydmodels.User":[[5,2,1,"","Config"],[5,3,1,"","id"]],"webserver.pydmodels.User.Config":[[5,3,1,"","orm_mode"]],"webserver.pydmodels.UserBase":[[5,3,1,"","disabled"],[5,3,1,"","role"],[5,3,1,"","username"]],"webserver.pydmodels.UserCreate":[[5,3,1,"","password"]],"webserver.pydmodels.UserModify":[[5,3,1,"","password"]],"webserver.pydmodels.UserSession":[[5,2,1,"","Config"],[5,3,1,"","id"],[5,3,1,"","user_id"]],"webserver.pydmodels.UserSession.Config":[[5,3,1,"","orm_mode"]],"webserver.pydmodels.XBeeMessageResult":[[5,3,1,"","message"],[5,3,1,"","status"]],"webserver.pydmodels.XBeeWaiting":[[5,3,1,"","time"]],"webserver.pydmodels.XBeeWaitingResult":[[5,3,1,"","message"],[5,3,1,"","status"],[5,3,1,"","time"]],"webserver.xbeesrv":[[5,5,1,"","MessageParseError"],[5,2,1,"","WebsocketMessageSender"],[5,5,1,"","XBeeServerError"],[5,1,1,"","at_command"],[5,1,1,"","discover_network"],[5,1,1,"","request_response"],[5,1,1,"","send_b64_data"],[5,1,1,"","unify_exceptions"],[5,1,1,"","wait"]],"webserver.xbeesrv.WebsocketMessageSender":[[5,4,1,"","run"],[5,3,1,"","websocket"]],make_admin:[[1,1,1,"","change_password"],[1,1,1,"","create_admin"],[1,1,1,"","get_user_by_username"],[1,1,1,"","make_admin_or_change_password"]],prepare:[[3,1,1,"","configure_custom_config"],[3,1,1,"","create_admin"],[3,1,1,"","create_admin_if_not_present"]],receiver:[[4,0,0,"-","config"],[4,0,0,"-","custom_config"],[4,0,0,"-","example_client"],[4,0,0,"-","notify_server"],[4,0,0,"-","request_response_server"],[4,0,0,"-","server_command"],[4,0,0,"-","socket_common"],[4,0,0,"-","xbee_console"],[4,0,0,"-","xbee_device_connection"],[4,0,0,"-","xbee_device_server"]],webserver:[[5,0,0,"-","config"],[5,0,0,"-","custom_config"],[5,0,0,"-","database"],[5,0,0,"-","dbmodels"],[5,0,0,"-","dbsrv"],[5,0,0,"-","main"],[5,0,0,"-","pwdcontext"],[5,0,0,"-","pydmodels"],[5,0,0,"-","run_server"],[5,0,0,"-","xbeesrv"]]},objnames:{"0":["py","module","Python module"],"1":["py","function","Python function"],"2":["py","class","Python class"],"3":["py","attribute","Python attribute"],"4":["py","method","Python method"],"5":["py","exception","Python exception"],"6":["py","data","Python data"]},objtypes:{"0":"py:module","1":"py:function","2":"py:class","3":"py:attribute","4":"py:method","5":"py:exception","6":"py:data"},terms:{"16":5,"2":5,"3":4,"64":5,"catch":5,"class":[4,5],"default":5,"float":[4,5],"function":[4,5],"int":[4,5],"long":5,"new":5,"return":[4,5],"switch":4,"true":5,"try":4,"while":[4,5],A:[4,5],AT:5,At:4,If:[4,5],It:[4,5],The:[4,5],To:4,accept:5,activ:[4,5],actual:4,ad:[4,5],add:5,addr:5,address16:5,address64:5,address:[4,5],admin:5,after:4,ago:5,all:[4,5],allow:5,also:5,an:[4,5],ands:4,ani:5,anoth:4,api:5,api_kei:5,apikeycooki:5,app:5,appli:5,applic:5,apply_chang:5,ar:[4,5],argument:[4,5],async:5,asyncio:5,at_command:5,at_command_data:5,at_command_result_format:5,atcommandbas:5,atcommandgetexecut:5,atcommandresult:5,atcommandset:5,atcommandwithtyp:5,attribut:5,authent:5,authenticate_us:5,author:5,autocommit:5,autoflush:5,automat:4,base64:5,base:[4,5],basemodel:5,been:5,befor:[4,5],belong:5,bind:5,bit:5,bool:5,broken:4,build:5,c:5,call:[4,5],callabl:5,can:[4,5],cannot:5,chang:5,change_password:[1,5],charact:[4,5],check:[4,5],check_csrf_token:5,class_:5,client:[4,5],clint:5,close:5,command:[4,5],command_data:5,command_queu:4,command_typ:5,commun:[4,5],communitaion:4,config:2,config_path:3,configur:[4,5],configure_custom_config:3,connect:[4,5],connection_startup_finish:4,connection_startup_success:4,connectionbrokenerror:4,console_thread_func:4,consolecommand:4,contain:5,content:[2,3],control:4,cooki:5,cookie_sid:5,coordin:[4,5],correct:5,creat:5,create_admin:[1,3],create_admin_if_not_pres:3,create_floor:5,create_us:5,cryptcontext:5,csrf:5,csrf_tokens_equ:5,current:5,current_us:5,currrent:5,custom:5,custom_config:2,daemon:4,data:[4,5],data_received_callback:4,databas:2,datastructur:5,db:[1,3,5],db_user:5,dbmodel:[1,2],dbsrv:2,debug:4,decl_api:5,decor:5,defin:[4,5],delet:5,delete_all_user_sess:5,delete_expired_user_sess:5,delete_floor:5,delete_us:5,deosn:5,depend:[4,5],describ:5,descript:4,devic:[4,5],device_timeout:5,deviceindiscoveryresult:5,dict:[4,5],digi:4,directori:4,disabl:5,discov:5,discover_network:[4,5],discoveri:5,discoveryresult:5,doc:4,document:5,doe:5,dominik:5,dure:4,e:4,each:4,either:5,element:4,ellipsi:5,encod:5,end:[4,5],end_all_user_sess:5,end_user_sess:5,endpoint:5,engin:5,equal:5,err:5,error:[4,5],event:4,exampl:4,example_cli:2,exceed:5,except:[4,5],execut:[4,5],execute_command:5,execute_discover_command:4,execute_one_request:4,execute_parallel_request:4,execute_send_command:4,execute_sequential_request:4,exetut:4,exist:5,expir:5,expire_on_commit:5,fail:5,fals:5,fastapi:5,featureless:5,file:5,finish:4,floor:5,floor_id:5,floorbas:5,floorcreat:5,follow:4,form:4,form_data:5,format:5,from:[4,5],func:5,gener:5,get:[4,5],get_all_floor:5,get_all_us:5,get_all_user_sess:5,get_argu:4,get_current_active_us:5,get_current_sess:5,get_current_session_w:5,get_current_us:5,get_db:5,get_floor_by_id:5,get_floor_image_by_id:5,get_nam:4,get_paramet:5,get_sess:5,get_session_and_refresh:5,get_session_by_session_id:5,get_us:5,get_user_by_id:5,get_user_by_usernam:[1,5],get_user_m:5,given:5,group:4,ha:5,handl:4,handle_xbee_error:5,handler:[4,5],hash:5,header:5,height:5,hexadecim:5,hierarchi:5,howto:4,html:4,http:4,httpexcept:5,i:4,id:[4,5],imag:5,image_media_typ:5,incorrect:5,index:0,insid:4,instanc:5,intend:[4,5],intern:4,invalid:5,inz:5,ip:4,is_valid_admin:5,is_valid_us:5,item:4,its:5,json:4,jsondecodeerror:4,kei:5,kwarg:5,last:5,linux:4,list:[4,5],listen:4,log:5,login:5,logout:5,logout_al:5,logout_all_us:5,m:4,mai:[4,5],main:[2,4],make:[4,5],make_admin:2,make_admin_or_change_password:1,manag:4,map:5,maximum:4,mean:5,media:5,messag:[4,5],message_prefix:5,message_to_send:5,message_websocket:5,messageparseerror:5,messagetoxbe:5,metadata:5,method:[4,5],mode:5,model:[4,5],modifi:5,modify_floor:5,modify_floor_image_by_id:5,modify_us:5,modul:[0,2],modyfi:5,monitor:5,more:5,multipl:4,must:4,name:5,need:5,network:5,new_password:[1,5],newli:5,newlin:4,next:4,ni:5,node:5,node_id:5,nodebas:5,nodecr:5,nodeinfloor:5,none:[4,5],nonetyp:5,notif:[4,5],notifications_thread_func:4,notify_queu:4,notify_serv:2,number:5,oauth2:5,oauth2passwordrequestform:5,obj:4,object:[4,5],obtain:5,occur:[4,5],ok:5,old:5,old_password:5,one:4,open:4,oper:5,option:[4,5],order:5,org:4,orm:[1,3,5],orm_mod:5,other:[4,5],otherwis:[4,5],othewis:5,out:5,outer:4,own:5,owner:5,p:4,packag:2,page:[0,5],parallel:4,parallelli:4,param:5,paramet:[4,5],pars:4,parse_argu:4,parse_command:4,part:[4,5],password:[1,3,5],password_chang:5,password_hash:5,passwordchang:5,patch:5,period:5,place:5,plain:5,port:4,possibl:5,post:5,prefix:5,prepar:2,prepare_parallel_request:4,prepare_sequential_request:4,presenc:4,present:[4,5],prev_data:4,previou:4,previous:4,primari:5,print_network:4,procedur:4,process:4,project:4,properli:4,provid:5,publish:4,purpos:[4,5],put:[4,5],pwd_context:5,pwdcontext:2,py:[4,5],pydant:5,pydmodel:2,python3:4,python:4,queue:4,queue_timeout:4,rais:[4,5],random:5,re:5,read:5,reading_config:5,readingconfig:5,readingconfigbas:5,readingconfiginnod:5,receiv:[2,5],recv_json:4,redirect:5,refresh:5,refresh_period:5,registri:5,relat:5,remain:4,remov:5,request:[4,5],request_respons:5,request_response_serv:2,requir:5,respons:[4,5],response_queu:4,result:5,role:5,root:5,run:[4,5],run_serv:2,s:[4,5],schema:5,script:4,se:4,search:0,second:5,secur:5,send:[4,5],send_b64_data:5,send_json:4,send_messag:5,sender:5,sent:[4,5],separ:4,sequenti:4,serial:4,server:[4,5],server_command:2,servercommand:4,session:[1,3,5],session_id:5,session_idle_tim:5,sessionloc:5,sessionmak:5,set:[4,5],set_floor_imag:5,set_paramet:5,setup:[4,5],should:[4,5],sid:5,singl:5,so:5,sock:4,socket:[4,5],socket_common:2,socketnotifyserv:4,socketrequestresponseserv:4,some:[4,5],sort:5,sould:4,specifi:5,split_result:4,sqlalchemi:[1,3,5],sqlite:5,starlett:5,start:[4,5],start_user_sess:5,startup:4,statu:5,store:5,str:[1,4,5],string:[4,5],studia:5,submodul:2,subscrib:4,success:[4,5],successfuli:5,successfulli:5,suppli:4,suppos:5,system:5,t:5,tcp:4,termin:4,test:[4,5],text:5,than:5,thei:[4,5],them:5,thi:[4,5],thread:4,time:[4,5],time_last_act:5,time_start:5,timeout:5,timeouterror:5,token:5,too:5,tupl:4,two:4,type:[4,5],unify_except:5,union:5,unrel:5,up:4,updat:5,upload:5,uploadfil:5,us:[4,5],usag:4,user:[1,5],user_id:5,user_sess:5,userbas:5,usercr:5,usermodifi:5,usernam:[1,3,5],usersess:5,util:4,valid:[4,5],valu:[4,5],variou:4,venv:4,version:5,wa:[4,5],wai:4,wait:5,webserv:[1,2],websocket:5,websocketmessagesend:5,when:[4,5],whenev:[4,5],which:[4,5],whom:5,whose:5,width:5,window:4,written:5,x:5,xbee:[4,5],xbee_consol:2,xbee_device_connect:2,xbee_device_serv:2,xbee_messag:4,xbee_thread_func:4,xbee_thread_loop:4,xbeedevic:4,xbeedeviceconnect:4,xbeemessageresult:5,xbeenetwork:4,xbeeservererror:5,xbeesrv:2,xbeewait:5,xbeewaitingresult:5,xnet:4,xsrf:5,y:5,yield:5,zigbe:5,zigbee_monitor:5},titles:["Welcome to ZigBee Monitor Server\u2019s documentation!","make_admin module","zigbee-monitor-app","prepare module","receiver package","webserver package"],titleterms:{app:2,config:[4,5],content:[4,5],custom_config:[4,5],databas:5,dbmodel:5,dbsrv:5,document:0,example_cli:4,indic:0,main:5,make_admin:1,modul:[1,3,4,5],monitor:[0,2],notify_serv:4,packag:[4,5],prepar:3,pwdcontext:5,pydmodel:5,receiv:4,request_response_serv:4,run_serv:5,s:0,server:0,server_command:4,socket_common:4,submodul:[4,5],tabl:0,webserv:5,welcom:0,xbee_consol:4,xbee_device_connect:4,xbee_device_serv:4,xbeesrv:5,zigbe:[0,2]}})