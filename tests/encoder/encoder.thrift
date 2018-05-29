/**
 * Types and Structures
 */
typedef i64 Timestamp

struct TTodo {
    1: required i32 id,
    2: required string title,
    3: required Timestamp created_at,
}

struct TFlattenData {
    1: required i32 required_field,
    2: optional i32 optional_field,
}

struct TEmbedData {
    1: required TFlattenData required_struct,
    2: required i32 required_scalar,
    3: required list<TFlattenData> required_list_struct
}

struct TMapOfStruct {
    1: map<string, TFlattenData> required_map
}

struct TListOfMapOfStruct {
    1: list<TMapOfStruct> required_list
}

typedef list<i32> TListOfInt
typedef list<TFlattenData> TListOfStruct
typedef list<TEmbedData> TListOfEmbedStruct

/**
 * Exceptions
 */
enum EncoderErrorCode {
    UNKNOWN_ERROR = 0,
    DATABASE_ERROR = 1,
    TOO_BUSY_ERROR = 2,
}

exception EncoderUserException {
   1: required EncoderErrorCode error_code,
   2: required string error_name,
   3: optional string message,
}

exception EncoderSystemException {
   1: required EncoderErrorCode error_code,
   2: required string error_name,
   3: optional string message,
}

exception EncoderUnknownException {
   1: required EncoderErrorCode error_code,
   2: required string error_name,
   3: required string message,
}

/**
 * API
 */
service EncoderService {
    bool ping()
        throws (1: EncoderUserException user_exception,
                2: EncoderSystemException system_exception,
                3: EncoderUnknownException unknown_exception,)

    i32 scalar(1:i32 id)
        throws (1: EncoderUserException user_exception,
                2: EncoderSystemException system_exception,
                3: EncoderUnknownException unknown_exception,)

    list<i32> list_of_scalar(1:i32 id)
        throws (1: EncoderUserException user_exception,
                2: EncoderSystemException system_exception,
                3: EncoderUnknownException unknown_exception,)

    TListOfInt list_of_scalar_in_struct(1:i32 id)
        throws (1: EncoderUserException user_exception,
                2: EncoderSystemException system_exception,
                3: EncoderUnknownException unknown_exception,)

    TListOfStruct list_of_struct_in_struct(1:i32 id)
        throws (1: EncoderUserException user_exception,
                2: EncoderSystemException system_exception,
                3: EncoderUnknownException unknown_exception,)

    TEmbedData struct_of_list_in_struct(1:i32 id)
        throws (1: EncoderUserException user_exception,
                2: EncoderSystemException system_exception,
                3: EncoderUnknownException unknown_exception,)

    TMapOfStruct map_of_struct(1:i32 id)
        throws (1: EncoderUserException user_exception,
                2: EncoderSystemException system_exception,
                3: EncoderUnknownException unknown_exception,)

    TListOfMapOfStruct list_of_map_of_struct(1:i32 id)
        throws (1: EncoderUserException user_exception,
                2: EncoderSystemException system_exception,
                3: EncoderUnknownException unknown_exception,)

    list<TTodo> list_todo()
        throws (1: EncoderUserException user_exception,
                2: EncoderSystemException system_exception,
                3: EncoderUnknownException unknown_exception,)

    void add_todo(1:string title)
        throws (1: EncoderUserException user_exception,
                2: EncoderSystemException system_exception,
                3: EncoderUnknownException unknown_exception,)

    void complete_todo(1:i32 id)
        throws (1: EncoderUserException user_exception,
                2: EncoderSystemException system_exception,
                3: EncoderUnknownException unknown_exception,)
}