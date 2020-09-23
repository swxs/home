--[[
    Delete key with match the repr.
    Accepted parameters:
        Keys:
            key_name - repr
        Return value:
            delete number
--]]
redis.replicate_commands()
local cursor = '0'
local delete_count = 0
repeat
    local result = redis.call('scan', cursor, 'MATCH', KEYS[1], 'COUNT', 100)
    cursor = result[1]
    local list = result[2]
    delete_count = delete_count + #list
    redis.call('del', unpack(list))
until (cursor == '0')
return delete_count
