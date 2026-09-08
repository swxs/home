--[[
    Count key with match the repr.
    Accepted parameters:
        Keys:
            key_name - repr
        Return value:
            delete number
--]]
local cursor = '0'
local count = 0
repeat
    local result = redis.call('SCAN', cursor, 'MATCH', KEYS[1], 'COUNT', 100)
    cursor = result[1]
    count = count + #result[2]
until cursor == '0'
return count
