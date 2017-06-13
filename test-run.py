#!/usr/bin/python

#<<author: cooldharma06@gmail.com>>
# Used for verifying the initial check of cloud setup
#  do following process: 1. create netowrk, router, vm, ping vm
#  if communication not established means debug the interfaces in each level
#
#




import subprocess
import time
import shlex
import sys


def subprocess_call(command):
    try:
        p = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE)
        out,err = p.communicate()
        return out
    except Exception as e:
        print("Error occured..",e)
        return 0

def create_network(net_name,net_range):
  try:
    p = subprocess.Popen(["openstack","network","create",net_name], stdout=subprocess.PIPE)
    out, err = p.communicate()
    print(out)
    print(net_name +"got created")
    time.sleep(2)
    p = subprocess.Popen(["openstack","subnet","create","--network",net_name,"--subnet-range",net_range+"/24","subnet"+net_name],stdout=subprocess.PIPE)
    out,err = p.communicate()
    print(out)
    print("subnet"+net_name+" got created")

    p = subprocess.Popen(shlex.split("openstack router add subnet rtr-test1-test2 subnet"+net_name), stdout=subprocess.PIPE)
    out,err = p.communicate()
    print(out)
    print("Interface subnet%s connected to router"%net_name)

  except Exception as e:
    print("Error occured",e)




def router():    
  try:
    p = subprocess.Popen(shlex.split("openstack router create rtr-test1-test2"), stdout=subprocess.PIPE)
    out,err = p.communicate()
    print("Router for test1 and test2 - got created")


  except Exception as e:
    print("Error occured",e)



def secgroup_rules_add():
    try:
        p = subprocess.Popen(shlex.split("openstack security group create test1"),stdout=subprocess.PIPE)
        out,err = p.communicate()

        p1 = subprocess.Popen(shlex.split("openstack security group rule create --protocol icmp test1"), stdout=subprocess.PIPE)
        out,err = p1.communicate()
  
        p2 = subprocess.Popen(shlex.split("openstack security group rule create --protocol tcp --dst-port 22:22 test1"), stdout=subprocess.PIPE)
        out,err = p2.communicate()
        
        print("TEST security rules and group - got created")
    except Exception as e:
        print("Error occured",e)
    



"""def create_vm():
    try:
"""


def cleanup():
   
    #TODO : router remove interface and router delete have to add
    

    try:
        p = subprocess.Popen(["openstack","network","list","-c","ID"], stdout=subprocess.PIPE)
        p2 = subprocess.Popen(shlex.split('awk "{print $2}"'),stdin=p.stdout,
                             stdout=subprocess.PIPE,stderr=subprocess.PIPE)

        p.stdout.close() # Allow proc1 to receive a SIGPIPE if proc2 exits.
        out,err=p2.communicate()
    except Exception as e:
        print("ERROR occured",e)
#   print(out)
#   print(type(out))
    network_id=out.split('\n')
    network_id = [ ele for ele in network_id if ((ele!='ID') and (ele != ''))]
    print(network_id)

    result = subprocess_call("openstack router remove subnet rtr-test1-test2 subnettest-net1")
    result2 = subprocess_call("openstack router remove subnet rtr-test1-test2 subnettest-net2")
    print("Interface removed from router rtr-test1-test2")
   
    router_del = subprocess_call("openstack router delete rtr-test1-test2")
    print(router_del)
 
    for i in network_id:
        try:
            p=subprocess.Popen(["openstack","network","delete",i],stdout=subprocess.PIPE)
            out,err=p.communicate()
        except Exception as e:
            print("ERROR occured",e)

    try:
        p = subprocess.Popen(shlex.split("openstack security group delete test1"),stdout=subprocess.PIPE)
        out,err = p.communicate()

        print("TEST security rules and group - got deleted")
    except Exception as e:
        print("Error occured",e)

  
    print("All test data got deleted")



if __name__ == '__main__':
     print(sys.argv)
     if sys.argv[1] == "--cleanup":
         cleanup()
     elif sys.argv[1] == "--all":
         router()
         create_network("test-net1","10.10.10.0")
         create_network("test-net2","11.11.11.0")
         secgroup_rules_add()
         cleanup()
     else:
         print("Required arguments 1.--cleanup 2.--all")
