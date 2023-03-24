# Software Requirements Specification of Server Group 1.0

Revision History:

| Date     | Author       | Description   |
| -------- | ------------ | ------------- |
| March 23 | Hu Jianzheng | Add use cases |

## Use Cases

Case: Input from Algorithm part

Case: Output to Algorithm part

Case: Input from Web part

Case: Output to Web part

Case: Input from Embeded System part

Case: Interaction with Mobile part

Case: Input from Database part

Case: Output to Database part

### Case : Input from Algorithm part

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

#### Basic Flow

| Actor                                                        | System                                                    |
| ------------------------------------------------------------ | --------------------------------------------------------- |
| Receive Server-to-Algorithm Request <Dataset ID，the number of record in this  Dataset> |                                                           |
|                                                              | Check the validity of the ID and the size of the package. |
|                                                              | Fetch dataset from the database                           |
|                                                              | Send the training dataset package with the certain name.  |
| Send the completion signal of the Server System.             |                                                           |

#### Alternative Flow

| Actor | System |
| ----- | ------ |
|       |        |
|       |        |
|       |        |
|       |        |
|       |        |

### Case : Output to Algorithm part

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

#### Alternative Flow

| Actor | System |
| ----- | ------ |
|       |        |
|       |        |
|       |        |
|       |        |
|       |        |

### Case: Input From Web part

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

#### Basic Flow

| Actor                                                  | System                                                      |
| ------------------------------------------------------ | ----------------------------------------------------------- |
| Receive the requests of Web part.                      |                                                             |
|                                                        | Build connections between the Web part and the Server part. |
|                                                        | The Client send HTTP PUSH to send message to the Server.    |
| The Server part get the instruction from the Web part. |                                                             |
| The Server stop the connection after exchanging data.  |                                                             |
|                                                        |                                                             |
|                                                        |                                                             |

#### Alternative Flow

| Actor | System |
| ----- | ------ |
|       |        |
|       |        |
|       |        |
|       |        |
|       |        |

### Case: Output to Web part

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

#### Basic Flow

| Actor                            | System                           |
| -------------------------------- | -------------------------------- |
| Server send request to send data |                                  |
| Server build the connection      |                                  |
|                                  | Web build connection with Server |
|                                  | Web receive data from the Server |
|                                  | Return complete signal           |
| Server get complete signal       |                                  |

#### Alternative Flow

| Actor | System |
| ----- | ------ |
|       |        |
|       |        |
|       |        |
|       |        |



### Case: Input From Embedded System part

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

#### Basic Flow

| Actor                                                   | System                                                      |
| ------------------------------------------------------- | ----------------------------------------------------------- |
| Receive the requests of Embedded System part.           |                                                             |
|                                                         | Build connections between the Web part and the Server part. |
|                                                         | Receive the data from Embeded System.                       |
|                                                         | Complete the transmission.                                  |
| Receive the completion signal from the Embedded System. |                                                             |
|                                                         |                                                             |
|                                                         |                                                             |

#### Alternative Flow

| Actor | System |
| ----- | ------ |
|       |        |
|       |        |
|       |        |
|       |        |
|       |        |

### Case: Interaction with Mobile part

- version: 1
- Created: March 23
- Authors: Hu Jianzheng
- Source: Server
- Actors: Mobile
- Goal: Exchange data between Server and Mobile.
- Frequency: Irregular.
- Precondition: The connection between Server and the Mobile has been built.
- Postconditions: No

#### Basic Flow

| Actor                                                     | System                                                       |
| --------------------------------------------------------- | ------------------------------------------------------------ |
| Receive the requests of Web part.                         |                                                              |
|                                                           | Build connections between the Mobile part and the Server part. |
|                                                           |                                                              |
| The Server receive data from and send data to the Mobile. |                                                              |
| The Server stop the connection after exchanging data.     |                                                              |
|                                                           |                                                              |
|                                                           |                                                              |

#### Alternative Flow

| Actor | System |
| ----- | ------ |
|       |        |
|       |        |
|       |        |
|       |        |
|       |        |

### Case: Input From Database part

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

#### Basic Flow

| Actor                                                      | System                                           |
| ---------------------------------------------------------- | ------------------------------------------------ |
| Build connection between the Server and the Database part. |                                                  |
|                                                            | The Databased part send data to the Server part. |
|                                                            |                                                  |
| Receive data from the Dataset part.                        |                                                  |
| Send completion signal when finished.                      |                                                  |
|                                                            |                                                  |
|                                                            |                                                  |

#### Alternative Flow

| Actor | System |
| ----- | ------ |
|       |        |
|       |        |
|       |        |
|       |        |
|       |        |

### Case: Output to Database part

- version: 1
- Created: March 23
- Authors: Hu Jianzheng
- Source: Server
- Actors: Server
- Goal: Send the data collected by Embedded System and other parts to the Database.
- Frequency: Irregular.
- Precondition: The data is structured and prepared by the Embedded System and the connection between the Server and Database part is built.
- Postconditions: No

#### Basic Flow

| Actor                                        | System                            |
| -------------------------------------------- | --------------------------------- |
| Send the requests to send data to Database   |                                   |
|                                              | Dataset Receive data from Server. |
|                                              | Dataset send completion signal.   |
| Receive the comletion signal after finished. |                                   |
|                                              |                                   |
|                                              |                                   |
|                                              |                                   |

#### Alternative Flow

| Actor | System |
| ----- | ------ |
|       |        |
|       |        |
|       |        |
|       |        |
|       |        |
