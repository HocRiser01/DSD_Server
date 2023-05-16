| version | Created by   | Date      |
| ------- | ------------ | --------- |
| 1.0     | Zhang Zhenwu | 5/14/2023 |

version 1.0 created by Zhang Zhenwu,5/14/2023

# 1. Introduction

## 1.1. Intended Audience and Purpose

This document is intended to provide information guiding the installation and development process, ensuring that all system requirements are met. The following entities may find the document useful:

Primary Customer - This page will detail all of the application requirements as understood by the production team. The customer should be able to determine that their requirements will be correctly reflected in the final product through the information found on this page.

User - A prospective user will be able to use this document to identify the main functionality included in the application. Furthermore, the application will have a set of system requirements before the application can be run. Details regarding these requirements can be found here.

Development Team - Details of specific requirements that the final software build must include will be located here. Developers can use this document to ensure the software addresses each of these requirements.

QA Team - By developing testing procedures founded in the system requirements, the QA Team can create a comprehensive testing regimen that will guarantee requirements are met.

## 1.2. How to use the document

# 2. System Design

## 2.1. Context

- Operating System:Linux
- Relational Database System:PostgreSQL
- Application Container Engine:Docker
- Android:

<table><tbody><tr><td><strong>Android Version</strong></td><td><strong>Name</strong></td><td><strong>API Level</strong></td></tr><tr><td>Android 14</td><td>U</td><td>34</td></tr><tr><td>Android 13</td><td>T</td><td>33</td></tr><tr><td>Android 12L</td><td>S</td><td>32</td></tr><tr><td>Android 12.0</td><td>S</td><td>31</td></tr><tr><td>Android 11.0</td><td>R</td><td>30</td></tr><tr><td>Android 10.0</td><td>Q</td><td>29</td></tr><tr><td>Android 9.0</td><td>Pie</td><td>28</td></tr><tr><td>Android 8.1</td><td>Orea</td><td>27</td></tr><tr><td>Android 8.0</td><td>Orea</td><td>26</td></tr></tbody></table>

- python= 3.7
- CUDA = 11.7
- pytorch =1.13.0

## 2.2. Design Pattern

## 2.3. Architecture

### 2.3.1 Componet Diagram

![](https://github.com/HocRiser01/DSD_Server/blob/main/public/images/1.jpg)
![](https://github.com/HocRiser01/DSD_Server/blob/main/public/images/1.jpg)

# 3. Module Interface Design

## 3.1. AI part interface

### 3.1.1. get_train

```python
def get_train(uid:string,train_data_set:ndarray[n,5,56],dtype=float64)->return acc
```

This function is to specialize training on a specific user's data.

uid represents the user id,

and train_data_set represents the specialization data for this user. It is a ndarray and it's size is$[n556]$，n means n datas,every data have 5 frames and every frame have 6∗9 sensor datas and one timestamps and one label.

When data error ,this funtion will throw Exception("data error")

When GPU not available,,this funtion will throw Exception("GPU error")

Return acc, which represents the training accuracy

It is a Sample：

```python
uid="zhang_asdsa"
train_data_set=np.array([[1.0,for x in range(1,56)]*5])
print(get_train(uid,train_data_set))
#the console outputs 0.92,mean acc=92%
```

### 3.1.2. get_predict

```python
def get_predict(uid:string,flow:ndarray[5,55],dtype=float64,opt:int,default)->return int
```

This function is to predict the current state of the user for a particular user and an array of prediction data.

uid represents the number of the user.

flow is a ndarray and it's size is$[5*55]$，representing the numerical values of the six sensors in 5 frames of 1 second and the current timestamps , opt=0 for calling the specialized model, and opt=1 for calling the generalization model. opt is default,you can not write it and we can decide it by function self.

For the return values: 0-6 means 7 actions, negative means an exception occurred, -1 means that the specialization model is missing and the get_train function should be called, -2 means that the data is abnormal.

It is a Sample：

```python
uid="zhang_asdsa"
flow=np.array([1.0 ,for x in range(1, 56)]*5)
print(get_predict(uid,flow)) 
# The console outputs 0, indicating that the prediction for this second is sitting,and opt is default
```

### 3.1.3. clear

```python
def clear(uid:string)->void
```

The purpose of this function is to clear the specialization model for that user.

uid represents the number of the user,and this function does not return a value.

It is a Sample：

```python
uid="zhang_asdsa"
clear(uid) 
# The user specialization model is cleared
```

### 3.1.4. get_train_time

```python
def get_train_time(train_data_set: ndarray[n,5,56],dtpye=float64) -> int 
#(The return time is in seconds)
```

This function predicts the time to train.The input is the train data set and it's define is same with function: get_train and the output is the estimated time to train in seconds

It is a Sample：

```python
uid="zhang_asdsa"
train_data_set=np.array([[1.0 ,for x in range(1, 56)]*5])
print(get_train_time(train_data_set))
# The console outputs 10,mean need 10 seconds to train
```

### 3.1.5.get_progress

```python
def get_progress(uid:string,train_data_set: ndarray[n,5,56],dtype=float64)-> ndarray[7],dtype=float64
```

This function show the preson data Collection progress,uid represents the user id, and train_data_set is same with function get_train.

Returns a seven-tuple representing the collection progress of each tag

It is a Sample：

```python
uid="zhang_asdsa"
train_data_set=np.array(null)
print(get_progress(uid,train_data_set))
#The console outputs [0,0,0,0,0,0,0],mean every progress is 0
```

## 3.2. Database part interface

### 3.2.1. AddUser

```python
AddUser(user_id:string,password:string,birthday:string,email:string,phone_number:string) -> void
```

Create a new user and his/her user information in the database with input information.

- throw Exception("reduplicated user_id error")
- throw Exception("unknown error")

### 3.2.2. LoginUser

```python
LoginUser(user_id:string,password:string) -> void
```

Check if the user ID and password used to login are correct, if correct, handle the login process.

- throw Exception("user_id or password error")
- throw Exception("user not exists error")
- throw Exception("unknown error")

### 3.2.3. DeleteUser

```python
DeleteUser(user_id:string)->void
```

Delete a user's information from the database.

- throw Exception("user not exists error")
- throw Exception("unknown error")

### 3.2.4. UpdateUserInfo

```python
UpdateUserInfo(user_id:string,birthday:string,phone_number:string,email:string)->void
```

Update a user's information in the database using input information.

- throw Exception("user not exists error")
- throw Exceprtion("unknown error")

### 3.2.5. GetUserInfo

```python
GetUserInfo(user_id:string)->birthday:string,phone_number:string,email:string
```

Return user information associated with the input user ID.

- throw Exception("user not exists error")
- throw Exception("unknown error")

### 3.2.6. GetMotionData

```python
GetMotionData(user_id:string)->motion_data:np.array((n,5,56))
```

Return motion data associated with the input user ID.
n: the seconds
5:  5 frames per second
56: 54 data+1 time_stamp+1 label

- throw Exception("user not exists error")
- throw Exception("unknown error")

### 3.2.7. CleanData

```Python
CleanData(np.array((k,55))) -> Cleaned_Online_Motion_Data:np.array((5,55))
```

Clean the collected motion data online and return the  result (for prediction).
k<=5
55: 54 data+ 1 timestamp

- throw Exception("invalid input error")

### 3.2.8. DeleteMotionRecord

```python
DeleteMotionRecord(user_idLstring,create_time:string)->void
```

Delete the motion record associated with the input user ID, created at the input creation time, from the database.

- throw Exception("user not exists error")
- throw Exception("motion record not exists error")
- throw Exception("unknown error")

### 3.2.9. SaveMotionData

```python
SaveMotionData(user_id:string,create_time:string,label:int,data:dict)->void
```

Insert collected motion data into the database.
n: the seconds
5:  5 frames per second
55: 54 data+1 time_stamp
k<=5

- throw Exception("user not exists error")
- throw Exception("unknown error")

### 3.2.10. GetDeviceInfo

```python
GetDeviceInfo(user_id:string)->ip:string,port:int
```

Return device information associated with the input user ID.

- throw Exception("user not exists error")
- throw Exception("unknown error")
- throw Exception("device not exists error")

### 3.2.11. BindDevice

```python
BindDevice(user_id:string,ip:string,port:string)->void
```

Insert device information into the database, and bind the device to the user with the input user ID.

- throw Exception("user repeat binding error")
- throw Exception("device repeat binding error")
- throw Exception("user_id not exists error")
- throw Exceprtion("unknown error")

### 3.2.12. UnbindDevice

```python
UnbindDevice(user_id:string)->void
```

Unbind the device previously binded to the user with the input user ID, and delete its device information from the database.

- throw Exception("device not exists error")
- throw Exception("unknown error")

### 3.2.13. GetMotionrecord

```python
GetMotionRecord(user_id:string)->label:list[int],create_time:list[string],last_time:list[string]
```

Return the list of all motion records associated with the input user ID.

- throw Exception("user_id not exists error")
- throw Exception("unknown error")

### 3.2.14. ModifyMotionRecord

```python
ModifyMotionRecord(user_id:string,create_time:string,label:int)->void
```

Change the label of the motion record associated with the input user ID, and created at the input creation time.

- throw Exception("user_id not exists error")
- throw Exception("label invaild error")
- throw Exception("unknown error")

## 3.3. Web part interface

### 3.3.1. Login

```javascript
/**
* A administrator login the management system
* @param {str}  email
* @param {str}  password
**/

function Login(email, password) 
```

```json
// JSON format
{email, password}
```



### 3.3.2. Logout

```javascript
/**
* A administrator logout the management system
* @param {int} userId
**/

function Login(userId) 
```

### 3.3.3. Check Login

```js
function checkLogin()
```

### 3.3.4. add user

```javascript
/**
* add a new user
* @param {int}  userId
* @param {str}  name
* @param {str}  email
* @param {str}  password
* @param {date} birthday
**/

function addUser(userId, name, email, password, birthday) 
```

```json
//JSON format I send
{
    "userID":
    	{
            "name",
            "email",
            "password",
            "birthday"
        }
    	
}
```



### 3.3.5. edit user

```js
/**
* modify the user's information
* @param {int}  userId
* @param {str}  name
* @param {str}  email
* @param {str}  password
* @param {date} birthday
**/

function editUser(userId, name, email, password, birthday) 
```

```json
//JSON format I send
{
    "userID":
    	{
            "name",
            "email",
            "password",
            "birthday"
        }
    	
}
```



### 3.3.6. delete user

```js
/**
* delete the user's information
* @param {int}  userId
**/

function delUser(userId) 
```

```json
// json I send
{"userID"}
```

### 3.3.7. Filter data

 ```js
/**
* choose the data by userId or userName or both
* @param {int} userId
* @param {str} userName
**/

function filterData(userId, userName)
 ```

```json
//JSON I send
{"userID", "userName"}
default the first person
//JSON I get
{
    "starttime",
    "endtime",
    sensor1:
		{
            x,
            y,
            z
        },
    sensor2:
		{
            x,
            y,
            z
        },
    sensor3:
        {
            x,
            y,
            z
        },
    sensor4:
		{
            x,
            y,
            z
        },
    sensor5:
		{
            x,
            y,
            z
        },
    sensor6:
		{
            x,
            y,
            z
        }
}
```



### 3.3.8. Get data

```js
/**
* get the new data in the database
* @param {int} userId
* @param {str} userName
**/

function getData(userId, userName)
```

```json
//JSON I send
{"userID", "userName"}
default the first person
//JSON I get
{
    "starttime",
    "endtime",
    sensor1:
		{
            x,
            y,
            z
        },
    sensor2:
		{
            x,
            y,
            z
        },
    sensor3:
        {
            x,
            y,
            z
        },
    sensor4:
		{
            x,
            y,
            z
        },
    sensor5:
		{
            x,
            y,
            z
        },
    sensor6:
		{
            x,
            y,
            z
        }
}
```

# 4. Detailed Design

## 4.1. Server Detailed Design

### Use Cases

Case: Input from Algorithm part

Case: Output to Algorithm part

Case: Input from Web part

Case: Output to Web part

Case: Input from Embeded System part

Case: Interaction with Mobile part

Case: Input from Database part

Case: Output to Database part

#### Case : Input from Algorithm part

- version: 1
- Created: March 23
- Authors: Hu Jianzheng
- Source: Server
- Actors: Server
- Goal: Exchange data with the AI algorithm part of the project.
- Summary: Server transmit the data collected to the AI part. After calculation in the AI part, the server part get the data and information from AI part.
- Trigger: The Server part PUSH(HTTP) the package to the Algorithm part, which include the information and the training data.
- Frequency: Irregular.
- Precondition: The Server part has got at least one complete package of training data from the Database. 
- Postconditions: No

![img](https://doc.ciel.pro/uploads/330b3aef93b0cd2a1c8ba5418.png)

##### Basic Flow

| Actor                                                        | System                                                    |
| ------------------------------------------------------------ | --------------------------------------------------------- |
| Receive Server-to-Algorithm Request <Dataset ID，the number of record in this  Dataset> |                                                           |
|                                                              | Check the validity of the ID and the size of the package. |
|                                                              | Fetch dataset from the database                           |
|                                                              | Send the training dataset package with the certain name.  |
| Send the completion signal of the Server System.             |                                                           |

##### Alternative Flow

| Actor | System |
| ----- | ------ |
|       |        |
|       |        |
|       |        |
|       |        |
|       |        |

#### Case : Output to Algorithm part

- version: 1
- Created: March 23
- Authors: Hu Jianzheng
- Source: Server
- Actors: Server
- Goal: Exchange data with the AI algorithm part of the project.
- Summary: Get the output of training model of AI part.
- Trigger: The AI algorithm has finished model training and got a reasonable output result.
- Frequency: Irregular.
- Precondition: The Server got a valid name whose data is prepared to be transmitted by the AI part.
- Postconditions: No

![](https://doc.ciel.pro/uploads/330b3aef93b0cd2a1c8ba541e.png)

- Basic Flow

| Actor                                            | System                                        |
| ------------------------------------------------ | --------------------------------------------- |
| Receive Algorithm-to-Server Request              |                                               |
|                                                  | Exchange the results from the Algorithm part. |
| Send the completion signal of the Server System. |                                               |
|                                                  |                                               |
|                                                  |                                               |

##### Alternative Flow

| Actor | System |
| ----- | ------ |
|       |        |
|       |        |
|       |        |
|       |        |
|       |        |

#### Case: Input From Web part

- version: 1
- Created: March 23
- Authors: Hu Jianzheng
- Source: Web
- Actors: Server
- Goal: Get the instruction from the Web part triggered by the user.
- Summary: When the user clicked the button on the webpage, get certain instructions from the Web part and deal with them.
- Trigger: The Web part gets the instructions from the user.
- Frequency: Irregular.
- Precondition: The Web part get the operation from the user which needs to send to server to deal with.
- Postconditions: No

##### Basic Flow

| Actor                                                  | System                                                      |
| ------------------------------------------------------ | ----------------------------------------------------------- |
| Receive the requests of Web part.                      |                                                             |
|                                                        | Build connections between the Web part and the Server part. |
|                                                        | The Client send HTTP PUSH to send message to the Server.    |
| The Server part get the instruction from the Web part. |                                                             |
| The Server stop the connection after exchanging data.  |                                                             |
|                                                        |                                                             |
|                                                        |                                                             |

##### Alternative Flow

| Actor | System |
| ----- | ------ |
|       |        |
|       |        |
|       |        |
|       |        |
|       |        |

#### Case: Output to Web part

- Version: 1
- Created:  March 23
- Authors: Hu Jianzheng
- Source: Server
- Actors: Server
- Goal: Show the data.
- Summary: When there is data waiting to be sent, the Server part PUSH(HTTP) the data to the Web part.
- Trigger: Get the data from the Database or Embedded System part.
- Frequency: Irregular.
- Precondition: No
- Postconditions: No

##### Basic Flow

| Actor                            | System                           |
| -------------------------------- | -------------------------------- |
| Server send request to send data |                                  |
| Server build the connection      |                                  |
|                                  | Web build connection with Server |
|                                  | Web receive data from the Server |
|                                  | Return complete signal           |
| Server get complete signal       |                                  |

##### Alternative Flow

| Actor | System |
| ----- | ------ |
|       |        |
|       |        |
|       |        |
|       |        |



#### Case: Input From Embedded System part

- version: 1
- Created: March 23
- Authors: Hu Jianzheng
- Source: Server
- Actors: Embeded System
- Goal: Get the data collected from Embeded System part.
- Summary: The Embeded System send all the collected data which are structured to the Server, and Server push them into Database.
- Trigger: The Embeded System has collected enough data.
- Frequency: Irregular.
- Precondition: The connection between Server part and Embeded System part is built.
- Postconditions: No

##### Basic Flow

| Actor                                                   | System                                                      |
| ------------------------------------------------------- | ----------------------------------------------------------- |
| Receive the requests of Embedded System part.           |                                                             |
|                                                         | Build connections between the Web part and the Server part. |
|                                                         | Receive the data from Embeded System.                       |
|                                                         | Complete the transmission.                                  |
| Receive the completion signal from the Embedded System. |                                                             |
|                                                         |                                                             |
|                                                         |                                                             |

##### Alternative Flow

| Actor | System |
| ----- | ------ |
|       |        |
|       |        |
|       |        |
|       |        |
|       |        |

#### Case: Interaction with Mobile part

- version: 1
- Created: March 23
- Authors: Hu Jianzheng
- Source: Server
- Actors: Mobile
- Goal: Exchange data between Server and Mobile.
- Frequency: Irregular.
- Precondition: The connection between Server and the Mobile has been built.
- Postconditions: No

##### Basic Flow

| Actor                                                     | System                                                       |
| --------------------------------------------------------- | ------------------------------------------------------------ |
| Receive the requests of Web part.                         |                                                              |
|                                                           | Build connections between the Mobile part and the Server part. |
|                                                           |                                                              |
| The Server receive data from and send data to the Mobile. |                                                              |
| The Server stop the connection after exchanging data.     |                                                              |
|                                                           |                                                              |
|                                                           |                                                              |

##### Alternative Flow

| Actor | System |
| ----- | ------ |
|       |        |
|       |        |
|       |        |
|       |        |
|       |        |

#### Case: Input From Database part

- version: 1
- Created: March 23
- Authors: Hu Jianzheng
- Source: Web
- Actors: Server
- Goal: Get the data from Database.
- Summary: Get the data from Database which is going to be sent to Web or Algorithm part.
- Frequency: Irregular.
- Precondition: The data is well-prepared by the Database and is going to be sent to Server.
- Postconditions: No

##### Basic Flow

| Actor                                                      | System                                           |
| ---------------------------------------------------------- | ------------------------------------------------ |
| Build connection between the Server and the Database part. |                                                  |
|                                                            | The Databased part send data to the Server part. |
|                                                            |                                                  |
| Receive data from the Dataset part.                        |                                                  |
| Send completion signal when finished.                      |                                                  |
|                                                            |                                                  |
|                                                            |                                                  |

##### Alternative Flow

| Actor | System |
| ----- | ------ |
|       |        |
|       |        |
|       |        |
|       |        |
|       |        |

#### Case: Output to Database part

- version: 1
- Created: March 23
- Authors: Hu Jianzheng
- Source: Server
- Actors: Server
- Goal: Send the data collected by Embedded System and other parts to the Database.
- Frequency: Irregular.
- Precondition: The data is structured and prepared by the Embedded System and the connection between the Server and Database part is built.
- Postconditions: No

##### Basic Flow

| Actor                                        | System                            |
| -------------------------------------------- | --------------------------------- |
| Send the requests to send data to Database   |                                   |
|                                              | Dataset Receive data from Server. |
|                                              | Dataset send completion signal.   |
| Receive the comletion signal after finished. |                                   |
|                                              |                                   |
|                                              |                                   |
|                                              |                                   |

##### Alternative Flow

| Actor | System |
| ----- | ------ |
|       |        |
|       |        |
|       |        |
|       |        |
|       |        |

## 4.2. Client(Android) Detailed Design

### Class diagram

![](3.png)

### Method Explanation

#### <p align = "center">User</p>

* __setUserInfo(string, string, string, Date):bool__ - This method should allow the user to update it's information. It takes as parameters three strings, representing the user's name, email and phone Number, and a Date representing the user's birthday. This method returns a bool representing it's success.
    </br> Ex:

```csharp
public bool setUserInfo(string name, string email, string phoneNumber, Date birthday)
	{
		if(!this.getLogged()) return false;
		
		using StringContent jsonContent = new(
        	JsonSerializer.Serialize(new
        	{
			type = "ChangeUserInfo",
			id = $"{this.getId()}",
			password = $"{this.getPassword()}",
            		username = $"{name}",
			email = $"{email}",
            		phoneNumber = $"{phoneNumber}",
			birthday = $"{birthday.toString()}"
        	}),
        	Encoding.UTF8,
        	"application/json");
		using HttpResponseMessage response = await httpClient.PostAsync(apiURL, jsonContent);
		if((int)response.StatusCode==404)return false; //Deal with patch failure (deal with other status codes)
		
		this.setName(name);
		this.setEmail(email);
		this.setPhoneNumber(phoneNumber);
		this.setBirthday(birthday);
		
		return true;
	}
```


* __updatePassword(string, string):bool__- This method is used to update the user's password when they're already logged into their account. The user inserts their previous password, and the password they wish to change it to. This method should compare the current user password, stored in the database, with the hash of the text in the previous user password text box, and if they match it should make a PUT/PATCH call to the user database API changing the previous password to the new one(the hash of the text in the new password text box). This method takes as parameter two strings, one storing the value the user wrote in the previousePassword textbox, and the other storing the value the user wrote in the newPassword textbox. This method returns a bool representing it's success.
    </br> Ex:

```csharp
public bool updatePassword(string newPassword,string oldPassword)//newPassword and oldPassword are the values inserted by the user in the textboxes
	{
		byte[] passwordBytes = Encoding.UTF8.GetBytes(oldPassword);
            	byte[] passwordHashBytes = SHA256.HashData(passwordBytes);//whatever hasing algorithm is used for the passwords in database
		string textBoxPreviousPassword = BitConverter.ToString(passwordHashBytes)
		if(user.getPassword() !=  oldPassword)
		{
			//Warn user wrong Password
			return;
		} 

		using StringContent jsonContent = new(
        	JsonSerializer.Serialize(new
        	{
            		password =  $"{newPassword}"
        	}),
        	Encoding.UTF8,
        	"application/json");
		using HttpResponseMessage response = await httpClient.PatchAsync(userURL + "/" + this.getId(), jsonContent);
		if((int)response.StatusCode==404) return false //Deal with patch failure (deal with other status codes)
		
		this.setPassword(password);
		return true;
	}
```

* __getUserGuide():File__ - This method should retrieve from user's phone a file explaining how the application operates and should be used, in order to provide some explanations and clarify some doubts they may have. This method returns a file containing that information, or null in the case of failure to retrieve it.

#### <p align="center">Authentication</p>

* __login(User, string, string):bool__ - This method should allow a user to login into their previously created account. If the credentials inserted by the user are associated with an existing account that's stored in the user database, and the login process is successful, this method updates the local user instance with the other information stored about that particular user in the user database. It takes as parameters two strings, one storing the value the user wrote in the id textbox in the login view, and the other one storing the value they wrote in the password textbox in the login view, and a User instance. This method should return false in the case of login failure and true in the case of success.
    </br> Ex:

```csharp
public static bool login(User user, string id, string password)
	{
				
		using StringContent jsonContent = new(
        	JsonSerializer.Serialize(new
        	{
			type = "Login",
			id = $"{id}",
			password = $"{password}"
        	}),
		Encoding.UTF8,
        	"application/json");
		
		using HttpResponseMessage response = await httpClient.PostAsync(apiURL, jsonContent);
		
		if(response.StatusCode == "404") return false; //We could verify for more status codes, displaying different messages

		user.setId(id);
		user.setPassword(password);
		
		using HttpResponseMessage getResponse = await httpClient.GetAsync(userURL + "?id=" + id, jsonContent);				
		var jsonResponse = await getResponse.Content.ReadAsStringAsync();		
		JsonNode jsonNode = JsonNode.Parse(jsonResponse);
		
		user.setLogged();
		user.setEmail(jsonNode["email"]);
		user.setPhoneNumber(Convert.ToInt32(jsonNode["phoneNumber"]));
		user.setUserName(jsonNode["userName"]);
		string birthday=jsonNode["birthday"];//verify if is null
		user.setBirthday(SimpleDateFormat("dd/MM/yyyy").parse(birthday););
		
		return true;
	}
```

* __logout(User)__ : bool - This method is called when the user wishes to logout of their account, deleting the User instance. It should return false in the case the user received isn't logged in, and true in case of success.
    </br> Ex:

```csharp
public static bool logout(User user)
	{
		if(!user.getLogged()) return false
		user.setLogged(); // if fails return false 
		user.setId(NULL);
		user.setEmail(NULL);
		user.setPassword(NULL);
		user.setEmail(NULL);
		user.setuserName(NULL);
		user.setBirthday(NULL);
		
		return true
	}
```

* __register(User, string, string):bool__ - This method should allow a user to register a new account for the application. If the credentials inserted by the user for the new account are accepted, and a new account is registered succesfully, this method updates the local User instance, storing in it the id and password. This method takes as parameter two strings, one storing the value the user wrote in the id textbox, and the other one storing what they wrote in the password textbox in the register view and an instance of User. This returns true in the case of registar success and false in the case of failure.

</br> Ex:

```csharp
public static bool register(User user, string id, string password)
	{		
		using StringContent jsonContent = new(
        	JsonSerializer.Serialize(new
        	{
			type = "Register",
			id = $"{id}",
			password = $"{password}",
            		username = NULL,
			email = NULL,
            		phoneNumber = NULL,
			birthday = NULL
        	}),
        	Encoding.UTF8,
        	"application/json");
	
    		using HttpResponseMessage response = await httpClient.PostAsync(apiURL, jsonContent);
    		if(response.StatusCode=="404") return false; // deal with other status codes

		user.setId(id);
		user.setPassword(password);
		user.setUsername(NULL);
		user.setEmail(NULL);
		user.setPhoneNumber(NULL);
		user.setBirthday(NULL);
		user.setLogged();
		
		return true;
	}
```

#### <p align="center">DataManagement</p>

* __getData(string):List<Motion__ - This method should allow the user to retrieve all data records, that they've collected, from the data database. The data being retrieved will be returned in a Json format that should then be parsed and used to create a list of Motion instance that the method then returns. This method takes as parameter a string representing the id of the user currently calling the method. This method returns the list of Motion instances generated in the case of success, or null in the case of failure.
    </br> Ex:

```csharp
public List<Motion> getData(string userId)/
{
	using StringContent jsonContent = new(
        	JsonSerializer.Serialize(new
        	{
			type = "GetData",
			id = "userId"
        	}),
        	Encoding.UTF8,
        	"application/json");
	
	HttpResponse response = await client.getAsync(apiURL, jsonContent);
	
	
	if(response.IsSuccessStatusCode){
		list<Motion> motionList = new List<Motion>();
		string json = await response.Content.ReadAsStringAsync();
    		jsonArray motionHistory = JsonConvert.DeserializeObject<jsonArray>(json);
	
    		foreach (jsonNode motionRecord in motionHistory)
    			{       			
				Motion motion = new Motion(motionRecord["startTime"], motionRecord["typeOfMotion"], motionRecord["duration"]);
            			motionList.Add(motion);
    			}
    		
		return motionList;
	}
	return null;
}
```



* __discardData(string, string):bool__ - This method should delete some data entry selected by the user from the data entries, associated with the user currently calling the method, in the data database. This method takes as a parameter a string representing the id of the user currently calling the method, and a string representing the id of the motion to be deleted. This method returns a bool representing it's success.
    </br> Ex:

```csharp
public bool discardData(string startTime, string userId){

	using StringContent jsonContent = new(
        	JsonSerializer.Serialize(new
        	{
			type = "DiscardData",
			id = $"{userId}",
			startTime = $"{startTime}"
        	}),
        	Encoding.UTF8,
        	"application/json");
	
	//the data linked to the user id will be deleted
	HttpResponse response = await client.PostAsync(apiURL, jsonContent);
	return response.IsSuccessStatusCode;
}

```


* __ChangeLabel(string, string, string):bool__ - This method should allow the user to changne the label associated with some previously collected data. This method takes in a string representing the new label the user wishes to associate with the data selected, a string representing the data whose label needs to be changed, and a string representing the id of the user currently calling the method. This method returns a bool representing it's success.

```csharp
public bool ChangeLabel(string motionType, string userId, string startTime){

	JsonSerializer.Serialize(new
       	{
		type = "ChangeLabel",
		account = $"{userId}",
		startTime = $"{startTime}",
   		label =  $"{motionType}"
       	}),
       	Encoding.UTF8,
       	"application/json");
	using HttpResponseMessage response = await httpClient.PatchAsync(apiURL, jsonContent);
	
	if((int)response.StatusCode==404) return false //Deal with patch failure (deal with other status codes)
	
	return true;
		
}

```


#### <p align="center">Equipment</p>

* __connectEquipment(string, string, int, int):bool__ - This method is supposed to allow the user currently calling it to connect to the sensors. If the equipment is available then the user should be able to connect to it, otherwise they should be warned of it's unavailability. This method takes as parameters two strings and two integers. The first string represents the id of the user currently calling the method, and the second string represents the type of equipment. The integers represent the port and the ip of the sensor. This method returns a bool based on it's success

</br> Ex:

```csharp
public bool connectEquipment(string userId, string type, int ip, int port){
	using StringContent jsonContent = new(
        	JsonSerializer.Serialize(new
        	{
			Type = "ConnectEquipment"
			id = $"{userId}"
            		ip = $"{ip}",
			type = $"{type}",
			port = $"{port}"
        	}),
        	Encoding.UTF8,
        	"application/json");
		
	HttpResponseMessage response = await client.PostAsync(apiURL , jsonContent);
	
	return response.IsSuccessStatusCode //Deal with the possibility of failure to connect
}

```

* __disconnectEquipment(string):bool__ - This method is supposed to allow the user currently calling it to disconnect from the sensors. This method should either only be allowed to be called by a user that successfully connected to the equipment (it was available and there were no errors on either the user or server end when performing the connection), or the user should be informed, when trying to call this method, that they need to connect to the equipment first. This method takes, as a parameter, a string representing the id of the user currently calling it, and returns a bool based on it's success.
    </br> Ex:

```csharp
public bool disconnectEquipment(string userId){
		
	using StringContent jsonContent = new(
        	JsonSerializer.Serialize(new
        	{
			Type = "DisconnectEquipment"
            		id = $"{userId}"
        	}),
        	Encoding.UTF8,
        	"application/json");	
	HttpResponseMessage response = await client.PostAsync(apiURL, jsonContent);
	
	return response.IsSuccessStatusCode //Deal with the possibility of failure to connect
}

```

* __collectData(string, string):bool__ - This method should warn the server that the user that last connected to the equipment wants to start collecting data. This method should either only be allowed to be called by a user that successfully connected to the equipment (it was available and there were no errors on either the user or server end when performing the connection), or the user should be informed, when trying to call this method, that they need to connect to the equipment first. This method takes as parameters a string representing the id of the user currently calling the method, and a string, representing the type of movemente the user intends to collect data for. This method returs a bool based on it's success.
    </br> Ex:

```csharp
public bool collectData(string userId, string movementType){
	
	using StringContent jsonContent = new(
        	JsonSerializer.Serialize(new
        	{
			Type = "CollectData"
            		userID = $"{userId}",
			label = $"{movementType}"
        	}),
        	Encoding.UTF8,
        	"application/json");
		
	HttpResponseMessage response = await client.PostAsync(apiURL, jsonContent);
	if(response.StatusCode == "404") return false; //Deal with other possible status codes
	
	return true; 	
}
```

* __collectDataStop(string):bool__ - This method should warn the server that the user that last connected wants to stop collecting data. This method should either only be allowed to be called by a user that successfully connected to the equipment (it was available and there were no errors on either the user or server end when performing the connection) and is currently collecting data, or the user should be informed, when trying to call this method, that they need to start collecting data before they can stop data collection. This method takes as parameter a string representing the id of the user currently calling the method, and returns a bool based on it's success.
    </br> Ex:

```csharp
public bool collectDataStop(string userId){
	
	using StringContent jsonContent = new(
        	JsonSerializer.Serialize(new
        	{
            		Type = "CollectDataStop"
            		userID = $"{userId}",
        	}),
        	Encoding.UTF8,
        	"application/json");
		
	HttpResponseMessage response = await client.PostAsync(apiURL, jsonContent);
	if(response.StatusCode == "404") return false; //Deal with other possible status codes

	return true;
}
```


* __getEquipmentStatus():string__ - This method should retrieve the status of the sensors. The method makes a get call to the sensor API, receiving a JsonArray with each entry representing a sensor. The method then parses the array, retreiving the status of each sensor and creating a string that is then returned. In case of failure the method returns null.
    </br> Ex:

```csharp
public string getEquipmentStatus(){
		
	HttpResponse response = await client.getAsync(sensorURL);
	
	
	if(response.IsSuccessStatusCode){
		string response = await response.Content.ReadAsStringAsync();

		JsonArray sensorArray = JsonSerializer.Deserialize<JsonArray>(response);
		string status="";
		
		foreach (JsonNode sensor in sensorArray.AsArray())
    		{
        		status += $"\nSensor {sensor["sensorId"]}: {sensor["status"]}";
        	}
		
		return status;
    	}
    	return null; //warn user of failure
}
```

* __getEquipmentInfo():string__ - This method should retrieve information about the sensors. The method makes a get call to the sensor API, receiving a JsonArray with each entry representing a sensor. The method then parses the array, retreiving the all the relevant information of each senso, creating a string of information that is then returned and can be presented. In case of failure the method returns null.
    </br> Ex:

```csharp
public string getEquipmentInfo(){
	
	HttpResponse response = await client.getAsync(sensorURL);
	
	
	if(response.IsSuccessStatusCode){
		string response = await response.Content.ReadAsStringAsync();

		JsonArray sensorArray = JsonSerializer.Deserialize<JsonArray>(response);
		string info="";
		
		foreach (JsonNode sensor in sensorArray.AsArray())
    		{
        		info += $"\nSensor {sensor["sensorId"]}: {sensor[" "]} ; {sensor[" "]}; {sensor[" "]}"; //repeat for all sensor info to present
        	}
		
		return info;
    	}
    	return null; //warn user of failure
}
```

#### <p align="center">PredictionModel</p>

* __getPrediction(string):string__ - This method should allow the user to retrieve prediction that the prediction model makes based on the current data the user is sending it and the data it has sent previously, and that is stored in the data database. This method takes as parameter a string representing the id of the user currently calling the method and returns a string that includes the current prediction model prediction. In case of failure the method returns null.
    </br> Ex:

```csharp
public string getPrediction(string userId){

	using StringContent jsonContent = new(
        	JsonSerializer.Serialize(new
        	{
            		Type = "GetPrediction"
            		userID = $"{userId}",
        	}),
        	Encoding.UTF8,
        	"application/json");

	HttpResponse response = await client.PostAsync(apiURL, jsonContent);
	if(response.StatusCode == "404") return null; //Deal with other possible status codes
	
	var jsonResponse = await response.Content.ReadAsStringAsync();		
	JsonNode jsonNode = JsonNode.Parse(jsonResponse);
	
	return jsonNode["prediction"].ToString();
}
```

* __predictUserMotions(string):string__ - This method should allow the user to start receiving real time predictions made by the prediction model, by starting a thread that executes the method predictUserMotion, responsible for calling the getPrediction method every two seconds. The predictions returned by this method are added to a prediction list that can then be displayed to the user in real time. This method should either only be allowed to be called by a user that is currently connected to the sensor equipment, or the user should be informed, when trying to call this method, that they need to connect to equipment first. This method takes as a parameter a string representing the id of the user currently calling the method, and returns a bool based on it's success.
    </br> Ex:

```csharp
public bool predictUserMotions(string userId){

	this.setIsPredicting(true);
	this.thread = new Thread(predictUserMotionLoop(userId));
	this.thread.Start();
	
	return true;
	
}

private void predictUserMotionLoop(string userId)
{
	while (this.getIsPredicting())
        {
            string prediction = this.getPrediction(userId);
            //update list of predictions
            
            Thread.Sleep(2000);
        }
}
```

* __predictUserMotionLoopStop():bool__ - This method should allow the user to stop the proccess started by the predictUserMotions method. This method should either only be allowed to be called by users that previously called the predictUserMotion method, and were successful, or should warn the user, when trying to call this method, that they need to start receiving predictions before they can call it. This method should set the isPredicting bool variable as false in order to stop the device from keeping on requesting more predictions, and should close the thread opened in the predictUserMotions method. This method takes as parameter a string representing the id of the user currently calling the method, and returns a bool based on it's success.
    </br> Ex:

```csharp
public bool predictUserMotionLoopStop(){

	this.IsPredicting(false);
	this.thread.Join();
	return true;
}
```

* __resetModel(string):bool__ - This method should allow the user to reset their personal predition model. This method should either only be allowed to be called by a user that as collected enough data to have their own prediction model (instead of the general prediction model available to all users), or the user should be informed, when trying to call this method, that they don't have a prediction model to reset. This method takes a string as paramenter representing the id of the user currently calling the method, and returns a bool based on it's success.
    </br> Ex:

```csharp
public bool resetModel(string userId){

	using StringContent jsonContent = new(
        	JsonSerializer.Serialize(new
        	{
            		Type = "ResetModel",
            		userID = $"{userId}"
        	}),
        	Encoding.UTF8,
        	"application/json");

	HttpResponse response = await client.PostAsync(apiURL, jsonContent);
	if(response.StatusCode == "404") return false; //Deal with other possible status codes
	return true;
}
```

#### <p align="center">Graphs</p>

* __draw(Motion) : bool__ - This method should draw the graphs created to display the data collected by the sensors and retrieved from the server during collectData. It can also be used to draw graphs based on previous sessions of data collection. This method takes as a parameter a Motion instance, and returns a bool based on the success of the method.

## 4.3. Client(Web/Desktop) Detailed Design

### Case 1: Administrator Wants to login the Web Page

Players: Administrators
Goals: The Administrators wants to login the management system.
Preconditions: The web page is open and running.
Case:  
1.1 From the Start page, the Administrators input the correct UID and password.
1.2 The Administrators click the “Login” button.
1.3 The pages turns to the main page.
Alternate Flows: 
1.2.1 The password or the UID are wrong.
      1.2.1.1 The UID is wrong.
                  The web page hint the UID is wrong.
      1.2.1.2 The password is wrong.
                  The web page hint the password is wrong.

Exception Flows:
Postconditons:

### Case 2: Administrator Wants to Logout the web page

Players: Administrator
Goals: The Administrators wants to logout the management system.
Preconditions: The web page is opened.
Case: 
2.1 The Administrator click the “Logout” button.
Postconditions: The page is open, waiting for its next instruction from the Administrator.

### Case 3: Administrators Wants to View the List of Devices

Players: Administrator
Goals: The Administrator is able to access information about the devices which are connecting with the system .
Preconditions: The management web page is open and running.
Case:
9.1 The user hovers his mouse over the devices key.
9.2 Web page shows devices linking with the system.
9.3 Administrators views the information.
Alternate Flows:
Exception Flows:
Postconditions: administrators should be able to obtain detailed information about the devices.

### Case 4: Administrators Wants to View the Historical Data

Players: Administrators
Goal: The Administrator is able to access information about the historical data. 
Preconditions: The management web page is opened.
Case:
10.1 The administrator hovers his mouse over the history key.
10.2 Web page shows the system historical data.
10.3 Administrators views the data.
Alternate Flows:
10.4 Administrator chooses to delete the history data.
10.5 If the administrator is successfully deleted, the page is returned.
10.6 If the administrator fails to delete, system prompt for deletion failed.
Exception Flows:
Postconditions: administrators can view the historical information and delete them.

### Case 5: Administrators Wants to Manage Users’ Information

Players: Administrators
Goal: The Administrator is able to manage information about the users. 
Preconditions: The management web page is opened.
Case:
11.1 The administrator hovers his mouse over the users management key.
11.2 Web page shows the users’ information and the add, delete, revise, import and derive keys.
11.3 Administrators views the data and choose the keys.
Alternate Flows:
11.4.1 Administrator chooses to add the users data.
11.4.2 Administrator fill the information about users and add it to the database.
11.5.1 Administrator chooses to delete the users data.
11.5.2 Administrator choose the information about users he want to delete and remove it from the database.
11.6.1 Administrator chooses to revise the users data.
11.6.2 Administrator choose the information about users he want to revise,revise it and renew it to the database.
Exception Flows:
Postconditions: administrators can manage the users’ information in the system.

### Case 6: Administrators Wants to Put a Notice on the Web Site

Players: Administrators
Goal: The Administrator is able to put a notice on the web site. 
Preconditions: The management web page is opened.
Case:
10.1 The administrator hovers his mouse over the notice adding key.
10.2 Web page turns to the page which has the function to edit a new notice.
10.3 Administrators add the new notice on the website.
Alternate Flows:
Exception Flows:
Postconditions: administrators can add a new notice on the web.

### Case 7: Administrators can Manage the System Log

Players: Administrators
Goal: The Administrator is able to system log. 
Preconditions: The management web page is opened.
Case:
10.1 The administrator hovers his mouse over the log management key.
10.2 Web page turns to the page which shows the list of the logs.
10.3 Administrators click the set key.
12.4 Administrators can revise or delete the log.
12.5 Administrators click the reserve button to reserve the log.
Alternate Flows:
Exception Flows:
Postconditions: administrators can manage the system logs.

### Case 8: View Real-time Information

Actors: Administrator
Goal: The user can see real time updated data.
Preconditions: The web page is opened.
Case:
14.1 The user clicks in the button to see charts.
14.2 Web page turns to the page which shows the charts.
14.3 The system updates the information every 3 seconds.
Alternate Flows:
Exception Flows:
Postconditions: administrators can constantly watch the data.

