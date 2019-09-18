struct CreateResult {
    1: required i32 code;
    2: optional string id;
    3: optional string msg;
}

struct UpdateResult {
    1: required i32 code;
    2: optional string id;
    3: optional string msg;
}

struct DeleteResult {
    1: required i32 code;
    2: optional string msg;
}

struct User {
    1: optional string id;
    2: optional string username;
    3: optional string nickname;
    4: optional string password;
    5: optional string salt;
    6: optional string avatar;
    7: optional string email;
    8: optional string mobile;
    9: optional string description;
}

struct UserResult {
    1: required i32 code;
    2: optional User user;
    3: optional string msg;
}

typedef list<User> UserList

struct UserSearchResult {
    1: required i32 code;
    2: optional UserList user_list;
    3: optional string msg;
}

struct Description {
    1: optional string id;
}

struct DescriptionResult {
    1: required i32 code;
    2: optional _description description;
    3: optional string msg;
}

typedef list<Description> DescriptionList

struct DescriptionSearchResult {
    1: required i32 code;
    2: optional DescriptionList description_list;
    3: optional string msg;
}


service UserService {
    CreateResult create_user_user(1:User user),
    UpdateResult update_user_user(1:User user),
    DeleteResult delete_user_user(1:list<string> idList),
    UserResult select_User_user(1: string oid),
    UserSearchResult search_User_user(),
    CreateResult create_user_description(1:_description description),
    UpdateResult update_user_description(1:_description description),
    DeleteResult delete_user_description(1:list<string> idList),
    _descriptionResult select_User_description(1: string oid),
    _descriptionSearchResult search_User_description(),
}
