from cmath import e
import requests
from requests import get
import sys
import urllib
import json
import os
import uuid
import re
import platform
from requests.compat import urljoin
import geocoder
#from notebook import notebookapp
#import IPython


'''
GENEREAL
'''

def check_internet():
        # initializing URL
    url = "https://www.google.com"
    timeout = 10
    try:
        # requesting URL
        request = requests.get(url,
                            timeout=timeout)
        return(True)
    

    except (requests.ConnectionError,requests.Timeout) as exception:
        return(False)

def push_log(data):

    url = "https://vqdpufpf4w.us-east-1.awsapprunner.com/push"

    payload = json.dumps(data)
    headers = {
      'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return(response.text)

def get_exec_machine():
    try:
        mac=':'.join(re.findall('..', '%012x' % uuid.getnode()))
        m=platform.uname()
        sys_info={'execution_machine':{'MAC':mac, 'system':m.system, 'node':m.node, 'release':m.release,'version':m.version, 'machine':m.machine, 'processor':m.processor}}
        return(sys_info)
    except Exception as e:
        return({'execution_machine':{'exception_raised':str(e)}})



def get_loc(ip):
    try:
        #response = requests.get(f'https://ipapi.co/{ip}/json/').json()
        res=geocoder.ip(ip)
        response=res.json
        location_data = {
            "ip": ip,
            "city": response.get("city"),
            "region": response['raw']['region'],
            "country_name": response.get("country"),
            "latitude":response.get("lat"),
            "longitude":response.get("lng"),
            "timezone":response["raw"]["timezone"],
            "utc_offset":response.get("utc_offset"),
            "postal":response.get("postal")
        }
        return location_data
    except Exception as e:
        return({"ip":str(e)})




'''
FOR COLAB
'''
def in_colab():
    try:
        if('google.colab' in sys.modules):
            from notebook import notebookapp
            servers = list(notebookapp.list_running_servers())
            if(servers[0]['hostname']!='localhost'):
                return True
    except:
        return False

def check_colab():
    try:
        global IN_COLAB
        import google.colab
        from notebook import notebookapp
        servers = list(notebookapp.list_running_servers())
        if(servers[0]['hostname']!='localhost'):
            IN_COLAB = True
        else:
            IN_COLAB = False
    except:
        IN_COLAB = False

    return(IN_COLAB)

def get_colab_cell_source(cells,current_index):
    try:
        if(current_index >= 0):
            cell_source=''.join(cells[current_index]['source'])
            if(cells[current_index]["cell_type"]!='code'):
                return({"execution_info":{"cell_no":current_index+1,"last_cell_source":cell_source}})
            if((not cells[current_index]['outputs'])==False and 'text' in cells[current_index]['outputs'][0].keys()):
                
                cell_output=''.join(cells[current_index]['outputs'][0]['text'])
                return({"execution_info":{"cell_no":current_index+1,"last_cell_source":cell_source, "last_cell_output":cell_output}})

            return({"execution_info":{"cell_no":current_index+1,"last_cell_source":cell_source}})
        else:
            return({"execution_info":{"cell_no":current_index+1}})
    except Exception as e:
        return({"execution_info":{"exception_raised":str(e)}})


def get_colab_cell():
    try:
        from google.colab import _message
        # fetch json, stringify
        notebook_json = _message.blocking_request('get_ipynb', request='', timeout_sec=5)

        current_index = None
        l=[]
        # list of all cells in notebook
        cells = notebook_json["ipynb"]["cells"]

        # observation: the cell being executed does not have "executionInfo" in metadata
        # logic: loop through list of all cells, find index without execution info
        for i in range(len(cells)):
            if (("executionInfo" not in cells[i]["metadata"]) and cells[i]["cell_type"]=="code"):
                l.append(i)

        for j in l:
            if(''.join(cells[j]['source'])!=''):
                current_index=j
                break
            else:
                continue

        return(cells, current_index)
    except:
        return(None)
    

def ipynb_name_colab():
    """
    NOTE: works only when the security is token-based or there is also no password
    """
    try:
        import ipykernel
        connection_file = os.path.basename(ipykernel.get_connection_file())
        kernel_id = connection_file.split('-', 1)[1].split('.')[0]
        from notebook import notebookapp
    except Exception as e:
        return({"file_name":"Exception in ipynb_name_colab : "+str(e)})

    for srv in notebookapp.list_running_servers():
        try:
            if srv['token']=='' and not srv['password']:  # No token and no password, ahem...
                req = urllib.request.urlopen(srv['url']+'api/sessions')
            else:
                req = urllib.request.urlopen(srv['url']+'api/sessions?token='+srv['token'])
            sessions = json.load(req)
            for sess in sessions:
                if sess['kernel']['id'] == kernel_id:
                    #print(sess['name'])
                    
                    return ({"file_name": str(sess['notebook']['name']), "path": str(sess['notebook']['path']), "last_activity":str(sess['kernel']['last_activity']), "execution_state":str(sess['kernel']['execution_state'])})

                    #return os.path.join(srv['notebook_dir'],sess['notebook']['path'])
        except Exception as e:
            return({"file_name":"Exception in ipynb_name_colab : "+str(e)})
              # There may be stale entries in the runtime directory
    

def get_ip_colab():

    try:

        import IPython
        from google.colab import output

        IPython.display.display(IPython.display.Javascript('''
        window.kuchbhi=new Promise(resolve => {
            

        function reqListener () {

        var ipResponse = this.responseText
        console.log(ipResponse);
        //return ipResponse

        const req2 = new XMLHttpRequest();
        req2.addEventListener("load",function(){

            //  this blocks runs after req2 and prints whole data    
        console.log(this.responseText)
        //IPython.notebook.kernel.execute(
            //     "json_obj = " + JSON.stringify(this.responseText, null, 4)
            // );
        //document.querySelector("#output-area").appendChild(document.createTextNode(JSON.stringify(this.responseText)));
        //var command= "json_obj = " + JSON.stringify(this.responseText)
        //var kernel = IPython.notebook.kernel;
        //kernel.execute(command);
        resolve(JSON.parse(this.responseText))


        });
        req2.open("GET", "https://ipapi.co/"+JSON.parse(ipResponse).ip+"/json/");
        req2.send();


        }

        const req = new XMLHttpRequest();
        req.addEventListener("load", reqListener);
        req.open("GET", "https://api64.ipify.org?format=json");
        req.send();



        }
        );
        //kuchbhi()
        '''))


        value = output.eval_js('kuchbhi')

        l={"ip":value['ip'],"city":value['city'] ,"region":value['region'] ,"country_name":value['country_name'] ,"latitude":value['latitude'] ,"longitude":value['longitude'] ,"timezone":value['timezone'] ,"utc_offset":value['utc_offset'] ,"postal":value['postal'] }

        return l
    
    except Exception as e:
        return({"ip":"Exception in get_ip_colab : "+str(e)})

'''
FOR SCRIPT
'''
def py_path():
    
    try:
        import __main__
        #print(__main__.__file__)
        file_name = os.path.basename(str(__main__.__file__))
        #return(str(__main__.__file__).split('/')[-1])
        return(file_name)
    except:
        return(None)

def get_py_line():
    try:
        import inspect
        previous_frame = inspect.currentframe().f_back
        #(filename, line_number, function_name, lines, index) = inspect.getframeinfo(previous_frame)
        #(_, filename, line_number, function_name, lines, index) = inspect.stack()[-1]

        #this is assuming there are 2 internal(layer) callers to the function get_py_line()
        (_, filename, line_number, function_name, lines, index) = inspect.getouterframes(previous_frame)[1]
        
        return({"execution_info":{"in_file":filename, "in_module":function_name, "line_no":line_number}})
        #return(outerframe)
    except Exception as e:
        return({"execution_info":{"exception_raised":str(e)}})

    # from inspect import currentframe, getframeinfo
    # frameinfo = getframeinfo(currentframe())
    # print(frameinfo.filename, frameinfo.lineno)

def get_ip_script():
    try:
        ip_address = requests.get('https://checkip.amazonaws.com').text.strip()
        return ip_address
    except:
        return(None)


'''
FOR JUPYTER NOTEBOOK
'''

def has_ipynb_shell():
    """Check if IPython shell is available"""
    try:
        from IPython import get_ipython
        cls = get_ipython().__class__.__name__
        return cls == 'ZMQInteractiveShell'
    except:
        return False


def in_notebook():
    """Check if this code is being executed in a notebook"""
    if not has_ipynb_shell():
        return False
    from ipykernel.kernelapp import IPKernelApp
    return IPKernelApp.initialized()



def ipynb_name_jupyter():
    """ 
        NOTE: works only when the security is token-based or there is also no password
    """
    try:
        import ipykernel
        connection_file = os.path.basename(ipykernel.get_connection_file())
        kernel_id = connection_file.split('-', 1)[1].split('.')[0]
        from notebook import notebookapp
    except Exception as e:
        return({"file_name":"Exception in ipynb_name_jupyter : "+str(e)})
    
    try:

        for srv in notebookapp.list_running_servers():
        
            if srv['token']=='' and not srv['password']: 
                req = urllib.request.urlopen(srv['url']+'api/sessions')
            else:
                req = urllib.request.urlopen(srv['url']+'api/sessions?token='+srv['token'])
            sessions = json.load(req)
            for sess in sessions:
                if  sess['kernel']['id'] == kernel_id:
                    nb_path = sess['notebook']['path']
                    #print(nb_path)
                    #return ntpath.basename(nb_path).replace('.ipynb', '') # handles any OS
                    to_return= {"file_name": str(sess['notebook']['path']), "path": str(sess['notebook']['name']), "last_activity":str(sess['kernel']['last_activity']), "execution_state":str(sess['kernel']['execution_state'])}
                    return to_return
                else:
                    to_return= {"file_name": str(sess['notebook']['path']), "path": str(sess['notebook']['name']), "last_activity":str(sess['kernel']['last_activity']), "execution_state":str(sess['kernel']['execution_state'])}
        return to_return
    except Exception as e:
        return({"file_name":"Exception in ipynb_name_jupyter : "+str(e)})


def check_jupyter_localhost():
    """ 
        NOTE: works only when the security is token-based or there is also no password
    """
    try:
        import ipykernel
        connection_file = os.path.basename(ipykernel.get_connection_file())
        kernel_id = connection_file.split('-', 1)[1].split('.')[0]
        from notebook import notebookapp
    except:
        return False

    for srv in notebookapp.list_running_servers():
        try:
            if srv['token']=='' and not srv['password']: 
                req = urllib.request.urlopen(srv['url']+'api/sessions')
            else:
                req = urllib.request.urlopen(srv['url']+'api/sessions?token='+srv['token'])
            sessions = json.load(req)
            for sess in sessions:
                if  sess['kernel']['id'] == kernel_id: 
                    nb_path = sess['notebook']['path']
                    print(nb_path)
                    if(srv["hostname"]=='localhost'):
                        return(True)
                    #print(sess)
                    #return ntpath.basename(nb_path).replace('.ipynb', '') # handles any OS
                    #return sess
        except Exception as e:
            print(e)
            return False  
    #raise FileNotFoundError("Can't identify the notebook name")


def get_notebook_path_py():
 # Python 3
    try:
        from notebook.notebookapp import list_running_servers
        import ipykernel
        """Get the full path of the jupyter notebook."""
        kernel_id = re.search('kernel-(.*).json',
                            ipykernel.connect.get_connection_file()).group(1)
        servers = list_running_servers()
        for ss in servers:
            response = requests.get(urljoin(ss['url'], 'api/sessions'),
                                    params={'token': ss.get('token', '')})
            if response.status_code == 200:
                for nn in json.loads(response.text):
                    if nn["kernel"] and nn['kernel']['id'] == kernel_id:
                        relative_path = nn['notebook']['path']
                        j= os.path.join(ss['notebook_dir'], relative_path)
                        return(str(j))
                    else:
                        relative_path = nn['notebook']['path']
                        j= os.path.join(ss['notebook_dir'], relative_path)
        return(str(j))
    except:
        return(None)


def get_jupyter_cell_source(cell_index):

    try:
        if(cell_index >= 0):
            import nbformat
            # d=ipynb_name_jupyter()
            # print(d)
            with open(get_notebook_path_py()) as f:
                    nb = nbformat.read(f, as_version=4)
            
            source=nb.cells[cell_index]
            cell_source=source['source']
            # print(cell_source)
            if(source["cell_type"]!='code'):
                return({"execution_info":{"cell_no":cell_index+1,"last_cell_source":cell_source}})
            if('text' in source['outputs'][0]):
                if((not source['outputs'])==False and 'text' in source['outputs'][0].keys()):
                    cell_output=source['outputs'][0]['text']
                    return({"execution_info":{"cell_no":cell_index+1,"last_cell_source":cell_source, "last_cell_output":cell_output}})
            elif((not source['outputs'])==False and 'text/plain' in source['outputs'][0]['data'].keys()):
                cell_output=source['outputs'][0]['data']['text/plain']
                return({"execution_info":{"cell_no":cell_index+1,"last_cell_source":cell_source, "last_cell_output":cell_output}})

            return({"execution_info":{"cell_no":cell_index+1,"last_cell_source":cell_source}})
        else:
            return({"execution_info":{"cell_no":cell_index+1}})
    except Exception as e:
        return({"execution_info":{"exception_raised":str(e)}})

def call_me(j_obj):
#     global j
    log_ipynb=dict()
    log_ipynb['is_jupyter_notebook']=True
    log_ipynb={**log_ipynb, **ipynb_name_jupyter()}
    #print(f"name recieved {log_ipynb}")
    ip,cell_idx=j_obj.split("|")
    #print(f"ip index splitted {log_ipynb}")
    log_ipynb={**log_ipynb, **get_loc(ip)}
    #print(f"location recieved {log_ipynb}")
    log_ipynb={**log_ipynb, **get_exec_machine()}
    #print(f"machine recieved {log_ipynb}")
    log_ipynb={**log_ipynb, **get_jupyter_cell_source(int(cell_idx)-1)}
    #print(f"execution recieved {log_ipynb}")
    push_log(log_ipynb)
    

import asyncio
def get_ip_jupyter():

    try:

        import IPython
        from IPython import get_ipython

        # print("in start")
        # time.sleep(5)

        # global json_obj
        # json_obj='in func'
        # print(json_obj)

        js_query='''
        function reqListener () {

        var ipResponse = this.responseText
        console.log(ipResponse);
        //return ipResponse

        const req2 = new XMLHttpRequest();
        req2.addEventListener("load",function(){

            //  this blocks runs after req2 and prints whole data    
        //console.log(typeof(this.responseText));
        //console.log(JSON.stringify(this.responseText));
        IPython.notebook.kernel.execute(
                "json_obj = " + JSON.stringify(this.responseText)
                );
        //document.querySelector("#output-area").appendChild(document.createTextNode(JSON.stringify(this.responseText)));
        var command= "json_obj2 = " + JSON.stringify(this.responseText)
        var kernel = IPython.notebook.kernel;
        kernel.execute(command);
        var j_obj=JSON.parse(this.responseText)["ip"]+"|"+cell_idx;
        console.log(j_obj)
        var jj=JSON.stringify(this.responseText);
        kernel.execute("import projectpro");
        kernel.execute("projectpro.call_me('" + j_obj + "')");
        return JSON.parse(this.responseText)


        });
        req2.open("GET", "https://ipapi.co/"+JSON.parse(ipResponse).ip+"/json/");
        req2.send();


        }

        //var kernel = IPython.notebook.kernel;
        //var j_obj="6.9.6.9";
        //kernel.execute("import javaRun");
        //kernel.execute("javaRun.call_me('" + j_obj + "')");

        var output_area = this;
        // find my cell element
        var cell_element = output_area.element.parents('.cell');
        // which cell is it?
        var cell_idx = Jupyter.notebook.get_cell_elements().index(cell_element);
        console.log(cell_idx)

        const req = new XMLHttpRequest();
        req.addEventListener("load", reqListener);
        req.open("GET", "https://api64.ipify.org?format=json");
        req.send();
        '''

        #p=IPython.display.Javascript(js_query)
        # print(p)

        get_ipython().run_cell_magic('javascript','',js_query)

        return({"log status":"async_process"})
        # return(json_obj)
         
    except:
        return(dict())



#print(push_log({"test_list":[1,2,"3a"]}))