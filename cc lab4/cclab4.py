import os
import requests

from azure.mgmt.compute import ComputeManagementClient
from azure.identity import DefaultAzureCredential
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.resource import ResourceManagementClient

##resource group
url = "https://management.azure.com/subscriptions/fe8dae68-fa89-4ee7-b8a4-72d42c38ab52/resourcegroups/PythonAzure?api-version=2021-04-01"
headers = {
    "Authorization": "Bearer removed as its a secret key",
    "Content-type": "application/json"
}

body = { "location":"westeurope",}

response = requests.put(url, headers=headers, json=body)
print(response.json())

##virtual net
url = "https://management.azure.com/subscriptions/fe8dae68-fa89-4ee7-b8a4-72d42c38ab52/resourceGroups/PythonAzure/providers/Microsoft.Network/virtualNetworks/PythonVnet?api-version=2023-05-01"
headers = {
   "Authorization": "Bearer removed as its a secret key",
    "Content-type": "application/json"
}
body = { 
  "properties": {
    "addressSpace": {
      "addressPrefixes": [
        "10.0.0.0/16"
      ]
    },
    "flowTimeoutInMinutes": 10
  },
  "location": "westeurope",
}
response = requests.put(url, headers=headers, json=body)
print(response.json())


##PublicIP
url = "https://management.azure.com/subscriptions/fe8dae68-fa89-4ee7-b8a4-72d42c38ab52/resourceGroups/PythonAzure/providers/Microsoft.Network/publicIPAddresses/PythonIP?api-version=2023-05-01"
headers = {
    "Authorization": "Bearer removed as its a secret key",
    "Content-type": "application/json"
    
}
body = {
    "properties": {
    "publicIPAllocationMethod": "Static",
    "idleTimeoutInMinutes": 10,
    "publicIPAddressVersion": "IPv4"
  },
  "sku": {
    "name": "Standard",
    "tier": "Regional"
  },
  "location": "westeurope",
}
response = requests.put(url, headers=headers, json=body)
print(response.json())


##Subnet
url = "https://management.azure.com/subscriptions/fe8dae68-fa89-4ee7-b8a4-72d42c38ab52/resourceGroups/PythonAzure/providers/Microsoft.Network/virtualNetworks/PythonVnet/subnets/PythonSubNet?api-version=2023-05-01"
headers = {
    "Authorization": "Bearer removed as its a secret key",
    "Content-type": "application/json"
}

body = {
    "properties": {
    "addressPrefix": "10.0.0.0/16"
  },
  "location": "westeurope",
}
response = requests.put(url, headers=headers, json=body)
print(response.json())


##NIC
url = "https://management.azure.com/subscriptions/fe8dae68-fa89-4ee7-b8a4-72d42c38ab52/resourceGroups/PythonAzure/providers/Microsoft.Network/networkInterfaces/PythonNIC?api-version=2023-05-01"
headers = {
    "Authorization": "Bearer removed as its a secret key",
    "Content-type": "application/json"
}
body = {
  "properties": {
    "ipConfigurations": [
      {
        "name": "ipconfig1",
        "properties": {
          "publicIPAddress": {
            "id": "/subscriptions/fe8dae68-fa89-4ee7-b8a4-72d42c38ab52/resourceGroups/PythonAzure/providers/Microsoft.Network/publicIPAddresses/PythonIP"
          },
          "subnet": {
            "id": "/subscriptions/fe8dae68-fa89-4ee7-b8a4-72d42c38ab52/resourceGroups/PythonAzure/providers/Microsoft.Network/virtualNetworks/PythonVnet/subnets/PythonSubNet"
          }
        }
      }
    ]
  },
  "location": "westeurope"
}
response = requests.put(url, headers=headers, json=body)
print(response.json())


##Making VM
url = "https://management.azure.com/subscriptions/fe8dae68-fa89-4ee7-b8a4-72d42c38ab52/resourceGroups/PythonAzure/providers/Microsoft.Compute/virtualMachines/PyAzure?api-version=2023-07-01"
headers = {
   "Authorization": "Bearer removed as its a secret key",
   "Content-type": "application/json"
}
body = {
  "id": "/subscriptions/fe8dae68-fa89-4ee7-b8a4-72d42c38ab52/resourceGroups/PythonAzure/providers/Microsoft.Compute/virtualMachines/PyAzure",
  "type": "Microsoft.Compute/virtualMachines",
  "properties": {
    "osProfile": {
      "adminUsername": "Ryan",
      "secrets": [
        
      ],
      "computerName": "PyVM",
      "linuxConfiguration": {
        "ssh": {
          "publicKeys": [
            {
              "path": "/home/Ryan/.ssh/authorized_keys",
              "keyData": "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCsxP2gmr2VhefmSeB07WtVpOP3IquuVmGgx23jjW7i hA+rJjsUnEA/ uf5a9Qr5tvA3fDlaADTKOn8A54j2KVut1My4soro4YL5ziyiIYjzcn9CCI7EUscB41f1vNQqGuhvJot2 UB4mKRLDgJgtCUzM5jm5Su32yJQa1Zybl9uxyU/ BFnK3JFiynoMl30ADbZYBz6owc4+yFJDy46l0SiAiOJRKlPQmrH10YMnWQyiFrON07b2RJRyPr80 QXt9t+ynWGwJeO5nv1WQZirNVuzze1yWCQtQ8L3ySFSj9LA3Xw2n34NEWUvK6PMGmJf1+Fnx jVzC6KxExKkglXXfcv8N9 paul@paul "
            }
          ]
        },
        "disablePasswordAuthentication": "true"
      }
    },
    "networkProfile": {
      "networkInterfaces": [
        {
          "id": "/subscriptions/fe8dae68-fa89-4ee7-b8a4-72d42c38ab52/resourceGroups/PythonAzure/providers/Microsoft.Network/networkInterfaces/PythonNIC",
          "properties": {
            "primary": "true"
          }
        }
      ]
    },
    "storageProfile": {
      "imageReference": {
        "sku": "16.04-LTS",
        "publisher": "Canonical",
        "version": "latest",
        "offer": "UbuntuServer"
      },
      "dataDisks": [
        
      ]
    },
    "hardwareProfile": {
      "vmSize": "Standard_D1_v2"
    },
    "provisioningState": "Creating"
  },
  "name": "PyAzure",
  "location": "westeurope",
}
response = requests.put(url, headers=headers, json=body)
print(response.json())
