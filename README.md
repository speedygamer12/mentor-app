## Tests Permissions
### test view - user
* if a user_type:1 accesses list view, wil get all list
* if a user_type:2/3 accesses list view, will be denied
* a user_type:1 can access all user details
* a user_type:2 can only access own detail.

## Rough User Scope
A custom user model based on AbstractUserModel with email login
Additional Fields: user_type(Three user type Lead and member), DSNID(regex checked in serializer)
User can be created via UserSerializer with fields: 'username', 'email', 'DSNID','user_type','password', 'password2'
After user is created, signal.py file will create user and save user based on user_type and will fill with temp detail.

### user models
* Lead: id, user, created, updated, objects
* tracks: id, track_name, created, updated, objects
* Mentor: id, gender, phone, user, created, track, expercience, updated, is_active, objects
* Mentee: id, gender, phone,  user, created, track, expercience, updated, is_active, objects

leaduser can turn is_active == True, via api call
* test if usertype1 generates Lead user
* test if usertype2 generates Mentor user
* test if usertype3 generates Mentee user

### Permissions and Serializers:
* IsAdmin: for unverified list of users --> UnverifiedMentorSerializer: edit only is_active 
* IsAdminOrReadOnly: for verified list of user --> MentorSerializer: cannot edit is_active and DSNID
* IsOwnerOrReadOnly: for user details --> MentorSerializer

### Views and URLS:
* UnverifiedMentorView: List of all unverified mentors and edit and delete Mentor(IsAdmin) (url: /addmentor)
* MentorListView: List of all verified mentors and Post(IsAdminOrReadOnly) (url: /mentors)
* MentorDetailView: Detail of verified mentors (IsOwnerOrReadOnly) (url: /mentor/<int:pk>)

### requests for mentor, mentee, tracks: get, post, put, delete
* for mentor only put and list, no post, delete 
* Admin can see a list of all unverified users(via list view) and can update is_active to true and delete the users
* if users are verified, they can view and update their details

## TESTS
### Login and Registrations
-

### Custom User
#### /tracks
* list admin(yes) others(yes)
* post admin(yes) others(no)
* put admin(yes) others(no)
* delete admin(yes) others(no)

#### /mentors
* list mentors others(yes)

#### /mentor/pk
* put admin(yes), owner(yes), others(no)

#### /addmentor (actions)
* Create a Lead User by using superuser account via /addmentor
* Get List of all Unverified mentors
* Go to the detail page of a specific mentor
* Change a mentor active status to True


note:
change Mentor view to generics.List and generics.Details

note:
fix social_auth dependency issues: No module facebook
Generate fackebook and twitter secret keys.
fix cloudinary issue
fix phoneModelIssue: phoneModel has no attribute mobile 











