# Swagger Petstore - OpenAPI 3.0

This is a sample Pet Store Server based on the OpenAPI 3.0 specification.  You can find out more about
Swagger at [https://swagger.io](https://swagger.io). In the third iteration of the pet store, we've switched to the design first approach!
You can now help us improve the API whether it's by making changes to the definition itself or to the code.
That way, with time, we can improve the API in general, and expose some of the new features in OAS3.

Some useful links:
- [The Pet Store repository](https://github.com/swagger-api/swagger-petstore)
- [The source API definition for the Pet Store](https://github.com/swagger-api/swagger-petstore/blob/master/src/main/resources/openapi.yaml)


# Pet


## PUT /pet

**Update an existing pet.**

Update an existing pet by Id.


Request body (application/json):

Uses the `Pet` schema.

Request body (application/xml):

Uses the `Pet` schema.

Request body (application/x-www-form-urlencoded):

Uses the `Pet` schema.

Responses:

- `200`: Successful operation
- `400`: Invalid ID supplied
- `404`: Pet not found
- `422`: Validation exception
- `default`: Unexpected error


## POST /pet

**Add a new pet to the store.**

Add a new pet to the store.


Request body (application/json):

Uses the `Pet` schema.

Request body (application/xml):

Uses the `Pet` schema.

Request body (application/x-www-form-urlencoded):

Uses the `Pet` schema.

Responses:

- `200`: Successful operation
- `400`: Invalid input
- `422`: Validation exception
- `default`: Unexpected error


## GET /pet/findByStatus

**Finds Pets by status.**

Multiple status values can be provided with comma separated strings.


Parameters:

- `status` (query, string, required): Status values that need to be considered for filter

Responses:

- `200`: successful operation
- `400`: Invalid status value
- `default`: Unexpected error


## GET /pet/findByTags

**Finds Pets by tags.**

Multiple tags can be provided with comma separated strings. Use tag1, tag2, tag3 for testing.


Parameters:

- `tags` (query, array, required): Tags to filter by

Responses:

- `200`: successful operation
- `400`: Invalid tag value
- `default`: Unexpected error


## GET /pet/{petId}

**Find pet by ID.**

Returns a single pet.


Parameters:

- `petId` (path, integer, required): ID of pet to return

Responses:

- `200`: successful operation
- `400`: Invalid ID supplied
- `404`: Pet not found
- `default`: Unexpected error


## POST /pet/{petId}

**Updates a pet in the store with form data.**

Updates a pet resource based on the form data.


Parameters:

- `petId` (path, integer, required): ID of pet that needs to be updated
- `name` (query, string, optional): Name of pet that needs to be updated
- `status` (query, string, optional): Status of pet that needs to be updated

Responses:

- `200`: successful operation
- `400`: Invalid input
- `default`: Unexpected error


## DELETE /pet/{petId}

**Deletes a pet.**

Delete a pet.


Parameters:

- `api_key` (header, string, optional): 
- `petId` (path, integer, required): Pet id to delete

Responses:

- `200`: Pet deleted
- `400`: Invalid pet value
- `default`: Unexpected error


## POST /pet/{petId}/uploadImage

**Uploads an image.**

Upload image of the pet.


Parameters:

- `petId` (path, integer, required): ID of pet to update
- `additionalMetadata` (query, string, optional): Additional Metadata

Request body (application/octet-stream):

Type: `string`.

Responses:

- `200`: successful operation
- `400`: No file uploaded
- `404`: Pet not found
- `default`: Unexpected error


# Store


## GET /store/inventory

**Returns pet inventories by status.**

Returns a map of status codes to quantities.


Responses:

- `200`: successful operation
- `default`: Unexpected error


## POST /store/order

**Place an order for a pet.**

Place a new order in the store.


Request body (application/json):

Uses the `Order` schema.

Request body (application/xml):

Uses the `Order` schema.

Request body (application/x-www-form-urlencoded):

Uses the `Order` schema.

Responses:

- `200`: successful operation
- `400`: Invalid input
- `422`: Validation exception
- `default`: Unexpected error


## GET /store/order/{orderId}

**Find purchase order by ID.**

For valid response try integer IDs with value <= 5 or > 10. Other values will generate exceptions.


Parameters:

- `orderId` (path, integer, required): ID of order that needs to be fetched

Responses:

- `200`: successful operation
- `400`: Invalid ID supplied
- `404`: Order not found
- `default`: Unexpected error


## DELETE /store/order/{orderId}

**Delete purchase order by identifier.**

For valid response try integer IDs with value < 1000. Anything above 1000 or non-integers will generate API errors.


Parameters:

- `orderId` (path, integer, required): ID of the order that needs to be deleted

Responses:

- `200`: order deleted
- `400`: Invalid ID supplied
- `404`: Order not found
- `default`: Unexpected error


# User


## POST /user

**Create user.**

This can only be done by the logged in user.


Request body (application/json):

Uses the `User` schema.

Request body (application/xml):

Uses the `User` schema.

Request body (application/x-www-form-urlencoded):

Uses the `User` schema.

Responses:

- `200`: successful operation
- `default`: Unexpected error


## POST /user/createWithList

**Creates list of users with given input array.**

Creates list of users with given input array.


Request body (application/json):

Type: `array`.

Responses:

- `200`: Successful operation
- `default`: Unexpected error


## GET /user/login

**Logs user into the system.**

Log into the system.


Parameters:

- `username` (query, string, optional): The user name for login
- `password` (query, string, optional): The password for login in clear text

Responses:

- `200`: successful operation
- `400`: Invalid username/password supplied
- `default`: Unexpected error


## GET /user/logout

**Logs out current logged in user session.**

Log user out of the system.


Responses:

- `200`: successful operation
- `default`: Unexpected error


## GET /user/{username}

**Get user by user name.**

Get user detail based on username.


Parameters:

- `username` (path, string, required): The name that needs to be fetched. Use user1 for testing

Responses:

- `200`: successful operation
- `400`: Invalid username supplied
- `404`: User not found
- `default`: Unexpected error


## PUT /user/{username}

**Update user resource.**

This can only be done by the logged in user.


Parameters:

- `username` (path, string, required): name that need to be deleted

Request body (application/json):

Uses the `User` schema.

Request body (application/xml):

Uses the `User` schema.

Request body (application/x-www-form-urlencoded):

Uses the `User` schema.

Responses:

- `200`: successful operation
- `400`: bad request
- `404`: user not found
- `default`: Unexpected error


## DELETE /user/{username}

**Delete user resource.**

This can only be done by the logged in user.


Parameters:

- `username` (path, string, required): The name that needs to be deleted

Responses:

- `200`: User deleted
- `400`: Invalid username supplied
- `404`: User not found
- `default`: Unexpected error
