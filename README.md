# InfilectFlicker

### API Endpoints

##### 1. Login

URL: `http://localhost:8000/api/v1/login`

Form Values: `username` and `password`

You can use the test values as:

username : owlcity_1

password : test_password

Response:

```json
{
    "token": "4f32807ad44359e9ce3a2429f5c58292562e2c02"
}
```

`All subsequent APIs need a value auth token in the header`

`Authorization=Token mytoken12312312`



#### 2. Get User Groups

URL : `http://localhost:8000/api/v1/groups/`

Returns the groups that the user is in.

Response:

```json
{
	"count": 3,
	"next": null,
	"previous": null,
	"results": [
		{
			"name": "group_0",
			"nsid": "GL7RHB",
			"photos_count": 32
		},
		{
			"name": "group_1",
			"nsid": "RKNP03",
			"photos_count": 33
		},
		{
			"name": "group_2",
			"nsid": "6F6CDK",
			"photos_count": 26
		}
	]
}
```

#### 3. Photos in a group

URL : `http:localhost:8000/api/v1/groups/<group_id>/`

Returns all the photo ids that belong to the given group.

Response: 

```json
{
	"count": 32,
	"next": "http://localhost:8000/api/v1/groups/GL7RHB/?page=2",
	"previous": null,
	"results": [
		{
			"photo_nsid": "6GXPW4"
		},
		{
			"photo_nsid": "FQBU3P"
		},
		{
			"photo_nsid": "6R1R2G"
		},
		{
			"photo_nsid": "F7OBAR"
		}
}
```

4. Get all photos belonging to a user

Returns all the photos for a given group.

URL : `http://localhost:8000/api/v1/photos/?group=<group_nsid>`

Response: 

```json
{
	"count": 32,
	"next": "http://localhost:8000/api/v1/photos/?group=GL7RHB&page=2",
	"previous": null,
	"results": [
		{
			"photo_nsid": "6GXPW4",
			"group_nsid": "GL7RHB",
			"uploaded_on": "1537699424",
			"taken_on": "1537699424",
			"license": "0",
			"owner": {
				"nsid": "NTXDSY",
				"username": "owlcity_5",
				"real_name": "Owl City 4",
				"location": "Alaska",
				"path_alias": "owl_city_4"
			}
		},
		{
			"photo_nsid": "FQBU3P",
			"group_nsid": "GL7RHB",
			"uploaded_on": "1537699425",
			"taken_on": "1537699425",
			"license": "0",
			"owner": {
				"nsid": "NTXDSY",
				"username": "owlcity_5",
				"real_name": "Owl City 4",
				"location": "Alaska",
				"path_alias": "owl_city_4"
			}
		}
}
```


#### 5. Get Photo Details

Returns photo details for the given photo nsid

URL : `http://localhost:8000/api/v1/photos/<photo_nsid>`

Response: 

```json
{
	"photo_nsid": "6GXPW4",
	"group_nsid": "GL7RHB",
	"uploaded_on": "1537699424",
	"taken_on": "1537699424",
	"license": "0",
	"owner": {
		"nsid": "NTXDSY",
		"username": "owlcity_5",
		"real_name": "Owl City 4",
		"location": "Alaska",
		"path_alias": "owl_city_4"
	},
	"comments": [
		{
			"comment": "This is a comment"
		}
	],
	"notes": [
		{
			"note": "This is a note"
		}
	],
	"tags": [
		{
			"name": "Tag_[0]",
			"authorname": "owlcity_1",
			"author": "O6J48P",
			"id": "1537700760"
		}
	]
}
```


#### 6. Logout

Invalidates a token

URL : `http://localhost:8000/api/v1/logout/`

Response: `200 OK`
