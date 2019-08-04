# Evil Twin tool
Disclaimer. This tool is for informational and educational purposes only.

Tested in kali linux 2019.b

python 2.7

## Introduction

The main goal of the tool is to perform MITM attack. The "victims" can be any AP around (Wifi access point). 
Also the mission was besides attack also defence against this attack.
This tool is mainly target open public wifi networks. 
Our victim will think he is fine and have full access to interenet but he doesn't he logged in malicious hotspot.
From here, you can do alot of things - for example to add bitcoin miner to each request, find a way to make client 
download malicious script and get full access to his computer and so on..

The tool also supports deauth attack (more explained in repository WiFi-Deauthentication-attack-tool)

The attack following by few steps:
#### 1.	Scanning the area, searching for wifi access
#### 2.	Selecting which wifi we want to attack
#### 3.	Sending probe requests / deauth packets cousing struggles there
#### 4.	Raising up fake AP with the same ESSID
#### 5.	Clients will connect to our fake AP
#### 6.	Gmail phishing site will be installed
#### 7.	Secret information will be stored in mysql db

When the client is connected to us, we can sniff information and this is what we doing here, in this example we store gmail phishing site and when client attempt to connect gmail he will actually see the fake page and will enter his details.

## Installation
We used few dependencies 
* dnsmasq
* hostapd
* pyaccesspoint
* scapy

Few things we have to do before running:
1.	Make sure we have /etc/hosts file
2.	Locate gmail folder as it is
3.	Provide mysql db – user,db and table

Make sure you do have network adapter supports monitor mode.
•	Pyaccesspoint edited so make sure to replace it after installation (might work without full installation of pyaccesspoint, didn't check)

## Usage
Launching the program – 

![WhatsApp Image 2019-08-03 at 18 32 05 (1)](https://user-images.githubusercontent.com/28596354/62425818-4356b500-b6e6-11e9-9ae9-5c657fd2d879.jpeg)

We see three options – 
1.	Deauth attack
2.	Evil Twin attack
3.	Evil Twin defend

![WhatsApp Image 2019-08-03 at 18 32 05 (2)](https://user-images.githubusercontent.com/28596354/62425825-579ab200-b6e6-11e9-91bd-f8d302969190.jpeg)

In this case we choose 2 – Evil twin attack
We will see all available networks around, we either can rescan or not.
![WhatsApp Image 2019-08-03 at 18 32 05 (3)](https://user-images.githubusercontent.com/28596354/62425829-608b8380-b6e6-11e9-8537-7f6e8613802f.jpeg)

Choosing our target, if you have two network cards the attack can perfom simultaneously – sending probe requests and raising access point.

![WhatsApp Image 2019-08-03 at 18 32 05 (4)](https://user-images.githubusercontent.com/28596354/62425838-76994400-b6e6-11e9-8db3-f446f6f79783.jpeg)

After this we start attacking our target 

![WhatsApp Image 2019-08-03 at 18 32 05 (5)](https://user-images.githubusercontent.com/28596354/62425844-87e25080-b6e6-11e9-9886-a22298cfd391.jpeg)

Then we start to raise our AP, the tool will do this automatically

![WhatsApp Image 2019-08-03 at 18 32 05 (7)](https://user-images.githubusercontent.com/28596354/62425856-9e88a780-b6e6-11e9-837a-d30128852303.jpeg)

That’s all! Our fake AP is online and we ready for our clients.
When client connects to our access point he manage to get full internet access, but when he will enter gmail (in our case) he will redirected to our phishing page.
It will look like here –

![Screenshot_20190804-121751_Chrome](https://user-images.githubusercontent.com/28596354/62425876-b95b1c00-b6e6-11e9-8527-cbc739aaa5e8.jpg)

Client will believe this is real login page of gmail so he will enter his account information

![Screenshot_20190804-121900_Chrome](https://user-images.githubusercontent.com/28596354/62425884-ca0b9200-b6e6-11e9-88eb-580c4de2da90.jpg)

Finally, client will redirect to account manager of google

![Screenshot_20190804-121839_Chrome](https://user-images.githubusercontent.com/28596354/62425888-d68fea80-b6e6-11e9-84c2-854ed12119ea.jpg)

Going to our database we will see new details added 

![imagephishing](https://user-images.githubusercontent.com/28596354/62425895-f9ba9a00-b6e6-11e9-9f3b-b0cd0f997a17.png)

•	I'm php expert therefore sensitive information about mysql connection may be exposed in php file.


## Defence
The defence is basically based on knowledge that we know our mac addresses of our trusted access point.
The stages –
#### 1.	Adding trusted mac address to mysql db
#### 2.	Execute the third option in the tool and naming the desired AP to defend
#### 3.	If evil twin has been found, we attack him

##### •	You have to setup mysql db & table

The attack here is again, probe request flooding.


### Usage
After we type 3 for entering the defent label,
We have to enter which AP name we would like to defend

![WhatsApp Image 2019-08-03 at 18 32 05 (10)](https://user-images.githubusercontent.com/28596354/62425914-53bb5f80-b6e7-11e9-87ca-f5b238073f28.jpeg)

The tool now will start to scan for access points around

![WhatsApp Image 2019-08-03 at 18 32 05 (11)](https://user-images.githubusercontent.com/28596354/62425928-6fbf0100-b6e7-11e9-917f-233b996308a6.jpeg)

If evil twin found, we will attack the treat 

![Screenshot from 2019-08-04 11-13-35](https://user-images.githubusercontent.com/28596354/62425940-a8f77100-b6e7-11e9-96b7-29f0eef713de.png)

SQL Table 

![Screenshot from 2019-08-04 11-14-57](https://user-images.githubusercontent.com/28596354/62425951-be6c9b00-b6e7-11e9-8084-4c2ead74e5ee.png)




