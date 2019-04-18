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

struct PasswordLock {
    1: optional string id;
    2: optional string name;
    3: optional string key;
    4: optional string website;
    5: optional string user_id;
}

struct PasswordLockResult {
    1: required i32 code;
    2: optional PasswordLock password_lock;
    3: optional string msg;
}

typedef list<PasswordLock> PasswordLockList

struct PasswordLockSearchResult {
    1: required i32 code;
    2: optional PasswordLockList password_lock_list;
    3: optional string msg;
}


service PasswordLockService {
    CreateResult create_password_lock_password_lock(1:PasswordLock password_lock),
    UpdateResult update_password_lock_password_lock(1:PasswordLock password_lock),
    DeleteResult delete_password_lock_password_lock(1:list<string> idList),
    PasswordLockResult select_PasswordLock_password_lock(1: string oid),
    PasswordLockSearchResult search_PasswordLock_password_lock(),
}
