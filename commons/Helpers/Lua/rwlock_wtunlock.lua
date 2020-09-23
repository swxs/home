--[[
    # None：释放成功
# 0：释放失败
# 1：释放成功，且锁释放
--]]
local write_key = 'write'
local mode = redis.call('hget', KEYS[1], 'mode')
if (mode == false) then
    return 1
end
local lockExists = redis.call('hexists', KEYS[1], write_key)
if (lockExists == 0) then
    return nil
end
if (mode == 'write') then
    redis.call('del', KEYS[1])
    return 1
end
return 0
