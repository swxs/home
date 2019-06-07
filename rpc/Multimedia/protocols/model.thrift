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

struct Artical {
    1: optional string id;
    2: optional string title;
    3: optional string author;
    4: optional string year;
    5: optional string source;
    6: optional string summary;
    7: optional string content;
    8: optional string ttype_id_list;
    9: optional string tag_id_list;
    10: optional string comment_id_list;
}

struct ArticalResult {
    1: required i32 code;
    2: optional Artical artical;
    3: optional string msg;
}

typedef list<Artical> ArticalList

struct ArticalSearchResult {
    1: required i32 code;
    2: optional ArticalList artical_list;
    3: optional string msg;
}

struct Movie {
    1: optional string id;
    2: optional string title;
    3: optional string year;
    4: optional string summary;
}

struct MovieResult {
    1: required i32 code;
    2: optional Movie movie;
    3: optional string msg;
}

typedef list<Movie> MovieList

struct MovieSearchResult {
    1: required i32 code;
    2: optional MovieList movie_list;
    3: optional string msg;
}

struct Tag {
    1: optional string id;
    2: optional string name;
    3: optional string color;
}

struct TagResult {
    1: required i32 code;
    2: optional Tag tag;
    3: optional string msg;
}

typedef list<Tag> TagList

struct TagSearchResult {
    1: required i32 code;
    2: optional TagList tag_list;
    3: optional string msg;
}

struct Ttype {
    1: optional string id;
    2: optional string name;
}

struct TtypeResult {
    1: required i32 code;
    2: optional Ttype ttype;
    3: optional string msg;
}

typedef list<Ttype> TtypeList

struct TtypeSearchResult {
    1: required i32 code;
    2: optional TtypeList ttype_list;
    3: optional string msg;
}


service MultimediaService {
    CreateResult create_multimedia_artical(1:Artical artical),
    UpdateResult update_multimedia_artical(1:Artical artical),
    DeleteResult delete_multimedia_artical(1:list<string> idList),
    ArticalResult select_Multimedia_artical(1: string oid),
    ArticalSearchResult search_Multimedia_artical(),
    CreateResult create_multimedia_movie(1:Movie movie),
    UpdateResult update_multimedia_movie(1:Movie movie),
    DeleteResult delete_multimedia_movie(1:list<string> idList),
    MovieResult select_Multimedia_movie(1: string oid),
    MovieSearchResult search_Multimedia_movie(),
    CreateResult create_multimedia_tag(1:Tag tag),
    UpdateResult update_multimedia_tag(1:Tag tag),
    DeleteResult delete_multimedia_tag(1:list<string> idList),
    TagResult select_Multimedia_tag(1: string oid),
    TagSearchResult search_Multimedia_tag(),
    CreateResult create_multimedia_ttype(1:Ttype ttype),
    UpdateResult update_multimedia_ttype(1:Ttype ttype),
    DeleteResult delete_multimedia_ttype(1:list<string> idList),
    TtypeResult select_Multimedia_ttype(1: string oid),
    TtypeSearchResult search_Multimedia_ttype(),
}
