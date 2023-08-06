import projectpro.utils as utils



def checkpoint():
    log_data=dict()
    
    try:
        
        if(utils.check_internet()==False):
            print("No Internet Connection...")
            return
        if(utils.in_colab()):
            print("Detected Colab Notebook...")
            print("Checkpoint Initialization... ")
            log_data['is_colab']=True
            log_data={**log_data, **utils.ipynb_name_colab()} #file_name, path, last_activity, execution_state
            log_data={**log_data, **utils.get_ip_colab()}
            log_data={**log_data, **utils.get_exec_machine()}

            cells_index=utils.get_colab_cell()
            if(cells_index!=None):
                exec_details=utils.get_colab_cell_source(cells_index[0],cells_index[1]-1)
                log_data={**log_data, **exec_details}
            response=utils.push_log(log_data)
            print(response)
            return
        
        
        elif(utils.py_path()!=None):
            print("Detected PY Script...")
            print("Checkpoint Initialization... ")
            log_data['file_name']=utils.py_path()
            ip_script=utils.get_ip_script()
            log_data={**log_data, **utils.get_loc(ip_script)}
            log_data={**log_data, **utils.get_exec_machine()}
            log_data={**log_data, **utils.get_py_line()}
            response=utils.push_log(log_data)
            print(response)
            return

        elif(utils.in_notebook()):
            print("Detected Jupyter Notebook...")
            print("Checkpoint Initialization... ")

            log_data={**log_data, **utils.ipynb_name_jupyter()}
            ip=utils.get_ip_script()
            #print(f"ip index splitted {log_ipynb}")
            log_data={**log_data, **utils.get_loc(ip)}
            #print(f"location recieved {log_ipynb}")
            log_data={**log_data, **utils.get_exec_machine()}
            #print(f"execution recieved {log_ipynb}")
            utils.push_log(log_data)

            print(utils.get_ip_jupyter())
            return({'log status': 'success'})

        else:
            return({'log status': 'failure'})
    except Exception as e:
        print(e)
        return({'log status': 'failure'})
        






            
            

        













        













#     js_query='''
#     function reqListener () {

#     var ipResponse = this.responseText
#     console.log(ipResponse);
#     //return ipResponse

#     const req2 = new XMLHttpRequest();
#     req2.addEventListener("load",function(){

#         //  this blocks runs after req2 and prints whole data    
#     console.log(this.responseText)
#     //document.querySelector("#output-area").appendChild(document.createTextNode(JSON.stringify(this.responseText)));

#     var command= "json_obj = " + JSON.stringify(this.responseText)
#    var kernel = IPython.notebook.kernel;
#    kernel.execute(command);
#     return JSON.stringify(this.responseText)


#     });
#     req2.open("GET", "https://ipapi.co/"+JSON.parse(ipResponse).ip+"/json/");
#     req2.send();


#     }

#     const req = new XMLHttpRequest();
#     req.addEventListener("load", reqListener);
#     req.open("GET", "https://api64.ipify.org?format=json");
#     req.send();
#     '''

#     p=IPython.display.Javascript(js_query)
#     return p
