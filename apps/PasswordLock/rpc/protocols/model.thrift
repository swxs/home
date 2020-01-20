struct CreateResult {
    1: required i32 code;
    2: optional string msg;
    3: optional string id;
}

struct UpdateResult {
    1: required i32 code;
    2: optional string msg;
    3: optional string id;
}

struct DeleteResult {
    1: required i32 code;
    2: optional string msg;
    3: optional i32 count;
}

struct PasswordLock {
    1: optional string id;
    2: optional string name;
    3: optional string key;
    4: optional string website;
    5: optional string user_id;
}

typedef list<PasswordLock> PasswordLockList

struct SelectPasswordLockResult {
    1: required i32 code;
    2: optional string msg;
    3: optional PasswordLock password_lock;
}

struct SearchPasswordLockResult {
    1: required i32 code;
    2: optional string msg;
    3: optional PasswordLockList password_lock_list;
}

service PasswordLockService {
    CreateResult create_password_lock_password_lock(1:PasswordLock password_lock),
    UpdateResult update_password_lock_password_lock(1:string id, 2:PasswordLock password_lock),
    DeleteResult delete_password_lock_password_lock(1:string id),
    SelectPasswordLockResult select_password_lock_password_lock(1:string id),
    SearchPasswordLockResult search_password_lock_password_lock(1:string search),
}
